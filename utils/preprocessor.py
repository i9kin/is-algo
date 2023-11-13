# https://rust-lang.github.io/mdBook/for_developers/preprocessors.html
import json
import sys
import abc
from pathlib import Path
import tree_lib
from models import CacheImages


class StringBuilder:
    def __init__(self):
        self.text = ""

    def append(self, text):
        self.text += str(text)

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


class FileInfo:
    def __init__(self, fname):
        self.fname = fname

    def parent(self):
        return Path(self.fname).parent

    def __str__(self):
        return str(self.fname)


class ModifyInterface(abc.ABC):
    def __init__(self, separator: Separator):
        self.separator = separator

    @abc.abstractmethod
    def process(self, segment: TextSegment, fileinfo: FileInfo) -> str:
        return segment.text


class JinjaModify(ModifyInterface):
    def __init__(self):
        super().__init__(EmptySeparator())

    def process(self, segment: TextSegment, fileinfo: FileInfo) -> str:
        return segment.text


class TikzModify(ModifyInterface):
    def __init__(self):
        super().__init__(Separator("```tree", "```"))

    def process(self, segment: TextSegment, fileinfo: FileInfo) -> str:
        string = segment.text.strip()
        string = string.split("\n")
        assert len(string) <= 2

        t = tree_lib.PreOrder(list(map(int, string[0].strip().split(" "))))

        # minipage + figure = https://tex.stackexchange.com/questions/329249/caption-a-tikzpicture-on-standalone
        # scaling = https://tex.stackexchange.com/questions/4338/correctly-scaling-a-tikzpicture
        # minipage :( TODO normal resizing
        caption = False
        if len(string) == 2:
            caption = True

        tex = StringBuilder()
        tex.append(
            r"""\documentclass{standalone}
        \usepackage{tikz}
        \usepackage{caption}
        \usetikzlibrary{graphs,graphdrawing,arrows.meta}
        \usegdlibrary{trees}
        \begin{document}
        	"""
        )
        if caption:
            tex.append(
                r"""
            \begin{minipage}{5cm}
            \begin{figure}
            \centering
            \resizebox{5cm}{3cm}{"""
            )

        tex.append(
            r"""
        	\begin{tikzpicture}
        		\graph [binary tree layout, level distance=5mm]
        		{ """
        )
        tex.append(t)
        tex.append(r"""};	\end{tikzpicture}""")
        if caption:
            tex.append(
                r"""
            }
            \captionsetup{labelformat=empty} \caption{"""
            )
            tex.append(string[1])
            tex.append(
                r"""}
            \end{figure}
            \end{minipage}"""
            )
        tex.append(r"""\end{document}""")
        f = CacheImages().get_svg(str(tex))
        return f.set_dir(fileinfo.parent())


class TextModify:
    def __init__(self, list: list[ModifyInterface]):
        self.list = list

    def process(self, text, fileinfo: FileInfo) -> str:
        for modify in self.list:
            string = StringBuilder()
            text_iter = TextIter(text, modify.separator)
            for segment in text_iter:
                string.append(text_iter.normal(segment))
                string.append(modify.process(segment, fileinfo))
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
        chapter["content"] = self.text_modify.process(
            chapter["content"], FileInfo(chapter["path"])
        )
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
    # ? self.file внутри TextModify а не в TikzModify и тп,
    # так как в таком случае было надо было создавать изначально классы с FileInfo , а его мы на данном этапе не знаем
    Book(book, m).run()
