import io
import datetime
from pathlib import Path

from .style import Style


class StyleSheet:
    def __init__(self, *styles: Style) -> None:
        self._styles = list(styles)
        self._by_class = {}
        self._used = set()

    def render(self, dynamic: bool = False, fp=None):
        if isinstance(fp, (str, Path)):
            fp = open(fp, "wt")

        if fp is None:
            fp = io.StringIO()

        fp.write("/* Made with violetear */\n")
        fp.write(f"/* Autogenerated on {datetime.datetime.now()} */\n\n")

        for style in self._styles:
            style.render(dynamic=dynamic, fp=fp, indent=0, used=self._used)
            fp.write("\n\n")

        if isinstance(fp, io.StringIO):
            result = fp.getvalue()
        else:
            result = None

        fp.close()
        return result

    def style(self, *class_name: str) -> Style:
        if not class_name:
            class_name = tuple([f"_c{len(self._styles)}"])

        style = Style(*class_name)
        self._styles.append(style)
        self._by_class[class_name] = style
        return style

    def media(self, min_width: int = None, max_width: int = None) -> "MediaSet":
        media = MediaSet(self, min_width=min_width, max_width=max_width)
        self._styles.append(media)
        return media

    def redefine(self, style: Style) -> Style:
        style = Style(selector=style._selector, parent=style)
        self._styles.append(style)
        return style

    def __getitem__(self, key) -> Style:
        class_name = tuple(key.split("__"))
        style = self._by_class[class_name]
        self._used.add(style)
        return style


class MediaSet(StyleSheet):
    def __init__(
        self, sheet: StyleSheet, min_width: int = None, max_width: int = None
    ) -> None:
        super().__init__()

        self._min_width = min_width
        self._max_width = max_width
        self._sheet = sheet

    def render(self, dynamic: bool = False, fp=None, indent: int = 0, used=None):
        query = []

        if self._min_width:
            query.append(f"min-width: {self._min_width}px")

        if self._max_width:
            query.append(f"max-width: {self._max_width}px")

        fp.write(f"@media({', '.join(query)})")
        fp.write("{\n")

        for style in self._styles:
            style.render(dynamic=dynamic, fp=fp, indent=indent + 1, used=used)
            fp.write("\n\n")

        fp.write("}\n")
