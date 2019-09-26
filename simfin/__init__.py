# This is also defined in setup.py and must be updated in both places.
__version__ = "0.1.0"

# Expose the following as top-level imports.

from simfin.bulk import load, load_income, load_balance, load_cashflow
from simfin.bulk import load_shareprices, load_companies, load_industries

from simfin.resample import resample, resample_daily

from simfin.config import set_api_key, load_api_key, get_api_key
from simfin.config import set_data_dir, get_data_dir, get_download_dir

from simfin.exceptions import ServerException
