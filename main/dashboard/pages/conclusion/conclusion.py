__author__ = ['Djakim Latumalea']
__copyright__ = ['Djakim Latumalea', 'Azadeh Pirzadeh', 'Peter Riesebos', 'Kai Lin', 'Hossain Shahadat']
__license__ = 'Apache 2.0'
__version__ = '0.1'


from pathlib import Path

import panel as pn

from model.abstract import Page

file_path = Path(Path(__file__).parent, 'conclusion.md')
file = file_path.read_text(encoding='utf8')


class ConclusionPage(Page):

    def __init__(self):
        self.pane = pn.pane.Markdown(file)
        self.button = pn.widgets.Button(name='Conclusion')

    def get_contents(self):
        return self.pane, self.button
