#! /usr/bin/env python

#  Copyright 2016 Gary Martin
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import argparse
import logging
from time import sleep

from blinkytape import BlinkyTape, listPorts


logging.basicConfig(level=logging.INFO)
colours = {
    'black': (0.0, 0.0, 0.0),
    'white': (1.0, 1.0, 1.0),
    'red': (1.0, 0.0, 0.0),
    'green': (0.0, 1.0, 0.0),
    'blue': (0.0, 0.0, 1.0),
}


def process_args():
    ports = listPorts()
    default_port = ports[0] if ports else '/dev/ttyACM0'

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument('-p', '--port', default=default_port,
                               help='specify the blinkytape port')
    common_parser.add_argument('--max-light-level', default=200, type=int,
                               help='Maximum brightness in range 0 to 255')

    repeat_parser = argparse.ArgumentParser(add_help=False)
    repeat_parser.add_argument('--repeat', default=False, action='store_true',
                               help='Repeat all phases forever')

    parser = argparse.ArgumentParser(
        description='A wakeup light using BlinkyTape.')

    subparsers = parser.add_subparsers()

    parser_wakeup = subparsers.add_parser(
        'wakeup', parents=[common_parser, repeat_parser],
        description='Wakeup with sunrise and optional sunset.',
        help='Wakeup with sunrise and optional sunset.'
    )
    parser_wakeup.set_defaults(func=wake_up)
    parser_wakeup.add_argument('--sunrise-minutes', default=15, type=float,
                               help='Number of minutes for sunrise phase')
    parser_wakeup.add_argument('--sunset-minutes', default=0, type=float,
                               help='Number of minutes for sunset phase')
    parser_wakeup.add_argument('--daytime-minutes', default=15, type=float,
                               help='Number of minutes to stay at brightest')

    parser_off = subparsers.add_parser(
        'off', parents=[common_parser],
        description="Turn off light.",
        help="Turn off light."
    )
    parser_off.set_defaults(func=light_off)

    return parser.parse_args()


def simple_brighten(blinky, start_colour, end_colour,
                    total_minutes=15, steps=255):
    logging.info("transitioning from {} to {} over {} minutes".format(
        start_colour, end_colour, total_minutes))
    start_r, start_g, start_b = start_colour
    end_red, end_green, end_blue = end_colour

    def c_step(min_c, max_c, steps):
        return 1.0 * (max_c - min_c) / steps

    r_step = c_step(start_r, end_red, steps)
    g_step = c_step(start_g, end_green, steps)
    b_step = c_step(start_b, end_blue, steps)

    total_seconds = total_minutes * 60.0
    sleep_time = total_seconds / steps

    new_red, new_green, new_blue = start_colour
    for step in range(steps):
        new_red += r_step
        new_green += g_step
        new_blue += b_step
        blinky.displayColor(int(new_red), int(new_green), int(new_blue))
        sleep(sleep_time)


def sunrise(blinky, minutes, steps):
    simple_brighten(blinky, colours['black'], colours['red'], minutes / 2.0,
                    steps)
    simple_brighten(blinky, colours['red'], colours['white'], minutes / 2.0,
                    steps)


def sunset(blinky, minutes, steps):
    simple_brighten(blinky, colours['white'], colours['red'], minutes / 2.0,
                    steps)
    simple_brighten(blinky, colours['red'], colours['black'], minutes / 2.0,
                    steps)


def wake_up(blinky, args):
    logging.info("sunrise for {} minutes".format(args.sunrise_minutes))
    sunrise(blinky, args.sunrise_minutes, args.max_light_level)
    logging.info("do nothing for {} minutes".format(args.daytime_minutes))
    sleep(60 * args.daytime_minutes)
    logging.info("start sunset for {} minutes".format(args.sunset_minutes))
    sunset(blinky, args.sunset_minutes, args.max_light_level)


def light_off(blinky, args):
    blinky.displayColor(0, 0, 0)


def set_up_colours(max_value):
    for key, colour in colours.items():
        colours[key] = tuple(int(x * max_value) for x in colour)


def main():
    args = process_args()
    blinky = BlinkyTape(args.port)
    set_up_colours(args.max_light_level)

    repeat = args.repeat if 'repeat' in args else False

    while True:
        args.func(blinky, args)
        if not repeat:
            break


if __name__ == '__main__':
    main()
