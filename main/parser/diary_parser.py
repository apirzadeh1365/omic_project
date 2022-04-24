__author__ = 'Djakim Latumalea'
__copyright__ = ['Djakim Latumalea', 'Azadeh Pirzadeh', 'Peter Riesebos', 'Kai Lin', 'Hossain Shahadat']
__license__ = 'Apache 2.0'
__version__ = '0.1'

import argparse
from pathlib import Path

import pandas as pd

columns = ['date', 'mask type', 'shaving', 'facial hygiene', 'make-up', 'temperature (°c)',
           'environment', 'note about kinds of skin and numbers of spots im the left and right part',
           'stress level(1-10)', 'sleep (h)', 'spo2-m1 (%) rh', 'spo2-m1 (%) lh', 'spo2-m2 (%) rh',
           'spo2-m2 (%) lh', 'spo2-m3 (%) rh', 'spo2-m3 (%) lh', 'start (t)', 'finish (t)']

float_cols = ['shaving', 'facial hygiene', 'make-up', 'stress level(1-10)',
              'sleep (h)', 'spo2-m1 (%) rh', 'spo2-m1 (%) lh', 'spo2-m2 (%) rh',
              'spo2-m2 (%) lh', 'spo2-m3 (%) rh', 'spo2-m3 (%) lh']

spo2_cols = ['spo2-m1 (%) rh', 'spo2-m1 (%) lh', 'spo2-m2 (%) rh',
             'spo2-m2 (%) lh', 'spo2-m3 (%) rh', 'spo2-m3 (%) lh']


def valid_path(path: str) -> bool:
    """Check if the provided path is valid."""
    if len(path) < 5:
        raise ValueError('File path to short!')

    extension = path[-4:]
    if extension != 'xlsx':
        raise ValueError('Expects a .xlsx file!')

    return True


class Parser:

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

        self.normalize_columns()

    def normalize_columns(self) -> None:
        self.df.columns = self.df.columns.str.lower()

    def clean_floats(self, col: pd.Series) -> pd.Series:
        return col.replace('[^.0-9]', '', regex=True).astype('float')

    def concatenate_cols(self, source: pd.Series, target: pd.Series) -> pd.DataFrame:
        df = self.df.copy()

        if source in df.columns and target in df.columns:
            df[target] = self.df[target].astype('str') + ',' + self.df[source].astype('str')

        return df

    def select_subset(self, columns: list) -> pd.DataFrame:
        df = self.df
        df = self.concatenate_cols('acne(total)',
                                   'note about kinds of skin and numbers of spots im the left and right part')
        df = df[df.columns.intersection(columns)]
        df = df[df['date'].notna()]

        return df

    def convert(self) -> pd.DataFrame:
        subset = self.select_subset(columns)
        subset[float_cols] = subset[float_cols].apply(self.clean_floats)
        subset[spo2_cols] = subset[spo2_cols].applymap(lambda x: x * 100 if x < 1 else x)
        subset['date'] = subset['date'].apply(lambda x: x.replace(year=2021) if x.year < 2021 else x)

        return subset


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Parse the raw .xlsx file.")
    parser.add_argument('-f', '--file_path', required=True, help='Path to .xlsx file to parse.')

    args = parser.parse_args()
    file_path = args.file_path

    if valid_path(file_path):
        df = pd.read_excel(file_path, sheet_name=1)

    parser = Parser(df)
    file = parser.convert()

    # TODO 
    # specify output name
    file.to_csv(Path('../../data/cleaned.csv'))
