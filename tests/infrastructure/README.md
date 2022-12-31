These services located in the test/infrastructure directory are used to build a quick and dirty test/lab build of FreeRADIUS with MariaDB + Maxscale Proxy/Loadbalancer to mimic a real deployment of FreeRADIUS.

Directory Structure explained:

/docker-entrypoint-initdb.d     -   Contains database init scripts to populate the test database with some basic users/groups/check/reply attributes
/freeradius                     -   Contains minimal configuration to work with this test infrastructure folder. Edit clients.conf for any IP addresses you need to communicate with Radius
/maxscale                       -   Minimal configuration for a read-only (port tcp/4008) and read/write (port tcp/4008) service, connecting to the mariadb container