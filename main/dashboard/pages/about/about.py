""" Module that contains the About-us page."""

__author__ = 'Djakim Latumalea'
__copyright__ = ['Djakim Latumalea', 'Azadeh Pirzadeh', 'Peter Riesebos', 'Kai Lin', 'Hossain Shahadat']
__license__ = 'Apache 2.0'
__version__ = '0.1'

from pathlib import Path

import panel as pn
from model.abstract import Page

about_path = Path(Path(__file__).parent, 'about.md')
about = about_path.read_text(encoding='utf8')

logo = Path(Path(__file__).parent, 'masks.jpg')


class AboutPage(Page):

    def __init__(self):
        self.pane = pn.Row(pn.pane.JPG(logo, width=300, height=300), pn.pane.markup.Markdown(about))
        self.button = pn.widgets.Button(name='About')

    def get_contents(self):
        return self.pane, self.button
