__author__ = ['Djakim Latumalea']
__copyright__ = ['Djakim Latumalea', 'Azadeh Pirzadeh', 'Peter Riesebos', 'Kai Lin', 'Hossain Shahadat']
__license__ = 'Apache 2.0'
__version__ = '0.1'

from pathlib import Path

import panel as pn

from model.abstract import Page

intro_path = Path(Path(__file__).parent, 'introduction.md')
intro = intro_path.read_text(encoding='utf8')

hyp_path = Path(Path(__file__).parent, 'hypothesis.md')
hyp = hyp_path.read_text(encoding='utf8')


class IntroPage(Page):

    def __init__(self):
        self.pane = pn.pane.Markdown(intro)
        self.button = pn.widgets.Button(name='Introduction')

    def get_contents(self):
        return self.pane, self.button


class HypothesisPage(Page):

    def __init__(self):
        self.pane = pn.pane.Markdown(hyp)
        self.button = pn.widgets.Button(name='Hypothesis')

    def get_contents(self):
        return self.pane, self.button
