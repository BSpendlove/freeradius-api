# freeradius-bng-api

This project/API isn't affiliated with FreeRADIUS but can sit on a FreeRADIUS server (or a separate server out of line with FreeRADIUS) to manage your FreeRADIUS database backend and add users/groups/attributes by exposing a few useful HTTP endpoints.

---

Would you rather be running INSERT statements against your FreeRADIUS database like this:

```
INSERT INTO radcheck (username, attribute, op, value) VALUES ('myUserName', 'Cleartext-Password', ':=', 'TestFromSQL')
INSERT INTO radreply (username, attribute, op, value) VALUES ('myUserName', 'Cisco-AVPair', '+=', 'test=true')
INSERT INTO radreply (username, attribute, op, value) VALUES ('myUserName', 'Cisco-AVPair', '+=', 'something=1.2.3.4')
INSERT INTO radusergroup (username, groupname, priority) VALUES ('myUserName', 'someGroupName', '123')
```

Or like this:
```
curl --location --request POST 'http://localhost:8083/api/v1/radius/users/' \
--header 'x-api-token: my-super-secure-api-token' \
--header 'Content-Type: text/plain' \
--data-raw '{
    "username": "myUserName",
    "check_attributes": [
        {
            "attribute": "Cleartext-Password",
            "op": ":=",
            "value": "TestFromAPI"
        }
    ],
    "reply_attributes": [
        {
            "attribute": "Cisco-AVPair",
            "op": "+=",
            "value": "test=true"
        },
        {
            "attribute": "Cisco-AVPair",
            "op": "+=",
            "value": "something=1.2.3.4"
        },
        {
            "attribute": "Cisco-AVPair",
            "op": "+=",
            "value": "addr=3.3.3.3"
        }
    ],
    "groups": [
        {
            "groupname": "someGroupName",
            "priority": 123
        }
    ]
}'
```

If you prefer the first option then close down this page and continue with your life because this project isn't for you... :-)

## Introduction

This python FastAPI app is created to work with a BNG type deployment (mainly tested in an internet service provider environment), however that doesn't mean it is limited to only that type of scenario, this API is actually built to interact with a database (supported by SQLAlchemy as long as freeradius has a driver for it) and can be used as a generic HTTP API for adding attribute pairs and users/groups into the database. Depending on your type of network, you may want to deploy this as a central API that interacts with your database backend to manage RADIUS attributes that are used during the AAA process of your BNG. Another way to deploy it if you are working on a smaller scale and have limited resources, running FreeRadius and the relevant database (which needs to implemented as a database driver) on the same VM however this isn't typically recommended in a production network.

Instead of giving applications direct access to your RADIUS backend database, you can put this API inbetween the OSS/BSS/External scripts world and the Radius infrastructure. Here are some deployment examples that you can consider:

![Deployment #1](docs/imgs/deployment_1.png)

![Deployment #2](docs/imgs/deployment_2.png)

![Deployment #3](docs/imgs/deployment_3.png)

![Deployment #4](docs/imgs/deployment_4.png)

## Environment Variables

Within the [app/config](./app/config/) folder there is an `app.py` file that contains the mapping of environment variables and 2 variables that can't be set in your docker image/docker-compose.yml, these are:

```
validate_avpairs: bool = False
freeradius_dictionary_paths: list = ["/freeradius_dictionaries"]
```

Any other variable can be set in the docker-compose.yml, or your .env file can be passed which might contain variables like this:

```
API_TOKEN_KEY=x-api-token
API_TOKEN=my-super-secure-token
SQLALCHEMY_DATABASE_URL="mysql+pymysql://username:password@localhost:3006/radius?charset=utf8mb4"
MONGODB_DATABASE_URI=mongodb://freeradius:changemeP!z@mongo:27017/
```

## Basic attribute check/reply valdiation - Not implemented currently with the new API routes

If you choose to run `validate_avpairs` as `True`, then ensure you pass the local FreeRADIUS dictionary path which is by default: `/usr/share/freeradius/` like this:

```
version: '3.1'

services:
  freeradius_bng_api:
    build: .
    volumes:
      - /usr/share/freeradius/:/freeradius_dictionaries:ro
```

Then if you set your `freeradius_dictionary_paths` variable to `["/freeradius_dictionaries"]` then the app will attempt to look at any files within this directory and parse them using the ttp python module. Any vendors and attributes will be added to the local MongoDB container, this can be a remote MongoDB replica set and shared between multiple docker instances this API runs on and assumes you have the same `vendor.dictionary` files loaded on each FreeRADIUS server.

I will in the future, provide some kind of validation check to further look into sub-attribute valdiation, for example with Cisco-AVPair and validating the "sub" AV pair `default-ipv4-gateway=100.70.254.1`, however for now I have only focused on the main vendor specific attributes that can be loaded.

If you want to prevent this validation and allow any attribute to be created in the radcheck, radreply, radgroupcheck and radgroupreply database tables, then ensure `validate_avpairs` is set to `False` in the `/api/config/app.py` file.

## Running the application

I am certain this section will be updated in the future however for now, you can just clone this project, copy the `.env-example` and rename it to `.env`, fill out the environment variables as required and then finally run `docker-compose up --build`.

You should technically be able to run this API across multiple FreeRADIUS servers natively without any additional changes however the minimal logging in the API will not be centralized, this is down to the user to properly implement centralized logging. While it is technically possible to perform attribute validation when the API isn't running directly on the FreeRADIUS servers, I have found this API works best when you are running it directly on the FreeRADIUS server and then work on the basis of if your radius server is down

## Running in production

Currently, I have a private fork of this API which is heavily modified to be used in production but I am slowly open-sourcing the parts I am allowed to since I work on this during my spare time. Saying that, there isn't anything complicated (or even any) security in place so I would suggest if you run this in production to modify it and ensure you use HTTPS with OAuth2 tokens or something along those lines.

The initial reason why I called this "freeradius-bng-api" is because I am not focusing on enterprise type radius attributes/profiles in the database during my testing, so with time there will be additional API endpoints that perform certain functions based on a specific vendor (eg. Cisco and Juniper) according to their best practices and attributes that should be added to the relevant users/group database tables. For example to add a user that is purely authorized and then given a speed package (eg. 150Mbps) then this can be consolidated into a single endpoint to add the Group which will automatically add the sub-qos in/out policies along with any additional parameters passed into the request like the accounting list, VRF or loopback etc... However this is all possible right now with the ability to simple create users/groups and call the relevant attribute API endpoint (eg. `http://freeradius-bng-api:8083/api/v1/radius/groups/SPEED_150/attribute/reply` to add an attribute to the radgroupreply table)

## Why would I use this?

Personally, I think the users/groups/attributes stored in the radius database tables are a little bit cluttered, a specific user/group may be returned multiple attributes but you need to manually correlate this together using database queries, I have done this for you so you:

1) Don't have to do it :-)
2) have correlated data from the API endpoint about a specific user, what groups they are in, and which attributes (both radcheck/radreply) relate to them.
3) Full support for all default freeradius database tables (as long as you haven't renamed them! however this is easy to change if required)
4) COA support - Either build your request manually via the route `/api/v1/radius/coa/{ip_address}` or use the routes to send COA attributes via either an Acct-Session-Id or Username like so `/api/v1/radius/coa/session/username/someusername` or `/api/v1/radius/coa/session/13522473`. These routes will make use of the existing radacct table to pull the latest session information to send to the relevant NAS IP address
5) Create RADIUS users and groups in a more efficient manner using the `/api/v1/radius/groups/` and `/api/v1/radius/users/` endpoints to add your check/reply attributes and user->group mappings in a single POST request (or delete if you want to delete all related attributes and user/group mappings)

Database Tables and API Endpoint mappings, POST, GET, UPDATE and DELETE are typically supported on all API routes for CRUD operation (Create, Read, Update and Delete)
```
nas             -   /api/v1/radius/nas/ [GET, POST, DELETE, PUT]
radacct         -   /api/v1/radius/radacct/ [GET, DELETE]
radpostauth     -   /api/v1/radius/radpostauth/ [GET, DELETE]
radcheck        -   /api/v1/radius/radcheck/ [GET, POST, DELETE, PUT]
radreply        -   /api/v1/radius/radreply/ [GET, POST, DELETE, PUT]
radgroupcheck   -   /api/v1/radius/radgroupcheck/ [GET, POST, DELETE, PUT]
radgroupreply   -   /api/v1/radius/radgroupreply/ [GET, POST, DELETE, PUT]
radusergroup    -   /api/v1/radius/radusergroup/ [GET, POST, DELETE, PUT]
```

Useful API endpoints that make life easier:
```
Create a user with attribute/group mappings         -   /api/v1/radius/users/ [POST]
Delete a user and the attribute/group mappings      -   /api/v1/radius/users/ [DELETE]
Get a user with attribute/group mappings            -   /api/v1/radius/users/{username} [GET]

Create a group with attribute/user mappings         -   /api/v1/radius/groups/ [POST]
Delete a group and the attribute/user mappings      -   /api/v1/radius/groups/ [DELETE]
Get a group with attribute/user mappings            -   /api/v1/radius/groups/{groupname} [GET]
```

For more details, visit the `API Documentation` section.

---

Below is an example of a specific user where FreeRADIUS will return IP information, VRF and Loopback interface to assign a static IP for a customer that pays for a 150Mbps service:

```
http://freeradius-bng-api:8083/api/v1/radius/users/4816c6b1-8176-4481-9863-0077cf35f05d

{
    "username": "4816c6b1-8176-4481-9863-0077cf35f05d",
    "groups": [
        {
            "id": 36,
            "groupname": "SPEED_150",
            "priority": 100
        }
    ],
    "check_attributes": [
        {
            "id": 21,
            "attribute": "Cleartext-Password",
            "op": ":=",
            "value": "default"
        }
    ],
    "reply_attributes": [
        {
            "id": 46,
            "attribute": "Cisco-AVPair",
            "op": "+=",
            "value": "delegated-prefix=2001:db8:1800::/48"
        }
    ]
}
```

## Adding your own custom routes/models/schemas

Currently there isn't a strict way of adding your own API routes, models and schemas however following best practices to ensure you are not overwriting existing files that make up the core project such as:

1) Custom Endpoints must be located in their own separate folder within the `api_v1\extended` folder
2) Custom Schemas and Models should be created in their own separate files within the related `extended` folder and then imported at the bottom of the `__init__.py` files. Examples are included for COA endpoint/schemas and Cisco BNG deployment

You can take a look at the [COA](./app/api/api_v1/extended/coa.py) example which is an extension to the API that doesn't belong to "directly interacting with FreeRADIUS database".

## API Documentation

You can visit the `/docs` endpoint to view an automatically generated swagger documentation for the common endpoints such as creating/reading/deleting users and groups, and adding check/reply attributes. However I will slowly be working on other documentation to go alongside with the in-build swagger UI documentation.

## TO DO

- Either fix pyrad or implement a radius COA client myself in Python because its terribly maintained (some FreeRADIUS dictionary files are not parsed properly)

- Potentially restructure the project since its getting a bit messy already...