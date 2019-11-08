# This is also defined in setup.py and must be updated in both places.
__version__ = "0.2.0"

# Expose the following as top-level imports.

from simfin.bulk import load, load_shareprices, load_companies, load_industries
from simfin.bulk import load_markets
from simfin.bulk import load_income, load_income_banks, load_income_insurance
from simfin.bulk import load_balance, load_balance_banks, load_balance_insurance
from simfin.bulk import load_cashflow, load_cashflow_banks, load_cashflow_insurance

from simfin.utils import add_date_offset
from simfin.resample import resample, resample_daily, asfreq, asfreq_daily
from simfin.resample import reindex, index_union

from simfin.config import set_api_key, load_api_key, get_api_key
from simfin.config import set_data_dir, get_data_dir, get_download_dir

from simfin.exceptions import ServerException
