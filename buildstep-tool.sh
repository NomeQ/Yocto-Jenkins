#!/bin/bash

# Pass the directory containing the autobuilder buildsteps as param, or it will
# automatically download from the official yocto-project site
default="/yocto-autobuilder/lib/python2.7/site-packages/autobuilder/buildsteps"
if [ $# -eq 1 -a -d $1/$default ]; then
	directory=$1/$default
	cp -r $directory ./
	cd buildsteps
else
	mkdir buildsteps
	cd buildsteps
	wget -r -np -A.py -nH --cut-dirs=10 "http://git.yoctoproject.org/cgit/cgit.cgi/yocto-autobuilder/plain/lib/python2.7/site-packages/autobuilder/buildsteps/"
fi

for f in $( ls . ); do
	sed -i 's/from buildbot.[a-z]*.[a-z]*/from jenkinsBuildSteps.stubs/' "$f"
done
 	
