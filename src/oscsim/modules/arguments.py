#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import shutil
import textwrap as _textwrap

from . import helper


def parse_arguments():
    class MultiLineFormatter(argparse.HelpFormatter):
        def __init__(self, prog, indent_increment=2, max_help_position=24):
            argparse.HelpFormatter.__init__(
                self,
                prog,
                indent_increment,
                max_help_position,
                width=shutil.get_terminal_size().columns,
            )

        def _fill_text(self, text, width, indent):
            paragraphs = text.split("|n")
            multi_line_text = ""
            for paragraph in paragraphs:
                formatted_paragraph = (
                    _textwrap.fill(
                        paragraph,
                        width,
                        initial_indent=indent,
                        subsequent_indent=indent,
                    )
                    + "\n"
                )
                multi_line_text = multi_line_text + formatted_paragraph
            return multi_line_text

    # noinspection PyTypeChecker
    parser = argparse.ArgumentParser(
        description="Tool to create some load on Orion Context Broker/FROST-Server.",
        formatter_class=MultiLineFormatter,
        allow_abbrev=False,
    )

    parser.epilog = (
        "Example #1:|n"
        "oscsim -s my-host.com -H Authorization "
        "'Bearer 039ea6d72a2f32227c2110bd8d78aae33acd6782' "
        "-H Fiware-service curltest|n"
        "One message is sent using id '1'.|n"
        "The tenant 'curltest' will be used "
        "as 'Fiware-service' in the "
        "header of the post.|n"
    )

    parser.epilog += (
        "|n|nExample #2:|n"
        "oscsim -s my-host.com -n 2 -m 50 ...|n"
        "100 messages will be sent (2 threads are sending 50 messages each)."
        "The id will be looped from '1' to '100'.|n"
    )

    parser.epilog += (
        "|n|nExample #3:|n"
        "oscsim -s my-host.com -n 5 -m 100 -f 123 -c ...|n"
        "500 messages will be sent (5 threads are sending 100 messages each)."
        "The id '123' (-f is first id) will be used for all messages (-c is static id).|n"
    )

    parser.epilog += (
        "|n|nExample #4:|n"
        "The payload that will be sent is constructed from the -y and "
        "the -aX parameters. Example:|n"
        "oscsim -y WeatherObserved -an temperature,f,-20,50 "
        "-an precipitation,i,1,20 ...|n"
        "will generate a payload looking like:|n"
        "{|n"
        '  "id":"1",|n'
        '  "type":"WeatherObserved",|n'
        '  "temperature": {|n'
        '    "type": "Number",|n'
        '    "value": -2.3|n'
        "  },|n"
        '  "precipitation": {|n'
        '    "type": "Number",|n'
        '    "value": 13|n'
        "  },|n"
        "}|n"
    )

    parser.epilog += (
        "|n|nExample #5:|n"
        "oscsim -d 100 200 -s my-host.com "
        "-H Authorization 'Bearer 039ea6d72a2f32227c2110bd8d78aae33acd6782'|n"
        "|n"
        "This will delete all IDs starting from 100 to 200 (inclusive)."
    )

    parser.add_argument(
        "-s",
        "--server",
        metavar="[protocol]host-name",
        dest="server",
        help='This host-name will be prepended by "https://", if protocol '
        "is omitted and appended "
        'with "/v2/" (NGSI-V2), "/ngsi-ld/v1" '
        '(NGSI-LD) or "/v1.1/" (SensorThings) resp. '
        "depending on the server-type (see -p/--protocol).",
        required=True,
    )

    parser.add_argument(
        "-p",
        "--protocol",
        choices=[
            helper.PROTOCOL_NGSI_V2,
            helper.PROTOCOL_NGSI_LD,
            helper.PROTOCOL_SENSOR_THINGS_MQTT,
            helper.PROTOCOL_SENSOR_THINGS_HTTP,
        ],
        default=helper.PROTOCOL_NGSI_V2,
        dest="protocol",
        help="Define the type of server. [Default: %s]" % helper.PROTOCOL_NGSI_V2,
    )

    parser.add_argument(
        "-i",
        "--insert-always",
        dest="insert_always",
        action="store_true",
        default=False,
        help="[Only NGSI-V2 and NGSI-LD!] If set, the contexts will always be inserted "
        "(via POST with option 'upsert') instead "
        "of trying to update first (via PATCH) and insert (via POST), if not "
        "existing (i.e. PATCH returns '404 Not Found').",
    )

    parser.add_argument(
        "-a",
        "--datastream-id",
        metavar="id",
        dest="datastream_id",
        help="[Only SensorThings!] If set, this Datastream-Id will be used for ALL "
        "Observations, instead of first searching for the Thing by it's name "
        "and the correct "
        "Datastream-Id afterwards.",
        type=int,
    )

    parser.add_argument(
        "-H",
        "--header",
        metavar=("key", "value"),
        dest="headers",
        action="append",
        nargs=2,
        help="Define a header by key and value.",
    )

    parser.add_argument(
        "-f",
        "--first-id",
        metavar="id",
        dest="first_id",
        help="Define the first id to be used or the one to be used "
        "if '-c/--static-id' is "
        "set. [Default: 1]",
        default=1,
        type=int,
    )

    parser.add_argument(
        "-e",
        "--prefix",
        dest="prefix",
        help="If set, the prefix will be prepended to the generated id.",
    )

    parser.add_argument(
        "-o",
        "--postfix",
        dest="postfix",
        help="If set, the postfix will be appended to the generated id.",
    )

    parser.add_argument(
        "-c",
        "--static-id",
        dest="static_id",
        action="store_true",
        default=False,
        help="If set, the id will not increment (i.e. -n times -m messages will be "
        "sent with the same id ['-f/--first-id' or '1' if omitted]).",
    )

    parser.add_argument(
        "-n",
        "--num-threads",
        metavar="num",
        dest="num_threads",
        help="Define, how many threads shall be used. [Default: 1]",
        default=1,
        type=int,
    )

    parser.add_argument(
        "-m",
        "--messages",
        metavar="num",
        dest="num_messages",
        help="Define, how many messages per thread shall be "
        "sent (ignored, if '-u/--unlimited' "
        "ist set). [Default: 1]",
        default=1,
        type=int,
    )

    parser.add_argument(
        "-u",
        "--unlimited",
        dest="unlimited",
        action="store_true",
        default=False,
        help="If set, '-m/--messages' is ignored and infinite messages "
        "will be send "
        "(in '-n/--num-threads' threads). "
        " Hit 'Ctrl-C' to interrupt or set '-l/--limit-time'.",
    )

    parser.add_argument(
        "-q",
        "--frequency",
        metavar="milliseconds",
        dest="frequency",
        help="If set, limits the frequency of the messages sent to the given "
        "number (per thread!).",
        type=int,
    )

    parser.add_argument(
        "-l",
        "--limit-time",
        metavar="seconds",
        dest="limit_time",
        help="Only in conjunction with '-u/--unlimited': Stops after the given "
        "time in seconds.",
        type=int,
    )

    parser.add_argument(
        "-y",
        "--type",
        metavar="name",
        dest="type",
        help="[Only NGSI-V2 and NGSI-LD!] If set, this type-name will be used in the payload.",
    )

    parser.add_argument(
        "-an",
        "--attribute-number",
        metavar="name,type,number[,max-number]",
        dest="numbers",
        action="append",
        nargs=1,
        help="Define a number attribute used for the payload by 'name' (The name "
        "of the "
        "attribute, e.g.: temperature), 'type' (One of i [integer] or "
        "f [floating point])"
        "and 'number' (The value to be used). If 'max-number' is set, the "
        "number written will be"
        " randomly between 'number' and 'max-number' (each including). "
        "Note: Multiple "
        "number attributes can be defined by repeating -an.",
    )

    parser.add_argument(
        "-as",
        "--attribute-string",
        metavar=("name", "value"),
        dest="strings",
        action="append",
        nargs=2,
        help="Define a string attribute used for the payload by 'name' "
        "(The name of the attribute, e.g.: instruction)"
        " and 'value' (the actual string). Note: Multiple "
        "string attributes can be defined by repeating -as.",
    )

    parser.add_argument(
        "-ad",
        "--attribute-date",
        metavar="name",
        dest="date_times",
        action="append",
        nargs=1,
        help="[Only NGSI-V2!] Define a DateTime attribute used for the payload "
        "by 'name' "
        "(The name of the attribute, "
        "e.g.: dateObserved). Note: The current time is used as value. "
        "Multiple DateTime "
        "attributes can be defined by repeating -ad.",
    )

    parser.add_argument(
        "-al",
        "--attribute-location",
        metavar="name,lat,long[,max-lat,max-long]",
        dest="locations",
        action="append",
        nargs=1,
        help="[Only NGSI-V2!] Define a location attribute used for the payload "
        "by 'name' (The name "
        "of the attribute, e.g.: position), 'lat' (The value for latitude) "
        "and 'long' "
        "(The value for longitude). If 'max-lat' and 'max-long' are set, "
        "the location "
        "written will be randomly between 'lat' and 'max-lat' and 'long' "
        "and 'max-long' "
        "resp. (each including). Note: Multiple location attributes "
        "can be defined by repeating -al.",
    )

    parser.add_argument(
        "-ab",
        "--attribute-boolean",
        metavar=("name", "value"),
        dest="booleans",
        action="append",
        nargs=2,
        help="[Only NGSI-V2!] Define a boolean attribute used for the payload "
        "by 'name' "
        "(The name of the attribute, "
        "e.g.: public) and 'value' (One of 'true', 'false' or 'toggle' "
        "[ie. randomly switch "
        "between true and false]). Note: Multiple boolean attributes can "
        "be defined "
        "by repeating -ab.",
    )

    parser.add_argument(
        "-ai",
        "--attribute-indent",
        metavar="indent",
        dest="indent",
        help="Define the number of characters for indenting the created payload. "
        "[Default: 0]",
        default=0,
        type=int,
    )

    parser.add_argument(
        "-r",
        "--dry-run",
        dest="dry_run",
        action="store_true",
        default=False,
        help="Do a dry run only - giving the chance to review what WOULD be done "
        "incl. seeing what the "
        "payload will look like.",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="Generate verbose output.",
    )

    parser.add_argument(
        "-d",
        "--delete",
        metavar=("from", "to"),
        dest="delete",
        type=int,
        nargs=2,
        help="If set, the entities within the given range "
        '(including "from" and "to") will be deleted.',
    )

    args = parser.parse_args()

    check_arguments(parser, args)

    return args


def check_arguments(parser, args):
    if args.delete is not None:
        if args.delete[0] > args.delete[1]:
            # switch the indexes
            t = args.delete[0]
            args.delete[0] = args.delete[1]
            args.delete[1] = t
        if args.unlimited:
            parser.error(
                "The switch '-u/--unlimited' cannot be used when deleting messages "
                "[-d/--delete]!"
            )
    else:
        if args.datastream_id is not None and args.datastream_id < 0:
            parser.error(
                "Please define a positive number for Datastream-Id [-a/--datastream-id]"
            )

        if args.num_threads == 0:
            parser.error(
                "Without any thread, no messages will be sent at all! "
                "[-n/--num-threads > 0]"
            )

        if args.num_messages <= 0:
            parser.error(
                "Please consider increasing the number of messages! [-m/--messages > 0]"
            )

        if args.limit_time is not None and not args.unlimited:
            parser.error(
                "Limiting the time [-l/--limit-time] is only valid with infinite "
                "run! [-u/--unlimited]"
            )

        if args.limit_time is not None and args.limit_time <= 0:
            parser.error("Please define a positive number for limit [-l/--limit-time]")

        if args.frequency is not None and args.frequency <= 0:
            parser.error(
                "Please define a positive number for frequency [-q/--frequency]"
            )

        if args.numbers is not None:
            for number in args.numbers:
                attribute_args = number[0].split(",")
                if len(attribute_args) < 3 or len(attribute_args) > 4:
                    parser.error(
                        "-an argument ['-an %s'] expects 3 or 4 comma-delimited "
                        "parameters!" % ",".join(attribute_args)
                    )
                if attribute_args[1] == "i":
                    t = 0
                    f = 0
                    try:
                        f = int(attribute_args[2])
                    except ValueError:
                        parser.error(
                            'Please check attribute "%s": "number" must be an '
                            "integer!" % attribute_args[0]
                        )
                    if len(attribute_args) == 4:
                        try:
                            t = int(attribute_args[3])
                        except ValueError:
                            parser.error(
                                'Please check attribute "%s": "max-number" must '
                                "be an integer!" % attribute_args[0]
                            )
                        if t < f:
                            parser.error(
                                'Please check attribute "%s": "max-number" must '
                                "be greater "
                                'than or equal to "number"!' % attribute_args[0]
                            )
                elif attribute_args[1] == "f":
                    t = 0.0
                    f = 0.0
                    try:
                        f = float(attribute_args[2])
                    except ValueError:
                        parser.error(
                            'Please check attribute "%s": "number" must be a '
                            "floating point number!" % attribute_args[0]
                        )
                    if len(attribute_args) == 4:
                        try:
                            t = float(attribute_args[3])
                        except ValueError:
                            parser.error(
                                'Please check attribute "%s": "max-number" must be a '
                                "floating point number!" % attribute_args[0]
                            )
                        if t < f:
                            parser.error(
                                'Please check attribute "%s": "max-number" must be '
                                "greater "
                                'than or equal to "number"!' % attribute_args[0]
                            )
                else:
                    parser.error(
                        'Please check attribute "%s": type must be one of [i | f]!'
                        % attribute_args[0]
                    )

        if args.locations is not None:
            for location in args.locations:
                attribute_args = location[0].split(",")
                if len(attribute_args) != 3 and len(attribute_args) != 5:
                    parser.error(
                        "-al argument ['-al %s'] expects 3 or 5 comma-delimited "
                        "parameters!" % ",".join(attribute_args)
                    )
                lat_from = 0.0
                lat_to = 0.0
                long_from = 0.0
                long_to = 0.0
                try:
                    lat_from = float(attribute_args[1])
                except ValueError:
                    parser.error(
                        'Please check attribute "%s": "lat" must be a floating '
                        "point number!" % attribute_args[0]
                    )
                if lat_from < -90.0 or lat_from > 90.0:
                    parser.error(
                        'Please check attribute "%s": "lat" must be in a range from '
                        "-90.0 to 90.0!" % attribute_args[0]
                    )

                try:
                    long_from = float(attribute_args[2])
                except ValueError:
                    parser.error(
                        'Please check attribute "%s": "long" must be a floating '
                        "point number!" % attribute_args[0]
                    )
                if long_from < -180.0 or long_from > 180.0:
                    parser.error(
                        'Please check attribute "%s": "long" must be in a range from '
                        "-180.0 to 180.0!" % attribute_args[0]
                    )

                if len(attribute_args) == 5:
                    try:
                        lat_to = float(attribute_args[3])
                    except ValueError:
                        parser.error(
                            'Please check attribute "%s": "max-lat" must be a '
                            "floating "
                            "point number!" % attribute_args[0]
                        )

                    if lat_to < -90.0 or lat_to > 90.0:
                        parser.error(
                            'Please check attribute "%s": "max-lat" must be in a '
                            "range "
                            "from -90.0 to 90.0!" % attribute_args[0]
                        )

                    try:
                        long_to = float(attribute_args[4])
                    except ValueError:
                        parser.error(
                            'Please check attribute "%s": "max-long" must be a '
                            "floating point number!" % attribute_args[0]
                        )
                    if long_to < -180.0 or long_to > 180.0:
                        parser.error(
                            'Please check attribute "%s": "max-long" must be in a '
                            "range "
                            "from -180.0 to 180.0!" % attribute_args[0]
                        )

                    if lat_to < lat_from:
                        parser.error(
                            'Please check attribute "%s": "max-lat" must be greater '
                            "than "
                            'or equal to "lat"!' % attribute_args[0]
                        )

                    if long_to < long_from:
                        parser.error(
                            'Please check attribute "%s": "max-long" must be greater '
                            "than "
                            'or equal to "long"!' % attribute_args[0]
                        )

        if args.booleans is not None:
            for boolean in args.booleans:
                if (
                    boolean[1] != "true"
                    and boolean[1] != "false"
                    and boolean[1] != "toggle"
                ):
                    parser.error(
                        'Please check attribute "%s": "value" must be one '
                        'of "true", '
                        '"false" or "toggle"!' % boolean[0]
                    )

        if not args.delete:
            # check scheme?
            if args.insert_always and (
                args.protocol != helper.PROTOCOL_NGSI_V2
                and args.protocol != helper.PROTOCOL_NGSI_LD
            ):
                parser.error(
                    "Insert always scheme [-i/--insert-always] is only valid "
                    "for NGSI-V2 and NGSI-LD!"
                )

            # is there any payload?
            if (
                args.protocol == helper.PROTOCOL_NGSI_V2
                or args.protocol != helper.PROTOCOL_NGSI_LD
            ):
                if (
                    ((args.numbers is None) or (len(args.numbers) == 0))
                    and ((args.booleans is None) or (len(args.booleans) == 0))
                    and ((args.locations is None) or (len(args.locations) == 0))
                    and ((args.strings is None) or (len(args.strings) == 0))
                    and ((args.date_times is None) or (len(args.date_times) == 0))
                ):
                    parser.error("Please define any payload!")
            else:
                if ((args.numbers is None) or (len(args.numbers) == 0)) and (
                    (args.strings is None) or (len(args.strings) == 0)
                ):
                    parser.error("Please define any payload!")

    return True
