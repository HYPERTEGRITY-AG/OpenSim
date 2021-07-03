# HowTo: Use min.io-Server for Uploading Blobs and Store the URIs in Orion Context Broker/FROST-Server

This short description will help with _first steps_ with min.io-Server and how to utilize the document-store together with Open Smart City-Sim.

## Prerequisites
* An up and running min.io-Server (e.g. `https://blob.myserver.com` - referred as `HOST` later on)
* Credentials (`ACCESS-KEY`/`SECRET-KEY`) for that server.
* A configured `bucket` on that server where the Blobs can be stored (e.g. `images` referred as `BUCKET` later on)  
  Note: For easy read-access (w/o authentication), this `bucket` can have a policy set to `download`.
* For browsing the blobs (at `HOST`/minio), the Admin-credentials are needed - except for public `buckets` (policy: `download`).

## Prepare min.io-Client
1. Download the min-io-Client-binary:
   * Linux: https://dl.min.io/client/mc/release/linux-amd64/mc
   * Windows: https://dl.min.io/client/mc/release/windows-amd64/mc.exe  
   * macOS (Install via Homebrew): `$ brew install minio/stable/mc`
   
   Note: Consider adding the binary to your PATH-Environment.
2. Configure an `alias` for the min.io-Server  
It's not possible to upload Blobs to the server directly. An `alias` is needed instead.  
   Create an `alias` with the following command:  
   ```commandline
   $ mc alias set ALIAS HOST ACCESS-KEY SECRET-KEY
   ```   
   Note: Subsequent access to the min.io-Server is now done with that `alias` (w/o further authentication).

## Upload a Blob
A Blob is uploaded with the following command:
```commandline
$ mc cp LOCAL_FILE ALIAS/BUCKET
```
The URI of that blob is: `HOST`/`BUCKET`/`LOCAL_FILE` 

Note: Any prepending directory from `LOCAL_FILE` (e.g.: `/subdir/filename`) is cut, so the URI does only contain the `filename`.  
Also note: Repeatedly uploads will overwrite an exiting file. 

## Store the URI in Orion Context Broker/FROST-Server
Afterwards, the URI can be sent to Orion Context Broker/FROST-Server via _oscsim_ using a String-Attribute:  
```commandline
$ oscsim ... --attribute-string "Name of the attribute" "URI"
```
Example:  
```commandline
$ oscsim -s http://myserver.com -p SensorThings-HTTP -as Picture https://blob.myserver.com/images/1.jpg
```

## Do Both, Upload and Store in One Step
Following bash-script lets you do both at once (assuming, the `alias` is already created, and the `bucket` exists):
```shell
#!/bin/bash

# min.io-Server specs
HOST=https://blob.myserver.com
ALIAS=mycloud
BUCKET=images

# The file to upload
LOCAL_FILE="my-images/test1.jpg"

# 1) Upload the file
echo Storing $LOCAL_FILE on $HOST
./mc cp $LOCAL_FILE $ALIAS/$BUCKET

# 2) Create the URI
# 2.1) Extract filename from path
REMOTE_FILE="${LOCAL_FILE##*/}"
# 2.2) Build up URI
URI=$HOST/$BUCKET/$REMOTE_FILE
echo The URI is: $URI

# 3) Store URI
oscsim -s http://myserver.com -p SensorThings-HTTP -as Picture $URI

```
Feel free to enhance this script to make use of parameters (e.g filename to upload/store) or even loop over a directory and store all contained files.

## Further Readings
For a Quickstart on how to use min.io-Client, please refer to https://docs.min.io/docs/minio-client-quickstart-guide.html.