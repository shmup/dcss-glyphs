#!/usr/bin/env python3
# http://crawl.neocities.org/glyphs.html
# usage: ./dcss-glyphs > out.html

import urllib.request
from string import Template
import random
import re
import datetime

monster_url = 'https://raw.githubusercontent.com/crawl/crawl/master/crawl-ref/source/mon-data.h'
color_url = 'https://raw.githubusercontent.com/crawl/crawl/master/crawl-ref/source/colour.cc'

monster_data = urllib.request.urlopen(monster_url)
color_data = urllib.request.urlopen(color_url)

template = Template('<span $colors class="fg$color" title="$title">$glyph</span>\r\n')

elemental_colors = {}
found = False
find_colors = False
color_type = ''

# HTML
html = """<!-- https://raw.githubusercontent.com/shmup/dcss-glyphs/master/dcss-glyphs.py -->
<!doctype html>
<html>
<meta charset="UTF-8">
<title>DCSS glyphs</title>
<link rel="image_src" href="cauldron.png" />
<script src="https://code.jquery.com/jquery-3.0.0.min.js"></script>
<link href="https://fonts.googleapis.com/css?family=Ubuntu+Mono" rel="stylesheet">
<style>
::-moz-selection { color: black; background: lime; }
::selection { color: black; background: lime; }
html, body, div#wrapper { width:100%; height:100%; margin:0; }
html, body, div#wrapper { width:100%; height:100%; margin:0; }
body { font-family: 'Ubuntu Mono', monospace; }
a { color: #FF69B4; }
div#info p { padding: 5px; color: white; margin: 0; }
div#glyphs { 
    padding: 5px;
    font-weight: bold;
    cursor: pointer;
    font-size: 2.5vw;
}
.selected { outline: 1px solid yellow; }
@media all and (orientation: portrait) { div#glyphs { font-size: 2.5vh; } }
div#glyphs span:hover { outline: 3px solid #FF69B4; }
body { background: black; }
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
    $("#glyphs span").on("click", function() {
        if (!this.title) return;
        window.open("http://crawl.develz.org/info/index.php?q=" + this.title);
    });

    $("[data-colors]").each(function() {
        var elem = this;
        var paused = null;
        $('body').on("mousemove", this, function(event) {
            if (!paused) {
                paused = setTimeout(function() {
                    paused = null;
                    var colors = $(elem).data("colors").split(" ");
                    var randomColor = colors[Math.floor(Math.random() * colors.length)];
                    elem.className = randomColor;
                }, 300);
            }
      });
    });

    $("input#filter").on("keyup", function(e) {
        var paused = null;
        if (!paused && e.keyCode !== 8 && e.keyCode !== 46) {
            paused = setTimeout(function() {
                paused = null;
                filter(e.target.value);
            }, 200);
        } else {
            filter(e.target.value);
        }
    });
});
function reset() {
    var filterBox = document.getElementById("filter");
    filterBox.value = "";
    filter();
    filterBox.focus();
}
function filter(thing) {
    $(".selected").removeClass("selected");
    if (!thing) return;
    $("span[title*='" + thing + "']").addClass("selected");
}
</script>
<body>
<div id="wrapper">
<div id="info">
<p>DCSS console glyphs last <a href="https://github.com/shmup/dcss-glyphs" target="_blank">generated</a> from <a href="https://raw.githubusercontent.com/crawl/crawl/master/crawl-ref/source/mon-data.h" target="_blank">mon-data.h</a> on """

html += '{:%Y-%m-%d %H:%M:%S}.'.format(datetime.datetime.now())

html += """</p>

<p>
Mouseover a glyph to see its name. Click to see the accompany <a href="http://crawl.develz.org/info/index.php?q=butterfly" target="_blank">LearnDB</a> entry.
</p>
<p><input id="filter" type="text" placeholder="filter" autofocus></input> <button onclick=reset()>reset</button></p>
</div>
<div id="glyphs">"""

def color(c):
    if "etc_" in c:
        return elemental_color(c)

    return {
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

def random_colors():
    nums = [x for x in range(1, 16)]
    nums.remove(8)
    return nums

def random_color():
    return random.choice(random_colors())

def elemental_color(c):
    if "random" in c:
        return random_color()
    return color(random.choice(elemental_colors[c]))

def ugly_thing_colors():
    misc_monster_data = 'https://raw.githubusercontent.com/crawl/crawl/5efadfb8913dc69beeaf7e8adeca6a1c9634ca9f/crawl-ref/source/mon-util.cc'
    misc_monster_data = urllib.request.urlopen(misc_monster_data)
    found = False

    for line in misc_monster_data:
        line = line.decode()
        if re.match('static const colour_t ugly_colour_values', line):
            found = True
        elif found and re.match('(\s+)?[A-Z]+.*', line):
            return [x.strip().lower() for x in line.split(',')]

def monster(data):
    parts = line.strip().split(',')

    return {
            'color': parts[2].strip().lower(),
            'title': parts[3].strip()[1:-1],
            'glyph': parts[1][2:-1]
            }

# Find colors for not fully specified monsters
for line in color_data:
    line = line.decode()
    # We found a monster's color(s)
    if re.match('\s+add_element_colour\(_create_random_.*', line):
        found = True
    # Collect monster information
    elif found and re.match('.*ETC_', line):
        # Get color type
        color_type = line.split(',')[0].strip().lower()
        if "UGLY_THING" in color_type:
            elemental_colors[color_type] = ugly_thing_colors()
            found = False
        else:
            elemental_colors[color_type] = []
            find_colors = True
    # End of monster information
    elif find_colors and ";" in line:
        found = False
        find_colors = False
    # Get color
    elif find_colors and re.match('.*\d+.*', line):
        elemental_colors[color_type].append(line.split(',')[1].strip().lower())

# Find all the monsters and get their colors, glyph and name
for line in monster_data:
    line = line.decode()
    colors = ''
    color_list = ''

    if re.match('\s+MONS_.*', line):
        m = monster(line)

        # etc_things
        if 'etc_' in m['color']:
            if 'random' in m['color']:
                color_list = ' '.join(['fg'+str(x) for x in random_colors()])
            else:
                color_list = ' '.join(['fg'+str(color(x)) for x in elemental_colors[m['color']]])
        # undefined color
        elif 'colour_undef' in m['color']:
            if "ugly thing" in m['title']:
                color_list = ' '.join(['fg'+str(color(x)) for x in ugly_thing_colors()])

        if color_list:
            m['color'] = random.choice(color_list.split(' '))[2:]
            colors = "data-colors='" + color_list + "'"
        else:
            m['color'] = color(m['color'])

        if m['color'] == 'colour_undef':
            m['color'] = random_color()

        # build and add the template
        html += str(template.substitute(
            colors=colors,
            color=m['color'],
            title=m['title'],
            glyph=m['glyph']
        ))

# HTML
html += """</div>
</div>
</body>
</html>"""

print(html)
