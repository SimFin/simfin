##########################################################################
#
# Various functions for calculating derivations of financial data,
# such as EBITDA, FCF, etc.
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################

from simfin.names import *

##########################################################################

def ebitda(df_income, df_cashflow, formula=NET_INCOME):
    """
    Calculate 'Earnings Before Interest, Taxes, Depreciation & Amortization'
    aka. EBITDA from columns in the given DataFrames. Two different EBITDA
    formulas are supported:

    - If `formula=NET_INCOME` then:
        EBITDA = Net Income + Interest + Taxes + Depreciation + Amortization

    - If `formula=OP_INCOME` then:
        EBITDA = Operating Income + Depreciation + Amortization

    :param df_income:
        Pandas DataFrame with Income Statements.

    :param df_cashflow:
        Pandas DataFrame with Cash-Flow Statements.

    :param formula:
        String for the formula to use in the EBITDA calculation.
        Use either NET_INCOME or OP_INCOME defined in `names.py`

    :return:
        Pandas Series with the EBITDA.
    """

    if formula == OP_INCOME:
        # Calculate EBITDA using Operating Income formula.
        df_result = df_income[OP_INCOME].fillna(0) \
                  + df_cashflow[DEPR_AMOR].fillna(0)
    elif formula == NET_INCOME:
        # Calculate EBITDA using Net Income formula.
        # Note that INTEREST_EXP_NET and INCOME_TAX have negative values
        # so in order to add them back to Net Income, we have to negate them.
        df_result = df_income[NET_INCOME].fillna(0) \
                  - df_income[INTEREST_EXP_NET].fillna(0) \
                  - df_income[INCOME_TAX].fillna(0) \
                  + df_cashflow[DEPR_AMOR].fillna(0)
    else:
        # Raise exception because of invalid arg.
        msg = 'arg `formula` was invalid.'
        raise ValueError(msg)

    # Rename the result.
    df_result.rename(EBITDA, inplace=True)

    return df_result

##########################################################################

def free_cash_flow(df_cashflow):
    """
    Calculate Free Cash Flow from columns in the given DataFrame using the
    formula:

        FCF = Net Cash from Operations - Capital Expenditures

    :param df_cashflow:
        Pandas DataFrame assumed to have columns named NET_CASH_OPS and CAPEX.

    :return:
        Pandas Series with the FCF.
    """

    # Calculate FCF.
    # Because CAPEX is defined as the Disposition *minus* Acquisition of
    # Fixed Assets and Intangibles, we have to add CAPEX to NET_CASH_OPS in
    # order to subtract the Acquisition-part and calculate the Free Cash Flow.
    # This is discussed in more detail in Tutorial 04.
    df_result = df_cashflow[NET_CASH_OPS].fillna(0) \
              + df_cashflow[CAPEX].fillna(0)

    # Rename the result to FCF.
    df_result.rename(FCF, inplace=True)

    return df_result

##########################################################################

def ncav(df_balance):
    """
    Calculate the so-called Net Current Asset Value (NCAV) which is a very
    conservative estimate of the liquidation value of a company, where only
    the Current Assets are counted at 100% and no other assets are counted,
    and then the Total Liabilities are subtracted from this.

    :param df_balance:
        Pandas DataFrame which is assumed to have the columns:
        TOTAL_CUR_ASSETS, TOTAL_LIABILITIES

    :return:
        Pandas Series
    """

    # Calculate NCAV.
    df_result = df_balance[TOTAL_CUR_ASSETS] - df_balance[TOTAL_LIABILITIES]

    # Rename the result.
    df_result.rename(NCAV, inplace=True)

    return df_result

##########################################################################

def netnet(df_balance):
    """
    Calculate the so-called NetNet Working Capital which is an even more
    conservative estimate of the liquidation value of a company compared to
    the NCAV, because Cash & Equivalents are counted at 100%, but Receivables
    are only counted at 75%, Inventories are counted at 50%, and no other
    assets are counted, and the Total Liabilities are subtracted from this.

    :param df_balance:
        Pandas DataFrame which is assumed to have the columns:
        CASH_EQUIV_ST_INVEST, ACC_NOTES_RECV, INVENTORIES, TOTAL_LIABILITIES

    :return:
        Pandas Series
    """

    # Calculate NetNet.
    df_result = df_balance[CASH_EQUIV_ST_INVEST].fillna(0) \
              + df_balance[ACC_NOTES_RECV].fillna(0) * 0.75 \
              + df_balance[INVENTORIES].fillna(0) * 0.5 \
              - df_balance[TOTAL_LIABILITIES]

    # Rename the result.
    df_result.rename(NETNET, inplace=True)

    return df_result

##########################################################################
