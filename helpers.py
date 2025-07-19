import solid2.extensions.bosl2 as bosl
from pathlib import Path
from typing import Any, Mapping
from attrs import define


class MultAttrNamespaceMeta(type):
    _orig_attrs: Mapping
    _INDENT = 3 * " "

    def __new__(mcs, name, bases, namespace):
        # Create the original class first
        cls = super().__new__(mcs, name, bases, namespace)

        addthem = {}
        orig_attrs = {}
        for attr, value in cls.__dict__.items():
            if isinstance(value, (int, float)):
                orig_attrs[attr] = value
                addthem[f"{attr}2"] = value * 2
                addthem[f"{attr}12"] = value / 2
            elif isinstance(value, type):
                # for our repr, also print subnamespaces
                orig_attrs[attr] = value
        
        for key, value in addthem.items():
            setattr(cls, key, value)
        
        setattr(cls, "_orig_attrs", orig_attrs)
        
        return cls

    def __getattr__(cls, name: str) -> Any:
        # Allow arbitrary class attribute access
        return None  # or raise AttributeError if you prefer

    def __repr__(cls) -> str:
        s = f"* Class '{cls.__name__}'\n"
        for key, value in cls._orig_attrs.items():
            value_str = str(value)
            if "\n" in value_str:  # we assume this means that `value` is also a MultAttrNamespace
                for line in value_str.splitlines():
                    s += f"{cls._INDENT}{line}\n"
            else:
                s += f"{cls._INDENT}{key}: {value_str}\n"
        return s


class MultAttrNamespace(metaclass=MultAttrNamespaceMeta):
    pass


def save_as_scad(d, stem: str, path: Path = Path("./out")):
    d.save_as_scad((path / Path(stem).name).with_suffix(".scad"))


# Create new color object every time, else recursionerror
@define
class _c:
    alpha: float = 1
    @property
    def red(self):
        return bosl.hsv(h=0, s=0.33, v=1, a=self.alpha)
    @property
    def green(self):
        return bosl.hsv(h=120, s=0.33, v=1, a=self.alpha)
    @property
    def blue(self):
        return bosl.hsv(h=240, s=0.33, v=1, a=self.alpha)
c = _c()
c2 = _c(alpha=.75)
c3 = _c(alpha=.5)
c4 = _c(alpha=.25)
c5 = _c(alpha=.1)
