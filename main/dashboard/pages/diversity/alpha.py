"""
This module contains the page that shows the alpha diversity.
"""

__author__ = ['Djakim Latumalea']
__copyright__ = ['Djakim Latumalea', 'Azadeh Pirzadeh', 'Peter Riesebos', 'Kai Lin', 'Hossain Shahadat']
__license__ = 'Apache 2.0'
__version__ = '0.1'

from typing import Callable

import panel as pn
import numpy as np
import pandas as pd
import plotly.express as px

from skbio.diversity.alpha import simpson, shannon

from model import get_column_barcodes_baseline, get_column_barcodes_intervention
from model.abstract import Page


def get_statistic(statistic: str) -> Callable:
    """Returns the function of the statistic.

    Keyword arguments:
        statistic -- the name of the statistical function to use.
    """
    if statistic not in ['simpson', 'shannon']:
        raise ValueError('Expects one of the values: "simpson", "shannon"')

    stats = {
        'simpson': simpson,
        'shannon': shannon
    }

    return stats[statistic]


def get_statistic_name(statistic: str) -> str:
    """ Returns the full name of the statistical abbreviation.

    Keyword arguments:
        statistic -- the abbrevation of the statistical function.
    """

    if statistic not in ['simpson', 'shannon']:
        raise ValueError('Expects one of the values: "simpson", "shannon"')

    names = {
        'simpson': 'Simpsons Diversity Index',
        'shannon': 'Shannon Diversity Index'
    }

    return names[statistic]


def get_simpson_description() -> pn.pane.Markdown:
    """Returns a Markdown pane containing a description of Simpsons Diversity Index."""

    pane = pn.pane.Markdown("""
    # Simpson's Diversity Index
    The Simpson's diversity index is a measure of species diversity [1]. 
    It returns a number between 0 and 1, where 1 represents complete diversity and 0 represents complete uniformity.

    Here we use the index on the baseline and experimental data. We are then able to compare them.
    """)

    return pane


def get_shannon_description() -> pn.pane.Markdown:
    """Returns a Markdown pane containing a description of Shannon-Wiener Diversity Index."""

    pane = pn.pane.Markdown("""
    # Shannon Diversity Index
    The Shannon Diversity Index is a way to measure the diversity of species in a community. 
    The higher the value of H, the higher the diversity of species. The lower, the lower the diversity. 
    
    We use the index on the baseline and experimental data.
    """)

    return pane


def get_references() -> pn.pane.Markdown:
    """Returns a Markdown pane containing the references for the Simpson and Shannon description."""

    references = pn.pane.Markdown("""
    ## References
    
    [1] A Guide to Simpson's Diversity Index, Royal Geographical Society with IBG.
    
    [2] Beachcomber Biology: The Shannon-Weiner Species Diversity Index
    Kathleen A. Noland, Jill E. Callahan    
    """)

    return references


def get_table_description() -> pn.pane.Markdown:
    """Returns a Markdown pane containing a description of the table containing the data."""

    pane = pn.pane.Markdown("""
    ## Table
    This table describes show the amount of bacteria, ordered from most prevalent to least prevalent.
    
    The Simpson and Shannon diversity indices use these data.
    """)

    return pane


class AlphaDiversity:
    """Calculates the Alpha Diversity using several metrics and can be integrated with Panel.

    Be aware that this class expects subjects with baseline data and experimental data.
    It expects that both datasets contain a 'species' column.

    n_subjects is the number of subjects that have a baseline and experimental dataset.
    """

    def __init__(self, n_subjects) -> None:
        # Number of subjects
        self.n_subjects = n_subjects

        self.subjects = {k: [] for k in np.arange(1, self.n_subjects + 1, 1)}
        self.simpson_index = {k: [] for k in np.arange(1, self.n_subjects + 1, 1)}

        self.populate()

    def get_plot(self) -> pn.Column:
        """Returns a formatted Column containing the tables, simpson tests, shannon tests, and descriptions."""
        tables = self.get_tables()
        simpson_stat = self.get_stats_table('simpson')
        shannon_stat = self.get_stats_table('shannon')

        simpson_bar = px.bar(simpson_stat.value, title='Simpson Diversity Index')
        shannon_bar = px.bar(shannon_stat.value, title='Shannon Diversity Index')

        simpson_descr = get_simpson_description()
        shannon_descr = get_shannon_description()
        table_descr = get_table_description()
        references = get_references()

        return pn.Column(simpson_descr, simpson_bar, simpson_stat,
                         shannon_descr, shannon_bar, shannon_stat,
                         pn.layout.Divider(), table_descr, tables,
                         pn.layout.Divider(), references)

    def get_bar_chart(self, df, title):
        data = df.copy(deep=True)
        data = data.reset_index()

        fig = px.bar(data, x='Subject', y=[data.columns[1:3].tolist()], title=title, barmode='group')

        return pn.pane.Plotly(fig)

    def populate(self) -> None:
        """Populate all subjects with their corresponding baseline and experiment data."""
        for subject in self.subjects.keys():
            baseline = get_column_barcodes_baseline(subject, ['species'])
            experiment = get_column_barcodes_intervention(subject, ['species'])

            self.subjects[subject].extend([baseline, experiment])

    def get_tables(self) -> pn.Tabs:
        """Return the tables containing microbiome data in tabs per user."""
        tables = []
        for subj in np.arange(1, self.n_subjects + 1, 1):
            tables.append((f'Subject {str(subj)}', self.get_df_table(subj)))
        tabs = pn.Tabs(objects=tables)

        return tabs

    def get_df_table(self, subject_number: int, n: int = 20) -> pn.widgets.DataFrame:
        """Returns a DataFrame widget containing the microbiome datasets of a subject.

        Keyword arguments:
            subject_number -- the number of the subject
            n -- the amount of rows to show.
        """
        if subject_number not in np.arange(1, self.n_subjects + 1, 1):
            raise KeyError('Subject number must be between 1 and {}'.format(self.n_subjects))

        rank = np.arange(1, n + 1, 1)
        data = self.subjects[subject_number]

        counts_baseline = data[0]['species'].value_counts()[:n]
        counts_experiment = data[1]['species'].value_counts()[:n]

        if len(counts_experiment) != len(counts_baseline):
            raise ValueError('Experiment and baseline counts should be of same length.')

        df = pd.DataFrame(data={'rank': rank,
                                'baseline species': counts_baseline.index,
                                'baseline counts': counts_baseline.tolist(),
                                'experiment species': counts_experiment.index,
                                'experiment counts': counts_experiment.tolist()})
        df = df.set_index('rank')

        return pn.widgets.DataFrame(df)

    def get_stats_table(self, statistic: str) -> pn.widgets.DataFrame:
        """Calculates the statistical function and returns a DataFrame widget.

        Keyword arguments:
            statistic: the name of the statistic
        """
        data = self.calculate_statistic(statistic)
        stat_name = get_statistic_name(statistic)

        subjects = []
        baseline_data = []
        experiment_data = []

        for subject, stats in data.items():
            subjects.append(subject)
            baseline_data.append(stats[0])
            experiment_data.append(stats[1])

        delta = np.array(experiment_data) - np.array(baseline_data)

        df = pd.DataFrame(data={'Subject': subjects, f'{stat_name} baseline': baseline_data,
                                f'{stat_name} experiment': experiment_data, 'Delta': delta})

        df = df.set_index('Subject')

        return pn.widgets.DataFrame(df)

    def calculate_statistic(self, statistic: str) -> dict:
        """Calculates a statistical function and returns a dictionary with data.

        Keyword arguments:
            statistic -- the name of the statistic
        """

        data = {k: [] for k in np.arange(1, self.n_subjects + 1, 1)}
        f = get_statistic(statistic)

        for subject, dfs in self.subjects.items():
            species_baseline = dfs[0]['species'].value_counts()
            species_experiment = dfs[1]['species'].value_counts()

            stat_baseline = np.round(f(species_baseline.tolist()), decimals=3)
            stat_experiment = np.round(f(species_experiment.tolist()), decimals=3)

            data[subject].extend([stat_baseline, stat_experiment])

        return data


class AlphaDiversityPage(Page):
    """Creates the page for the Alpha Diversity."""

    def __init__(self):
        alpha_diversity = AlphaDiversity(n_subjects=5)
        self.pane = alpha_diversity.get_plot()
        self.button = pn.widgets.Button(name='Alpha Diversity')

    def get_contents(self):
        return self.pane, self.button
