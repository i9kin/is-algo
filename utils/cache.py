import subprocess
import sys


def debug(s):
    sys.stderr.write(str(s) + "\n")


def shell_command(command: str, input_string: str = " ") -> str:
    try:
        p = subprocess.Popen(
            command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except:
        raise Exception("Invalid command ", command)
    std_out, std_err = p.communicate(input_string.encode())
    if p.returncode != 0:
        err_msg = "%s. Code: %s" % (std_err.decode().strip(), p.returncode)
        raise Exception(err_msg)
    return std_out.decode()
