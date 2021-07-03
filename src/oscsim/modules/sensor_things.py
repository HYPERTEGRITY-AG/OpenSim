#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import socket
import sys
from time import sleep

import paho.mqtt.client as mqtt  # type: ignore
import requests

from . import helper

# some "const" values
INVALID_ID: int = -1
ERROR: int = -2


def get_sensor_things_relevant_attribute_count(args):
    num_attributes = 0

    if args.numbers is not None:
        num_attributes += len(args.numbers)
    if args.strings is not None:
        num_attributes += len(args.strings)

    return num_attributes


def init_mqtt(host):
    mqtt_client = mqtt.Client()

    try:
        mqtt_client.connect(host.split("/")[2].split(":")[0], 1883, 60)
        print("Waiting for MQTT-Broker to be connected...", end="", flush=True)
        mqtt_client.loop_start()

        while not mqtt_client.is_connected():
            print(".", end="", flush=True)
            sleep(0.1)

        print("OK", flush=True)
    except (socket.gaierror, Exception):
        print("\nError connecting to MQTT-Broker at '%s'!\nExiting..." % host)
        sys.exit(0)

    return mqtt_client


def delete_thing(session, host, thing_id, args):
    url = "%s/v1.1/Things(%i)" % (host, thing_id)

    headers = {helper.CONTENT_TYPE: helper.APPLICATION_JSON}

    if args.headers is not None:
        headers.update(args.headers)

    return session.delete(url, headers=headers)


def create_thing(session, host, thing_name, args):
    try:
        url = "%s/v1.1/Things" % host

        headers = {helper.CONTENT_TYPE: helper.APPLICATION_JSON}

        if args.headers is not None:
            headers.update(args.headers)

        payload = helper.create_thing_payload(thing_name, args.indent)

        resp = session.post(url, data=payload, headers=headers)

        if resp.status_code == 201:
            thing_id, ms2 = get_thing_id(session, host, thing_name, args)

            return thing_id, resp

    except (requests.exceptions.RequestException, Exception):
        return INVALID_ID, None

    return INVALID_ID, resp


def create_data_stream(session, host, thing_id, data_stream_name, args):
    try:
        url = "%s/v1.1/Things(%i)/Datastreams" % (host, thing_id)

        headers = {helper.CONTENT_TYPE: helper.APPLICATION_JSON}

        if args.headers is not None:
            headers.update(args.headers)

        payload = helper.create_data_stream_payload(data_stream_name, args.indent)

        resp = session.post(url, data=payload, headers=headers)
        ms = int(resp.elapsed.total_seconds() * 1000)

        if resp.status_code == 201:
            thing_id, ms2 = get_data_stream_id(
                session, host, thing_id, data_stream_name, args
            )

            ms = int((ms + ms2) / 2)
            return thing_id, ms

    except (requests.exceptions.RequestException, Exception):
        return ERROR, 0

    return INVALID_ID, ms


def create_observation(
    mqtt_client, session, host, use_mqtt, data_stream_id, value, args
):
    payload = helper.create_observation_payload(value, args.indent)

    if use_mqtt:
        topic = "v1.1/Datastreams(%i)/Observations" % data_stream_id
        mqtt_client.publish(topic, payload)
        # simulate http response
        resp = requests.Response()
        resp.status_code = 201
        return resp
    else:
        try:
            url = "%s/v1.1/Datastreams(%i)/Observations" % (host, data_stream_id)

            headers = {helper.CONTENT_TYPE: helper.APPLICATION_JSON}

            if args.headers is not None:
                headers.update(args.headers)

            return session.post(url, data=payload, headers=headers)

        except (requests.exceptions.RequestException, Exception):
            return None


def get_thing_id(session, host, thing_name, args):
    try:
        url = "%s/v1.1/Things?$select=name,id&$filter=name eq '%s'" % (host, thing_name)

        headers = {}

        if args.headers is not None:
            headers.update(args.headers)

        resp = session.get(url, headers=headers)

        if resp.status_code == 200:
            obj = json.loads(resp.text)
            value = obj["value"]

            if len(value) > 0:
                return value[0]["@iot.id"], resp
            else:
                # not found
                resp.status_code = 404
        else:
            return ERROR, resp
    except (requests.exceptions.RequestException, Exception):
        return ERROR, None

    return INVALID_ID, resp


def get_data_stream_id(session, host, thing_id, data_stream_name, args):
    try:
        url = "%s/v1.1/Things(%i)/Datastreams?$select=name,id&$filter=name eq '%s'" % (
            host,
            thing_id,
            data_stream_name,
        )

        headers = {}

        if args.headers is not None:
            headers.update(args.headers)

        resp = session.get(url, headers=headers)

        if resp.status_code == 200:
            obj = json.loads(resp.text)
            value = obj["value"]

            if len(value) > 0:
                return value[0]["@iot.id"], int(resp.elapsed.total_seconds() * 1000)
    except (requests.exceptions.RequestException, Exception):
        return ERROR, 0

    return INVALID_ID, 0
