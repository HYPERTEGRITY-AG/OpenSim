# HowTo: Parse a gpx-File and Store the Locations in Orion Context Broker/FROST-Server

This short "how to" will show how to parse a gpx-file with [xmlstarlet](http://xmlstar.sourceforge.net/doc/UG/xmlstarlet-ug.html) and send the positions timed with opensim.py.

## Prerequisites
* You need a gpx-file with a route.
* xmlstarlet need to be installed.

## Install xmlstarlet 
Find out, how to install xmlstarlet [here](http://xmlstar.sourceforge.net/download.php).  
If you want to dive into this great tool, please refer to its [documentation](http://xmlstar.sourceforge.net/doc/UG/xmlstarlet-ug.html).

## Prepare a Route-File 
There are lots of Tools out there letting you define a route and export it in gpx format.  
As an example, I will show how to achieve this with [GPX Generator](https://www.gpxgenerator.com).
* Open the [website](https://www.gpxgenerator.com).
* Start creating the route by clicking waypoints.  
  Note: The timespan between two waypoints is calculated by the distance and the chosen speed. You can even simulate velocity by increasing the speed from point to point. 
* When ready, export the route in gpx-format into a file (e.g. `sample.gpx`).

The exported file will look like:
```xml
<?xml version="1.0"?>
<gpx version="1.1" creator="gpxgenerator.com">
<wpt lat="51.726578514305174" lon="8.759472002022175">
    <ele>112.62</ele>
    <time>2021-03-30T09:53:58Z</time>
</wpt>
<wpt lat="51.72652534946479" lon="8.759300340645222">
    <ele>112.75</ele>
    <time>2021-03-30T09:53:59Z</time>
</wpt>
<wpt
    ...    
</wpt>
</gpx>
```
Find a short [gpx-file (sample.gpx)](./files/sample.gpx) in the [files-folder](./files) for a first try.

## Prepare the Script 
Take the [script](./files/track.sh) from the [files-folder](./files) and change
* the filename of the gpx-file to your needs (line #4)
* the call to opensim.py to your needs (line #60)

## Run the Script
Let the script run and voilá - we are simulating a bus driving through your city continuously sending its location!

