## how to use

`-f` is a flag to treat input as files
`-t` is an arg to override the default svg file in `/tmp`. Target can by any file extension which matplotlib supports.

```bash
# piped input
echo <WKT> | geoviz

cat *.wkt | geoviz 
# where *.wkt is a list of files containing wkt strings one per line
# files must end with newline for cat to concatenate them properly

# file input
geoviz -f *.geojson
geoviz -t wkt.svg -f *.wkt
# reads contents of files as geojson or wkt based off file extension
```
where <WKT> is a valid WKT string.

##
creates a SVG file in /tmp
prints the path to the SVG file in terminal

