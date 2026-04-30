import importlib

import pandas as pd

from simfin.names import PUBLISH_DATE, REPORT_DATE, RESTATED_DATE, TICKER

load_module = importlib.import_module('simfin.load')


def test_load_does_not_pass_removed_date_parser(monkeypatch, tmp_path):
    csv_path = tmp_path / 'us-income-quarterly.csv'
    csv_path.write_text(
        'Ticker;Report Date;Publish Date;Restated Date;Value\n'
        'B;2024-01-31;2024-02-15;2024-03-01;2\n'
        'A;2024-01-30;2024-02-14;2024-02-20;1\n'
    )

    monkeypatch.setattr(load_module, '_maybe_download_dataset',
                        lambda **kwargs: None)
    monkeypatch.setattr(load_module, '_path_dataset',
                        lambda **kwargs: str(csv_path))

    original_read_csv = pd.read_csv

    def _read_csv(*args, **kwargs):
        assert 'date_parser' not in kwargs
        return original_read_csv(*args, **kwargs)

    monkeypatch.setattr(load_module.pd, 'read_csv', _read_csv)

    df = load_module.load(
        dataset='income',
        variant='quarterly',
        market='us',
        parse_dates=[REPORT_DATE, PUBLISH_DATE, RESTATED_DATE],
        index=[TICKER, REPORT_DATE],
        refresh_days=0,
    )

    assert list(df.index.get_level_values(TICKER)) == ['A', 'B']
    assert isinstance(df.index.get_level_values(REPORT_DATE), pd.DatetimeIndex)
