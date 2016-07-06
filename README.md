I wanted to generate all of the various monster glyphs and their appropriate colors. It simply looks through two crawl files:

 1. Monster data first: https://raw.githubusercontent.com/crawl/crawl/master/crawl-ref/source/mon-data.h
 2. Grab some color information: https://raw.githubusercontent.com/crawl/crawl/master/crawl-ref/source/colour.cc
 3. Spit out some HTML

You can check out an example here: http://crawl.neocities.org/glyphs.html

It turns out [Neil](http://s-z.org/neil/) did a similar thing with perl, and the information is tabular and a lot more useful. Right now I just have the goal of being accurate and asthetically pleasing.

 * http://s-z.org/neil/tmp/crawl-glyphs-narrow.html
 * http://s-z.org/neil/tmp/crawl-glyphs (script)

