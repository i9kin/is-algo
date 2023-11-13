# https://tex.stackexchange.com/questions/492413/lualatex-rendering-from-input-buffer-instead-of-filename
# https://tex.stackexchange.com/questions/51757/how-can-i-use-tikz-to-make-standalone-svg-graphics
import utils
import os
from peewee import SqliteDatabase, CharField, Model, TextField, BlobField
import hashlib
from typing import Optional
from pathlib import Path


def _hash(x) -> int:
    return int(hashlib.sha1(str(x).encode("utf-8")).hexdigest(), 16)


cache = SqliteDatabase(os.path.join(os.path.dirname(__file__), "cache.sqlite"))


class FileModel(Model):
    key = CharField(unique=True)
    data = BlobField()

    class Meta:
        database = cache
        db_table = "file_cache"


class CacheFile:
    def __init__(self):
        self.data = None
        self.fname = None
        self.prefix = None
        self.tex_hash = None

    def set_tex_hash(self, tex_hash):
        self.tex_hash = tex_hash

    def set_prefix(self, prefix):
        self.prefix = prefix

    def set_fname(self, fname):
        self.fname = fname

    def load_data(self, data: BlobField):
        self.data = data

    def _set_path(self, path: str):
        if self.data is None:
            utils.debug("[rename]" + path)
            Path(f"{self.fname}.{self.prefix}").rename(path)
        else:
            utils.debug("[write_bytes]" + path)
            Path(path).write_bytes(self.data)

    def set_dir(self, dir) -> str:
        if self.data is None:
            self._set_path(f"src/{dir}/{self.tex_hash}.{self.prefix}")
        else:
            self._set_path(f"{self.fname}.{self.prefix}")
        return f'<img src = "{self.tex_hash}.{self.prefix}" class="center"/>'


class CacheImages:
    def __get(self, tex: str, extension: str) -> Optional[FileModel]:
        files = [
            f
            for f in FileModel().select().where(FileModel.key == _hash(tex + extension))
        ]
        if len(files) == 1:
            return files[0]
        else:
            return None

    def __set(self, key: str, extension: str, data: bytes) -> BlobField:
        f = FileModel()
        f.key = _hash(key + extension)
        f.data = data
        f.save()
        return f.data

    def get_svg(self, tex) -> CacheFile:
        file = self.__get(tex, "svg")
        f = CacheFile()
        f.set_tex_hash(_hash(tex + "svg"))
        f.set_prefix("svg")
        f.set_fname("tmp")
        if file is not None:
            utils.debug("cache")
            f.load_data(file.data)
            f.set_fname(_hash(tex + "svg"))
            return f
        Path("tmp.tex").write_text(tex)
        utils.shell_command("lualatex -synctex=1 -interaction=nonstopmode tmp.tex")
        utils.shell_command("pdf2svg tmp.pdf tmp.svg")
        self.__set(tex, "svg", open("tmp.svg", "rb").read())
        return f

    def get_png(self, tex) -> CacheFile:
        file = self.__get(tex, "png")
        f = CacheFile()
        f.set_tex_hash(_hash(tex + "png"))
        f.set_prefix("png")
        f.set_fname("tmp")
        if file is not None:
            utils.debug("[cache]")
            f.load_data(file.data)
            f.set_fname(_hash(tex + "png"))
            return f
        cache_file = self.get_svg(tex)
        utils.debug("_set_path direct")
        cache_file._set_path("tmp.svg")
        utils.shell_command("convert -density 300 tmp.svg tmp.png")
        self.__set(tex, "png", open("tmp.png", "rb").read())

        return f


if __name__ == "__main__":
    cache.drop_tables([FileModel])
    cache.create_tables([FileModel])
