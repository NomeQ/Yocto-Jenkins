#!/bin/bash

# Pass the directory containing the autobuilder buildsteps as param
default="/yocto-autobuilder/lib/python2.7/site-packages/autobuilder/buildsteps"
if [ -d ~/$default ]; then
	directory=~/$default
elif [ $# -eq 1 -a -d $1/$default ]; then
	directory=$1/$default
else
	echo "Buildstep directory not found. Usage: './buildstep-tool.sh [/path/to/autobuilder/buildsteps]"
fi

cp -r $directory ./
rm ./buildsteps/*.pyc
cd ./buildsteps

for f in $( ls . ); do
	sed -i 's/from buildbot.[a-z]*.[a-z]*/from jenkinsBuildSteps.stubs/' "$f"
done
 	
