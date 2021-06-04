#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

from . import helper

# some "consts"
V2_ENTITIES = "/v2/entities/"
LD_ENTITIES = "/ngsi-ld/v1/entities/"
OPTIONS_UPSERT = "?options=upsert"
ATTRS = "/attrs/"
TYPE_IS = "?type="


def do_delete(session, host, ngsi_id, headers, args):
    if args.protocol == helper.PROTOCOL_NGSI_V2:
        url = host + V2_ENTITIES
    else:
        url = host + LD_ENTITIES

    try:
        url_delete = url + helper.create_id(
            ngsi_id,
            args.prefix,
            args.postfix,
            0,
            args.protocol == helper.PROTOCOL_NGSI_LD,
        )
        return session.delete(url_delete, headers=headers)
    except (requests.exceptions.RequestException, Exception):
        return None


def do_post(session, host, first_id, headers, upsert, args):
    if args.protocol == helper.PROTOCOL_NGSI_V2:
        url = host + V2_ENTITIES
        if upsert:
            url += OPTIONS_UPSERT
        payload = helper.create_payload_ngsi_v2(first_id, True, args)
    else:
        url = host + LD_ENTITIES
        if upsert:
            url += OPTIONS_UPSERT
        payload = helper.create_payload_ngsi_ld(first_id, args, True)

    try:
        resp = session.post(url, data=payload, headers=headers)
    except (requests.exceptions.RequestException, Exception):
        return None, payload

    return resp, payload


def do_patch(session, host, first_id, headers, args):
    if args.protocol == helper.PROTOCOL_NGSI_V2:
        url = (
            host
            + V2_ENTITIES
            + helper.create_id(first_id, args.prefix, args.postfix, 0, False)
            + ATTRS
        )
        if args.type is not None:
            url += TYPE_IS
            url += args.type

        payload = helper.create_payload_ngsi_v2(None, False, args)
    else:
        url = (
            host
            + LD_ENTITIES
            + helper.create_id(first_id, args.prefix, args.postfix, 0, True)
            + ATTRS
        )
        payload = helper.create_payload_ngsi_ld(None, args, False)

    try:
        resp = session.patch(url, data=payload, headers=headers)
    except (requests.exceptions.RequestException, Exception):
        return None, payload

    return resp, payload
