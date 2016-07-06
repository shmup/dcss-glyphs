# 1!/usr/bin/env python3
#http://crawl.neocities.org/glyphs.html
#usage: ./dcss-glyphs > out.html

import urllib.request
from string import Template
import random
import re
import pprint

monster_data = 'https://raw.githubusercontent.com/crawl/crawl/master/crawl-ref/source/mon-data.h'
raw_monster_data = urllib.request.urlopen(monster_data)

t = Template('<span $colors class="fg$color" title="$title">$glyph</span>\r\n')

h = """<!-- http://ix.io/10LD/python -->
<!doctype html>
<html>
<meta charset="UTF-8">
<title>DCSS glyphs</title>
<script src="https://code.jquery.com/jquery-3.0.0.min.js"></script>
<style>
::-moz-selection { color: black; background: lime; }
::selection { color: black; background: lime; }
html, body { width: 100%; height: 100%; margin: 0, padding: 0; }
body {
    font-family: monospace;
    font-size: 24pt;
    font-weight: bold;
    background: black;
    cursor: pointer;
}
.fg0 { color: #000000; } /* black */
.fg1 { color: #204a87; } /* blue */
.fg2 { color: #4e9a06; } /* green */
.fg3 { color: #06989a; } /* cyan */
.fg4 { color: #a40000; } /* red */
.fg5 { color: #5c3566; } /* magenta */
.fg6 { color: #8f5902; } /* brown */
.fg7 { color: #babdb6; } /* lightgray */
.fg8 { color: #555753; } /* darkgray */
.fg9 { color: #729fcf; } /* lightblue */
.fg10 { color: #8ae234; } /* lightgreen */
.fg11 { color: #34e2e2; } /* lightcyan */
.fg12 { color: #ef2929; } /* lightred */
.fg13 { color: #ad7fa8; } /* lightmagenta */
.fg14 { color: #fce94f; } /* yellow */
.fg15 { color: #eeeeec; } /* white */
</style>
<script>
$(function() {
    $("[data-colors]").each(function() {
     var elem = this;
      $('body').on("mousemove", this, function() {
        var colors = $(elem).data("colors").split(" ");
        var randomColor = colors[Math.floor(Math.random() * colors.length)];
        elem.className = randomColor;
      });
    });
});
</script>
<body>
"""

elemental_colors = {}

def color(c):
    if "etc_" in c:
        return elemental_color(c)

    return {
        "black":        0,
        "blue":         1,
        "green":        2,
        "cyan":         3,
        "red":          4,
        "magenta":      5,
        "brown":        6,
        "lightgrey":    7,
        "darkgrey":     8,
        "darkgray":     8,
        "lightblue":    9,
        "lightgreen":   10,
        "lightcyan":    11,
        "lightred":     12,
        "lightmagenta": 13,
        "yellow":       14,
        "white":        15
    }.get(c, 15)

def elemental_color(c):
    if "random" in c:
        return random.randrange(0, 16)
    return color(random.choice(elemental_colors[c]))

color_data = 'https://raw.githubusercontent.com/crawl/crawl/master/crawl-ref/source/colour.cc'
raw_color_data = urllib.request.urlopen(color_data)

found = False
find_colors = False
current_monster = ''

# Find all the elemental (etc_foo) colors
for line in raw_color_data:
    line = line.decode()
    if re.match('\s+add_element_colour\(_create_random_.*', line):
        found = True
    elif found and re.match('.*ETC_', line):
        current_monster = line.split(',')[0].strip().lower()
        elemental_colors[current_monster] = []
        find_colors = True
    elif find_colors and ";" in line:
        found = False
        find_colors = False
    elif find_colors and re.match('.*\d+.*', line):
        elemental_colors[current_monster].append(line.split(',')[1].strip().lower())

# pprint.pprint(elemental_colors)

# Find all the monsters and get their colors, glyph and name
for line in raw_monster_data:
    line = line.decode()
    if re.match('\s+MONS_.*', line):
        parts = line.strip().split(',')
        c = parts[2].strip().lower()

        foo = ''

        if 'etc_' in c:
            if 'random' not in c:
                foo = "data-colors='" + ' '.join(['fg'+str(color(x)) for x in elemental_colors[c]]) + "'"

        h += str(t.substitute(
            colors=foo,
            color=color(c),
            title=parts[3][2:-1],
            glyph=parts[1][2:-1]
        ))

h += """</body>
</html>"""

print(h)
