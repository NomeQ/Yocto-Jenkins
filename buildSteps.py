from buildsteps import *
from jenkinsBuildSteps.stubs import Property
import os, sys
from ConfigParser import SafeConfigParser

jenkinsHome = os.environ.get("JENKINS_HOME")
workspace = os.environ.get("WORKSPACE")
yjHome = os.environ.get("YJ_HOME")
sys.path.append(yjHome + "/buildsteps")

# Parse .conf, env variables necessary for bitbake and some buildsteps
# Copied from yocto-start-autobuilder
parser = SafeConfigParser()
parser.read('yocto-jenkins.conf')
print "Reading " + os.path.join(yjHome, "yocto-jenkins.conf")
for section_name in parser.sections():
    for name, value in parser.items(section_name):
        print 'Setting %s to %s' % (name.upper(), value)
        os.environ[name.upper()] = value.strip('"').strip("'")
        if os.environ[name.upper()].endswith("_DIR"):
            if not os.path.exists(value):
                try:
                    os.mkdirs(value)
                    print ' Creating %s at %s' % (name.upper(), value)
                except:
                    pass
        print

# Factory and args are set up to be compatible with Autobuilder buildsteps, factory always
# being null here.
os.environ["FLUNK_BUILD"] = "False"
factory = None
kwargs = {}
steps = []

# Global variables and properties used by Autobuilder
YOCTO_ABBASE = yjHome
buildprops = Property()
kwargs["properties"] = buildprops
ab_props = {"workdir": workspace, "repository": os.environ.get("GIT_URL"), "builddir": workspace}
for k, v in ab_props.iteritems():
    buildprops.setProperty(k, v, "Auto")

# These autobuilder steps are redundant or incompatible with Jenkins
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


         
