from subprocess import Popen, PIPE


def shell_command(command: str, input: str = " ") -> str:
    p = Popen(command.split(), stdout=PIPE, stdin=PIPE, stderr=PIPE)
    return p.communicate(input=input.encode())[0].decode()
