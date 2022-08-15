from .selector import Selector
from .units import Unit, pt


class Style:
    def __init__(self, *class_name: str, id: str = None, selector=None) -> None:
        if selector is not None:
            self._selector = selector
        else:
            self._selector = Selector(id, *class_name)

        self._rules = {}

    def rule(self, attr: str, value) -> "Style":
        self._rules[attr] = value
        return self

    def font(self, size: Unit = None, weight: str = None) -> "Style":
        if size:
            if not isinstance(size, Unit):
                size = pt(size)

            self.rule("font-size", size)

        if weight:
            self.rule("font-weight", weight)

        return self

    def display(self, display: str) -> "Style":
        self.rule("display", display)
        return self

    def apply(self, other: "Style") -> "Style":
        for attr, value in other._rules.items():
            self.rule(attr, value)

        return self

    def css(self) -> str:
        rules = "\n".join(
            f"    {attr}: {value};" for attr, value in self._rules.items()
        )

        return f"{self._selector.css()} {{\n{rules}\n}}"

    def inline(self) -> str:
        rules = " ".join(f"{attr}: {value};" for attr, value in self._rules.items())
        return f'style="{rules}"'