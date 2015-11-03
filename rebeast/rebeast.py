#!/usr/bin/env python

# Copyright (C) 2015 Jonathan Chang <jonathan.chang@ucla.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""reBEAST updates the starting parameters in a BEAST 1.x XML file, based on
the averaged parameters from one or more BEAST tracelogs.
"""

from __future__ import division

__version__ = "0.2"

import os.path
import math
import sys
import argparse
import collections
import multiprocessing
import functools
import xml.dom.minidom as minidom

def set_args():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("xml", help="BEAST .xml file")
    parser.add_argument("log", nargs="+", help="BEAST .log file(s)")
    parser.add_argument('-o', '--outfile', help="Output XML file")
    parser.add_argument("--burnin", default=0, type=int, help="Number of states n to discard")
    parser.add_argument("--lastn", type=int, help="Average over the last n recorded states")
    parser.add_argument("--ignore", nargs="+", default=[], help="Ignore these parameters.")
    parser.add_argument("--ignore-tag", nargs="+", default=[], help="Ignore parameters that are nested within these tags in the XML file.")

    return parser.parse_args()


def process_log(file, args):
    """Returns all parameter values from a BEAST tracelog as a dictionary,
    optionally discarding burnin or retrieving only the last N recorded states.
    """

    cols = None
    values = None
    with open(file, "rU") as rfile:
        for line in rfile:
            line = line.strip()

            # Skip comments
            if line.startswith("#"):
                continue

            # Column names not set, so define them now
            if cols is None:
                cols = line.strip().split("\t")[1:] # ignore state column
                values = []
                for col in cols:
                    # use a deque for fast appends
                    values.append(collections.deque(maxlen=args.lastn))
                continue

            nums = line.split("\t")
            if int(nums.pop(0)) < args.burnin:
                continue
            assert len(nums) == len(cols)
            for ii in xrange(len(nums)):
                values[ii].append(float(nums[ii]))
    return dict(zip(cols, values))

def get_col_means(dicts):
    merged = collections.defaultdict(list)
    result = dict()
    if len(dicts) > 1:
        # merge dicts together
        for dic in dicts:
            for key, value in dic.iteritems():
                merged[key].extend(value)
    else:
        # only one dict, so just use that one
        merged = dicts.pop()
    for key, value in merged.iteritems():
        result[key] = sum(value) / len(value)
    return result

def find_parent(element, tags):
    """Searches the parents of `element` searching for a tag name present in `tags`."""
    while True:
        parent = element.parentNode
        if parent is None:
            return None
        if parent.nodeName in tags:
            return parent
        element = parent


def main():
    args = set_args() # global args

    if args.burnin > 0:
        print "Discarding {0} states of burnin...".format(args.burnin)
    if args.lastn is not None:
        print "Only keeping the last {0} recorded states...".format(args.lastn)

    # Async read the tracelogs, then parse the XML file while we're waiting
    pool = multiprocessing.Pool()
    partial_process_log = functools.partial(process_log, args=args)
    promise_log = pool.map_async(partial_process_log, args.log)
    tree = minidom.parse(args.xml)
    vals = get_col_means(promise_log.get())

    ctr = 0
    for param in tree.getElementsByTagName("parameter"):
        pid = param.getAttribute("id")
        value = param.getAttribute("value")
        if pid == "" or value == "" or pid not in vals:
            continue

        if math.isnan(vals[pid]):
            print "[{0}] {1} => skipped due to invalid average".format(pid, value)

        if pid in args.ignore:
            print "[{0}] {1} => in ignore list".format(pid, value)
            continue

        parent = find_parent(param, args.ignore_tag)
        if parent is not None:
            print "[{0}] {1} => child of '{2}'".format(pid, value, parent.nodeName)
            continue

        print "[{0}] {1} => {2}".format(pid, value, vals[pid])
        param.setAttribute("value", str(vals[pid]))
        ctr += 1

    print "{0} starting values updated".format(ctr)

    if args.outfile is None:
        args.outfile = os.path.splitext(args.xml)[0] + ".rebeast.xml"

    with open(args.outfile, "w") as wfile:
        tree.writexml(wfile)
    print "reBEAST output written to " + args.outfile

    return 0

if __name__ == '__main__':
    main()
