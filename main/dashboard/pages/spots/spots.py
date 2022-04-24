"""This module contains the page that counts the amount of acne spots.

Hossain Shahadat:
- Created graph

Kai Lin:
- Added tooltips
- Added statistical test

Djakim Latumalea:
- Created overall structure
"""

__author__ = ['Hossain Shahadat', 'Kai Lin', 'Djakim Latumalea']
__copyright__ = ['Djakim Latumalea', 'Azadeh Pirzadeh', 'Peter Riesebos', 'Kai Lin', 'Hossain Shahadat']
__license__ = 'Apache 2.0'
__version__ = '0.1'


import panel as pn
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import DatetimeTickFormatter, HoverTool
from bokeh.models.widgets import Tabs, Panel

from model import get_column
from model.abstract import Page


# create a dataframe of subjects using model:
def create_df(subject_number):
    df = pd.DataFrame(get_column(subject_number, ['date', 'masktype', 'acne']))
    df['date'] = pd.to_datetime(df['date'])
    return df


def get_average_acne_number(choose_type="baseline"):
    """
    to get average of acne number for each subject.
    choose_type: str, "baseline" or "intervention" to return average of acne number for each subject.
    return:list, average of acne number for each subject
    """
    df_subj_1 = create_df(subject_number=1)['acne']
    df_subj_2 = create_df(subject_number=2)['acne']
    df_subj_3 = create_df(subject_number=3)['acne']
    df_subj_4 = create_df(subject_number=4)['acne']
    df_subj_5 = create_df(subject_number=5)['acne']
    df_subj_list = [df_subj_1,df_subj_2,df_subj_3,df_subj_4,df_subj_5]
    get_average_list =[]
    for i in range (5):
        if choose_type == "intervention":
            get_average_list.append(df_subj_list[i][:8].sum()/ len(df_subj_list[i][:8]))
        elif choose_type == "baseline":
            get_average_list.append(df_subj_list[i][8:].sum()/ len(df_subj_list[i][8:]))
    return get_average_list

def statistics_output():
    """
    H0 = "There is no significant more amount of spots"
    H1 = "There is significant more amount of spots"
    """
    from scipy.stats import ttest_rel
    a = get_average_acne_number("intervention")
    b = get_average_acne_number("baseline")
    _,p_value = ttest_rel(a,b,alternative= "greater")
    return p_value


def acne_plot(df, subject_number):

    # dividing the data frame according to masktype
    df_surgical = df[df['masktype'] == 'surgical']
    df_none = df[df['masktype'] == 'None']

                
    plot = figure(x_axis_type='datetime', x_axis_label="Date", y_axis_label="Acne number", plot_height=600,
                  plot_width=600, toolbar_location=None, y_range=(0, 10))
    plot.xaxis.major_label_orientation = "vertical"
    plot.xaxis.formatter = DatetimeTickFormatter(days=["%Y-%m-%d"], months=["%Y-%m-%d"], years=["%Y-%m-%d"])
    plot.title.text = 'Acne Count of Subject ' + subject_number

    plot.line(x=df_surgical['date'], y=df_surgical['acne'], line_width=5, color='red', legend_label='Surgical Mask')
    plot.line(x=df_none['date'], y=df_none['acne'], line_width=5, color='blue', legend_label='No Mask')
    plot.circle(x=df_surgical.date, y=df_surgical['acne'], fill_color="green", size=8)
    plot.circle(x=df_none.date, y=df_none['acne'], fill_color="orange", size=8)
    plot.xgrid.grid_line_color = None
    plot.y_range.start = 0

    subject1 = Panel(child=plot)
    subject2 = Panel(child=plot)
    subject3 = Panel(child=plot)
    subject4 = Panel(child=plot)
    subject5 = Panel(child=plot)
    tabs = Tabs(tabs=[subject1, subject2, subject3, subject4, subject5])
    return (tabs)


def get_plot():
    plot_1 = acne_plot(df=create_df(subject_number=1), subject_number='1')
    plot_2 = acne_plot(df=create_df(subject_number=2), subject_number='2')
    plot_3 = acne_plot(df=create_df(subject_number=3), subject_number='3')
    plot_4 = acne_plot(df=create_df(subject_number=4), subject_number='4')
    plot_5 = acne_plot(df=create_df(subject_number=5), subject_number='5')

    tab_subj_1 = Panel(child=plot_1, title="subject 1")
    tab_subj_2 = Panel(child=plot_2, title="subject 2")
    tab_subj_3 = Panel(child=plot_3, title="subject 3")
    tab_subj_4 = Panel(child=plot_4, title="subject 4")
    tab_subj_5 = Panel(child=plot_5, title="subject 5")

    tabs = Tabs(tabs=[tab_subj_1, tab_subj_2, tab_subj_3, tab_subj_4, tab_subj_5])
    description = get_description()
    statistics_result = statistics_output()

    statistics = pn.pane.Markdown("We use paired t-test. We reject alternative hypothesis because the p-value = {:.2f} is > 0.05. \n\nConclusion: There is no significant more amount of spots between wearing and without mask.".format(statistics_result))

    return pn.Row(pn.Column(description,statistics), tabs)


def get_description():
    description = pn.pane.Markdown("""
    #Spot 
    Here we show the change in the amount of spots during the whole experiment.
    
    Research question: are the number of spots significantly higher when wearing a KN95 mask than not wearing a mask?
        
    H0 = The amount of spots is not significantly higher when wearing a KN95 mask.
    
    H1 = The amount of spots is significantly higher when wearing a KN95 mask.
    """)

    return description


class SpotsPage(Page):

    def __init__(self):
        self.pane = get_plot()
        self.button = pn.widgets.Button(name='Spots')

    def get_contents(self):
        return self.pane, self.button

if __name__ == '__main__':
    df = create_df(5)
    print(df)