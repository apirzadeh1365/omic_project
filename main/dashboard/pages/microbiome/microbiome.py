"""This module shows the microbiome page.

Kai Lin:
- Wrote the code of the plots

Djakim Latumalea
- Reformatted some parts
"""

__author__ = '[Kai Lin', 'Djakim Latumalea]'
__copyright__ = ['Djakim Latumalea', 'Azadeh Pirzadeh', 'Peter Riesebos', 'Kai Lin', 'Hossain Shahadat']
__license__ = 'Apache 2.0'
__version__ = '0.1'

import json
from pathlib import Path

import panel as pn
import pandas as pd
from bokeh.plotting import figure
from model import get_dataset
from bokeh.models.widgets import Tabs, Panel
from bokeh.models import Legend

from model.abstract import Page

color_map_path = Path(Path(__file__).parent, 'color_map.json')
swabbing_setup_path = Path(Path(__file__).parent, 'swabbing_setup.png')


def get_species(choosetype="baseline", choosesubject=6):
    """
    to get species data.
    if choosetype = str, intervention return intervention species; baseline return baseline species
       choosesubject: int, for choosing subject you want. 6 for all subject.
    """

    get_data = get_dataset(choosetype)
    barcode_list = ['barcode01', 'barcode02', 'barcode03', 'barcode04', 'barcode05']
    if choosesubject == 6:
        get_data = get_data[(get_data.barcode == 'barcode01') | (get_data.barcode == 'barcode02')
                            | (get_data.barcode == 'barcode03') | (get_data.barcode == 'barcode04')
                            | (get_data.barcode == 'barcode05')]
    elif choosesubject < 6:
        get_data = get_data[(get_data.barcode == barcode_list[choosesubject - 1])]
    species_data = get_data.species.value_counts(normalize=True)
    return species_data


def choose_seq_df(get_top=5, choosesubject=1, choosetype="baseline",
                  subject_list=['Subject 1', 'Subject 2', 'Subject 3', 'Subject 4', 'Subject 5', "Total"]):
    """
    to get species sequence df.
    get_top : int, to choose how many species you want to show
    choosetype : str, intervention return intervention species , baseline return baseline species
    choosesubject: int, for choosing subject you want. 6 for all subject.
    return df
    """
    species_data = get_species(choosetype, choosesubject)
    species = species_data.index[:get_top].tolist() + ["other"]
    sizes = species_data.values[:get_top].round(decimals=2).tolist() + [
        (1 - sum(species_data.values[:get_top].round(decimals=2)))]
    sizes = [element * 100 for element in sizes]
    data = {subject_list[choosesubject - 1] + " " + choosetype: sizes}
    df = pd.DataFrame(data)
    df.index = species
    return df


def compare_seq_df(get_top=5, choosesubject=1):
    """
    to get comparism species sequence df (baseline and intervention).
    get_top : int, to choose how many species you want to show
    choosesubject: int, for choosing subject you want. 6 for all subject.
    return df
    """
    frames = []
    baseline_df = choose_seq_df(get_top, choosesubject, choosetype="baseline", )
    intervention_df = choose_seq_df(get_top, choosesubject, choosetype="intervention", )
    frames.append(baseline_df)
    frames.append(intervention_df)
    result = pd.concat(frames, axis=1).fillna(0)
    return result.sort_index()


def get_hex_color():
    """
    for setting the color of the bar
    """
    import random
    r = lambda: random.randint(0, 255)
    return ('#%02X%02X%02X' % (r(), r(), r()))


def load_color_map():
    with open(color_map_path) as json_data:
        data = json.load(json_data)

    return data


def make_compare_bar_chart(get_top=5, choosesubject=1,
                           subject_list=['Subject 1', 'Subject 2', 'Subject 3', 'Subject 4', 'Subject 5', "Total"]):
    """
    to make a compare bar chart.
    get_top : int, to choose how many species you want to show
    choosesubject: int, for choosing subject you want. 6 for all subject.
    return graph object. please put it into show
    """
    # load colors
    color_map = load_color_map()

    df = compare_seq_df(get_top, choosesubject)
    sample = df.columns.tolist()
    species = df.index.tolist()
    data = {'sample': sample}

    for i in range(len(species)):
        data[species[i]] = df.iloc[i].tolist()

    colors = [color_map[bact] for bact in species]

    p = figure(x_range=sample, height=450, width=800,
               title='{} microbiome species'.format(subject_list[choosesubject - 1]),
               y_axis_label="Relative abundance (% of total sequence reads)",
               toolbar_location=None, tools='hover', tooltips="$name :@$name %")
    v = p.vbar_stack(species, x='sample', width=0.9, color=colors, source=data, )
    legend = Legend(items=[(b.name, [b]) for b in v], location='center')
    p.add_layout(legend, 'right')
    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    return p


def get_plot():
    get_top = 10
    plot_1 = make_compare_bar_chart(get_top, choosesubject=1)
    plot_2 = make_compare_bar_chart(get_top, choosesubject=2)
    plot_3 = make_compare_bar_chart(get_top, choosesubject=3)
    plot_4 = make_compare_bar_chart(get_top, choosesubject=4)
    plot_5 = make_compare_bar_chart(get_top, choosesubject=5)
    plot_6 = make_compare_bar_chart(get_top, choosesubject=6)

    # tab_png = Panel(child=swabbing_png, title='Swabbing Setup')
    tab_subj1 = Panel(child=plot_1, title="Subject 1")
    tab_subj2 = Panel(child=plot_2, title="Subject 2")
    tab_subj3 = Panel(child=plot_3, title="Subject 3")
    tab_subj4 = Panel(child=plot_4, title="Subject 4")
    tab_subj5 = Panel(child=plot_5, title="Subject 5")
    tab_subj6 = Panel(child=plot_6, title="Total")

    tabs = Tabs(tabs=[tab_subj1, tab_subj2, tab_subj3, tab_subj4, tab_subj5, tab_subj6])

    description = get_description()
    heading = get_heading()
    image = get_img()

    return pn.Row(pn.Column(heading, image, description), tabs)


def get_img():
    swabbing_png = pn.pane.PNG(swabbing_setup_path)
    return swabbing_png


def get_heading():
    return pn.pane.Markdown("""#Microbiome""")


def get_description():
    description = pn.pane.Markdown("""
    This page shows the change in the composition of the subjects' microbiome:
    
    Subject 1 = The percentage of *Staphylococcus saccharolyticus* changed a lot, from 27% to 1%.
    This shows a big difference between the baseline and the intervention. The percentage of *Cutibacterium acnes* changed from 32% to 19%.
    
    Subject 2 = The percentage of *Staphylococcus saccharolyticus* decreased from 17% to not being of any significance.
    The change in the *Staphylococcus capitis* is from not being of any significance to 41%, and the percentage of *Staphylococcus epidermidis* has increased five fold after the experiment.
    
    Subject 3 = The percentage of *Cutibacterium acnes* has decreased five fold, from 26% to 5%,
    the percentage of *Staphylococcus capitis* has increased from almost 0% to 58% and *Staphylococcus saccharolyticus* has decreased 10 fold after the experiment.
    
    Subject 4 = The percentage of *Cutibacterium acnes* has increased from 38% to 60%. Taking up the greater part of the whole microbiome. The percentage for *Staphylococcus saccharolyticus* decreased from 19% to almost 0%.
    Subject 4 is the only subject who had an increase in the percentage of *Cutibacterium acnes*. It is one of the bacteria that can cause acne. This appears to be one of the reasons subject 4 had an increase in acne after the experiment.
    
    Subject 5 = *Staphylococcus saccharolyticus* decreased from 45% to being of no significance. The change in *Staphylococcus capitis* is from 1% to 41%.
    
    All = The percentage of *Staphylococcus saccharolyticus* decreased while the *Staphylococcus capitis* increased.
    *S. saccharolyticus* can grow under oxic conditions, and, in particular, in a CO2-rich atmosphere.[1]
    
    References:
    
    1. *Staphylococcus saccharolyticus*: An Overlooked Human Skin Colonizer.(Ahle er al.,2020)
    """)

    return description


class MicrobiomePage(Page):

    def __init__(self):
        self.pane = get_plot()
        self.button = pn.widgets.Button(name='Microbiome')

    def get_contents(self):
        return self.pane, self.button


if __name__ == '__main__':
    print(compare_seq_df())
