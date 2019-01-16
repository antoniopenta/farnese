## FARNESE

FARNESE (FlAsk RaNge quEry SErvice): a lightweight REST service in Flask (Python) to retrieve Point Of Interest (PoI) from  PostGiS using spatial range queries.

## What it does:

- It is able to return a set of  Points of Interest (PoI)  within a radius to a query point: **range query**
- The data are stored in PostGIS.
- The output is a GeoJson file.

- A working post request (using Heroku):
 ```bash
curl -X POST -H  "Content-Type: application/json" -d '{"lat":51.5369436, "lng":-0.0767174, "radius":200}' https://geo-rest-service.herokuapp.com/restpoi/poi/poifromcoord
```

which means retrieve all the Points of Interest that are within the radius of 200 meter from the center point specified with latitude 51.5369436 and  longitude -0.0767174.

## Dependencies

-  Python >= 3.6
-  [PostGis database](https://postgis.net/)
-  Python Libraries in the requirements.txt:
```bash
 pip install -r  requirements.txt
 ```
 - The suggestion is to create a dedicate virtual env.

## Example of Data

- In the folder data, there is a file 'anemities.csv', that contains PoI around a limited area of London scraped from [OpenStreetMap](https://www.openstreetmap.org/#map=7/53.465/-8.240)
- Example:

| lat        | lng        | amenity_type | name              |
|------------|------------|--------------|-------------------|
| 51.5331624 | -0.0522468 | post_box     |                   |
| 51.5328464 | -0.0571304 | post_box     |                   |
| 51.5519609 | -0.0746921 | pub          | marquis_lansdowne |


- lat is latitude
- lng is longitude
- amenity_type is the type of anemity
- name is the name of the anemity
- Data stored in PostGIS can be viewed [here](https://www.google.com/maps/d/viewer?hl=it&hl=it&ll=51.544019781040895%2C-0.06072770000002947&z=14&mid=1CVS-tA_iLeWerJJSVmXi3bWenarx9wp0)

## Create PostGIS Database

- We assume that a PostGIS instance is up and running

- [PgAdmin](https://www.pgadmin.org/) can be used to execute the following SQL command (stored as files in the SQL folder):


```sql
 --- use post gis estension
 CREATE EXTENSION postgis;

 --create schema
 create schema poi;


 -- create table with PostGis extension (geom4326 geometry)
 CREATE TABLE poi.anemity
 (
   id serial,
   lat double precision,
   lng double precision,
   amenity_type character varying(50),
   name character varying(1000),
   geom4326 geometry
 );


 --add primary constraints
 alter table poi.anemity add primary key (id);

 ```
- In this example, we have just one table for the REST service

- To upload the data in PostGIS, you can use the script 'write_data_to_postgres.py' in the folder scripts.

- To run  'write_data_to_postgres.py', you need to modify the credential string in the file:

```python
credential = 'postgres://youname:yourpwd@ip_adress:5432/name_db'
```

Then, you can run:
```bash
python scripts/write_data_to_postgres.py
```
- After the data have been uploaded, you need to update the geometry field 'geom4326' in the database and create and index for run the query faster, with the following  SQL commands:

```sql
 -- create geometry values
 UPDATE poi.anemity SET geom4326 = ST_GeomFromText('POINT(' || lng || ' ' || lat || ')',4326);

 -- create index
 CREATE INDEX poi_anemity_geom4326_gist ON poi.anemity USING gist(geom4326);
```

- Check if the geometry field 'geom4326' are not null:

```sql
select * from poi.anemity
```

## Run the Service in localhost

-  We assume that you have already an instance of PostGIS up and running  (locally or remote) with the data.

- To run the service in localhost:

```bash
python run-localhost.py config/localhost.json
```

- The file localhost.json contains some inputs:

```json
{
  "SERVER_DB": "sever db to specify",
  "DBNAME": " db name to specify ",
  "USER": "used db to specify ",
  "PWD": "pwd db to specify",
  "DEBUG" : 1,
  "PORT" : 5005,
  "APPLICATION_HOST" : "localhost",
  "URL_PREFIX" : "/restpoi",
  "LOG_F_NAME" : "ers.log",
  "DEFAULT_RADIUS" : 200
}
```
- debug = 1 will print some info when a request will hit the the service.
- URL_PREFIX is used to name the url for the service (I will explain this later in the session 'Notes about the code'.)
- default radius (in meter) is used if the post request will not specify the radius in input

- if the service is up, you should have something like this:
```bash
 * Serving Flask app "run-localhost" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://localhost:5005/ (Press CTRL+C to quit)
```

- now, you can lunch a post request as following:

```bash
curl -X POST -H  "Content-Type: application/json" -d '{"lat":51.5369436, "lng":-0.0767174, "radius":200}' http://localhost:5005/restpoi/poi/poifromcoord
```

An example of endpoint that runs on  Heroku:

```bash
curl -X POST -H  "Content-Type: application/json" -d '{"lat":51.5369436, "lng":-0.0767174, "radius":200}' https://geo-rest-service.herokuapp.com/restpoi/poi/poifromcoord
```

- For example, if you have the service in localhost and you lunch a post request you should have something like this:

```bash
$ curl -X POST -H  "Content-Type: application/json" -d '{"lat":51.5369436, "lng":-0.0767174, "radius":200}' http://localhost:5005/restpoi/poi/poifromcoord

{"type": "FeatureCollection", "features": [{"type": "Feature", "id": 0, "geometry": {"type": "Point", "coordinates": [-0.0767174, 51.5369436]}, "properties": {"value": "telephone"}}, {"type": "Feature", "id": 1, "geometry": {"type": "Point", "coordinates": [-0.0765892, 51.5384183]}, "properties": {"value": "post_box"}}, {"type": "Feature", "id": 2, "geometry": {"type": "Point", "coordinates": [-0.0789765, 51.5366022]}, "properties": {"value": "restaurant"}}, {"type": "Feature", "id": 3, "geometry": {"type": "Point", "coordinates": [-0.077055, 51.53678]}, "properties": {"value": "car_sharing"}}, {"type": "Feature", "id": 4, "geometry": {"type": "Point", "coordinates": [-0.0769705, 51.5352734]}, "properties": {"value": "pub"}}, {"type": "Feature", "id": 5, "geometry": {"type": "Point", "coordinates": [-0.0764387, 51.5383578]}, "properties": {"value": "atm"}}, {"type": "Feature", "id": 6, "geometry": {"type": "Point", "coordinates": [-0.0787015, 51.536925]}, "properties": {"value": "restaurant"}}, {"type": "Feature", "id": 7, "geometry": {"type": "Point", "coordinates": [-0.0765497, 51.53847]}, "properties": {"value": "bicycle_parking"}}, {"type": "Feature", "id": 8, "geometry": {"type": "Point", "coordinates": [-0.0765569, 51.5383961]}, "properties": {"value": "bicycle_parking"}}, {"type": "Feature", "id": 9, "geometry": {"type": "Point", "coordinates": [-0.0792785, 51.5371169]}, "properties": {"value": "grit_bin"}}, {"type": "Feature", "id": 10, "geometry": {"type": "Point", "coordinates": [-0.0756359, 51.5373217]}, "properties": {"value": "restaurant"}}, {"type": "Feature", "id": 11, "geometry": {"type": "Point", "coordinates": [-0.0758015, 51.5369207]}, "properties": {"value": "cafe"}}, {"type": "Feature", "id": 12, "geometry": {"type": "Point", "coordinates": [-0.0758099, 51.5365652]}, "properties": {"value": "bicycle_rental"}}, {"type": "Feature", "id": 13, "geometry": {"type": "Point", "coordinates": [-0.0791622, 51.537288]}, "properties": {"value": "bicycle_rental"}}, {"type": "Feature", "id": 14, "geometry": {"type": "Point", "coordinates": [-0.0774854, 51.5357686]}, "properties": {"value": "community_centre"}}, {"type": "Feature", "id": 15, "geometry": {"type": "Point", "coordinates": [-0.0766026, 51.5368875]}, "properties": {"value": "arts_centre"}}]}
```
- **Note** , if you run curl using the Heroku signature, the results could be slow the first time, because I am using a free instance, and **Heroku sleeps after 30-mins of inactivity the service**.

## Deploy the Service in  Heroku

- First, you need to create an account Heroku, then you can use the Heroku console to deploy the code as in GitHub.
```bash
 $ git add .
 $ git commit -am "make it better"
 $ git push heroku master
 ```
- You need also to attach to your app a PostGIS dyno.
- Heroku will give you all the fields that will help you to access the PostGIS dyno (DB) using PgAdmin.
- When, you have access to the DB, you can just create the database as explained in the previous session.
- Few notes and commands for deploying the service on Heroku:
    - you need to use the Procfile to tell Heroku what it should run:
    ```bash
      web: gunicorn 'run-heroku:load_app("config/heroku.json")'
    ```
    - The file Procfile specifies which application to run remotely and which file the app should use as configuration file,
    - Remotely, we are also using the web server gunicorn.
    - In "config/heroku.json" :
        -  you need to specify the DB credential that you can read from the PostGIS dyno (with the data) attached to the Heroku app.
        - The debug is also set to 0 and you don't need to have a port and application host (the biding with an IP address and a port will be done automatically by Heroku) as for the localhost.
- Some commands that can help you to manage  the Heroku app:
```bash
 heroku login (to login in Heroku)
 heroku logs --tail (to read the log of your deployed app)
 heroku drains (to clean log of your deployed app)
 heroku restart -a app_name (to restart your app )
 heroku run bash (to run bash command Heroku )
 heroku apps (to show what are the name of the apps that are running)
```
Note if you have an error like '..already in use..', it is because you are using both gunicorn and Flask, so you need to avoid to lunch the method 'run()' in python.
This is why 'run-heroku.py' return just the pointer to the Flask object.


## Notes about the code

- The REST interface is defined in application.py. In particular, the following instruction is used to register the method (RetrivePoiFromCoord) to respond to the post request :
 ```python
api_poi.add_resource(RetrivePoiFromCoord, '/poifromcoord',resource_class_kwargs={'datasource': datasource,'conf':conf})
```
-The syntax of the url :
 ```bash
http://localhost:5005/restpoi/poi/poifromcoord
```
has the following meaning:
		- restpoi is the basic url prefix
		- poi is the api that have been created in application.py.
		- poifromcoord is the string associated to the method used to respond to the post request

- If you would like to create a new API (endpoint), you need to add code similar to:

```python
- API_NAME = 'poi'
api_poi_bp = Blueprint('poi_api', __name__)
url_prefix = '{prefix}/{name}'.format(prefix=conf.PARAM['URL_PREFIX'], name=API_NAME)
api_poi = Api(api_poi_bp, prefix=url_prefix)
api_poi.add_resource(RetrivePoiFromCoord, '/poifromcoord',resource_class_kwargs={'datasource': datasource,'conf':conf})
app.register_blueprint(api_poi_bp)
```
or if you want to add just new service on the same API just register a new method in the same API as done in
 ```python
api_poi.add_resource(RetrivePoiFromCoord, '/poifromcoord',resource_class_kwargs={'datasource': datasource,'conf':conf})
```
- The code implements a **DAO pattern**, which helps your to map the relational table to an class object.

- The range query used to retrieve the POI is based on the PostGIS operators and it is similar to this one:
```sql
Query:  SELECT * from poi.anemity WHERE  ST_DWithin(st_transform(geom4326,26986),st_transform(ST_SetSRID(ST_Point(-0.0767174,51.5369436),4326),26986),200)
```
- 26986  RID is used because the radius is expressed in meters


## Donations

![AVSI](https://i.imgur.com/oRnsKLL.jpg)


- **If you found this code useful, please condider to make a donation to [AVSI](https://www.avsi.org/en/)**
    - https://www.avsi.org/en/country/
    - http://www.avsi-usa.org/donate.html
    - https://www.avsi.org/it/donation/

## Authors

   **Antonio Penta**
