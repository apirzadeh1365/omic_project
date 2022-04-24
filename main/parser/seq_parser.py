__author__ = 'Djakim Latumalea'
__copyright__ = ['Djakim Latumalea', 'Azadeh Pirzadeh', 'Peter Riesebos', 'Kai Lin', 'Hossain Shahadat']
__license__ = 'Apache 2.0'
__version__ = '0.1'

import argparse
from typing import List
from pathlib import Path

import pandas as pd


def valid_path(path: str) -> bool:
    """Check if the provided path is valid."""
    if len(path) < 4:
        raise ValueError('File path to short!')

    extension = path[-3:]
    if extension != 'csv':
        raise ValueError('Expects a .csv file!')

    return True


class Parser:
    def __init__(self, df) -> None:
        self.df = df

    def split_files(self, subjects) -> List[pd.DataFrame]:
        try:
            files = [self.df[self.df['barcode'] == subject] for subject in subjects]
        except KeyError:
            raise ('Subject not present.')

        return files


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Parse the microbiome .csv file.")
    parser.add_argument('-f', '--file_path', required=True, help='Path to .csv file to parse.')

    args = parser.parse_args()
    file_path = args.file_path

    if valid_path(file_path):
        df = pd.read_csv(file_path)

    parser = Parser(df)

    subjects = [
        'barcode01',
        'barcode02',
        'barcode03',
        'barcode04',
        'barcode05'
    ]
    files = parser.split_files(subjects=subjects)

    for i, file in enumerate(files):
        file.to_csv(Path('../data/sequencing/parsed/{}.csv'.format(subjects[i])))
