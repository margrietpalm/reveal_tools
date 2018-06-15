# Reveal tools

## Dependencies
- Python (2.7 or later)
- Python library future (for Python < 3)


## clean_pres_im

Identify images in *image* folder that are not used in the presentation:

```
usage: clean_pres_im.py [-h] [-q] [--imfolder IMFOLDER] [--mdfolder MDFOLDER]
                        [--index INDEX] [--delete]
                        [path]

Clean images folders

positional arguments:
  path                 path to reveal base dir (default: ./)

optional arguments:
  -h, --help           show this help message and exit
  -q, --quiet          suppress output
  --imfolder IMFOLDER  path to images in reveal base dir (default: images/)
  --mdfolder MDFOLDER  path to markdown in reveal base dir (default:
                       markdown/)
  --index INDEX        html index (default: index.html)
  --delete             delete unused images (default: False)
```

## clean_pres_mov

Identify movies in *movie* folder that are not used in the presentation.


```
usage: clean_pres_mov.py [-h] [-q] [--movfolder MOVFOLDER]
                         [--mdfolder MDFOLDER] [--index INDEX] [--delete]
                         [path]

Clean images folders

positional arguments:
  path                  path to reveal base dir (default: ./)

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           suppress output
  --movfolder MOVFOLDER
                        path to movies in reveal base dir (default: movies/)
  --mdfolder MDFOLDER   path to markdown in reveal base dir (default:
                        markdown/)
  --index INDEX         html index (default: index.html)
  --delete              delete unused images (default: False)
```

## extract_notes

Extract reveal notes from markdown file and collect them in a markdown file. Expected syntax for notes:
```
Slide title
----------------
content

Note:
- say something
```

This script expect that slides are separated by 3 blank lines and subslides by 2 blank lines.

```
usage: extract_notes.py [-h] [-q] [-o OUTFILE] [--to-pdf] [--to-html]
                        [--number-slides]
                        [mdfile]

Clean images folders

positional arguments:
  mdfile                path to reveal base dir (default: slides.md)

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           suppress output
  -o OUTFILE, --outfile OUTFILE
  --to-pdf              convert to pdf
  --to-html             convert to html
  --number-slides
```
