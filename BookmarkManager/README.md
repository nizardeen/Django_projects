Description :
    A Django Bookmark app With Geolocation
   
Models :
    Customer, Bookmark

./_api/create:
    
        Method : POST
        Form parameters are:
        (title : youtube, url : https://youtube.com, source_name : youtube, geolocation : 12.9173, 77.6012)
 
 
 ./_api/browse:
    
        Method : GET
        Query Parameters: "http://127.0.0.1:8000/_api/browse?geolocation=12.9716,77.5946-6&sort_by=Title"
        Parameters can be given any one of the following along with sort_by: ( cust_id, geolocation, source_name, title_contains, date)
        
        date range format should be as : (10/05/2020-15/05/2020)
        geolocation format as : (12.9716,77.5946-6) where "6" after the hyphen refers to the radius in km
        sort_by param values are : (Customer, Title, Source_Name, Date)
