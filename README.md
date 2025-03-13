# Build system

We generate `src/downloads.txt` that is being used to generate
`${DEST}/downloads.html`.  To generate the source file, run
```
$ python3 downloads.py ${PATH_TO_DEST}
```
where `${PATH_TO_DEST}/download` is the path to the directory that contains all
PDF-files and compressed releases (probably `~/apps/flintlib_org/`).

Furthermore, we also generate `src/citation.txt` that is being used to generate
`${DEST}/citation.html`.  To generate the source file, run
```
$ python3 citation.py
```
This uses HISTORY, so make sure that HISTORY is ordered and up-to-date.

Following this, generate all HTML pages via
```
$ python3 build.py ${PATH_TO_DEST}
```
which outputs all HTML files to `${PATH_TO_DEST}` (probably
`~/apps/flintlib_org/`).



# Source file structure

In the source directory:

- `./`:		Building scripts are located in the top directory.
- `src/`:	Text files that are to be used to generated to HTML files.



# Output file system

The following directories in the output directory `${PATH_TO_DEST}` needs to be
populated already:

- `img/`:	Images for website, such as figures and picture of authors.
- `download/`:	PDF documentation along with releases (`.tar.gz` and `.zip`)
		files.
