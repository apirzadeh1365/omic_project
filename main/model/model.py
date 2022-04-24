"""Module that contains functions to retrieve data.

Peter Riesebos:
- Created get_* functions.

Djakim Latumalea:
- Created config.yaml
- Created possibility to execute specific pages in their own page.py file, by getting the correct path.
"""

__author__ = ['Peter Riesebos', 'Djakim Latumalea']
__copyright__ = ['Djakim Latumalea', 'Azadeh Pirzadeh',
                 'Peter Riesebos', 'Kai Lin', 'Hossain Shahadat']
__license__ = 'Apache 2.0'
__version__ = '0.1'

from pathlib import Path

import yaml
import pandas as pd
import numpy as np

cwd = str(Path.cwd())
root_idx = cwd.index('main')
root_path = cwd[:root_idx + len('main')]

N = 5
BARCODES = np.arange(1, N + 1, 1)

with open(Path(root_path, 'config.yaml'), 'r') as stream:
    config = yaml.safe_load(stream)


def path_to_diary(config, root_path, subject_file):
    diary_dir = config['diarydir']
    path = Path(root_path, diary_dir, 'parsed', subject_file)

    return path


def path_to_baseline_barcodes(config, root_path, subject_file):
    barcodes_dir = config['barcodesdir']
    path = Path(root_path, barcodes_dir, 'parsed_baseline', subject_file)

    return path


def path_to_intervention_barcodes(config, root_path, subject_file):
    barcodes_dir = config['barcodesdir']
    path = Path(root_path, barcodes_dir, 'parsed_exp', subject_file)

    return path


subjects = {
    1: path_to_diary(config, root_path, 'subject_1.csv'),
    2: path_to_diary(config, root_path, 'subject_2.csv'),
    3: path_to_diary(config, root_path, 'subject_3.csv'),
    4: path_to_diary(config, root_path, 'subject_4.csv'),
    5: path_to_diary(config, root_path, 'subject_5.csv')
}

barcodes_baseline = {
    1: path_to_baseline_barcodes(config, root_path, 'barcode01.csv'),
    2: path_to_baseline_barcodes(config, root_path, 'barcode02.csv'),
    3: path_to_baseline_barcodes(config, root_path, 'barcode03.csv'),
    4: path_to_baseline_barcodes(config, root_path, 'barcode04.csv'),
    5: path_to_baseline_barcodes(config, root_path, 'barcode05.csv')
}

barcodes_intervention = {
    1: path_to_intervention_barcodes(config, root_path, 'barcode01.csv'),
    2: path_to_intervention_barcodes(config, root_path, 'barcode02.csv'),
    3: path_to_intervention_barcodes(config, root_path, 'barcode03.csv'),
    4: path_to_intervention_barcodes(config, root_path, 'barcode04.csv'),
    5: path_to_intervention_barcodes(config, root_path, 'barcode05.csv')
}


def get_column(subject, column=None):
    df_diary = pd.read_csv(subjects[subject])
    if column != None:
        selected = df_diary[column]
    else:
        selected = df_diary
    return selected


def get_column_barcodes_baseline(barcode, column=None):
    df_barcode = pd.read_csv(barcodes_baseline[barcode])
    if column != None:
        selected = df_barcode[column]
    else:
        selected = df_barcode
    return selected


def get_dataset(period):
    if period not in ['baseline', 'intervention']:
        raise ValueError('Expects period "baseline" or "intervention".')

    collection = []
    for barcode in BARCODES:

        if period == 'baseline':
            df = pd.read_csv(barcodes_baseline[barcode])
        else:
            df = pd.read_csv(barcodes_intervention[barcode])

        collection.append(df)

    return pd.concat(collection)


def get_column_barcodes_intervention(barcode, column=None):
    df_barcode = pd.read_csv(barcodes_intervention[barcode])
    if column != None:
        selected = df_barcode[column]
    else:
        selected = df_barcode
    return selected
