""" Module that contains the About-us page."""

__author__ = 'Djakim Latumalea'
__copyright__ = ['Djakim Latumalea', 'Azadeh Pirzadeh', 'Peter Riesebos', 'Kai Lin', 'Hossain Shahadat']
__license__ = 'Apache 2.0'
__version__ = '0.1'

from pathlib import Path

import panel as pn
from model.abstract import Page

md_file = Path(Path(__file__).parent, 'welcome.md')
md = md_file.read_text(encoding='utf8')

picture = Path(Path(__file__).parent, 'facemask_wearer.jpg')


class WelcomePage(Page):

    def __init__(self):
        self.pane = pn.Column(pn.pane.markup.Markdown(md), pn.Column(pn.pane.JPG(picture, height=500),
                                                                  pn.pane.Markdown('Photo by <a href="https://unsplash.com/@aminmoshrefi?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Amin Moshrefi</a> on <a href="https://unsplash.com/s/photos/corona?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>')))
        self.button = pn.widgets.Button(name='Welcome')

    def get_contents(self):
        return self.pane, self.button
