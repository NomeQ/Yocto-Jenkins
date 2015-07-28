#!/bin/bash
PYENV_HOME=$WORKSPACE/.pyenv/

if [ -d $PYENV_HOME ]; then
	echo "Using existing virtual environment"
else
	echo "Creating new virtual environment"
	virtualenv --no-site-packages $PYENV_HOME	
fi

. $PYENV_HOME/bin/activate

python $JENKINS_HOME/yocto-jenkins/buildSteps.py $@

