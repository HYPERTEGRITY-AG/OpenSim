#!/bin/bash

# TODO: Change the filename/location to your needs
input_file=sample.gpx

# empty arrays for the values
lat=()
lon=()
timestamp=()

echo "Parsing file $input_file..."

# read latitudes
for l in $(xmlstarlet select -t -v '//wpt/@lat' $input_file)
do
   lat+=("$l")
done

# read longitudes
for l in $(xmlstarlet select -t -v '//wpt/@lon' $input_file)
do
   lon+=("$l")
done

# read timestamps
for t in $(xmlstarlet select -t -v '//wpt/time' $input_file)
do
   timestamp+=("$t")
done

echo "Ready"
echo

# show what we've got
echo "Found ${#lat[@]} latitudes."
echo "Found ${#lon[@]} longitudes."
echo "Found ${#timestamp[@]} timesstamps."
echo

# TODO: Check if the array sizes are identical

# loop though arrays
StartDate=$(date -u -d "${timestamp[0]}" +"%s.%N")

for (( i=0; i<${#lat[@]}; i++ ))
do
  echo "Waypoint #$((i+1)):"

  # calculate sleep
  ThisDate=$(date -u -d "${timestamp[$i]}" +"%s.%N")
  difference=$(awk '{print $1-$2}' <<< "$ThisDate $StartDate")
  echo "Sleeping for $difference second(s)"
  sleep "$difference"

  StartDate=$ThisDate
  echo "Sending with:"
  echo "  lat: ${lat[$i]}"
  echo "  lon: ${lon[$i]}"
  # TODO: Change the call to oscsim to your needs
  oscsim -s myserver.com -y BusTracker -ad dateObserved -al "Current Location",${lat[$i]},${lon[$i]}
  echo
done


