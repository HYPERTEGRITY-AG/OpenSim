#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

from modules import helper

# some "consts"
V2_ENTITIES = "/v2/entities/"
OPTIONS_UPSERT = "?options=upsert"
ATTRS = "/attrs/"
TYPE_IS = "?type="


def do_delete(session, host, ngsi_id, headers, args):
    url = host + V2_ENTITIES

    try:
        url_delete = url + helper.create_id(ngsi_id, args.prefix, args.postfix, 0)
        return session.delete(url_delete, headers=headers)
    except (requests.exceptions.RequestException, Exception):
        return None


def do_post(session, host, first_id, headers, upsert, args):
    url = host + V2_ENTITIES
    if upsert:
        url += OPTIONS_UPSERT

    payload = helper.create_payload_ngsi(first_id,
                                         True,
                                         args)
    try:
        resp = session.post(url, data=payload, headers=headers)
    except (requests.exceptions.RequestException, Exception):
        return None, payload

    return resp, payload


def do_patch(session, host, first_id, headers, args):
    url = host + V2_ENTITIES + helper.create_id(first_id, args.prefix, args.postfix, 0) + ATTRS
    if args.type is not None:
        url += TYPE_IS
        url += args.type

    payload = helper.create_payload_ngsi(None,
                                         False,
                                         args)
    try:
        resp = session.patch(url, data=payload, headers=headers)
    except (requests.exceptions.RequestException, Exception):
        return None, payload

    return resp, payload
