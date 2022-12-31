---
--- Create Maxscale replication account
---
CREATE USER 'maxscale'@'%' IDENTIFIED BY 'maxscale';

--
--  Create default administrator for RADIUS
--
CREATE USER 'radius'@'radius_maxscale' IDENTIFIED BY 'radius';
CREATE USER 'radius'@'radius' IDENTIFIED BY 'radius';

--
--  Create our radius_write user
--
CREATE USER 'radius_write'@'radius_maxscale' IDENTIFIED BY 'radius_write';
CREATE USER 'radius_write'@'%' IDENTIFIED BY 'radius_write';

--
--  Create our radius_read user
--
CREATE USER 'radius_read'@'radius_maxscale' IDENTIFIED BY 'radius_read';
CREATE USER 'radius_read'@'radius' IDENTIFIED BY 'radius_read';
