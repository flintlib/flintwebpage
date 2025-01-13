# downloads.py: generate downloads.txt

import sys
import glob
import re
from itertools import groupby

if len(sys.argv) != 2:
	print("Usage:  python3 downloads.py ARG\n"
	      "\n"
	      "For documentation on ARG, see README.md.")
	exit(1)

path = sys.argv[1]
output = "src/downloads.txt"

page_top = r"""<h2>Downloads</h2>

<p>For a list of changes in each release, see the <a href="https://www.flintlib.org/doc/history.html">history</a> section of the documentation.</p>
"""

files = glob.glob(path + '/download/flint-*')

# Only keep files that are on the form MAJOR.MINOR.PATCH and that is not alpha,
# beta or devel.
pattern = re.compile(r".*/flint-(\d+)\.(\d+)\.(\d+)\.(.*)")
files = [fp for fp in files if pattern.match(fp)]

def sort_key(file):
	match = pattern.match(file)
	if match:
		return (int(match.group(1)), int(match.group(2)), int(match.group(3)), match.group(4))
	return (float('inf'), float('inf'), float('inf'), float('inf'))

files.sort()
files.sort(key=sort_key)

# Find out how long PATH is
pathdownlen = 0
pathlen = 0
pathmatch = re.match(r"(.*/download/)", files[0])
if pathmatch:
	pathdownlen = len(pathmatch.group(1))
	pathlen = pathdownlen - len("download/")
else:
	print("Could not match PATH.  Exiting...")
	exit(1)

# Extract triplets and sort the files by triplets
parsed_files = []
for item in files:
	match = pattern.match(item)
	if match:
		parsed_files.append((match.group(1, 2, 3), item))

# Read HISTORY
with open('HISTORY', 'r') as file:
    history_lines = file.read()

# NOTE: We do not capture 3.1.3-p1.
history = []
pattern = re.compile(r"(\d+)\.(\d+).(\d+)\s+(\d{4}-\d{2}-\d{2})")
for line in history_lines.splitlines():
	match = pattern.match(line)
	if match:
		history.append(((match.group(1), match.group(2), match.group(3)), match.group(4)))

# Group by triplets and perform actions
ver = "1"
page = "</ul>\n"
for triplet, group in groupby(parsed_files, key=lambda x: x[0]):
	group_strings = [item[1] for item in group]

	# Print previous series header to page if needed if triplet[0] != ver:
	if triplet[0] != ver:
		tmp = "</ul>\n\n<h3>FLINT " + ver + ".x series</h3>\n\n<ul>\n"
		page = tmp + page
		ver = triplet[0]

	# Start of new item
	this_item = "<li>"

	# Find date
	found_date = False
	for htriplet, hdate in history:
		if htriplet == triplet:
			this_item += hdate + ": "
			found_date = True
	if not found_date:
		this_item += "XXXX-XX-XX: "

	# We want the PDF to come last.
	if group_strings[0].endswith(".pdf"):
		group_strings = group_strings[1:] + group_strings[:1]

	for ix, string in enumerate(group_strings):
		if ix != 0:
			this_item += ", "

		if string.endswith(".tar.gz") or string.endswith(".zip"):
			this_item += f"""<a href="{string[pathlen:]}"><b>{string[pathdownlen:]}</b></a>"""
		elif string.endswith(".pdf"):
			this_item += f"""documentation: <a href="{string[pathlen:]}"><b>{string[pathdownlen:]}</b></a>"""
		else:
			print("error")
			exit(1)

	# End of item
	this_item += "</li>\n"

	page = this_item + page


tmp = "\n<h3>FLINT " + ver + ".x series</h3>\n\n<ul>\n"
page = tmp + page

final = page_top + page
with open(output, "w") as file:
	file.write(final)
