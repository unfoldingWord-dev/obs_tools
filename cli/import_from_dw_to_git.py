#!/usr/bin/env python2
# -*- coding: utf8 -*-
#
#  Copyright (c) 2016 unfoldingWord
#  http://creativecommons.org/licenses/MIT/
#  See LICENSE file for details.
#
#  Contributors:
#  Phil Hopper <phillip_hopper@wycliffeassociates.org>
#

from __future__ import print_function, unicode_literals
import argparse
import sys
from general_tools.print_utils import print_ok
from obs.importer.from_dokuwiki import OBSDokuwikiImporter


if __name__ == '__main__':
    print()
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-l', '--lang', dest='lang', default=False,
                        required=True, help='Language code of resource.')
    parser.add_argument('-r', '--gitrepo', dest='gitrepo', default=False,
                        required=True, help='Git repository where the source can be found.')
    parser.add_argument('-o', '--outdir', dest='outdir', default=False,
                        required=True, help='The output directory for markdown files.')

    args = parser.parse_args(sys.argv[1:])

    # do the import
    with OBSDokuwikiImporter(args.lang, args.gitrepo, args.outdir, False) as importer:
        importer.run()

    print_ok('ALL FINISHED: ', 'Please check the output directory.')
