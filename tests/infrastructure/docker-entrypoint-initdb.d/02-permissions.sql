---
---  Allow Maxscale to view mysql users and additional SELECT statements
---
GRANT SHOW DATABASES ON *.* TO 'maxscale'@'%';
GRANT SELECT ON mysql.user TO 'maxscale'@'%';
GRANT SELECT ON mysql.db TO 'maxscale'@'%';
GRANT SELECT ON mysql.tables_priv TO 'maxscale'@'%';
GRANT SELECT ON mysql.roles_mapping TO 'maxscale'@'%';
GRANT SELECT ON mysql.* TO 'maxscale'@'%';

GRANT BINLOG ADMIN,
   READ_ONLY ADMIN,
   RELOAD,
   REPLICA MONITOR,
   REPLICATION MASTER ADMIN,
   REPLICATION REPLICA ADMIN,
   REPLICATION REPLICA,
   SHOW DATABASES
   ON *.*
   TO 'maxscale'@'%';

--
--  The server can read the authorisation data
--
GRANT SELECT ON radius.radcheck TO 'radius'@'radius_maxscale';
GRANT SELECT ON radius.radreply TO 'radius'@'radius_maxscale';
GRANT SELECT ON radius.radusergroup TO 'radius'@'radius_maxscale';
GRANT SELECT ON radius.radgroupcheck TO 'radius'@'radius_maxscale';
GRANT SELECT ON radius.radgroupreply TO 'radius'@'radius_maxscale';

GRANT SELECT ON radius.radcheck TO 'radius'@'radius';
GRANT SELECT ON radius.radreply TO 'radius'@'radius';
GRANT SELECT ON radius.radusergroup TO 'radius'@'radius';
GRANT SELECT ON radius.radgroupcheck TO 'radius'@'radius';
GRANT SELECT ON radius.radgroupreply TO 'radius'@'radius';

--
--  The server can write accounting and post-auth data
--
GRANT SELECT, INSERT, UPDATE ON radius.radacct TO 'radius'@'radius_maxscale';
GRANT SELECT, INSERT, UPDATE ON radius.radpostauth TO 'radius'@'radius_maxscale';
GRANT SELECT, INSERT, UPDATE ON radius.radacct TO 'radius'@'radius';
GRANT SELECT, INSERT, UPDATE ON radius.radpostauth TO 'radius'@'radius';

--
--  The server can read the NAS data
--
GRANT SELECT ON radius.nas TO 'radius'@'radius_maxscale';
GRANT SELECT ON radius.nas TO 'radius'@'radius';

--
--  In the case of the "lightweight accounting-on/off" strategy, the server also
--  records NAS reload times
--
GRANT SELECT, INSERT, UPDATE ON radius.nasreload TO 'radius'@'radius_maxscale';
GRANT SELECT, INSERT, UPDATE ON radius.nasreload TO 'radius'@'radius';

---
---  radius_write
---
GRANT ALL PRIVILEGES ON radius.* TO 'radius_write'@'radius_maxscale' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON radius.* TO 'radius_write'@'%' WITH GRANT OPTION;

---
---  radius_read
---
GRANT SELECT ON radius.radcheck TO 'radius_read'@'radius_maxscale';
GRANT SELECT ON radius.radreply TO 'radius_read'@'radius_maxscale';
GRANT SELECT ON radius.radusergroup TO 'radius_read'@'radius_maxscale';
GRANT SELECT ON radius.radgroupcheck TO 'radius_read'@'radius_maxscale';
GRANT SELECT ON radius.radgroupreply TO 'radius_read'@'radius_maxscale';
GRANT SELECT ON radius.radacct TO 'radius_read'@'radius_maxscale';
GRANT SELECT ON radius.radpostauth TO 'radius_read'@'radius_maxscale';
GRANT SELECT ON radius.nas TO 'radius_read'@'radius_maxscale';
GRANT SELECT ON radius.nasreload TO 'radius_read'@'radius_maxscale';

GRANT SELECT ON radius.radcheck TO 'radius_read'@'radius';
GRANT SELECT ON radius.radreply TO 'radius_read'@'radius';
GRANT SELECT ON radius.radusergroup TO 'radius_read'@'radius';
GRANT SELECT ON radius.radgroupcheck TO 'radius_read'@'radius';
GRANT SELECT ON radius.radgroupreply TO 'radius_read'@'radius';
GRANT SELECT ON radius.radacct TO 'radius_read'@'radius';
GRANT SELECT ON radius.radpostauth TO 'radius_read'@'radius';
GRANT SELECT ON radius.nas TO 'radius_read'@'radius';
GRANT SELECT ON radius.nasreload TO 'radius_read'@'radius';
