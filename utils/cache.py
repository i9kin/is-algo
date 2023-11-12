import subprocess
import sys
from pathlib import Path
import hashlib


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


# https://tex.stackexchange.com/questions/492413/lualatex-rendering-from-input-buffer-instead-of-filename
# https://tex.stackexchange.com/questions/51757/how-can-i-use-tikz-to-make-standalone-svg-graphics


def generate_image(tex, fileinfo):
    tex = str(tex)
    open("tmp.tex", "w").write(tex)

    shell_command("lualatex -synctex=1 -interaction=nonstopmode tmp.tex", tex)
    shell_command("pdf2svg tmp.pdf tmp.svg", tex)
    shell_command("convert -density 300 tmp.svg tmp.png", tex)

    file_name = int(hashlib.sha1(tex.encode("utf-8")).hexdigest(), 16)
    Path("tmp.png").rename(f"src/{fileinfo.parent()}/{file_name}.png")
    return f'<img src = "{file_name}.png" class="center"/>'
