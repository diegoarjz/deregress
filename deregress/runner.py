from subprocess import Popen, PIPE
import os

from deregress.exceptions import InvalidExecutable

class Runner:
    def __init__(self):
        self._executable = None
        self._arguments = []
        self._stdout_path = None
        self._stedrr_path = None

    def executable(self, path_to_executable):
        self._executable = path_to_executable
        return self

    def arg(self, argument):
        self._arguments.append(argument)
        return self

    def args(self, args):
        self._arguments = args
        return self

    def stdout(self, redirect):
        self._stdout_path = redirect
        return self

    def stderr(self, redirect):
        self._stedrr_path = redirect
        return self

    def run(self):
        if not os.path.exists(self._executable):
            raise InvalidExecutable("Unable to find executable file %s" % self._executable)            

        if not os.access(self._executable, os.X_OK):
            raise InvalidExecutable("Executable doesn't have executable permissions")

        command = [self._executable] + self._arguments

        redirections = {}
        if self._stdout_path is not None:
            redirections["stdout"] = open(self._stdout_path, "wb")
        if self._stedrr_path is not None:
            redirections["stderr"] = open(self._stedrr_path, "wb")

        process = Popen(command, **redirections)
        process.wait()

        for open_file in redirections.values():
            open_file.close()
