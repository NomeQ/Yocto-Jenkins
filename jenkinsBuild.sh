#!/bin/bash
export YJ_HOME=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
PYENV_HOME=$YJ_HOME/.pyenv/

if [ -d $PYENV_HOME ]; then
	echo "Using existing virtual environment"
else
	echo "Creating new virtual environment"
	virtualenv --no-site-packages $PYENV_HOME	
fi

. $PYENV_HOME/bin/activate

if [ ! -d buildsteps ]; then
        echo "Running buildstep tool"
	$YJ_HOME/buildstep-tool.sh
fi

python $YJ_HOME/buildSteps.py $@

