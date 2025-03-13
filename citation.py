# citation.py: generate citation.txt

import sys
import re

if len(sys.argv) != 1:
    print("Usage:  python3 citation.py")
    exit(1)

output = "src/citation.txt"

# Read HISTORY
with open('HISTORY', 'r') as file:
    history_lines = file.read()

version = ""
year = ""

# NOTE: We do not capture 3.1.3-p1.  We just want the last proper version.
pattern = re.compile(r"(\d+)\.(\d+).(\d+)\s+(\d{4})-\d{2}-\d{2}")
for line in history_lines.splitlines():
    match = pattern.match(line)
    if match:
        version = f"{match.group(1)}.{match.group(2)}.{match.group(3)}"
        year = f"{match.group(4)}"

page = r"""<h2>Citing FLINT</h2>

<p>When citing FLINT, the following form is recommended:</p>

<blockquote>The FLINT team. FLINT: Fast Library for Number Theory, """ + year + r""".
Version """ + version + r""", https://flintlib.org.</blockquote>

<pre>
@manual{flint,
  key = {{FLINT}},
  author = {The {FLINT} team},
  title = {{FLINT}: {F}ast {L}ibrary for {N}umber {T}heory},
  year = {""" + year + r"""},
  note = {Version """ + version + r""", \url{https://flintlib.org}}
}
</pre>

<p>
Please consider also looking up whether there is a paper discussing
the specific feature(s) in FLINT which you are using. In many cases, there is such a paper!
For example, research using the ball arithmetic component of FLINT (Arb) may cite:</p>

<blockquote>
F. Johansson. "Arb: efficient arbitrary-precision midpoint-radius interval arithmetic", IEEE Transactions on Computers, 66(8):1281-1292, 2017. DOI: <a href="https://doi.org/10.1109/TC.2017.2690633">10.1109/TC.2017.2690633</a>
</blockquote>

<pre>
@article{7891956,
  author = {Fredrik Johansson},
  journal = {{IEEE} Transactions on Computers},
  title = {{A}rb: Efficient Arbitrary-Precision Midpoint-Radius Interval Arithmetic},
  year = {2017},
  volume = {66},
  number = {8},
  pages = {1281-1292},
  doi = {10.1109/TC.2017.2690633}
}
</pre>

<p>Research using FLINT's number fields may cite:</p>

<blockquote>William B. Hart. "ANTIC: Algebraic number theory in C", Computeralgebra-Rundbrief: Vol. 56, 2015</blockquote>

<p>Many other references can be found <a href="https://www.flintlib.org/doc/references.html">in the bibliography of the FLINT documentation</a>.</p>

<p>For a list of changes in each release, see the <a href="https://www.flintlib.org/doc/history.html">history</a> section of the documentation.</p>
"""

with open(output, "w") as file:
    file.write(page)
