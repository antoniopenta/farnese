-- create geometry values
UPDATE poi.anemity SET geom4326 = ST_GeomFromText('POINT(' || lng || ' ' || lat || ')',4326);

-- create index
CREATE INDEX poi_anemity_geom4326_gist ON poi.anemity USING gist(geom4326);
