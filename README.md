# PySTAC IO

PySTAC IO is a Python library that provides additional IO implementations for [`pystac.STAC_IO`](https://pystac.readthedocs.io/en/latest/concepts.html#using-stac-io).

PySTAC IO extends [pystac](https://github.com/stac-utils/pystac) to support the following url schemes:

| Module | Scheme | Reads? | Writes? |
|--------|-----------------|---|---|
| fsspec | [many](#FSSpec) | X | X |
| https  | `https://`      | X |   |
| s3     | `s3://`         | X | X |

## Installation

Install via pip:

```shell
pip install pystac-io
```

You'll also need to install the dependencies for the modules you wish to use.
For example, to use the `s3` module:  

```shell
pip install "pystac-io[s3]"
```

## Usage

Import `pystac_io` and the submodule you plan to use, register the submodule to enable it, and then use `pystac` normally!

```python
import pystac
import pystac_io
import pystac_io.s3   # Import the IO module you plan to `register()`

pystac_io.register("s3")
s3_catalog = pystac.Catalog.from_file("s3://bucket/path/to/catalog.json")
```

### Advanced Usage

#### FSSpec

pystac-io provides a [fsspec](https://filesystem-spec.readthedocs.io/en/latest/) module which uses `fsspec` as a backend to read and write many different local and remote filesystem formats. For a complete list of available backends:
```python
from fsspec.registry import known_implementations
known_implementations
```

Some of these backends require additional dependencies. Install with:
```shell
pip install fsspec[<backend>]
```

For example, to install the dependencies for the `s3` backend:

```shell
pip install fsspec[s3]
```

#### Multiple IO Modules

`pystac.STAC_IO` is only able to register a single global read and write handler. If you need to use multiple `pystac_io` modules in the same script you need to unregister one before registering another.

Enable a module with `pystac_io.register` and disable with `pystac_io.unregister` or use `pystac_io.register` as a  context manager:

```python
import pystac
import pystac_io

# Manual management
import pystac_io.s3
pystac_io.register("s3")
s3_catalog = pystac.Catalog.from_file("s3://bucket/path/to/catalog.json")
pystac_io.unregister()

# Context manager
import pystac_io.https
with pystac_io.register("https"):
    https_catalog = pystac.Catalog.from_file("https://foo.com/path/to/catalog.json")
```

#### Adding Your Own IO Module

PySTAC IO makes it easy to register, load, and unload your custom IO modules.

Implement `pystac.STAC_IO` read and write methods:

```python
def my_custom_read_text_method(uri):
    ...

def my_custom_write_text_method(uri, text):
    ...
```

Make pystac_io aware of your module:

```python
import pystac_io

pystac_io.add(
    "my_custom_module",
    pystac_io.IoReadWrite(my_custom_read_text_method, my_custom_write_text_method)
)
```

Use your custom module:

```python
import pystac

pystac_io.register("my_custom_module")
custom_catalog = pystac.Catalog.from_file("...")
```

## Developing

Install the development requirements:

```shell
pip install -r requirements-dev.txt
```

Make changes as desired, then run:

```shell
./scripts/test
```

## Releasing a new version

Follow the checklist in [RELEASE.md](./RELEASE.md)
