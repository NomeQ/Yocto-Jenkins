#!/bin/bash
YJ_HOME=`pwd`
PYENV_HOME=$YJ_HOME/.pyenv/

export YJ_HOME

if [ -d $PYENV_HOME ]; then
	echo "Using existing virtual environment"
else
	echo "Creating new virtual environment"
	virtualenv --no-site-packages $PYENV_HOME	
fi

. $PYENV_HOME/bin/activate

if [ ! -d buildsteps ]; then
        echo "Running buildstep tool"
	./buildstep-tool.sh
fi

python $YJ_HOME/buildSteps.py $@

