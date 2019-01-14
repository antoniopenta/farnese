
--create schema
create schema poi;


-- create table
CREATE TABLE poi.anemity
(
  id serial,
  lat double precision,
  lng double precision,
  amenity_type character varying(50),
  name character varying(1000),
  geom4326 geometry
);


--add some constraints
alter table poi.anemity add primary key (id);



