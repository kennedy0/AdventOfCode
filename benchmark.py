import os
import subprocess
import sys
from utils.timer import Timer


def profile_all() -> int:
    with Timer("all challenges"):
        for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), "2020")):
            for f in files:
                if f.endswith(".py"):
                    with Timer(f):
                        profile(file=os.path.join(root, f))
    return 0


def profile(file: str) -> int:
    use_shell = os.name == "nt"
    cmd = ["python", file]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=use_shell)
    stdout, stderr = proc.communicate()
    return proc.returncode


if __name__ == "__main__":
    sys.exit(profile_all())
