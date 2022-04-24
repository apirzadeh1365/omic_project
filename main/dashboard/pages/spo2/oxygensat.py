"""
This module contains the page that shows the oxygen saturation (SpO2) levels.

Azadeh Pirzadeh:
- Created spo2 plot

Djakim Latumalea:
- Created general structure
- Implemented spo2 plot
- Refactored whole spo2 plot in several functions
"""



import pandas as pd
import panel as pn
import numpy as np
from bokeh.models import DatetimeTickFormatter, NumeralTickFormatter, HoverTool
from bokeh.models.widgets import Tabs, Panel
from bokeh.plotting import figure
from bokeh.transform import dodge

from scipy.stats import ttest_ind
from scipy.stats import norm

from model import get_column
from model.abstract import Page


def create_df(subject_number: int) -> pd.DataFrame:
    """Returns a dataframe from the data of the given subject.

    It also adds the mean of the measurements that are taken concerning the SpO2 levels.
    """
    df = pd.DataFrame(get_column(subject_number,
                                 ['date', 'masktype', 'spo2_m1_r', 'spo2_m1_l', 'spo2_m2_r',
                                  'spo2_m2_l', 'spo2_m3_r', 'spo2_m3_l']))
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')

    # if masktype medical change it to surgical
    def mask(x):
        if x == 'Medical':
            return 'surgical'

        return x

    df['masktype'] = df['masktype'].apply(mask)

    # round to two decimals
    df['spo2_m1_r'] = df['spo2_m1_r'].round(decimals=2)
    df['spo2_m1_l'] = df['spo2_m1_l'].round(decimals=2)
    df['spo2_m2_r'] = df['spo2_m2_r'].round(decimals=2)
    df['spo2_m2_l'] = df['spo2_m2_l'].round(decimals=2)
    df['spo2_m3_r'] = df['spo2_m3_r'].round(decimals=2)
    df['spo2_m3_l'] = df['spo2_m3_l'].round(decimals=2)

    # get the mean of spo2 moment 1, 2 and 3 (left and right) of the subject
    df['spo2_m1_mean'] = np.mean([df['spo2_m1_r'], df['spo2_m1_l']], axis=0)
    df['spo2_m2_mean'] = np.mean([df['spo2_m2_r'], df['spo2_m2_l']], axis=0)
    df['spo2_m3_mean'] = np.mean([df['spo2_m3_r'], df['spo2_m3_l']], axis=0)

    # get the mean of all moment 1, 2 and 3 in total
    df['mean'] = np.mean([df['spo2_m1_mean'], df['spo2_m2_mean'], df['spo2_m3_mean']], axis=0)

    # get the mean of the right hand and the left hand
    df['spo2_r_mean'] = np.mean([df['spo2_m1_r'], df['spo2_m2_r'], df['spo2_m3_r']], axis=0)
    df['spo2_l_mean'] = np.mean([df['spo2_m1_l'], df['spo2_m2_l'], df['spo2_m3_l']], axis=0)

    return df


def generate_plot(df, subject_number):
    """Returns a plot with a graph of the SpO2 values and tests the hypothesis.
    """
    xlabel = 'Date'
    ylabel = 'SpO2 average of right and left hand'
    legend_label = 'Click on legend entries to hide the correspnding lines'

    # Divide the DataFrame into a DataFrame containing data from the surgical mask and one containing data without wearing a mask.
    df_surgical = df[df['masktype'] != 'None']
    df_none = df[df['masktype'] == 'None']

    # create a plot for surgical mask data
    fig_s = child_plot(df_surgical, subject_number, xlabel, ylabel, legend_label)

    # create a plot for no-mask data
    fig_n = child_plot(df_none, subject_number, xlabel, ylabel, legend_label)

    # Add the plots to tabs
    children = [fig_s, fig_n]
    titles = ['Surgical Mask', 'No Mask']
    tabs = fill_tabs(children, titles)

    # Calculate statistical test
    statistics = get_statistical_plots(df, df_surgical, df_none)

    return pn.Column(pn.Row(statistics, tabs), pn.pane.HTML("""<br><br><br><br>"""),
                     pn.Row(pn.layout.Divider()), pn.Row(get_df(subject_number)))


def generate_vbar():
    subjects = ['subject1', 'subject2', 'subject3', 'subject4', 'subject5']

    sub = {
        'subjects': subjects,
        'Surgical Mask': [
            np.mean(create_df(1).loc[create_df(1)['masktype'] != 'None']['mean']),
            np.mean(create_df(2).loc[create_df(2)['masktype'] != 'None']['mean']),
            np.mean(create_df(3).loc[create_df(3)['masktype'] != 'None']['mean']),
            np.mean(create_df(4).loc[create_df(4)['masktype'] != 'None']['mean']),
            np.mean(create_df(5).loc[create_df(5)['masktype'] != 'None']['mean']),
        ],
        'No Mask': [
            np.mean(create_df(1).loc[create_df(1)['masktype'] == 'None']['mean']),
            np.mean(create_df(2).loc[create_df(2)['masktype'] == 'None']['mean']),
            np.mean(create_df(3).loc[create_df(3)['masktype'] == 'None']['mean']),
            np.mean(create_df(4).loc[create_df(4)['masktype'] == 'None']['mean']),
            np.mean(create_df(5).loc[create_df(5)['masktype'] == 'None']['mean']),
        ]
    }

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,hover"

    p = figure(x_range=subjects, y_range=[0.97, 0.99], tools=TOOLS, width=400, height=600, tooltips='@sub')
    p.vbar(x=dodge('subjects', 0.1, range=p.x_range), name='Surgical Mask', top='Surgical Mask', width=0.2, source=sub,
           color="#ffff00",
           legend_label='Surgical mask')
    p.vbar(x=dodge('subjects', -0.1, range=p.x_range), name='No Mask', top='No Mask', width=0.2, source=sub,
           color="#66ffff",
           legend_label='No Mask')

    p.xgrid[0].grid_line_color = None
    p.ygrid[0].grid_line_alpha = 0.5
    p.xaxis.axis_label = 'Subject number'
    p.yaxis.axis_label = 'Spo2'
    p.yaxis.formatter = NumeralTickFormatter(format='0 %')

    hover = HoverTool()
    hover.tooltips = """
    <div>
    
    <div><strong>subjects: </strong>@subjects</div>
    <div><strong>value: <strong> @$name</div>    
    
    </div>
    """

    p.add_tools(hover)

    description = get_description_vbar()

    return pn.Row(p, description)


def get_stats_vbar():
    """@Azadeh Pirzadeh"""
    Y1 = []
    Y2 = []
    for i in range(5):
        Y1.extend(create_df(i + 1).loc[create_df(i + 1)['masktype'] != 'None']['mean'])
        Y2.extend(create_df(i + 1).loc[create_df(i + 1)['masktype'] == 'None']['mean'])

    y1 = np.array(Y1)
    y2 = np.array(Y2)

    _, p_value = ttest_ind(y1, y2, alternative='less')

    return p_value


def get_description_vbar():
    p_value = get_stats_vbar()
    question = "Is the blood oxygen saturation significantly lower when wearing a KN95 mask than wearing no mask?"
    h0 = "The blood oxygen saturation is not significantly lower when wearing a KN95 mask."
    h1 = "The blood oxygen saturation is significantly lower when wearing a KN95 mask."
    pane = get_statistical_plot(1, question, h0, h1, p_value)

    return pane


def get_df(subject_number):
    df = create_df(subject_number)
    return pn.pane.markup.DataFrame(df)


def fill_tabs(children, titles):
    tabs = []
    for child, title in list(zip(children, titles)):
        tabs.append(Panel(child=child, title=title))

    return pn.pane.Bokeh(Tabs(tabs=tabs))


def child_plot(df: pd.DataFrame, subject_number, xlabel, ylabel, legend_label):
    """Generate a child plot that can be used with a container"""

    TOOLS = 'pan, wheel_zoom, box_zoom, reset, save, hover'

    # Data contains only values between 0.94 and 1
    fig = figure(tools=TOOLS, x_axis_type='datetime', width=600, height=600, y_range=[0.94, 1], tooltips='value, @y')
    fig.xaxis.formatter = DatetimeTickFormatter(months=['$d,%m'])
    fig.title.text = 'SpO2 chart of subject {}'.format(subject_number)

    index = df.index

    fig = add_measurement(fig, df['spo2_m1_mean'], index, 'First Measurement', 'red')
    fig = add_measurement(fig, df['spo2_m2_mean'], index, 'Second Measurement', 'green')
    fig = add_measurement(fig, df['spo2_m3_mean'], index, 'Third Measurement', 'yellow')

    fig.ygrid[0].grid_line_alpha = 0.5
    fig.xgrid[0].grid_line_alpha = 0.5

    fig.xaxis.axis_label = xlabel
    fig.yaxis.axis_label = ylabel
    fig.yaxis.formatter = NumeralTickFormatter(format='0 %')

    fig.legend.title = legend_label
    fig.legend.location = 'bottom_left'
    fig.legend.click_policy = 'hide'

    return fig


def add_measurement(fig: figure, data_series: pd.Series, index: list, label: str, color: str):
    fig.line(index, data_series, line_width=2, color=color, alpha=0.8, legend_label=label)
    fig.circle(index, data_series, fill_color=color, size=8)

    return fig


def get_statistical_plots(df, df_surgical, df_none):
    # Calculate statistical test
    ## index fingers
    right_index_mean = df['spo2_r_mean']
    left_index_mean = df['spo2_l_mean']
    question = "Is there a significant difference between the oxygen saturation of the left and right index finger?"
    h0 = "There is no significant difference in blood oxygen saturation between the right and left index finger."
    h1 = "There is a significant difference in blood oxygen saturation between the right and left index finger."
    _, p_val = ttest_ind(right_index_mean, left_index_mean, alternative='two-sided')
    stat_plot_fingers = get_statistical_plot(1, question, h0, h1, p_val)

    ## Difference between wearing a mask and not wearing a mask
    y1 = df_surgical['mean']
    y2 = df_none['mean']
    _, p_val = ttest_ind(y1, y2, alternative='less')
    question = "Is the blood oxygen saturation significantly lower when wearing a KN95 mask than wearing no mask?"
    h0 = "The blood oxygen saturation is not significantly lower when wearing a KN95 mask."
    h1 = "The blood oxygen saturation is significantly lower when wearing a KN95 mask."
    stat_plot_spo2 = get_statistical_plot(2, question, h0, h1, p_val)

    return pn.Column(stat_plot_fingers, pn.layout.Divider(), stat_plot_spo2)


def get_statistical_plot(i, question, h0, h1, p_val):
    heading = pn.pane.Markdown("""
    # Research Question {} 
    **{}** 
    To answer this question, we formulate the following hypotheses: <br>
    **H<sub>0</sub>**: {}<br>
    **H<sub>1</sub>**: {}<br>\
    """.format(i, question, h0, h1))

    h_accepted = pn.pane.Markdown("We accept **H<sub>1</sub>** because the p-value {:.3f} < 0.05.<br>".format(p_val))
    conclusion_accepted = pn.pane.Markdown("**Conclusion: {}**".format(h1[0].lower() + h1[1:]),
                                           style={'color': 'whitesmoke', 'font-size': '16px'})

    h_rejected = pn.pane.Markdown("We reject **H<sub>1</sub>** because the p-value {:.3f} > 0.05.<br>".format(p_val))
    conclusion_rejected = pn.pane.Markdown("**Conclusion: {}**".format(h0[0].lower() + h0[1:]),
                                           style={'color': 'whitesmoke', 'font-size': '16px'})

    if p_val < 0.05:
        return pn.Column(heading, h_accepted, conclusion_accepted)
    else:
        return pn.Column(heading, h_rejected, conclusion_rejected)


def ttest(right, left):
    t_samp, p_val = ttest_ind(right, left, equal_var=False)

    return t_samp, p_val


def stats_test(y1, y2):
    n_1 = len(y1)
    n_2 = len(y2)
    p_ML_1 = np.mean(y1)
    p_ML_2 = np.mean(y2)
    O_1 = np.sum(y1)
    O_2 = np.sum(y2)
    pi_p = (O_1 + O_2) / (n_1 + n_2)
    z = (p_ML_1 - p_ML_2) / np.sqrt(pi_p * (1 - pi_p) * (1 / n_1 + 1 / n_2))

    p_value = norm.cdf(z)

    return p_value


class SpO2Page(Page):

    def __init__(self):
        subj_1 = create_df(1)
        subj_2 = create_df(2)
        subj_3 = create_df(3)
        subj_4 = create_df(4)
        subj_5 = create_df(5)

        plot_1 = generate_plot(subj_1, 1)
        plot_2 = generate_plot(subj_2, 2)
        plot_3 = generate_plot(subj_3, 3)
        plot_4 = generate_plot(subj_4, 4)
        plot_5 = generate_plot(subj_5, 5)

        comparison_plot = generate_vbar()

        self.pane = pn.Tabs(("Subject 1", plot_1),
                            ("Subject 2", plot_2),
                            ("Subject 3", plot_3),
                            ("Subject 4", plot_4),
                            ("Subject 5", plot_5),
                            ("Comparison", comparison_plot)
                            )
        self.button = pn.widgets.Button(name='SpO2')

    def get_contents(self):
        return self.pane, self.button


if __name__ == '__main__':
    oxy = SpO2Page()
    oxy_pane, oxy_btn = oxy.get_contents()

    oxy_pane.show(port=50001)
