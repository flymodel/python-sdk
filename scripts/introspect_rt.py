from pathlib import Path
from textwrap import dedent

from client import models

path = Path(__file__).parent.parent / "src" / "flymodel" / "models"


def model_import_stmt_pyi(name: str):
    return f"from flymodel.client.models import {name}"


def model_import_stmt_py(name: str):
    return f"from flymodel.client.models import {name}"


def imports_for_mod(mod):
    return list(filter(lambda v: not v.startswith("__"), dir(mod)))


def getatt_or_empty_str(obj, att):
    v = getattr(obj, att, "")
    return v if v else ""


PER_MODULE_EXTENSIONS = {
    "models.enums": """
from enum import IntEnum
class Lifecycle(IntEnum):
    Prod = 0
    Qa = 1
    Stage = 2
    Test = 3
"""
}


def introspect_models():
    top_level = imports_for_mod(models)

    pyi = ""
    for mod in top_level:
        pyi += model_import_stmt_pyi(mod) + "\n"

    with open(path / "__init__.pyi", "w") as f:
        f.write(pyi)

    for mod in top_level:
        module = getattr(models, mod)
        imports = imports_for_mod(module)
        pyi = path / (mod + ".pyi")
        if (pyi).exists():
            print(f"skipping {mod}")
        else:
            doc = getatt_or_empty_str(module, "__doc__")
            spec = getatt_or_empty_str(module, "__spec__")

            pyi_stub = dedent(
                f"""
__all__ = {imports!r}
__doc__ = {doc!r}
__spec__ = {spec!r}
"""
            )
            ext = PER_MODULE_EXTENSIONS.get("models." + mod)
            if ext:
                pyi_stub += "\n" + ext
            with open(pyi, "w") as f:
                f.write(pyi_stub)
        py = path / (mod + ".py")
        ext = "\n".join((f"{s} = {mod}.{s}" for s in imports))
        py_stub = dedent(
            f"""
from flymodel.client.models import {mod}
{ext}
"""
        )
        with open(py, "w") as f:
            f.write(py_stub)


if __name__ == "__main__":
    assert path.exists()
    assert path.is_dir()
    introspect_models()
