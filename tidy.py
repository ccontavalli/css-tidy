#!/usr/bin/python

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

class Stylesheet(object):
  def __init__(self, uri):
    self.uri = uri
    self.blacklist = set()

def main():
  argparser = argparse.ArgumentParser(description="blah")
  argparser.add_argument("--csv-file", dest="csvfile",
                         help="CSS files to parse")
  argparser.add_argument("--keep-comments", dest="comments", action="store_false",
                         default=True, help="Keep comments in generatd output files?")
  #argparser.add_argument("files", metavar="CSS-FILE", nargs="+",
  #                       help="CSS files to parse")
  args = argparser.parse_args()
  style_options = STYLE_OPTIONS
  style_options["keepComments"] = args.comments

  stylesheets = []
  reader = csv.reader(open(args.csvfile))
  for line, columns in enumerate(reader):
    if line == 0:
      for column in columns:
        stylesheets.append(Stylesheet(column))
    if line == 1:
      continue

    for stylen, column in enumerate(columns):
      stylesheets[stylen].blacklist.add(column)

  cssparser = cssutils.CSSParser()
  for stylesheet in stylesheets:
    print "Working on", stylesheet.uri
    css = cssparser.parseUrl(stylesheet.uri, validate=False)
    output = cssutils.css.CSSStyleSheet()
    for key, value in style_options.iteritems():
      output.setSerializerPref(key, value)
    for rule in css:
      if rule.type != rule.STYLE_RULE:
        output.add(rule)
        continue
      selectors = cssutils.css.SelectorList(parentRule=rule.selectorList.parentRule)
      for selector in rule.selectorList:
        if selector.selectorText in stylesheet.blacklist:
          print "BLACKLISTED", selector.selectorText
          continue
        selectors.appendSelector(selector)

      if not selectors.length:
        continue

      newrule = cssutils.css.CSSStyleRule(
          style=rule.style, parentRule=rule.parentRule,
          parentStyleSheet=rule.parentStyleSheet)
      newrule.selectorList = selectors
      output.add(newrule)

    outputfile = os.path.basename(stylesheet.uri)
    print "Saving stripped stylesheet in", outputfile
    open(outputfile, "w").write(output.cssText)

if __name__ == "__main__":
  sys.exit(main())
