#!/usr/bin/env python3

import argparse
from datetime import date

from aoc2022.manager import aoc


def main():
    try:
        from rich.traceback import install as install_rich_traceback
        install_rich_traceback(show_locals=True)
    except ImportError:
        pass

    advent_start = date(aoc.year, 12, 1)
    delta_days = (date.today() - advent_start).days + 1

    if delta_days < 1:
        err_no_day_msg = f"Advent of Code {aoc.year} starts within {-delta_days} days."
        today = None
    elif delta_days > 25:
        err_no_day_msg = f"Advent of Code {aoc.year} ended {delta_days - 25} days ago."
        today = None
    else:
        today = delta_days

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", metavar="DAY", type=int, choices=range(1, 26), default=today,
                        help="day to run (default: today's day)")
    parser.add_argument("-p", metavar="PART", type=int, choices=[1, 2, 3], default=None,
                        help="part to run (3: both if implemented, default: last implemented)")
    input_group = parser.add_mutually_exclusive_group(required=False)
    input_group.add_argument("-i", metavar="INPUT_STRING", type=str, default=None,
                             help="input string")
    input_group.add_argument("-f", metavar="INPUT_FILE", type=argparse.FileType('r'), default=None,
                             help="input filename (default: `input/dayXX.txt`)")

    args = parser.parse_args()

    day = args.d

    if day is None:
        parser.error(err_no_day_msg)

    if day not in aoc.days():
        parser.error(f"day {day} hasn't been implemented yet")

    part = args.p or max(aoc.parts(day))

    if part not in aoc.parts(day):
        parser.error(f"day {day} part {part} hasn't been implemented (yet)")

    if args.i:
        data = args.i
    elif args.f:
        data = args.f.read()
        args.f.close()
    else:
        file = open(f"input/day{day:02d}.txt", 'r')
        data = file.read()
        file.close()

    aoc.solve(day, part, data)


if __name__ == '__main__':
    main()
