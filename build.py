# build.py: generate the HTML files from text files

import sys
import glob
import urllib.request
from time import gmtime, strftime
import os

if len(sys.argv) != 2:
	print("Usage:  python3 build.py ARG\n"
	      "\n"
	      "For documentation on ARG, see README.md.")
	exit(1)

PAGE_TOP = r"""
<!DOCTYPE html>
<html>
<head>
<title>FLINT: Fast Library for Number TheoryTITLE</title>

<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Code+Pro:wght@500&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Nunito&display=swap" rel="stylesheet">

<style type="text/css" media="screen">
body { font-family: 'nunito', arial, sans-serif; font-size: 16px; line-height: 1.5em; margin: 2em; background-color:#fcfcfc; color: #111; }

h1, h2, h3 { line-height: 1.5em; }
h1 { font-weight: bold; font-size:36px; margin-bottom: 0.5em; text-align:center; }
h2 { background-color: #f6f6f6; padding: 0.3em; border: 1px solid #fafafa; }

h3 { border-bottom: 1px solid #888; }
h4 { background-color: #f8f8f8; }

table { border-collapse:collapse; }
table, th, td { border: 1px solid #aaa; }
th, td { padding:0.3em; }
tt { font-family: 'source code pro', monospace; font-size:0.8em;
 background-color: #f8f8f8;
 padding: 0.2em;
 border: 1px solid #f0f0f0;
}
a { color: #004fa0; font-weight: bold; text-decoration: none; }
a:hover { color: #206fc0; text-decoration: none; background-color: #fafafa; }

#content { margin-left: auto; margin-right: auto; margin-top: 1em; max-width: 1000px; background-color:#fff; padding-left: 2em; padding-right: 1em; border:1px solid #f0f0f0; border-radius:4px; box-shadow: 4px 4px #ddd; padding-bottom: 2em; }
#postmain { margin-left: auto; margin-right: auto; margin-top: 1em; max-width: 1000px; padding-left: 2em; padding-right: 1em; padding-bottom: 2em; }

.benchmark { border-collapse:collapse; }
.benchmark td, .benchmark th { border:1px solid #ccc; padding:3px 7px 2px 7px; }
.benchmark th { text-align:left; padding-top:5px; padding-bottom:4px; background-color:#eee; color:#000; }
.benchmark tr.alt td { color:#000; background-color:#f8f8f8; }

blockquote { font-style: italic; }

</style>

%KATEX%

</head>

<body>

<h1>FLINT : <span style="color:#cc3333">Fast Library for Number Theory</span></h1>

<!-- <div style="text-align:center; margin-bottom:1.5em"><img style="scale:90%" src="img/factor200.svg"></div> -->
<!-- <div style="text-align:center; margin-bottom:1.5em"><img style="scale:90%" src="img/factor.svg"></div> -->


<div style="text-align:center; margin-bottom:1.5em; overflow:scroll">

<script>
var formulas = [
  "img/delta.svg",
  "img/factor.svg",
  "img/factorpoly.svg",
  "img/bernoulli.svg",
  "img/zeta.svg",
];

var size = formulas.length;
var x = Math.floor(size*Math.random());
var imgStr = '<img src="' + formulas[x] + '" style="scale:90%" />';
document.write(imgStr); document.close();
</script>
</div>

MENU

<div id="content">
"""

PAGE_BOTTOM = r"""

</div>

<div id="postmain">
<hr style="border:0; height:1px; color:#ccc; background-color:#ccc; margin-top:2em;" />

<div style="line-height:1em">
<p><i>TIMESTAMP</i></p>
<p><i>Contact: <a href="mailto:fredrik.johansson@gmail.com">Fredrik Johansson</a>, <a href="https://groups.google.com/g/flint-devel">flint-devel mailing list</a></i></p>
</div>

</div>

</body>
</html>
"""

PAGE_KATEX = r"""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.19/dist/katex.min.css" integrity="sha384-7lU0muIg/i1plk7MgygDUp3/bNRA65orrBub4/OSWHECgwEsY83HaS1x3bljA/XV" crossorigin="anonymous">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.19/dist/katex.min.js" integrity="sha384-RdymN7NRJ+XoyeRY4185zXaxq9QWOOx3O7beyyrRK4KQZrPlCDQQpCu95FoCGPAE" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.19/dist/contrib/auto-render.min.js" integrity="sha384-hCXGrW6PitJEwbkoStFjeJxv+fSOOQKOPbJxSfM6G5sWZjAyWhXiTIIAmQqnlLlh" crossorigin="anonymous"
        onload="renderMathInElement(document.body);"></script>
<script>
  document.addEventListener("DOMContentLoaded", function() {
      renderMathInElement(document.body, {
          delimiters: [
            {left: "$$", right: "$$", display: true},
            {left: "$", right: "$", display: false}
          ]
      });
  });
</script>
"""

indent = 11

urllib.request.urlretrieve("https://raw.githubusercontent.com/flintlib/flint/refs/heads/main/AUTHORS", "AUTHORS")
authors_data = open("AUTHORS").read().splitlines()

lines = authors_data[authors_data.index("Major contributors")+2 : authors_data.index("Other contributors")]
lines_contributors = authors_data[authors_data.index("Other contributors")+5 : authors_data.index("Other credits")]


prefixes = ["  email    ", "  web      ", "  github   ", "  grants   ", "  what     "]

lines2 = []
for line in lines:
    if line.startswith("  ") and not any(line.startswith(pre) for pre in prefixes):
        lines2[-1] += line
    else:
        lines2.append(line)

lines = lines2

authors = []

i = 0
while i < len(lines):
    line = lines[i]
    if line and not line.startswith("  "):
        name = line
        for a in authors:
            if a[0] == name:
                raise ValueError("duplicate author", name)
        authors.append([name, dict()])
    elif line.startswith("  email    "):
        authors[-1][1]["email"] = line[indent:].strip()
    elif line.startswith("  web      "):
        authors[-1][1]["web"] = line[indent:].strip()
    elif line.startswith("  github   "):
        authors[-1][1]["github"] = line[indent:].strip()
    elif line.startswith("  what     "):
        authors[-1][1]["what"] = line[indent:].strip()
    elif line.startswith("  grants   "):
        authors[-1][1]["grants"] = line[indent:].strip()
    elif line.startswith("  "):
        authors[-1][1]["what"] = line[2:].strip()
    i += 1

authorlist = ""
contributorlist = ""

contributorlist += """<ul style="columns: 3;">"""
for line in lines_contributors:
    if line.strip():
        contributorlist += "<li>%s</li>\n" % line

contributorlist += "</ul>"

authorphoto = {
    "William Hart"      : "img/people/bill.jpg",
    "Fredrik Johansson" : "img/people/fredrik.jpg",
    "Albin Ahlbäck"     : "img/people/albin.jpg",
    "Andy Novocin"      : "img/people/andy.jpg",
    "Daniel Schultz"    : "img/people/daniel.jpg",
    "David Harvey"      : "img/people/david.jpg",
    "Mike Hansen"       : "img/people/mike.jpg",
    "Pascal Molin"      : "img/people/pascal.jpg",
    "Alex Best"         : "img/people/alex.jpg",
    "D.H.J. Polymath"   : "img/people/polymath.jpg",
}

if 0:
    authorlist += "<table>"
    for author in authors:
        author, data = author
        s = ""
        s += """<tr><td style="min-width:200px; text-align:center">"""
        if data.get("web"):
            s += """<a href="%s">%s</a>""" % (data.get("web"), author)
        else:
            s += """<b>%s</b>""" % author
        if author in authorphoto:
            s += """<br/><img src="%s" style="max-width:150px; max-height:150px" />""" % authorphoto[author]
        #if data.get("github"):
        #    s += """<br/><a href="https://github.com/flintlib/flint/commits?author=%s">commits</a>""" % data.get("github")
        s += "</td><td>"
        s += """<p>%s</p>""" % data.get("what")
        if data.get("grants"):
            s += """<p><i>Supported by %s.</i></p>""" % (data.get("grants"))
        s += "</td></tr>\n"
        authorlist += s
    authorlist += "</table>"
else:
    authorlist += "<dl>"
    for author in authors:
        author, data = author
        s = ""
        if author in authorphoto:
            s += """<div style="float:right; clear:both; text-align:center; border:1px solid #f8f8f8; padding:0.3em; background-color:#fcfcfc; margin-left:0.5em; margin-bottom:0.5em"><img src="%s" style="max-width:130px; max-height:130px;" /><br/>%s</div>""" % (authorphoto[author], author)
        s += "<dt>"
        if data.get("web"):
            s += """<a href="%s">%s</a>""" % (data.get("web"), author)
        else:
            s += """<b>%s</b>""" % author
        s += "</dt>"
        s += "<dd>"
        s += """%s""" % data.get("what")
        if data.get("grants"):
            s += """ <i>Supported by %s.</i>    """ % (data.get("grants"))
        s += "</dd>"
        authorlist += s
    authorlist += "</dl>"

source_prefix = "src/"
source_suffix = ".txt"
pages = [
	"index",
	"citation",
	"applications",
	"news",
	"documentation",
	"downloads",
	"development",
	"authors",
	"links"
]

page_titles = []
page_texts = []
page_want_katex = []

for page in pages:
    if 0 and page == "documentation":
        text = ""
        title = "Documentation"
    else:
        text = open(source_prefix + page + source_suffix, "r").read()
        title = text[text.find("<h2>")+4 : text.find("</h2>")]
    page_want_katex.append("%WANT_KATEX" in text)
    text = text.replace("%AUTHORLIST", authorlist)
    text = text.replace("%CONTRIBUTORLIST", contributorlist)
    text = text.replace("%WANT_KATEX", "")
    page_texts.append(text)
    page_titles.append(title)




timestamp = strftime("Last updated: %Y-%m-%d %H:%M:%S GMT", gmtime())


columns = 3
rows = (len(pages) + columns - 1) // columns

for i in range(len(pages)):
    if 0:
        menu = """<table style="margin-left:auto; margin-right:auto; border-collapse:collapse; border:none;"><tr>\n"""

        for j in range(len(pages)):
            if j % rows == 0:
                menu += """<td style="vertical-align:top"><ul>"""
            if i == j:
                menu += """<li>%s</li>\n""" % page_titles[j]
            else:
                menu += """<li><a href="%s.html">%s</a></li>\n""" % (pages[j], page_titles[j])
            if j % rows == rows - 1 or j == len(pages) - 1:
                menu += """</ul></td>"""

        menu += """</table></tr>\n"""
    else:
        menu = """<div style="text-align:center">"""
        for j in range(len(pages)):
            if i == j:
                menu += """ %s """ % page_titles[j]
            else:
                menu += """<a href="%s.html">%s</a> """ % (pages[j], page_titles[j])
            if j < len(pages) - 1:
                menu += """ &nbsp;<span style="color:#888">&middot;</span>&nbsp; """
        menu += """</div>"""

    title = page_titles[i]
    if title == "What is FLINT ?":
        title = ""
    else:
        title = " - " + title

    path = sys.argv[1]
    fp = open(path + "/" + pages[i] + ".html", "w")
    fp.write(PAGE_TOP.replace("TITLE", title).replace("MENU", menu).replace("%KATEX%", PAGE_KATEX if page_want_katex[i] else ""))
    fp.write(page_texts[i])
    fp.write(PAGE_BOTTOM.replace("TIMESTAMP", timestamp))
    fp.close()


