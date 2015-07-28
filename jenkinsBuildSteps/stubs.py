import subprocess
import os
import sys
import time
import signal

SUCCESS, WARNINGS, FAILURE, SKIPPED, EXCEPTION, RETRY = range(6)

class BuildStep:
    haltOnFailure = False
    flunkOnFailure = True
    name = "Anonymous Build Step" 
    def __init__(self, **kwargs):
        self.start()

    def start(self):
        fout = "echo " + self.describe(done=False)
        subprocess.call(fout.split(" "))

    def finished(self, results):
        self.results = results
        fout = "echo "
        if self.results is SUCCESS:
            fout += "SUCCESS: "
        elif self.results is FAILURE:
            fout += "FAILURE: "
            if self.flunkOnFailure is True:
                os.environ["FLUNK_BUILD"] = "True"
            if self.haltOnFailure is True:
                sys.exit("HALTING ON FAILURE: " + self.describe(done=True))
        elif self.results is WARNINGS:
            fout += "WARNING: "
        elif self.results is SKIPPED:
            fout += "SKIPPED: "
        elif self.results is EXCEPTION:
            fout += "EXCEPTION: "
        elif self.results is RETRY:
            fout += "RETRY NOT SUPPORTED: "
        fout += self.describe(done=True)
        subprocess.call(fout.split(" ")) 

    def getProperty(self, propname):
        pass

    def setProperty(self, propname, value, source='Step'):
        pass

    def describe(self, done=False):
        if done:
            return self.name
        else:
            return "Running " + self.name + "..."

class LoggingBuildStep(BuildStep):
    def __init__(self, **kwargs):
        BuildStep.__init__(self, **kwargs)

    def commandComplete(self, cmd):
        pass

class ShellCommand(LoggingBuildStep):
    name = "Shell Command"
    def __init__(self, **kwargs):
        LoggingBuildStep.__init__(self, **kwargs)
	
    def start(self):
        LoggingBuildStep.start(self)
	if self.timeout is None:
            self.exit_status = subprocess.call(self.command.split(" "))
        else:
            self.exit_status = self.timeoutCommand(self.command, self.timeout)
        self.commandComplete(self.command)
        if self.exit_status is 0:
            self.finished(SUCCESS)
        elif self.exit_status is None:
            self.finished(WARNINGS)
        else:
            self.finished(FAILURE)

    def timeoutCommand(self, cmd, timeout):
        # This method was heavily guided by example from Amir Salihefendic @ amix.dk 
        # What is our policy on borrowed code?
        start_time = time.time()
        proc = subprocess.Popen(cmd.split(" "))
        while proc.poll() is None:
            time.sleep(0.1)
            cur_time = time.time()
            if (cur_time - start_time) > (timeout/1000):
                print "TIMEOUT: Killing " + self.name
                os.kill(proc.pid, signal.SIGKILL)
                os.waitpid(-1, os.WNOHANG) 
                return None
        return proc.returncode                        
