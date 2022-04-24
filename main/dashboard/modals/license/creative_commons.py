"""Module that contains the license of the project."""

__author__ = 'Djakim Latumalea'
__copyright__ = ['Djakim Latumalea', 'Azadeh Pirzadeh', 'Peter Riesebos', 'Kai Lin', 'Hossain Shahadat']
__license__ = 'Apache 2.0'
__version__ = '0.1'

from pathlib import Path
from model.abstract import Page

import panel as pn

path = Path(Path(__file__).parent, 'creative_commons.md')
file = path.read_text(encoding='utf8')


class CreativeCommons(Page):

    def __init__(self):
        self.modal = pn.pane.Markdown(file, style={'color': 'white'})
        self.button = pn.widgets.Button(name='License')

    def get_contents(self):
        return self.modal, self.button
