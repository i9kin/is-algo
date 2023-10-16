from subprocess import Popen, PIPE, STDOUT
from pathlib import Path
import re

formatter = "clang-format --style=file:utils/.clang-format"


def format_code(code: str) -> str:
    p = Popen(formatter.split(), stdout=PIPE, stdin=PIPE, stderr=PIPE)
    return p.communicate(input=code.encode())[0].decode()


def modify_code(text: str) -> str:
    res = ""
    p = 0
    while True:
        start = text.find("```cpp", p)
        if start == -1:
            break
        end = text.find("```", start + 6)
        code = format_code(text[start + 7 : end - 1])
        res += text[p:start] + "```cpp\n" + code + "\n```"
        p = end + 3
    res += text[p:]
    return res


def modify_dash(text: str) -> str:
    return (
        text.replace("—", "&mdash;")
        .replace(r"\\(", "$")
        .replace(r"\\)", "$")
        .replace(r"\\[", "$$")
        .replace(r"\\]", "$$")
        .replace(r"\\{", r"\{")
        .replace(r"\\}", r"\}")
    )


def modify_asymptotic(text: str) -> str:
    regex = "O\((?:(?!\)).)+\)"

    def repl(matchobj):
        start, end = matchobj.span()
        match = matchobj.group(0)
        if (
            start - 3 >= 0
            and end + 3 <= len(text)
            and text[start - 3 : start] == r"\\("
            and text[end : end + 3] == r"\\)"
        ):
            return match
        else:
            return r"\\(" + match + r"\\)"

    return re.sub(regex, repl, text)


def modify_file(file: Path, func):
    file.write_text(func(file.read_text()))


files = list(Path(".").rglob("*.md"))
files.remove(Path("src/SUMMARY.md"))
for file in files:
    print("file =", file)
    modify_file(file, modify_code)
    modify_file(file, modify_dash)
    # modify_file(file, modify_asymptotic) TODO fix pls
