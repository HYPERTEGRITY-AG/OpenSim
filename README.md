![GitHub Workflow Status](https://img.shields.io/github/workflow/status/HYPERTEGRITY-AG/OpenSim/all-lints)

# Open Smart City - Sim

Copyright (c) 2021 Will Freitag, Version: 1.1.1

## TL;DR
_oscsim_ is a lightweight tool to send test data to an Orion Context Broker or FROST-Server respectively. \
It can be used to send just a single message to test your installation and also to send thousands of messages in multiple threads in order to stress your installation. \
Creation of test-data w/o integrating any sensors is another aspect that can be handled with this tool. \
For this to end, not the complete APIs of both, Orion and FROST are implemented (it's not an Orion- or FROST-Client!), but the API needed to send Data (Contexts and Things/Datastreams/Observations resp.) is in place.  

A simple call of this tool like...
```commandline
$ oscsim -s http://myserver.com -p NGSI-V2 -ad dateObserved -an temperature,f,20.5
```
...will send one context to an Orion Context Broker at myserver.com with a payload defining a weather observation (date and temperature).  
And if you don't want to read this documentation at all: Remember that you can use --help at any time! :-)
```commandline
$ oscsim -h
Open Smart City-Sim, Copyright (c) 2021 Will Freitag, Version 1.1.1
usage: oscsim [-h] -s [protocol]host-name [-p {NGSI-V2,NGSI-LD,SensorThings-MQTT,SensorThings-HTTP}] [-i]
              [-a id] [-H key value] [-f id] [-e PREFIX] [-o POSTFIX] [-c] [-n num] [-m num] [-u]
              [-q milliseconds] [-l seconds] [-y name] [-an name,type,number[,max-number]] [-as name value]
              [-ad name] [-al name,lat,long[,max-lat,max-long]] [-ab name value] [-ai indent] [-r] [-v]
              [-d from to]
Tool to create some load on Orion Context Broker/FROST-Server.

optional arguments:
  -h, --help            show this help message and exit
  -s [protocol]host-name, --server [protocol]host-name
                        This host-name will be prepended by "https://", if protocol is omitted and appended with
                        "/v2/" (NGSI-V2), "/ngsi-ld/v1" (NGSI-LD) or "/v1.1/" (SensorThings) resp. depending on
                        the server-type (see -p/--protocol).
  -p {NGSI-V2,NGSI-LD,SensorThings-MQTT,SensorThings-HTTP}, --protocol {NGSI-V2,NGSI-LD,SensorThings-MQTT,SensorThings-HTTP}
                        Define the type of server. [Default: NGSI-V2]
  -i, --insert-always   [Only NGSI-V2 and NGSI-LD!] If set, the contexts will always be inserted (via POST with
                        option 'upsert') instead of trying to update first (via PATCH) and insert (via POST), if
                        not existing (i.e. PATCH returns '404 Not Found').
  -a id, --datastream-id id
                        [Only SensorThings!] If set, this Datastream-Id will be used for ALL Observations,
                        instead of first searching for the Thing by it's name and the correct Datastream-Id
                        afterwards.
  -H key value, --header key value
                        Define a header by key and value.
  -f id, --first-id id  Define the first id to be used or the one to be used if '-c/--static-id' is set.
                        [Default: 1]
  -e PREFIX, --prefix PREFIX
                        If set, the prefix will be prepended to the generated id.
  -o POSTFIX, --postfix POSTFIX
                        If set, the postfix will be appended to the generated id.
  -c, --static-id       If set, the id will not increment (i.e. -n times -m messages will be sent with the same
                        id ['-f/--first-id' or '1' if omitted]).
  -n num, --num-threads num
                        Define, how many threads shall be used. [Default: 1]
  -m num, --messages num
                        Define, how many messages per thread shall be sent (ignored, if '-u/--unlimited' ist
                        set). [Default: 1]
  -u, --unlimited       If set, '-m/--messages' is ignored and infinite messages will be send (in '-n/--num-
                        threads' threads). Hit 'Ctrl-C' to interrupt or set '-l/--limit-time'.
  -q milliseconds, --frequency milliseconds
                        If set, limits the frequency of the messages sent to the given number (per thread!).
  -l seconds, --limit-time seconds
                        Only in conjunction with '-u/--unlimited': Stops after the given time in seconds.
  -y name, --type name  [Only NGSI-V2 and NGSI-LD!] If set, this type-name will be used in the payload.
  -an name,type,number[,max-number], --attribute-number name,type,number[,max-number]
                        Define a number attribute used for the payload by 'name' (The name of the attribute,
                        e.g.: temperature), 'type' (One of i [integer] or f [floating point])and 'number' (The
                        value to be used). If 'max-number' is set, the number written will be randomly between
                        'number' and 'max-number' (each including). Note: Multiple number attributes can be
                        defined by repeating -an.
  -as name value, --attribute-string name value
                        Define a string attribute used for the payload by 'name' (The name of the attribute,
                        e.g.: instruction) and 'value' (the actual string). Note: Multiple string attributes can
                        be defined by repeating -as.
  -ad name, --attribute-date name
                        [Only NGSI-V2!] Define a DateTime attribute used for the payload by 'name' (The name of
                        the attribute, e.g.: dateObserved). Note: The current time is used as value. Multiple
                        DateTime attributes can be defined by repeating -ad.
  -al name,lat,long[,max-lat,max-long], --attribute-location name,lat,long[,max-lat,max-long]
                        [Only NGSI-V2!] Define a location attribute used for the payload by 'name' (The name of
                        the attribute, e.g.: position), 'lat' (The value for latitude) and 'long' (The value for
                        longitude). If 'max-lat' and 'max-long' are set, the location written will be randomly
                        between 'lat' and 'max-lat' and 'long' and 'max-long' resp. (each including). Note:
                        Multiple location attributes can be defined by repeating -al.
  -ab name value, --attribute-boolean name value
                        [Only NGSI-V2!] Define a boolean attribute used for the payload by 'name' (The name of
                        the attribute, e.g.: public) and 'value' (One of 'true', 'false' or 'toggle' [ie.
                        randomly switch between true and false]). Note: Multiple boolean attributes can be
                        defined by repeating -ab.
  -ai indent, --attribute-indent indent
                        Define the number of characters for indenting the created payload. [Default: 0]
  -r, --dry-run         Do a dry run only - giving the chance to review what WOULD be done incl. seeing what the
                        payload will look like.
  -v, --verbose         Generate verbose output.
  -d from to, --delete from to
                        If set, the entities within the given range (including "from" and "to") will be deleted.

Example #1:
oscsim -s my-host.com -H Authorization 'Bearer 039ea6d72a2f32227c2110bd8d78aae33acd6782' -H Fiware-service
curltest
One message is sent using id '1'.
The tenant 'curltest' will be used as 'Fiware-service' in the header of the post.

Example #2:
ocssim -s my-host.com -n 2 -m 50 ...git commit -a -m "removed mypy from linting - it has a bug reporting false positive"

100 messages will be sent (2 threads are sending 50 messages each).The id will be looped from '1' to '100'.

Example #3:
oscsim -s my-host.com -n 5 -m 100 -f 123 -c ...
500 messages will be sent (5 threads are sending 100 messages each).The id '123' (-f is first id) will be used
for all messages (-c is static id).

Example #4:
The payload that will be sent is constructed from the -y and the -aX parameters. Example:
oscsim -y WeatherObserved -an temperature,f,-20,50 -an precipitation,i,1,20 ...
will generate a payload looking like:
{
  "id":"1",
  "type":"WeatherObserved",
  "temperature": {
    "type": "Number",
    "value": -2.3
  },
  "precipitation": {
    "type": "Number",
    "value": 13
  },
}

Example #5:
oscsim -d 100 200 -s my-host.com -H Authorization 'Bearer 039ea6d72a2f32227c2110bd8d78aae33acd6782'

This will delete all IDs starting from 100 to 200 (inclusive).
```
## Why Not Simply Use "curl" or "Postman/Newman"?
While it's easy to think about a shell script, that runs curl in a loop adding data via the backend's REST-Api, one important drawback is, that if your server is TLS-secured ('https://...), curl isn't able to cache that TLS-handshake. That means, that EVERY call will do this handshake ending up in response times like one or more seconds. It's hard to generate load this way with hundreds of messages per second. Putting more than one URL in a single curl is a solution for this, but it's hard to aggregate the results and what, if there is more logic needed (e.g. Call this URL after that URL, but only if the first call gave you an 404...)  

Postman is a nice "alternative" for curl - not only because of its nice UI and tons of useful features. Beside all of that, it is able to run in a batch mode (together with Newman), AND it caches TLS-handshakes as well! But still it's hard to generate load, since Postman is resource consuming and when you run more than one instance simultaneously, you'll soon find out your test-machine is the bottleneck. 

# Supported Backends
This script is tested with:
* Orion Context Broker, 2.5.0
* Orion-LD, post-v0.7 (experimental)
* FROST-Server, 1.13.0-SNAPSHOT  

Other versions may be compatible, but we do not currently run tests against those.
  
# Supported Python Versions
Python 3.6 and 3.7 are fully supported and tested (Linux and Windows).  
This script may work on later versions of 3, but we do not currently run tests against those versions.

# Installation
## From Package
### Install
Run `pip[3] install ocssim`.
### Run Open Smart City-Sim
Simply run `oscsim`.
## From Source
### Get Repository
Clone or download repository from [Github](https://github.com/HYPERTEGRITY-AG/OpenSim).
### Prerequisites
By running: `pip[3] install -r requirements.txt [--user]` the required libraries can be installed at once.  
Alternatively, the required libraries can be installed manually.  
Following libraries need to be installed:
* **Requests**  \
Web-site: https://github.com/psf/requests \
Install with: `$ pip install requests`
* **Eclipse Paho™ MQTT Python Client** \
Web-site: https://github.com/eclipse/paho.mqtt.python \
Install with: `$ pip install paho-mqtt`
### Run Open Smart City-Sim
From the `src` directory run `python[3] -m oscsim`.
## What's that "ID"?
In Orion Context Broker (NGSI-XX), Contexts are stored as entities, and these entities are referred by their **"id"** (e.g. "urn:ngsi-v2:AirQualityObserved:RZ:Obsv4567"). Such an entity will then have some meta-data and one or more attributes. \
In FROST (SensorThings), It all starts with a "Thing" that has a **"name"** and an internal (numeric) id. Dependencies (Datastreams, Observations) are related to that internal id that is generated by FROST. \
oscsim uses a numeric "id" (starting with simply '1') that can easily be looped. 
This id is then used as the entity's "id" (Orion) and "name" (FROST) respectively.    
Please note: This numeric id can be prepended/appended with strings, letting it look more like a "real" entity/thing, if wanted.

## What is a "Message"?
A "message" is the attempt, to store a single attribute (SensorThings) or one or more attributes at once (NGSI-XX). For this attempt, one or more calls to the server's API are needed, depending on the type of server (NGSI or ServerThings), the scheme that is used (NGSI), a looping or static id (SensorThings) and even the number of messages and attributes (SensorThings).  

| # | Backend | Scheme | Protocol | Static-Id | # of Messages | # of Attributes | API-Access | Summary |   
| --- | --- | --- | --- | --- | --- | --- | --- | --- |  
| 1.1 | NGSI-XX | POST-Always | - | yes/no | 1-n | 1-n | 1 POST with 'upsert' | 1 access |  
| 1.2 |  | PATCH/POST | - | yes/no | 1-n | 1-n | 1 PATCH and if not found, 1 POST afterwards (but only once per entity) | 1 access for known entities, <br>2 accesses for new entities |  
| 2.1 | ServerThings | - | HTTP | yes | 1 | 1 | 1 GET on _Things_ to get the thing-id and if not found, 1 POST on _Things_ to create thing and 1 more GET to get thing-id from _Things_. 1 GET on Datastreams to get datastream-id and if not found, 1 POST on _Datastreams_ to create datastream and 1 more GET to get thing-id from _Datastreams_. 1 POST on _Observations_. | 7 accesses for a new Thing, <br>5 accesses for a known Thing and new Datastream, <br>3 accesses for known Thing and known Datastream |  
| 2.2 |              | - |      | yes | n | 1 | 1 GET on _Things_ to get the thing-id and if not found, 1 POST on _Things_ to create thing and 1 more GET to get thing-id from _Things_. 1 GET on Datastreams to get datastream-id and if not found, 1 POST on _Datastreams_ to create datastream and 1 more GET to get thing-id from _Datastreams_. 1 POST on _Observations_. | Like 2.1 for the first message, 3 accesses for all others |  
| 2.3 |              | - |      | yes | 1 | n | 1 GET on _Things_ to get the thing-id and if not found, 1 POST on _Things_ to create thing and 1 more GET to get thing-id from _Things_. For each attribute: 1 GET on Datastreams to get datastream-id and if not found, 1 POST on _Datastreams_ to create datastream and 1 more GET to get thing-id from _Datastreams_. 1 POST on _Observations_. | Like 2.1 for the Thing, but up to 3 accesses for each attribute and 1 for the Observation |  
| 2.4 |              | - |      | yes | n | n | 1 GET on _Things_ to get the thing-id and if not found, 1 POST on _Things_ to create thing and 1 more GET to get thing-id from _Things_. For each attribute: 1 GET on Datastreams to get datastream-id and if not found, 1 POST on _Datastreams_ to create datastream and 1 more GET to get thing-id from _Datastreams_. 1 POST on _Observations_. | Like 2.1 for the Thing, but up to 3 accesses for each attribute and 1 for the Observation |  
| 2.5 |              | - |      | no | n | n | 1 GET on _Things_ to get the thing-id and if not found, 1 POST on _Things_ to create thing and 1 more GET to get thing-id from _Things_. For each attribute: 1 GET on Datastreams to get datastream-id and if not found, 1 POST on _Datastreams_ to create datastream and 1 more GET to get thing-id from _Datastreams_. 1 POST on _Observations_. | Like 2.1 for EVERY Thing, and up to 3 accesses for each attribute and 1 for the Observation |  
| 2.6 |              | - | MQTT | yes | 1 | 1 | 1 GET on _Things_ to get the thing-id and if not found, 1 POST on _Things_ to create thing and 1 more GET to get thing-id from _Things_. 1 GET on Datastreams to get datastream-id and if not found, 1 POST on _Datastreams_ to create datastream and 1 more GET to get thing-id from _Datastreams_. 1 PUBLISH via MQTT on that _Observation_. | 7 accesses for a new Thing, <br>5 accesses for a known Thing and new Datastream, <br>3 accesses for known Thing and known Datastream |  
| 2.7 |              | - |      | yes | n | 1 | 1 GET on _Things_ to get the thing-id and if not found, 1 POST on _Things_ to create thing and 1 more GET to get thing-id from _Things_. 1 GET on Datastreams to get datastream-id and if not found, 1 POST on _Datastreams_ to create datastream and 1 more GET to get thing-id from _Datastreams_. 1 PUBLISH via MQTT on that _Observation_. | Like 2.6 for the first message, 3 accesses for all others |  
| 2.8 |              | - |      | yes | 1 | n | 1 GET on _Things_ to get the thing-id and if not found, 1 POST on _Things_ to create thing and 1 more GET to get thing-id from _Things_. For each attribute: 1 GET on Datastreams to get datastream-id and if not found, 1 POST on _Datastreams_ to create datastream and 1 more GET to get thing-id from _Datastreams_. 1 PUBLISH via MQTT on that _Observation_. | Like 2.6 for the Thing, but up to 3 accesses for each attribute and 1 for the Observation |  
| 2.9 |              | - |      | yes | n | n | 1 GET on _Things_ to get the thing-id and if not found, 1 POST on _Things_ to create thing and 1 more GET to get thing-id from _Things_. For each attribute: 1 GET on Datastreams to get datastream-id and if not found, 1 POST on _Datastreams_ to create datastream and 1 more GET to get thing-id from _Datastreams_. 1 PUBLISH via MQTT on that _Observation_. | Like 2.6 for the Thing, but up to 3 accesses for each attribute and 1 for the Observation |  
| 2.10 |              | - |      | no | n | n | 1 GET on _Things_ to get the thing-id and if not found, 1 POST on _Things_ to create thing and 1 more GET to get thing-id from _Things_. For each attribute: 1 GET on Datastreams to get datastream-id and if not found, 1 POST on _Datastreams_ to create datastream and 1 more GET to get thing-id from _Datastreams_. 1 PUBLISH via MQTT on that _Observation_. | Like 2.6 for EVERY Thing, and up to 3 accesses for each attribute and 1 for the Observation |  

With this in mind, you should be able to find out the meaning of _msg/sec_ and how to compare throughput.  
And remember: For Orion Context Broker the overall number of messages is simply (_"--num-threads"_ x _"--num-messages"_) while for FROST the calculation is (_"--num-threads"_ x _"--num-messages"_ x _"number of attributes"_). 

## Update or Insert?
When sending a message...do I insert a new Context/Entity/Thing/whatever or am I updating an existing one?  
In short: It depends on the current data-basis. If the entity doesn't exist yet, it will be created, if it already exists, it will be updated. That means: On an empty database the very first call of _oscsim_ with one id, and an overall number of messages of one, will create a new entity while exact the same call will update the existing one if running again. So it's a good idea to keep track of the data you created and just keep in mind: _oscsim_ knows how to delete data!

# Usage

## Define the Target
Let's start with the WHERE and WHAT - where do all those message go and what kind of server is that. 
* **--server _[protocol]host-name_** \
The server - you are running your test against - will look like _data.my-domain.com_ or maybe _127.0.0.1_. Sometimes you need a special port (_domain.com:9997_) and/or sub-directory (_domain.com:1234/server_). If you omit the protocol, _'https://'_ will be prepended, so if you want to access the server unsecured, your server-parameter will look like _http://domain..._ 
* **--protocol _NGSI-V2|SensorThings-MQTT|SensorThings-HTTP_** \
Choose between _NGSI-V2_ (the server is Orion Context Broker, V2) and _SensorThings_ (here you have to choose between _HTTP_ and _MQTT_). If omitted, _NGSI_ is assumed.  
Please note: Even with _SensorThings-MQTT_, the HTTP-port of FROST will be used for finding out the Thing- and DataStream-id.  

## Define Headers
Headers are easily defined by key and value.
* **--header key value** \
This will create a Header, that looks like:
  ```
  'key':'value'
  ```
  Examples:
  ```html
  --header X-Gravitee-Api-Key YOUR-API-KEY-GOES-HERE
  Creates header:
  'X-Gravitee-Api-Key':'YOUR-API-KEY-GOES-HERE'
  
  --header Authorization "Bearer YOUR-TOKEN-GOES-HERE"
  Creates header:
  'Authorization':'Bearer YOUR-TOKEN-GOES-HERE'
  
  --header Fiware-service MY_TENANT
  Creates header:
  'Fiware-service':'MY_TENANT'
  ```

## Define the Scheme to be Used
* **--insert-always** \
[NGSI-V2 and NGSI-LD only] Storing Contexts in Orion Context Broker can be done in different ways. Two of them are used here: 
  * Try to update an Entity by PATCHing the data into a given _id_.  
    If this fails, because the entity does not exist yet, POST the data in order to create new entity. Next time, a PATCH on that _id_ will succeed.  
    The great advantage of this scheme is, that it gives you a "last chance" to perform some action (e.g. you can create a subscription on that _id_) in case, a new entity is introduced to the system.
  * Always POST your data to Orion Context Broker with 'options=upsert' and let the system decide if an insert or update has to take place. This might be slightly faster than the first approach, but you will not be aware of newly created entities.    
The first approach is default, the latter is enabled when _--insert-always_ is set.    
* **--datastream-id _id_** \
[SensorThings only] Unlike Orion Context Broker (with a flat non-SQL-Database), FROST is based on an RDBMS behind a resource-based REST-Api that doesn't let you update multiple tables at once. This is, why you have to deal first with _Things_, based on a specific _Thing_ you have to deal with its _Datastreams_ and once you gathered all the information, you can place your _Observations_ linked to a specific _Datastream_ (identified by its unique _id_).  
  In order to get rid of all the preparing stuff, you can figure out the needed _Datastream-id_ by hand (using Postman or a database-client of your choice) and set that _id_ with _--datastream-id_ directly. Open Smart City-Sim will NOT look for a _Thing_ then or find the correct _Datastream_ (by the name of the attribute), but store the attributes values immediately.  
  Be aware that those _Observations_ may corrupt (logical only, not technical) your data.

## Define the Load
Now that we know how (in general) and where we want to send our data, it's time to talk about the amount of data, we will send and how the _id_ (the unique identifier for the entities and Things respectively) is used.
* **--first-id _id_** \
Since the _id_ might be looped, it's a numeric value starting with '1'. With every message sent, this id will be increased by one. If you send 1000 messages, ids from 1 to 1000 are used. _--first-id_ can be used to set a starting id different from '1'.
* **--prefix _PREFIX_** and  **--postfix _POSTFIX_** \
These strings can be used to let your ids look a little more "realistic". So the numeric id **1027** can look like "PREFIX**1027**POSTFIX" or "urn:ngsi-v2:AirQualityObserved:RZ:Obsv**1027**.version.1.12.004" 
* **--static-id** \
If set, the id is NOT increased with every message sent, but will be '1' for all messages (or _--first-id_, if set).
* **--num-threads _num_** \
By default, all your messages are sent from within one thread. This is sufficient if you only want to test your system. If you are about to stress-test your server, try to increase the number of threads to be used.
* **--messages _num_** \
The amount of messages sent (per thread).
* **--unlimited** \
Keeps sending messages until you press 'Ctrl-C' or time is up.
* **--limit-time _seconds_** \
When used with _--unlimited_, sets the timeout.
* **--frequency _milliseconds_** \
Limits the sending of messages to the given frequency.

## Define the Payload
We are almost ready to send our first message....but what's the use of empty messages without any content? They will probably get tagged "Return to Sender".  
After a short discussion on how to set up your payload, we will send our first message - I promise!
* **--type _name_** \
[NGSI-V2 and NGSI-LD only] Type will be stored within the payload and (if set) is the unique identifier (together with the id) of an entity within Orion Context Broker. That means: You can have the same _id_ with different _types_:  
  ```json
  {
    "id":"1",
    "type":"WeatherObserved",
    "temperature": {
      "type": "Number",
      "value": -2.3
    },
    "..."
  }  
  ```
  ...and...
  ```json
  {
    "id":"1",
    "type":"Open311ServiceType",
    "..."
  }  
  ```
  ...can exist at the same time.  
  Be aware that with the above data-basis any attempt to send a message to id "1" w/o _--type_ will fail with an "ambiguity error".
* **--attribute-number _name,type,number[,max-number]_** \
Define a numeric (either integer or floating-point) attribute. With _max-number_ set, the resulting value (at runtime) will be a random number in the range [number - max-number] (each including).  
As with all other attributes: The _name_ of the attribute is stored within the payload for Orion Context Broker while it is used to refer to a _Datastream_ in FROST.
* **--attribute-string _name value_** \
Simple enough...a string-literal will be stored.
* **--attribute-date _name_** \
[NGSI-V2 only] Same here: The current Date-Time (local time of the machine, oscsim is executed on in 'ISO 8601'-format) will be stored.
* **--attribute-location _name,lat,long[,max-lat,max-long]_** \
[NGSI-V2 only] Stores a location (in 'geo:json'-format). Like with number, setting max-lat and max-long will result in a random location within the given range.
* **--attribute-boolean _name value_** \
[NGSI-V2 only] Nothing interesting here.

## Useful
* **--dry-run** \
When oscsim starts, it will give a short overview of what will happen ("Will send 1000 messages in 10 threads...(and I might create 1000 new entities!)").  
With _--dry-run_ set, the script will stop right before the messages will be sent. This gives you the chance to determine, if the shown action is what you really want!  
Besides that, the payload is printed out giving you an overview of the data-model that will be created.  
* **--attribute-indent _indent_** \
A print-out of the payload is nice but somewhat hard to read if the json is printed in a single line. Defining indention makes your payload more readable but increases the payload slightly. Don't forget to remove indention when you are sure about your payload and ready to run.
* **--verbose** \
In verbose-mode, not only a single line with the current progress is displayed, but EVERY response is printed out with the id used, the return code (hopefully some 2xx), the response-time in milliseconds and the first 120 characters of the responses body - mostly interesting in case of an error.

## If You Want to Rollback Your Data...
* **--delete _from to_** \
If you keep track of the data, you created during the execution of the script, it will be an easy task to delete this data.  
So, if you run the script with `...-n 1 -m 1000 -f 1000` on an empty database, you will create entities from "1000" to "1999".  
To delete exactly those entities, simply use `...-d 1000 1999`. If you used pre- or postfixes for creation [-e, -o] use the same, when deleting data. Easy. 

## What About More Realistic Data?
With `... --type WeatherObserved --attribute-number temperature,f,21.5 --unlimited --frequency 60000` you can define, that every minute a message is sent with a temperature of 21.5 °C.  
While the time-span is realistic enough, having the same temperature all the time is boring and watching the historical data in some time-series-database even more. Changing to `... --attribute-number temperature,f,20.0,35.0` will give a nicer picture, but having the temperature jumping between 20.0 and 35.0 °C in a minute is funny, but not realistic.  
The missing logic can easily be build up with some bash- or cmd-scripting. The following examples should be self-explaining:  

Linux:
```shell
#!/bin/bash

limit=10
temperature=20
i=1; while [ $i -le $limit ]; do
  echo "The current temperature is "$temperature
  oscsim -s server.com -y WeatherObserved -ad dateObserved -an temperature,f,$temperature
  temperature=$((temperature+1))
i=$((i+1))
sleep 60;
done
```
Windows:
```commandline
@echo off
SET /A "i = 1"
SET /A "limit = 10"
SET /A "temperature = 20"
:while
if %i% leq %limit% (
   echo The current temperature is %temperature%
   oscsim -s server.com -y WeatherObserved -ad dateObserved -an temperature,f,%temperature%
   SET /A "temperature = temperature + 1"
   SET /A "i = i + 1"
   timeout /T 60 /nobreak > nul
   goto :while
)
```
It's up to your fantasy to create a script that increases the temperature slightly over the day and cools down by night or even have higher air polution from Monday to Friday and a clean weekend.

In the HowTos-folder you'll find some interesting use cases on:
* [Using min.io-server to store images and send the URI.](./HowTos/Use%20min.io-Server.md)
* [Parsing a gpx-file and send the positions in a timed manner.](./HowTos/Send%20Route%20(gpx).md)
