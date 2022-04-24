"""
This module contains the page that shows the comparison of Cutibacterium Acnes between the dataset.

Azadeh Pirzadeh:
- Created all plots.

Djakim Latumalea:
- Formatting such as rearranging plots.
"""

__author__ = ['Azadeh Pirzadeh', 'Djakim Latumalea']
__copyright__ = ['Djakim Latumalea', 'Azadeh Pirzadeh', 'Peter Riesebos', 'Kai Lin', 'Hossain Shahadat']
__license__ = 'Apache 2.0'
__version__ = '0.1'

import panel as pn
from model import get_column_barcodes_intervention, get_column_barcodes_baseline
from model.abstract import Page

from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.models import NumeralTickFormatter, HoverTool


def find_acne_count(barcode_number, period):
    if period not in ['baseline', 'intervention']:
        raise ValueError('Expects period ot be one of "baseline", "intervention".')

    if period == 'baseline':
        df = get_column_barcodes_baseline(barcode_number, column=['species'])
    else:
        df = get_column_barcodes_intervention(barcode_number, column=['species'])

    acne = df.loc[(df['species'] == 'Cutibacterium acnes')].count()[0]
    n_rows = len(df)

    return acne / n_rows


def get_plot():
    subjects = ['subject1', 'subject2', 'subject3', 'subject4', 'subject5']
    months = ['surgical Mask', 'No Mask']

    acne_base_1 = find_acne_count(1, period='baseline')
    acne_base_2 = find_acne_count(2, period='baseline')
    acne_base_3 = find_acne_count(3, period='baseline')
    acne_base_4 = find_acne_count(4, period='baseline')
    acne_base_5 = find_acne_count(5, period='baseline')

    acne_mask_1 = find_acne_count(1, period='intervention')
    acne_mask_2 = find_acne_count(2, period='intervention')
    acne_mask_3 = find_acne_count(3, period='intervention')
    acne_mask_4 = find_acne_count(4, period='intervention')
    acne_mask_5 = find_acne_count(5, period='intervention')

    sub = {'subject': subjects, 'No Mask': [acne_base_1, acne_base_2, acne_base_3, acne_base_4, acne_base_5],
           'surgical Mask': [acne_mask_1, acne_mask_2, acne_mask_3, acne_mask_4, acne_mask_5]
           }

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,hover"

    p = figure(x_range=subjects, y_range=[0, 1], tools=TOOLS, width=600, height=600, tooltips='@sub' )
    p.vbar(x=dodge('subject', -0.1, range=p.x_range), name='No Mask', top='No Mask', width=0.2, source=sub, color="orange",
           legend_label='No Mask')
    p.vbar(x=dodge('subject', 0.1, range=p.x_range), name='surgical Mask', top='surgical Mask', width=0.2, source=sub, color="blue",
           legend_label='Surgical mask')

    hover = HoverTool()
    hover.tooltips = """
      <div>

      <div><strong>subject: </strong>@subject</div>
      <div><strong>value: <strong> @{No Mask}{%0.2f}.No Mask</div>    
      <div><strong>value: <strong> @{surgical Mask}{%0.2f}.surgical Mask</div>    

      </div>
      """

    p.add_tools(hover)

    m0 = pn.pane.Markdown("""
    #Cutibacterium Acnes
    
    Here we describe the change in the amount of *Cutibacterium Acnes* between the baseline and the experiment.
    """)
    m1 = pn.pane.Markdown("""
    As you can see, the percentage of the *Cutibacterium Acnes* decreased after using a surgical mask. 
    An exception to the rule is subject 4.
    
    The amount **decreased** by **12.33%** for subject 1.<br>
    The amount **decreased** by **5.45%** for subject 2.<br>
    The amount **decreased** by **20.23%** for subject 3.<br>
    The amount **increased** by **21.75%** for subject 4.<br>
    The amount **decreased** by **5.05%** for subject 5.
    
    We do not know the exact reason why the amount of *Cutibacterium Acnes* increased for subject 4.
    It could be due to:
    <ul>
    <li>The type of skin.</li>
    </ul>
    """)

    t = pn.Column(m0, m1)

    p.title = 'Cutibacterium acnes'
    p.xgrid[0].grid_line_color = None
    p.ygrid[0].grid_line_alpha = 0.5
    p.xaxis.axis_label = 'Subject_number'
    p.yaxis.axis_label = 'Percentage of Cutibacterium acnes'
    p.yaxis.formatter = NumeralTickFormatter(format='0 %')

    return pn.Row(t, p)


class AcnesPage(Page):

    def __init__(self):
        self.pane = get_plot()
        self.button = pn.widgets.Button(name='Acnes')

    def get_contents(self):
        return self.pane, self.button
