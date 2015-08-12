#!/bin/bash
export YJ_HOME=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

if [ ! -d $YJ_HOME/buildsteps ]; then
        echo "Running buildstep tool"
	$YJ_HOME/buildstep-tool.sh
fi

python $YJ_HOME/buildSteps.py $@

