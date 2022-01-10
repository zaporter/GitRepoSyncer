#!/bin/bash

SCRIPT_PATH=`readlink -f "$0"`
SCRIPT_DIR=`dirname "$SCRIPT_PATH"`

/usr/bin/ln -s $SCRIPT_DIR/gitreposyncer.py /usr/bin/gitreposyncer


echo "This was installed at $SCRIPT_DIR. If you want to move the git repo, make sure to reinstall at the correct location"
echo "use the command gitreposyncer to interact with this tool"
