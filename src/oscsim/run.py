#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import signal
import sys
from datetime import datetime
from threading import Lock, Thread
from time import sleep
from typing import Dict

import requests

from .modules import arguments, helper, ngsi, output, sensor_things

# some globals
start = datetime.now()
errors = 0
unique_errors = dict()  # type: Dict[str, int]
overall_messages = 0
overall_time = 0
deleted = 0
not_deleted = 0
send_threads = []
delete_thread = Thread()
halt = False


def do_delete(session, lock, args, max_id_length):
    global errors, deleted, not_deleted, overall_messages
    delimiter = ""

    host = helper.create_host_url(args.server)

    headers = {}

    if args.headers is not None:
        headers.update(args.headers)

    for i in range(args.delete[0], args.delete[1] + 1):
        if halt:
            return
        connection_error = False

        if (
            args.protocol == helper.PROTOCOL_NGSI_V2
            or args.protocol == helper.PROTOCOL_NGSI_LD
        ):
            resp = ngsi.do_delete(session, host, i, headers, args)
            if resp is None:
                connection_error = True
            else:
                if resp.status_code == 204:
                    deleted += 1
                elif resp.status_code == 404:
                    not_deleted += 1
                else:
                    errors += 1
        else:
            thing_name = helper.create_id(i, args.prefix, args.postfix, 0, False)
            thing_id, ms = sensor_things.get_thing_id(session, host, thing_name, args)
            if thing_id == sensor_things.INVALID_ID:
                not_deleted += 1
                resp = requests.Response()
                resp.status_code = 404
            else:
                resp = sensor_things.delete_thing(session, host, thing_id, args)
                if resp.status_code == 200:
                    deleted += 1
                else:
                    errors += 1

        with lock:
            if resp is None:
                errors += 1
                error_as_string = "Connection Error"
                if error_as_string in unique_errors.keys():
                    num = unique_errors[error_as_string]
                    unique_errors[error_as_string] = num + 1
                else:
                    unique_errors[error_as_string] = 1
            else:
                error_as_string = (
                    str(resp.status_code) + " " + " ".join(resp.text.split())[0:120]
                )

                if error_as_string in unique_errors.keys():
                    num = unique_errors[error_as_string]
                    unique_errors[error_as_string] = num + 1
                else:
                    unique_errors[error_as_string] = 1

            overall_messages += 1

            if args.verbose:
                if connection_error:
                    print(
                        "%s%s  ??? %s"
                        % (
                            delimiter,
                            helper.create_id(
                                i,
                                args.prefix,
                                args.postfix,
                                max_id_length,
                                args.protocol == helper.PROTOCOL_NGSI_LD,
                            ),
                            error_as_string,
                        ),
                        end="",
                    )
                else:
                    print(
                        "%s%s  %3i %s"
                        % (
                            delimiter,
                            helper.create_id(
                                i,
                                args.prefix,
                                args.postfix,
                                max_id_length,
                                args.protocol == helper.PROTOCOL_NGSI_LD,
                            ),
                            resp.status_code,
                            " ".join(resp.text.split())[0:120],
                        ),
                        end="",
                    )
                delimiter = "\n"


def do_send(mqtt_client, session, lock, args, offset, max_id_length):
    global errors, unique_errors, overall_time, overall_messages

    first_id = args.first_id + offset
    host = helper.create_host_url(args.server)

    # We'll start with unknown Thing/Datastream...let's see, if we can cache them later
    # thing_id will not change if --static-id is set!
    thing_id = sensor_things.INVALID_ID
    # data_stream_id will not change if only ONE attribute is set!
    data_stream_id = sensor_things.INVALID_ID

    if args.unlimited:
        # there is no infinite mode :-) - but don't send more than one billion messages!
        args.num_messages = 1000000000

    # how many attributes (relevant for SensorThings) do we have at all?
    num_attributes = sensor_things.get_sensor_things_relevant_attribute_count(args)

    for i in range(args.num_messages):
        start_time_ms = datetime.now()

        if halt:
            return

        if (
            args.protocol == helper.PROTOCOL_NGSI_V2
            or args.protocol == helper.PROTOCOL_NGSI_LD
        ):
            if args.protocol == helper.PROTOCOL_NGSI_V2:
                headers = {helper.CONTENT_TYPE: helper.APPLICATION_JSON}
            else:
                headers = {helper.CONTENT_TYPE: helper.APPLICATION_JSON_LD}

            if args.headers is not None:
                headers.update(args.headers)

            if args.insert_always:
                resp, payload = ngsi.do_post(
                    session, host, first_id, headers, True, args
                )
                if resp is None:
                    ms = 0
                    okay = False
                else:
                    ms = int(resp.elapsed.total_seconds() * 1000)
                    okay = resp.status_code == 204 or resp.status_code == 201
            else:
                resp, payload = ngsi.do_patch(session, host, first_id, headers, args)
                if resp is None:
                    ms = 0
                    okay = False
                else:
                    ms = int(resp.elapsed.total_seconds() * 1000)
                    if resp.status_code == 404:
                        # It would be very okay not to use "options=upsert" in this POST, but when
                        # running more than one thread, those POSTs will interfere each other!
                        # The 5th parameter is True in order to use "options=upsert"
                        # TODO: Orion-LD (currently) does not support upsert at all! As soon as
                        # this works, set 5th parameter to True again
                        resp, payload = ngsi.do_post(
                            session,
                            host,
                            first_id,
                            headers,
                            args.protocol == helper.PROTOCOL_NGSI_V2,
                            args,
                        )
                        if resp is None:
                            ms = 0
                        else:
                            ms += int(resp.elapsed.total_seconds() * 1000)
                    # At this point, resp.status_code has to be either 204 (after PATCH)
                    # or 201 (after POST) in order to be "okay"
                    if resp.status_code == 204 or resp.status_code == 201:
                        okay = True
                    else:
                        okay = False

            with lock:
                if not okay:
                    errors += 1
                    if resp is None:
                        error_as_string = "Connection Error"
                    else:
                        error_as_string = (
                            str(resp.status_code)
                            + " "
                            + " ".join(resp.text.split())[0:160]
                        )

                    if error_as_string in unique_errors.keys():
                        num = unique_errors[error_as_string]
                        unique_errors[error_as_string] = num + 1
                    else:
                        unique_errors[error_as_string] = 1

                overall_time += ms
                overall_messages += 1

                if args.verbose:
                    if resp is None:
                        print(
                            "%s  ???  ---- Connection Error!"
                            % helper.create_id(
                                first_id,
                                args.prefix,
                                args.postfix,
                                max_id_length,
                                args.protocol == helper.PROTOCOL_NGSI_LD,
                            )
                        )
                    else:
                        message = " ".join(resp.text.split())[0:120]
                        # There is this funny thing that Orion sometimes tells
                        # us about 400 ParseError
                        # see https://github.com/telefonicaid/fiware-orion/issues/3731
                        if resp.status_code == 400:
                            message += "\nPayload was:\n" + payload

                            # try to resend
                            # if insert_always:
                            #     url = host + "/v2/entities/?options=upsert"
                            #
                            #     resp = session.post(url, data=payload, headers=headers)

                            # In 100%, resending exactly the same payload again gives a 201

                        print(
                            "%s  %3i  %4i %s"
                            % (
                                helper.create_id(
                                    first_id,
                                    args.prefix,
                                    args.postfix,
                                    max_id_length,
                                    args.protocol == helper.PROTOCOL_NGSI_LD,
                                ),
                                resp.status_code,
                                ms,
                                message,
                            )
                        )
        else:
            #  Here we go with SensorThings-HTTP/SensorThings-MQTT
            resp = None
            ms = 0

            if args.datastream_id is not None:
                okay = True
                thing_id = 0
                data_stream_id = args.datastream_id
            else:
                if thing_id != sensor_things.INVALID_ID:
                    okay = True
                else:
                    #  1. Get the Thing's id and create if not existing yet
                    with lock:  # since we might be running in more than one thread, use lock!
                        okay = True

                        if thing_id == sensor_things.INVALID_ID:
                            thing_name = helper.create_id(
                                first_id,
                                args.prefix,
                                args.postfix,
                                0,
                                args.protocol == helper.PROTOCOL_NGSI_LD,
                            )

                            #  check, if the thing with the given name (thing_name) already exists:
                            thing_id, resp = sensor_things.get_thing_id(
                                session, host, thing_name, args
                            )
                            if resp is None:
                                okay = False
                            elif resp.status_code == 404:
                                ms = int(resp.elapsed.total_seconds() * 1000)
                                thing_id, resp = sensor_things.create_thing(
                                    session, host, thing_name, args
                                )
                                if resp.status_code != 201:
                                    okay = False
                            elif resp.status_code == 200:
                                # everything is fine
                                okay = True
                            else:
                                # neither 200 nor 404 - error!
                                okay = False

            if (
                okay
                and thing_id != sensor_things.INVALID_ID
                and thing_id != sensor_things.ERROR
            ):
                if args.numbers is not None:
                    for number in args.numbers:
                        attribute_args = number[0].split(",")

                        # shortcut: if at this point data_stream_id != INVALID_ID, then we
                        #           only have ONE attribute at all! So, no need to find out
                        #           data_stream_id...create an Observation immediately instead
                        if (
                            args.datastream_id is None
                            and data_stream_id == sensor_things.INVALID_ID
                        ):
                            with lock:  # since we might be running in more than one thread!
                                data_stream_name = attribute_args[0]
                                data_stream_id, ms2 = sensor_things.get_data_stream_id(
                                    session, host, thing_id, data_stream_name, args
                                )

                                ms = int((ms + ms2) / 2)

                                if data_stream_id == sensor_things.ERROR:
                                    okay = False
                                elif data_stream_id == sensor_things.INVALID_ID:
                                    (
                                        data_stream_id,
                                        ms2,
                                    ) = sensor_things.create_data_stream(
                                        session, host, thing_id, data_stream_name, args
                                    )
                                    ms = int((ms + ms2) / 2)
                                    if data_stream_id == sensor_things.ERROR:
                                        okay = False
                                        data_stream_id = sensor_things.INVALID_ID

                        # Create an observation
                        value = helper.create_value_from_attribute_args(attribute_args)

                        resp = sensor_things.create_observation(
                            mqtt_client,
                            session,
                            host,
                            args.protocol == helper.PROTOCOL_SENSOR_THINGS_MQTT,
                            data_stream_id,
                            value,
                            args,
                        )

                        if resp is not None:
                            ms2 = int(resp.elapsed.total_seconds() * 1000)
                            ms = int((ms + ms2) / 2)

                        if num_attributes > 1:
                            data_stream_id = sensor_things.INVALID_ID

                if args.strings is not None:
                    for string in args.strings:
                        data_stream_name = string[0]
                        with lock:  # since we might be running in more than one thread, use lock!
                            data_stream_id, ms2 = sensor_things.get_data_stream_id(
                                session, host, thing_id, data_stream_name, args
                            )

                            ms = int((ms + ms2) / 2)

                            if data_stream_id == sensor_things.ERROR:
                                okay = False
                            elif data_stream_id == sensor_things.INVALID_ID:
                                data_stream_id, ms2 = sensor_things.create_data_stream(
                                    session, host, thing_id, data_stream_name, args
                                )
                                ms = int((ms + ms2) / 2)
                                if data_stream_id == sensor_things.ERROR:
                                    okay = False
                                    data_stream_id = sensor_things.INVALID_ID

                        # Create an observation
                        resp = sensor_things.create_observation(
                            mqtt_client,
                            session,
                            host,
                            args.protocol == helper.PROTOCOL_SENSOR_THINGS_MQTT,
                            data_stream_id,
                            string[1],
                            args,
                        )

                        if resp is not None:
                            ms2 = int(resp.elapsed.total_seconds() * 1000)
                            ms = int((ms + ms2) / 2)

                        if num_attributes > 1:
                            data_stream_id = sensor_things.INVALID_ID

            with lock:
                overall_messages += 1

                if not okay:
                    errors += 1
                    if resp is None:
                        error_as_string = "Connection Error"
                    else:
                        error_as_string = (
                            str(resp.status_code)
                            + " "
                            + " ".join(resp.text.split())[0:120]
                        )

                    if error_as_string in unique_errors.keys():
                        num = unique_errors[error_as_string]
                        unique_errors[error_as_string] = num + 1
                    else:
                        unique_errors[error_as_string] = 1

                overall_time += ms

                if args.verbose:
                    if resp is None:
                        print(
                            "%s  ???  ---- Connection Error!"
                            % helper.create_id(
                                first_id,
                                args.prefix,
                                args.postfix,
                                max_id_length,
                                args.protocol == helper.PROTOCOL_NGSI_LD,
                            )
                        )
                    else:
                        message = " ".join(resp.text.split())[0:120]
                        print(
                            "%s  %3i  %4i %s"
                            % (
                                helper.create_id(
                                    first_id,
                                    args.prefix,
                                    args.postfix,
                                    max_id_length,
                                    args.protocol == helper.PROTOCOL_NGSI_LD,
                                ),
                                resp.status_code,
                                ms,
                                message,
                            )
                        )

        if not args.static_id:
            thing_id = sensor_things.INVALID_ID
            first_id += 1

        if args.frequency is not None:
            delta = datetime.now() - start_time_ms
            milliseconds = int(delta.total_seconds() * 1000)
            sleep_for_ms = args.frequency - milliseconds
            sleep_for_ms -= 10  # give some extra for the call itself
            if sleep_for_ms > 0:
                sleep(sleep_for_ms / 1000)


def signal_handler(*_):
    stop_send_threads()
    print("\nInterrupted!")
    output.show_result(False, start, errors, unique_errors)
    sys.exit(0)


def signal_handler_delete(*_):
    stop_delete_thread()
    print("\nInterrupted!")
    output.show_result(True, start, errors, unique_errors)
    sys.exit(0)


def wait_for_delete_thread(args):
    ready = False
    while not ready:
        sleep(0.5)
        if overall_messages > 0 and not args.verbose:
            if args.unlimited:
                print(
                    "\rMessages sent: %i with %i not found and %i other error(s)      "
                    % (overall_messages, not_deleted, errors),
                    end="",
                    flush=True,
                )
            else:
                print(
                    "\rMessages sent: %i (%i%%) with %i not found and %i other error(s)      "
                    % (
                        overall_messages,
                        (overall_messages / (args.delete[1] - args.delete[0] + 1))
                        * 100,
                        not_deleted,
                        errors,
                    ),
                    end="",
                    flush=True,
                )

        ready = True
        if delete_thread.is_alive():
            ready = False
            continue


def create_and_start_delete_thread(session, lock, args, max_id_length):
    global delete_thread

    delete_thread = Thread(target=do_delete, args=(session, lock, args, max_id_length))

    delete_thread.daemon = True
    delete_thread.start()


def stop_delete_thread():
    global delete_thread, halt

    halt = True
    while delete_thread.is_alive():
        sleep(0.5)


def handle_delete(args, session, lock, max_id_length):
    global start, delete_thread

    # noinspection PyTypeChecker
    signal.signal(signal.SIGINT, signal_handler_delete)

    # print what will be done...
    output.print_server_used(True, args.server)
    output.print_type_of_server(args.protocol)
    output.print_will_delete(args)

    # dry run only?
    if args.dry_run:
        print("Dry run only. Exiting...", flush=True)
        sys.exit(0)

    start = datetime.now()

    if args.verbose:
        print("ID, Response-Code, Content")

    create_and_start_delete_thread(session, lock, args, max_id_length)

    wait_for_delete_thread(args)

    print("\nReady", flush=True)


def create_send_threads(args, mqtt_client, session, lock, max_id_length):
    print("Starting %i thread(s)" % args.num_threads, end="", flush=True)

    offset = 0

    for i in range(args.num_threads):
        t = Thread(
            target=do_send,
            args=(mqtt_client, session, lock, args, offset, max_id_length),
        )
        send_threads.append(t)
        print(".", end="", flush=True)

        if not args.static_id:
            offset += args.num_messages


def start_send_threads():
    for t in send_threads:
        t.daemon = True
        t.start()


def wait_for_send_threads(limit_time, verbose, msg_num, unlimited):
    ready = False
    temp_ms = 0

    while not ready:
        sleep(0.5)
        temp_end = datetime.now()
        temp_delta = temp_end - start
        temp_s = int(temp_delta.total_seconds())
        temp_ms = int(temp_delta.total_seconds() * 1000)

        if limit_time is not None and temp_s >= limit_time:
            ready = True
            continue

        if not verbose:
            output.print_messages_send(
                overall_messages, errors, overall_time, temp_ms, msg_num, unlimited
            )

        ready = True
        for t in send_threads:
            if t.is_alive():
                ready = False
                continue

    if not verbose:
        output.print_messages_send(
            overall_messages, errors, overall_time, temp_ms, msg_num, unlimited
        )

    if limit_time is not None:
        print("\nTime is up!", flush=True)

    return temp_ms


def stop_send_threads():
    global send_threads, halt

    halt = True

    ready = False
    while not ready:
        ready = True
        for t in send_threads:
            if t.is_alive():
                ready = False
                continue
        sleep(0.5)


def handle_send(args, session, lock, msg_num, max_id_length):
    global start, send_threads

    # noinspection PyTypeChecker
    signal.signal(signal.SIGINT, signal_handler)

    # print what will be done...
    output.print_server_used(False, args.server)
    output.print_type_of_server(args.protocol)
    output.print_schema(args)
    if args.datastream_id is None:
        output.print_id_used(args, msg_num)
    else:
        output.print_data_stream_id_used(args.datastream_id)
    if args.dry_run:
        output.print_payload(args)
    output.print_will_send_messages(args, msg_num)
    if args.frequency is not None:
        output.print_frequency(args.frequency, args.num_threads > 1)

    # dry run only?
    if args.dry_run:
        print("Dry run only. Exiting...", flush=True)
        sys.exit(0)

    mqtt_client = (
        sensor_things.init_mqtt(helper.create_host_url(args.server))
        if args.protocol == helper.PROTOCOL_SENSOR_THINGS_MQTT
        else None
    )

    create_send_threads(args, mqtt_client, session, lock, max_id_length)

    start = datetime.now()
    start_send_threads()

    print("Ready\nRunning...", flush=True)

    if args.verbose:
        print("ID, Response-Code, Response-Time, Content", flush=True)

    # Wait for all threads to finish
    ms = wait_for_send_threads(args.limit_time, args.verbose, msg_num, args.unlimited)

    if not args.verbose:
        print("", flush=True)
    print("Ready", flush=True)

    if mqtt_client is not None:
        mqtt_client.loop_stop()

    if args.verbose:
        output.print_messages_send(
            overall_messages, errors, overall_time, ms, msg_num, args.unlimited
        )
        print("")


def main(args=None):
    output.print_version()
    args = arguments.parse_arguments()
    # if there was any error on the arguments, the function already gave some hint and exited.

    # calculate the overall number of messages to be sent
    msg_num = args.num_threads * args.num_messages

    max_id_length = helper.calculate_max_id_length(args, msg_num)

    if args.delete:
        handle_delete(args, requests.Session(), Lock(), max_id_length)
    else:
        handle_send(args, requests.Session(), Lock(), msg_num, max_id_length)

    output.show_result(args.delete, start, errors, unique_errors)

    sys.exit(0)


if __name__ == "__main__":
    main()
