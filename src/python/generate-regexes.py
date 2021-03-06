#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""
This script generates regexes for omorfi.
"""


# Author: Omorfi contributors, 2014

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import argparse

from omorfi.formats.ftb3_formatter import Ftb3Formatter
from omorfi.formats.omor_formatter import OmorFormatter
from omorfi.formats.regex_formatter import format_rules_regex


# standard UI stuff


def main():
    """Command-line interface for regex generation in omorfi."""
    # initialise argument parser
    ap = argparse.ArgumentParser(
        description="Generate Xerox twolcs for Finnish")
    ap.add_argument("--quiet", "-q", action="store_false", dest="verbose",
                    default=False,
                    help="do not print output to stdout while processing")
    ap.add_argument("--verbose", "-v", action="store_true", default=False,
                    help="print each step to stdout while processing")
    ap.add_argument("--output", "-o", type=argparse.FileType("w"),
                    required=True, metavar="OFILE",
                    help="write output to OFILE")
    ap.add_argument("--ruleset", "-r", required=True, action="store",
                    metavar="RULES", help="compile RULES ruleset")

    ap.add_argument("--format", "-f", action="store", default="omor",
                    help="use specific output format for twolc data",
                    choices=["omor", "apertium",
                             "giella", "ftb3", "segments", "google"])

    args = ap.parse_args()
    # check args
    formatter = None
    if args.format == "omor":
        formatter = OmorFormatter(args.verbose)
    elif args.format == "ftb3":
        formatter = Ftb3Formatter(args.verbose)
    else:
        print("Not implemented yet format", args.format)
        exit(1)
    # setup files
    if args.verbose:
        print("Writing everything to", args.output.name)
    # print definitions to rootfile
    if args.verbose:
        print("Creating Rules")
    print(format_rules_regex(formatter, args.ruleset), file=args.output)
    exit(0)


if __name__ == "__main__":
    main()
