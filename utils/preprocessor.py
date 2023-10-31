# https://rust-lang.github.io/mdBook/for_developers/preprocessors.html
import hashlib
import json
import sys
import abc
from collections import defaultdict
from cache import shell_command
from pathlib import Path


def debug(s):
    sys.stderr.write(str(s))


class StringBuilder:
    def __init__(self):
        self.text = ""

    def append(self, text):
        self.text += text

    def __str__(self):
        return self.text


class TextSegment:
    def __init__(self, text, l, r):
        self.text = text
        self.l = l
        self.r = r

    def __str__(self):
        return self.text


class Separator:
    def __init__(self, l, r):
        self.left = l
        self.right = r


class EmptySeparator(Separator):
    def __init__(self):
        pass


class ModifyInterface(abc.ABC):
    def __init__(self, separator: Separator):
        self.separator = separator

    @abc.abstractmethod
    def process(self, segment: TextSegment) -> str:
        return segment.text


class JinjaModify(ModifyInterface):
    def __init__(self):
        super().__init__(EmptySeparator())

    def process(self, segment: TextSegment) -> str:
        return segment.text


class TikzModify(ModifyInterface):
    def __init__(self):
        super().__init__(Separator("```tree", "```"))

    def process(self, segment: TextSegment) -> str:
        string = segment.text.strip()
        string = string.split("\n")
        assert len(string) == 2
        root = int(string[0])
        g = defaultdict(list)
        for ab in [edge for edge in string[1].split(";") if edge]:
            a, b = map(int, ab.split())
            g[a].append(b)
            g[b].append(a)

        def dfs(v, p=-1):
            childs = []
            for u in sorted([u for u in g[v] if u != p]):
                childs.append(dfs(u, v))
            return f"{v}{'[first]' if v < p else '[second]'} -> {{{','.join(childs)}}}"

        tex = StringBuilder()
        tex.append(
            r"""\documentclass[tikz,border=5]{standalone}
        \usetikzlibrary{graphs,graphdrawing,arrows.meta}
        \usegdlibrary{trees}
        \begin{document}
        	\begin{tikzpicture}
        		\graph [binary tree layout, level distance=5mm]
        		{ """
        )
        tex.append(dfs(root))
        tex.append(
            r"""};	\end{tikzpicture}
        \end{document}"""
        )
        # https://tex.stackexchange.com/questions/492413/lualatex-rendering-from-input-buffer-instead-of-filename
        # https://tex.stackexchange.com/questions/51757/how-can-i-use-tikz-to-make-standalone-svg-graphics
        tex = str(tex)
        open("tmp.tex", "w").write(tex)
        shell_command("lualatex -synctex=1 -interaction=nonstopmode tmp.tex")
        shell_command("pdf2svg tmp.pdf tmp.svg")
        file_name = int(hashlib.sha1(tex.encode("utf-8")).hexdigest(), 16)
        Path("tmp.svg").rename(f"src/{file_name}.svg")
        return f'<img src = "{file_name}.svg"/>'


class TextModify:
    def __init__(self, list: list[ModifyInterface]):
        self.list = list

    def process(self, text) -> str:
        for modify in self.list:
            string = StringBuilder()
            text_iter = TextIter(text, modify.separator)
            for segment in text_iter:
                string.append(text_iter.normal(segment))
                string.append(modify.process(segment))
            string.append(text_iter.normal_end())
            text = string.text
        return text


class TextIter(object):
    def __init__(self, text, separator):
        self.text = text
        self.separator = separator
        self.prev_pos = 0
        self.cur_pos = 0

    def segment(self):
        start = self.text.find(self.separator.left, self.cur_pos)
        if start == -1:
            return None
        end = self.text.find(self.separator.right, start + len(self.separator.left))
        if end == -1:
            return None
        self.cur_pos = end + len(self.separator.right)
        return (start, self.cur_pos)

    def __iter__(self):
        if type(self.separator) is EmptySeparator:
            self.cur_pos = len(self.text)
            return TextSegment(self.text, 0, self.cur_pos)

        self.prev_pos = 0
        while True:
            res = self.segment()
            if res is None:
                break
            l, r = res
            yield TextSegment(
                self.text[l + len(self.separator.left) : r - len(self.separator.right)],
                l,
                r,
            )
            self.prev_pos = r

    def normal(self, segment: TextSegment):
        return self.text[self.prev_pos : segment.l]

    def normal_end(self):
        return self.text[self.prev_pos :]


class Book:
    def __init__(self, data, text_modify: TextModify):
        self.data = data
        self.text_modify = text_modify

    def chapter(self, chapter):
        chapter = chapter["Chapter"]
        chapter["content"] = self.text_modify.process(chapter["content"])
        if "sub_items" in chapter:
            for k in chapter["sub_items"]:
                self.chapter(k)

    def run(self):
        for section in self.data["sections"]:
            self.chapter(section)
        print(json.dumps(self.data))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "supports":
            sys.exit(0)
    context, book = json.load(sys.stdin)
    m = TextModify([TikzModify(), JinjaModify()])
    Book(book, m).run()
