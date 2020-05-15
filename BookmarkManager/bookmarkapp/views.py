from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from datetime import datetime
import traceback
from django.http import JsonResponse
from .models import Bookmark,Customer
from django.db.models.expressions import RawSQL


# Api for creating the bookmark
@csrf_exempt
def create(request):

    status = ''
    # To get the request data from the post
    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST

    try:
        # Loading up all the values from post
        name = requestData.get('name',None)
        title = requestData.get('title',None)
        url = requestData.get('url',None)
        source_name = requestData.get('source_name',None)
        geolocation = requestData.get('geolocation',None)

        # Extracting latlng from the geolocation value
        lat = float(geolocation.split(',')[0].strip())
        lng = float(geolocation.split(',')[1].strip())

        # Creating the bookmark with title, url and source name
        bookmark_obj = Bookmark.objects.create(Title=title,Url=url,Source_Name=source_name)

        # Createing the customer object with latitude and longitude
        customer = Customer(Latitude=lat,Longitude=lng)
        
        # Saving the customer save
        customer.save()

        # Adding the customer to the bookmark object to create an relationship between two tables
        bookmark_obj.Customer.add(customer)

        status = 'success'

    # Handling an exceptional case
    except Exception as e:
        traceback.print_exc()
        status = 'failed to store'

    return JsonResponse({'status':status},status=200)



# Api for broswing the bookmark
@csrf_exempt
def browse(request):

    status = ''
    bookmark_obj=None

    # Getting the params for the GET request
    requestData = request.GET

    try:
        # Getting the parameters
        cust_id = requestData.get('cust_id',None)
        lat_lng_radius = requestData.get('geolocation',None)
        source_name = requestData.get('source_name',None)
        date = requestData.get('date',None)
        title_contains = requestData.get('title_contains',None)
        sort_by = requestData.get('sort_by',None)

        # Check if whether the params has cust id
        if cust_id != None:
            bookmark_obj = Bookmark.objects.filter(Customer=cust_id)

        # Check if whether the params has source name
        if source_name != None:
            bookmark_obj = Bookmark.objects.filter(Source_Name__iexact=source_name)

        # Check if whether the params has date range
        if date != None:
            from_date  = datetime.strptime(date.split('-')[0], '%d/%m/%Y')
            to_date = datetime.strptime(date.split('-')[1], '%d/%m/%Y')
            bookmark_obj = Bookmark.objects.filter(Date__gte=from_date,Date__lte=to_date)

        # Check if whether the params has title contains
        if title_contains != None:
            bookmark_obj = Bookmark.objects.filter(Title__icontains=title_contains)

        # Check if whether the params has latlng
        if lat_lng_radius != None:
            
            # The surronding radius in km
            distance_radius = None

            # Check if the radius in km is given or not
            if '-' in lat_lng_radius:
                latlng = lat_lng_radius.split('-')[0]
                # Setting the radius value
                distance_radius = float(lat_lng_radius.split('-')[1])
            
            else:
                latlng = lat_lng_radius


            # Getting the user's lat lng from the requestdata
            lat = float(latlng.split(',')[0])
            lng = float(latlng.split(',')[1])

            # Getting all the nearby location by hitting a function
            nearby_location_bookmarks = get_locations_nearby_coords(lat,lng, distance_radius)

            # Filtering the bookmark objects from the list of customer's id
            bookmark_obj = Bookmark.objects.filter(Customer__in = nearby_location_bookmarks.values_list('id', flat=True))

        # Check if whether the params has sort by keyword        
        if sort_by != None and sort_by != '':
            # Sorting the bookmark values with given keyword
            bookmark_obj = bookmark_obj.order_by(sort_by)


        status = 'success'

    except Exception as e:
        traceback.print_exc()
        status = 'failed to retrieve data'

    return JsonResponse({'status':status,"data":list(bookmark_obj.values())},status=200)



# To get the nearby location bookmark values by the co-ordinates
def get_locations_nearby_coords(latitude, longitude, max_distance=None):
    """
    Return objects sorted by distance to specified coordinates
    which distance is less than max_distance given in kilometers
    """

    # Great circle distance formula for getting the circle radius with kilometer measure
    gcd_formula = """6371 * acos(least(greatest(\
    cos(radians(%s)) * cos(radians("Latitude")) \
    * cos(radians("Longitude") - radians(%s)) + \
    sin(radians(%s)) * sin(radians("Latitude")) \
    , -1), 1))"""

    # performing a rawsql query in order to perform a normal sql query
    distance_raw_sql = RawSQL(
        gcd_formula,
        (latitude, longitude, latitude)
    )
    
    # Adding an annotate query for adding the distance which find in the above sql
    qs = Customer.objects.all().annotate(distance=distance_raw_sql).order_by('distance')

    # Filterting the queryset by the given max distance 
    if max_distance is not None:
        qs = qs.filter(distance__lte=max_distance)
        
    return qs