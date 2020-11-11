import fsspec

from .. import add, IoReadWrite


def fsspec_read_text_method(uri):
    with fsspec.open(uri) as f:
        return f.read()


def fsspec_write_text_method(uri, txt):
    with fsspec.open(uri, "w") as f:
        return f.write(txt)


add("fsspec", IoReadWrite(fsspec_read_text_method, fsspec_write_text_method))
