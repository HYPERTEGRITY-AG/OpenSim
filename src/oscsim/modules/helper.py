#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import random
from datetime import datetime

# some "consts"
VERSION = "1.1.1"
CONTENT_TYPE = "Content-Type"
APPLICATION_JSON = "application/json"
# TODO: swagger says, content-type is "application/json;application/ld+json"!
APPLICATION_JSON_LD = "application/ld+json"
LD_PREFIX = "urn:"
PROTOCOL_NGSI_V2 = "NGSI-V2"
PROTOCOL_NGSI_LD = "NGSI-LD"
PROTOCOL_SENSOR_THINGS_HTTP = "SensorThings-HTTP"
PROTOCOL_SENSOR_THINGS_MQTT = "SensorThings-MQTT"


def get_version():
    return VERSION


def create_id(first_id, prefix, postfix, align, is_ngsi_ld):
    ret = str(first_id)

    if prefix is not None:
        ret = prefix + ret

    if postfix is not None:
        ret += postfix

    if is_ngsi_ld:
        ret = LD_PREFIX + ret

    if align == 0:
        return ret

    return ret.rjust(align, " ")


def create_host_url(host):
    if host.startswith("http://") or host.startswith("https://"):
        return host

    return "https://" + host


def create_value_from_attribute_args(attribute_args):
    value = None
    if attribute_args[1] == "i":
        f = int(attribute_args[2])
        value = f
        if len(attribute_args) > 3:
            t = int(attribute_args[3])
            value = random.randint(f, t)
    elif attribute_args[1] == "f":
        f = float(attribute_args[2])
        value = f
        if len(attribute_args) > 3:
            t = float(attribute_args[3])
            value = round(random.uniform(f, t), 1)

    return value


def create_thing_payload(thing_name, indent):
    payload = dict()

    payload["name"] = thing_name
    payload["description"] = "This Thing was created by oscsim"

    location = dict()
    location["name"] = thing_name
    location["description"] = "This Location was created by oscsim"
    location["encodingType"] = "application/vnd.geo+json"
    loc = dict()
    loc["type"] = "Point"
    coordinates = list()
    coordinates.append(8.759449427022547)
    coordinates.append(51.72663719884235)
    loc["coordinates"] = coordinates
    location["location"] = loc
    locations = list()
    locations.append(location)
    payload["Locations"] = locations

    if indent > 0:
        return json.dumps(payload, indent=indent)
    else:
        return json.dumps(payload)


def create_data_stream_payload(data_stream_name, indent):
    payload = dict()

    payload["name"] = data_stream_name
    payload["description"] = "This Datastream was created by oscsim"
    payload[
        "observationType"
    ] = "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement"

    unit_of_measurement = dict()
    unit_of_measurement["name"] = "number"
    unit_of_measurement["symbol"] = "#"
    unit_of_measurement["definition"] = "unknown"

    payload["unitOfMeasurement"] = unit_of_measurement

    observed_property = dict()
    observed_property["name"] = data_stream_name
    observed_property["description"] = "This ObservedProperty was created by oscsim"
    observed_property["definition"] = "unknown"

    payload["ObservedProperty"] = observed_property

    sensor = dict()
    sensor["name"] = "Pseudo Sensor created by oscsim"
    sensor["description"] = "I'm not real!"
    sensor["encodingType"] = "application/pdf"
    sensor["metadata"] = "https://i-dont-have.any/data-sheet.pdf"

    payload["Sensor"] = sensor

    if indent > 0:
        return json.dumps(payload, indent=indent)
    else:
        return json.dumps(payload)


def create_observation_payload(value, indent):
    payload = dict()

    time_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.00Z")

    payload["result"] = value
    payload["phenomenonTime"] = time_string
    payload["resultTime"] = time_string

    if indent > 0:
        return json.dumps(payload, indent=indent)
    else:
        return json.dumps(payload)


def create_payload_ngsi_v2(first_id, meta_data, args):
    payload = dict()
    if meta_data:
        if first_id is not None:
            payload["id"] = create_id(
                first_id,
                args.prefix,
                args.postfix,
                0,
                args.protocol == PROTOCOL_NGSI_LD,
            )
        if args.type is not None:
            payload["type"] = args.type

    if args.date_times is not None:
        for date_time in args.date_times:
            attr = {
                "type": "DateTime",
                "value": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.00Z"),
            }
            payload[date_time[0]] = attr

    if args.numbers is not None:
        for number in args.numbers:
            attribute_args = number[0].split(",")

            attr = {}

            # type
            if attribute_args[1] == "i" or attribute_args[1] == "f":
                attr["type"] = "Number"

            # value
            value = create_value_from_attribute_args(attribute_args)
            attr["value"] = value
            payload[attribute_args[0]] = attr

    if args.strings is not None:
        for string in args.strings:
            attr = {"type": "Text", "value": string[1]}
            payload[string[0]] = attr

    if args.booleans is not None:
        for boolean in args.booleans:
            attr = {"type": "Boolean"}

            # value
            if boolean[1] == "false":
                attr["value"] = False
            elif boolean[1] == "true":
                attr["value"] = True
            else:
                attr["value"] = bool(random.getrandbits(1))
            payload[boolean[0]] = attr

    if args.locations is not None:
        for location in args.locations:
            attribute_args = location[0].split(",")

            attr = {"type": "geo:json"}

            # value
            coord = {"type": "Point"}
            lat_from = float(attribute_args[1])
            long_from = float(attribute_args[2])
            coord["coordinates"] = [lat_from, long_from]

            if len(attribute_args) > 3:
                lat_to = float(attribute_args[3])
                long_to = float(attribute_args[4])
                coord["coordinates"] = [
                    random.uniform(lat_from, lat_to),
                    random.uniform(long_from, long_to),
                ]

            attr["value"] = coord
            payload[attribute_args[0]] = attr

    if args.indent > 0:
        return json.dumps(payload, indent=args.indent)
    else:
        return json.dumps(payload)


def create_payload_ngsi_ld(first_id, args, is_post):
    payload = dict()

    if first_id is not None:
        context = {
            "id": create_id(
                first_id,
                args.prefix,
                args.postfix,
                0,
                args.protocol == PROTOCOL_NGSI_LD,
            ),
            "type": args.type,
        }
    else:
        context = {"type": args.type}
    payload["@context"] = context

    if is_post:
        if first_id is not None:
            payload["id"] = create_id(
                first_id,
                args.prefix,
                args.postfix,
                0,
                args.protocol == PROTOCOL_NGSI_LD,
            )
        payload["type"] = args.type

    if args.date_times is not None:
        for date_time in args.date_times:
            attr = {
                "type": "DateTime",
                "value": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.00Z"),
            }
            payload[date_time[0]] = attr

    if args.numbers is not None:
        for number in args.numbers:
            attribute_args = number[0].split(",")

            attr = {}

            # type
            if attribute_args[1] == "i" or attribute_args[1] == "f":
                attr["type"] = "Property"  # TODO: "Number" must be accepted!

            # value
            value = create_value_from_attribute_args(attribute_args)
            attr["value"] = value
            payload[attribute_args[0]] = attr

    if args.strings is not None:
        for string in args.strings:
            attr = {"type": "Text", "value": string[1]}
            payload[string[0]] = attr

    if args.booleans is not None:
        for boolean in args.booleans:
            attr = {"type": "Boolean"}

            # value
            if boolean[1] == "false":
                attr["value"] = False
            elif boolean[1] == "true":
                attr["value"] = True
            else:
                attr["value"] = bool(random.getrandbits(1))
            payload[boolean[0]] = attr

    if args.locations is not None:
        for location in args.locations:
            attribute_args = location[0].split(",")

            attr = {"type": "geo:json"}

            # value
            coord = {"type": "Point"}
            lat_from = float(attribute_args[1])
            long_from = float(attribute_args[2])
            coord["coordinates"] = [lat_from, long_from]

            if len(attribute_args) > 3:
                lat_to = float(attribute_args[3])
                long_to = float(attribute_args[4])
                coord["coordinates"] = [
                    random.uniform(lat_from, lat_to),
                    random.uniform(long_from, long_to),
                ]

            attr["value"] = coord
            payload[attribute_args[0]] = attr

    if args.indent > 0:
        return json.dumps(payload, indent=args.indent)
    else:
        return json.dumps(payload)


def calculate_max_id_length(args, msg_num):
    if args.delete:
        max_id_length = len(str(args.delete[1]))
        if args.prefix is not None:
            max_id_length += len(args.prefix)
        if args.postfix is not None:
            max_id_length += len(args.postfix)
    else:
        if args.static_id:
            max_id_length = len(str(args.first_id))
        else:
            max_id_length = len(str(args.first_id + msg_num - 1))

        if args.prefix is not None:
            max_id_length += len(args.prefix)
        if args.postfix is not None:
            max_id_length += len(args.postfix)

    return max_id_length
