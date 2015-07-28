from buildsteps import *
import sys
import os

jenkinsHome = os.environ.get("JENKINS_HOME")
workspace = os.environ.get("WORKSPACE")
sys.path.append(jenkinsHome + "/yocto-jenkins/buildsteps")

# Factory and args are set up to be compatible with Autobuilder buildsteps, factory always
# being null here.
os.environ["FLUNK_BUILD"] = "False"
factory = None
kwargs = {}
steps = []

def parseBuildstep(arg):
    if "=" in arg:
        key, value = arg.split("=")
        kwargs[key] = value
    else:
        steps.append(arg)

for arg in sys.argv[1:]:
    parseBuildstep(arg)


for step in steps:
    m = __import__ (step)
    func = getattr(m, step)
    func(factory, kwargs)

flunk = os.environ.get("FLUNK_BUILD")
if flunk=="True":
    sys.exit(1)


         
