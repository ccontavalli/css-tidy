#!/usr/bin/python

"""
Indents a .css file.
"""

import argparse
import sys
import cssutils
import csv
import os

STYLE_OPTIONS = {
  "indent": "  ",
  "keepAllProperties": False,
  "keepUnknownRules": False,
  "omitLastSemicolon": False,
  "indentClosingBrace": False,
  "keepComments": True,
}

def main():
  argparser = argparse.ArgumentParser(description=__doc__)
  argparser.add_argument("inputfiles", metavar="INPUT-FILE", nargs=1, help="CSS file to parse")
  argparser.add_argument("--ignore-comments", dest="comments", action="store_false",
                         default=True, help="Keep comments in generatd output files?")
  args = argparser.parse_args()
  style_options = STYLE_OPTIONS
  style_options["keepComments"] = args.comments

  cssparser = cssutils.CSSParser()
  for stylesheet in args.inputfiles:
    if "://" in stylesheet:
      css = cssparser.parseUrl(stylesheet, validate=False)
    else:
      css = cssparser.parseFile(stylesheet, validate=False)
    for key, value in style_options.iteritems():
      css.setSerializerPref(key, value)
    print css.cssText

if __name__ == "__main__":
  sys.exit(main())
