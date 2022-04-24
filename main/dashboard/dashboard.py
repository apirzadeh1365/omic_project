"""This module provides a Dashboard class, which can be used to instantiate a Dashboard.
It expects to be given panes, such that it used the panes to attach to the Dashboard.

Djakim Latumalea:
- Created Dashboard
"""

__author__ = 'Djakim Latumalea'
__copyright__ = ['Djakim Latumalea', 'Azadeh Pirzadeh', 'Peter Riesebos', 'Kai Lin', 'Hossain Shahadat']
__license__ = 'Apache 2.0'
__version__ = '0.1'

import panel as pn

pn.extension('plotly', loading_spinner='dots', sizing_mode='stretch_width')


class Dashboard:
    """ Returns an interactive dashboard for data visualization.

    Keyword arguments:
        title -- the title of the dashboard.
        panes -- a dictionary of panel panes and identifiers.
        btns -- a dictionary of panel buttons and identifiers.
        home_pane -- the key of the pane that is shown by default.
    """

    def __init__(self, title: str, panes: dict, modal: dict, btns: dict, home_pane: str) -> None:
        if home_pane not in panes:
            raise ValueError('Home pane must be in panes.')
        if len(panes) < 1:
            raise ValueError('Expects at least one pane.')
        if len(modal) > 1:
            raise ValueError('Only 1 modal is allowed.')

        # accent_base_color='#xxxxxx' changes the accent, default is pink
        self.base = pn.template.FastListTemplate(title=title,
                                                 accent_base_color='#66ffff',
                                                 theme='dark',
                                                 logo='dashboard/assets/img/logo_solo.png')
        self.panes = panes
        self.btns = btns
        self.modals = modal

        # create a row and append it to the main panel of the template
        self.row = pn.Row(self.panes[home_pane])
        self.base.main.append(
            pn.Column(
                self.row
            )
        )

        # assign callbacks to the buttons and append them to the sidebar
        if len(self.btns) > 0:
            for k in self.btns.keys():
                self.btns[k].on_click(self.get_callback(k))

            self.base.sidebar.extend([btn for btn in self.btns.values()])

        if len(self.modals) > 0:
            self.base.modal.extend([modal for modal in self.modals.values()])

    def get_callback(self, key):
        """Callbacks that can alter the dashboard."""

        def change_pane(event):
            self.row[0] = self.panes[key]

        def open_modal(event):
            self.base.open_modal()

        collection = {
            'welcome': change_pane,
            'about': change_pane,
            'introduction': change_pane,
            'definition': change_pane,
            'contribution': change_pane,
            'hypothesis': change_pane,
            'design': change_pane,
            'conclusion': change_pane,
            'paper': change_pane,
            'biome': change_pane,
            'spo2': change_pane,
            'alpha_diversity': change_pane,
            'acnes': change_pane,
            'spots': change_pane,
            'cc': open_modal
        }

        return collection[key]

    def serve(self, port):
        self.base.show(port=port)


