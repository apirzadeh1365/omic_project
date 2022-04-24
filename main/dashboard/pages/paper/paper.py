""" This module contains the page that shows the research paper.

"""

__author__ = 'Djakim Latumalea'
__copyright__ = ['Djakim Latumalea', 'Azadeh Pirzadeh', 'Peter Riesebos', 'Kai Lin', 'Hossain Shahadat']
__license__ = 'Apache 2.0'
__version__ = '0.1'


from pathlib import Path

import panel as pn

from model.abstract import Page

about_path = Path(Path(__file__).parent, 'paper.md')
about = about_path.read_text(encoding='utf8')


class PaperPage(Page):

    def __init__(self):
        self.pane = pn.pane.Markdown(about)
        self.button = pn.widgets.Button(name='Paper')

    def get_contents(self):
        return self.pane, self.button
