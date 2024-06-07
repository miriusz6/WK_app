import flet as ft
import re


class TextHighlightable(ft.Text):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.highlight_style = ft.TextStyle(bgcolor="yellow")
        self.default_style = self.style
        self._value = self.value


    def highlight_all(self):
        self.spans = []
        self.value = self._value
        self.style = self.highlight_style

    def unhighlight_all(self):
        self.spans = []
        self.value = self._value
        self.style = self.default_style

    def highlight(self, fraze:str, case_sensitive=False):
        txt = self.value
        self.spans = []
        # [m.start() for m in re.finditer('test', 'test test test test')]
        fraze = re.escape(fraze)
        if case_sensitive:
            occurrences = [(m.start(), m.end()) for m in re.finditer(fraze, txt)]
        else:
            occurrences = [(m.start(), m.end()) for m in re.finditer(fraze.lower(), txt.lower())]
        last_indx = 0
        for start, end in occurrences:
            if start - last_indx > 0:
                self.spans.append(ft.TextSpan(text=txt[last_indx:start],
                                              style=self.default_style))
            self.spans.append(ft.TextSpan(text=txt[start:end],
                                          style=self.highlight_style))
            last_indx = end
        if len(txt) - last_indx > 0 :
            self.spans.append(ft.TextSpan(text=txt[last_indx:],
                                          style=self.default_style))
        self.value = ""



    def set_value(self):
        self.value = self._value





