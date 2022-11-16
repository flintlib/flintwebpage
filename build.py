import glob

PAGE_TOP = r"""<html>
<head>
<title>FLINT: Fast Library for Number TheoryTITLE</title>

<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<style type="text/css" media="screen">
body, table { font-family: arial, sans-serif; font-size: 16px; line-height:1.4em; background-color:#fff; color: #111; }
h1, h2, h3 { font-weight: normal; }
h1 { font-weight: bold; font-size:40px; line-height:40px; font-family: arial, sans-serif; margin-bottom: 0.5em; }
h2 { background-color: #f8f8f8; color: #444; border-radius:0.2em; padding: 0.2em 0.2em 0.2em 0.5em; }
h3 { font-weight: bold; border-bottom: 2px dotted #aaa; }
h4 { color: #777; }
a { color: #004fa0; text-decoration: none; }
a:hover { color: #206fc0; text-decoration: none; background-color: #fafafa; }
pre { padding-left: 2em; }
#main { padding: 1em; max-width:900px; margin: 0 auto; }
#content { }

.benchmark { border-collapse:collapse; }
.benchmark td, .benchmark th { border:1px solid #ccc; padding:3px 7px 2px 7px; }
.benchmark th { text-align:left; padding-top:5px; padding-bottom:4px; background-color:#eee; color:#000; }
.benchmark tr.alt td { color:#000; background-color:#f8f8f8; }


</style>
</head>

<body>
<div id="main">

<h1 style="text-align:center">FLINT : <span style="color:#cc3333">Fast Library for Number Theory</span></h1>

<!-- <div style="text-align:center; margin-bottom:1.5em"><img style="scale:90%" src="factor200.svg"></div> -->
<!-- <div style="text-align:center; margin-bottom:1.5em"><img style="scale:90%" src="factor.svg"></div> -->


<div style="text-align:center; margin-bottom:1.5em">

<script>
var formulas = [
  "delta.svg",
  "factor.svg",
  "factorpoly.svg",
  "bernoulli.svg",
];

var size = formulas.length;
var x = Math.floor(size*Math.random());
var imgStr = '<img src="' + formulas[x] + '" style="scale:90%" />';
document.write(imgStr); document.close();
</script>
</div>

MENU

<br/>

<!-- <hr/> -->

<div id="content">
"""

PAGE_BOTTOM = r"""

<hr style="border:0; height:1px; color:#ccc; background-color:#ccc; margin-top:2em;" />

<div style="line-height:1em">
<p><i>TIMESTAMP</i></p>

<p><i>Contact: <a href="mailto:fredrik.johansson@gmail.com">Fredrik Johansson</a>, <a href="https://groups.google.com/g/flint-devel">flint-devel mailing list</a></i></p>

</div>

</div>
</div>

</body>
</html>
"""

pages = ["index", "news", "documentation", "downloads", "development", "authors", "links"]

page_titles = []
page_texts = []

for page in pages:
    if 0 and page == "documentation":
        text = ""
        title = "Documentation"
    else:
        text = open(page + ".txt", "r").read()
        title = text[text.find("<h2>")+4 : text.find("</h2>")]
    page_texts.append(text)
    page_titles.append(title)




from time import gmtime, strftime
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
    if title == "Overview":
        title = ""
    else:
        title = " - " + title

    fp = open(pages[i] + ".html", "w")
    fp.write(PAGE_TOP.replace("TITLE", title).replace("MENU", menu))
    fp.write(page_texts[i])
    fp.write(PAGE_BOTTOM.replace("TIMESTAMP", timestamp))
    fp.close()


