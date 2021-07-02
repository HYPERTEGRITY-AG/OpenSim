#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from . import helper


def print_version():
    print(
        "Open Smart City-Sim, Copyright (c) 2021 Will Freitag, Version %s"
        % helper.get_version(),
        flush=True,
    )


def print_delimiter():
    print(
        "----------------------------------------------"
        "-------------------------------------------",
        flush=True,
    )


def print_duration(what, start, end):
    print(
        "%s ran from [%s] to [%s]"
        % (
            what,
            start.strftime("%d.%m.%Y - %H:%M:%S"),
            end.strftime("%d.%m.%Y - %H:%M:%S"),
        )
    )


def print_time_spent(ms):
    if ms < 1000:
        print("Time spent: %i ms" % ms, flush=True)
    elif ms < 60000:
        print("Time spent: %i sec" % (ms / 1000), flush=True)
    else:
        minutes = ms / 60000
        ms -= int(minutes) * 60000
        print("Time spent: %i:%02i" % (minutes, ms / 1000), flush=True)


def show_result(delete, start, errors, unique_errors):
    if errors > 0:
        print("\nErrors:", flush=True)
        for key in unique_errors.keys():
            print('%i time(s) "%s"' % (unique_errors[key], key))

    end = datetime.now()
    delta = end - start
    ms = int(delta.total_seconds() * 1000)

    print_delimiter()
    print_time_spent(ms)

    if delete:
        print_duration("Delete", start, end)
    else:
        print_duration("Test", start, end)


def print_server_used(delete, host):
    if delete:
        print("Will delete on %s" % helper.create_host_url(host), flush=True)
    else:
        print("Running load against %s" % helper.create_host_url(host), flush=True)


def print_type_of_server(protocol):
    print("Type of server is: %s" % protocol, flush=True)


def print_schema(args):
    if args.protocol == helper.PROTOCOL_NGSI_V2:
        if args.insert_always:
            print(
                "Note: POST-always schema is used to store contexts. "
                "(Use --help to get more information)",
                flush=True,
            )
        else:
            print(
                "Note: PATCH/POST schema is used to store contexts. "
                "(Use --help to get more information)",
                flush=True,
            )


def print_data_stream_id_used(datastream_id):
    print(
        "The Datastream-Id %i will be used for ALL Observations! "
        "(Use --help to get more information)" % datastream_id,
        flush=True,
    )


def print_id_used(args, msg_num):
    if args.static_id:
        print(
            'ID "%s" will be used for all messages.'
            % helper.create_id(
                args.first_id,
                args.prefix,
                args.postfix,
                0,
                args.protocol == helper.PROTOCOL_NGSI_LD,
            ),
            flush=True,
        )
    else:
        if msg_num == 1:
            print(
                'The used ID will be "%s".'
                % helper.create_id(
                    args.first_id,
                    args.prefix,
                    args.postfix,
                    0,
                    args.protocol == helper.PROTOCOL_NGSI_LD,
                ),
                flush=True,
            )
        elif args.unlimited:
            print(
                'The used ID will be starting at "%s" and increase continuously.'
                % helper.create_id(
                    args.first_id,
                    args.prefix,
                    args.postfix,
                    0,
                    args.protocol == helper.PROTOCOL_NGSI_LD,
                ),
                flush=True,
            )
        else:
            print(
                'The used ID will be from "%s" to "%s".'
                % (
                    helper.create_id(
                        args.first_id,
                        args.prefix,
                        args.postfix,
                        0,
                        args.protocol == helper.PROTOCOL_NGSI_LD,
                    ),
                    helper.create_id(
                        args.first_id + msg_num - 1,
                        args.prefix,
                        args.postfix,
                        0,
                        args.protocol == helper.PROTOCOL_NGSI_LD,
                    ),
                ),
                flush=True,
            )


def print_payload(args):
    if args.protocol == helper.PROTOCOL_NGSI_V2:
        if args.insert_always:
            print(
                "The payload will look like:\n%s"
                % helper.create_payload_ngsi_v2(args.first_id, True, args),
                flush=True,
            )
        else:
            print(
                "The payload will look like:\n%s"
                % helper.create_payload_ngsi_v2(None, False, args),
                flush=True,
            )
    elif args.protocol == helper.PROTOCOL_NGSI_LD:
        print(
            "The payload will look like:\n%s"
            % helper.create_payload_ngsi_ld(args.first_id, args, True),
            flush=True,
        )
    else:
        thing_name = helper.create_id(
            args.first_id,
            args.prefix,
            args.postfix,
            0,
            args.protocol == helper.PROTOCOL_NGSI_LD,
        )

        print(
            "The payload will look like:\nThing:\n%s\n\nDatastream: \n%s\n\nObservation: \n%s"
            % (
                helper.create_thing_payload(thing_name, args.indent),
                helper.create_data_stream_payload("AttributeName", args.indent),
                helper.create_observation_payload(1.5, args.indent),
            ),
            flush=True,
        )


def print_will_delete(args):
    print(
        'Will delete %i contexts from "%s" to "%s".'
        % (
            args.delete[1] - args.delete[0] + 1,
            helper.create_id(
                args.delete[0],
                args.prefix,
                args.postfix,
                0,
                args.protocol == helper.PROTOCOL_NGSI_LD,
            ),
            helper.create_id(
                args.delete[1],
                args.prefix,
                args.postfix,
                0,
                args.protocol == helper.PROTOCOL_NGSI_LD,
            ),
        ),
        flush=True,
    )


def print_will_send_messages(args, msg_num):
    if args.unlimited:
        if args.limit_time is not None:
            print(
                "Will send messages in %i thread(s) for %i seconds."
                % (args.num_threads, args.limit_time),
                flush=True,
            )
        else:
            print(
                "Will send infinite messages in %i thread(s). Hit 'Ctrl-C' to interrupt."
                % args.num_threads,
                flush=True,
            )
    else:
        if msg_num == 1:
            print("Will send one message.", flush=True)
        else:
            print(
                "Will send %i messages in %i thread(s)." % (msg_num, args.num_threads),
                flush=True,
            )


def print_frequency(frequency, more_than_one_thread):
    if more_than_one_thread:
        print(
            "The frequency of messages sent is limited to %i milliseconds (per thread!)."
            % frequency,
            flush=True,
        )
    else:
        print(
            "The frequency of messages sent is limited to %i milliseconds." % frequency,
            flush=True,
        )


def print_messages_send(overall_messages, errors, overall_time, ms, msg_num, unlimited):
    net_messages = overall_messages - errors
    msg_per_second = 0
    response_time = -1

    if net_messages > 0:
        response_time = int(overall_time / net_messages)

    if ms > 0:
        msg_per_second = max(0, int(((overall_messages - errors) * 1000) / ms))

    if unlimited:
        # In this case, there is no percentage
        msg = (
            "\rMessages sent: %i with %i error(s), "
            "avg. response-time: %s ms, load: %i msg/sec      "
            % (
                overall_messages,
                errors,
                str(response_time) if response_time >= 0 else "--",
                msg_per_second,
            )
        )
    else:
        # Here we go with some percentage
        percentage = (overall_messages / msg_num) * 100
        msg = (
            "\rMessages sent: %i (%i%%) with %i error(s), "
            "avg. response-time: %s ms, load: %i msg/sec      "
            % (
                overall_messages,
                percentage,
                errors,
                str(response_time) if response_time >= 0 else "--",
                msg_per_second,
            )
        )

    print(msg, end="", flush=True)
