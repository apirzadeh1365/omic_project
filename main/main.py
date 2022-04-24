#!/usr/bin/env python
""" Main module creates a Dashboard and populates it with panes and buttons for visualization purposes.

Djakim Latumalea:
- Created main.py and corresponding logic.
- Created all __init__ files.
- Created architecture of the application.
"""

__author__ = 'Djakim Latumalea'
__copyright__ = ['Djakim Latumalea', 'Azadeh Pirzadeh', 'Peter Riesebos', 'Kai Lin', 'Hossain Shahadat']
__license__ = 'Apache 2.0'
__version__ = '0.1'

from dashboard import Dashboard
from dashboard.pages import PaperPage, AboutPage, MicrobiomePage, SpO2Page, \
    AlphaDiversityPage, AcnesPage, SpotsPage, IntroPage, ConclusionPage, WelcomePage, \
    DefinitionsPage, HypothesisPage, ContributionPage, StudyDesignPage
from dashboard.modals import CreativeCommons

# pages
about_page = AboutPage()
paper_page = PaperPage()
biome_page = MicrobiomePage()
spo2_page = SpO2Page()
alpha_diversity_page = AlphaDiversityPage()
acnes_page = AcnesPage()
spots_page = SpotsPage()
intro_page = IntroPage()
concl_page = ConclusionPage()
welcome_page = WelcomePage()
definition_page = DefinitionsPage()
hyp_page = HypothesisPage()
contr_page = ContributionPage()
design_page = StudyDesignPage()

# modal
cc = CreativeCommons()

# page panes and buttons
about_pane, about_btn = about_page.get_contents()
paper_pane, paper_btn = paper_page.get_contents()
biome_pane, biome_btn = biome_page.get_contents()
spo2_pane, spo2_btn = spo2_page.get_contents()
alpha_diversity_pane, alpha_diversity_btn = alpha_diversity_page.get_contents()
acnes_pane, acnes_btn = acnes_page.get_contents()
spots_pane, spots_btn = spots_page.get_contents()
intro_pane, intro_btn = intro_page.get_contents()
concl_pane, concl_btn = concl_page.get_contents()
welcome_pane, welcome_btn = welcome_page.get_contents()
definition_pane, definition_btn = definition_page.get_contents()
hyp_pane, hyp_btn = hyp_page.get_contents()
contr_pane, contr_btn = contr_page.get_contents()
design_pane, design_btn = design_page.get_contents()

# modal and button
cc_modal, cc_btn = cc.get_contents()

panes = {
    'welcome': welcome_pane,
    'introduction': intro_pane,
    'definition': definition_pane,
    'paper': paper_pane,
    'about': about_pane,
    'contribution': contr_pane,
    'design': design_pane,
    'hypothesis': hyp_pane,
    'biome': biome_pane,
    'spo2': spo2_pane,
    'alpha_diversity': alpha_diversity_pane,
    'acnes': acnes_pane,
    'spots': spots_pane,
    'conclusion': concl_pane
}

modals = {
    'cc': cc_modal
}

btns = {
    'welcome': welcome_btn,
    'about': about_btn,
    'introduction': intro_btn,
    'definition': definition_btn,
    'contribution': contr_btn,
    'design': design_btn,
    'hypothesis': hyp_btn,
    'spo2': spo2_btn,
    'biome': biome_btn,
    'alpha_diversity': alpha_diversity_btn,
    'acnes': acnes_btn,
    'spots': spots_btn,
    'conclusion': concl_btn,
    'paper': paper_btn,
    'cc': cc_btn,
}


if __name__ == '__main__':
    dashboard = Dashboard(title='SIGMA', panes=panes, modal=modals, btns=btns, home_pane='welcome')
    dashboard.serve(50046)



