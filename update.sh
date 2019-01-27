#!/bin/bash -eu
PARENT_DIR=$(cd $(dirname $0);pwd)
cd $PARENT_DIR/listup-repo/
python listup_repos.py
cd $PARENT_DIR/scrap-repo/
python scrap_repo.py
cd $PARENT_DIR/attach-geotag/
python attach_geotag.py
cd $PARENT_DIR/gen-website/
python gen_website.py
cd $PARENT_DIR/star-repos/
python star_repos.py
