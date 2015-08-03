from buildsteps import *
import sys
import os

jenkinsHome = os.environ.get("JENKINS_HOME")
workspace = os.environ.get("WORKSPACE")
yjHome = os.environ.get("YJ_HOME")
sys.path.append(yjHome + "/buildsteps")

# Factory and args are set up to be compatible with Autobuilder buildsteps, factory always
# being null here.
os.environ["FLUNK_BUILD"] = "False"
factory = None
kwargs = {}
steps = []

#These autobuilder steps are redundant or incompatible with Jenkins
badsteps = ["CheckOutLayers", "SendErrorReport", "SendQAEmail", "SetDest", "TriggerBuilds"]

def parseBuildstep(arg):
    if "=" in arg:
        key, value = arg.split("=")
        kwargs[key] = value
    else:
        steps.append(arg)

for arg in sys.argv[1:]:
    parseBuildstep(arg)

for step in steps:
    if step in badsteps:
        print step + " is not compatible with Yocto-Jenkins. Skipping."
    else:
        m = __import__ (step)
        func = getattr(m, step)
        func(factory, kwargs)

flunk = os.environ.get("FLUNK_BUILD")
if flunk=="True":
    sys.exit(1)


         
