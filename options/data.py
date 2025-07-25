import logging
from enum import Enum

import time

import numpy as np
import pandas as pd

from options.common import export_df
from options.common import get_file_name
from options.download import get_ticker
from options.result import __get_result_of_output_files
from options.headers import __straddle_headers, final_headers

log = logging.getLogger("options - data")
logging.basicConfig(level=logging.INFO)


class View(Enum):
    STRADDLE = 1
    STACKED = 2
    ALL = 3


stacked_name = 'options_chain'
straddle_name = 'straddle'


def __reformat(df, option_type, date, symbol):
    df.insert(loc=0, column='option_type', value=option_type)
    df.insert(loc=1, column='expire_date', value=date)
    df.insert(loc=2, column='symbol', value=symbol)
    return df


def __get_options_view_data(symbol):
    """
        exports the options chain from yfinance api in the straddle view and tabulated view
    """
    if not isinstance(symbol, str):
        log.error("Please enter a valid symbol for the instrument")
        return None, None

    yticker = get_ticker(symbol)
    if yticker is None:
        log.error(f"No data for {symbol} returned from the API")
        return None, None

    try:
        expire_dates = yticker.options
    except Exception as e:
        log.error(f"Could not retrieve expiration dates for {symbol}: {e}")
        return None, None

    calls_df_list = []
    puts_df_list = []
    straddle_df_list = []

    for date in expire_dates:
        log.info(f"{symbol} downloading exercise date {date}")
        options_chain = None

        # Retry up to 3 times
        for attempt in range(3):
            try:
                options_chain = yticker.option_chain(date)
                break  # success
            except Exception as e:
                log.error(f"Attempt {attempt+1}/3 failed for {symbol} on {date}: {e}")
                time.sleep(1.5 * (attempt + 1))  # backoff

        if options_chain is None:
            log.error(f"Giving up on {symbol} for {date}")
            continue

        try:
            calls_df = __reformat(options_chain.calls, 'CALLS', date, symbol)
            puts_df = __reformat(options_chain.puts, 'PUTS', date, symbol)
            straddle_df = pd.merge(
                calls_df, puts_df, on=['expire_date', 'strike'],
                how='inner', suffixes=('_call', '_put'), sort=False
            )

            calls_df_list.append(calls_df)
            puts_df_list.append(puts_df)
            straddle_df_list.append(straddle_df)
        except Exception as e:
            log.error(f"Failed to process options chain for {symbol} on {date}: {e}")
            continue

    stacked_all_df = pd.DataFrame()
    straddle_all_df = None

    if straddle_df_list:
        straddle_all_df = pd.concat(straddle_df_list, ignore_index=True)
        straddle_all_df = straddle_all_df[__straddle_headers]
        straddle_all_df.insert(loc=0, column='symbol', value=symbol)
        straddle_all_df['inTheMoney_call'] = np.where(straddle_all_df['inTheMoney_call'], 'Y', 'N')
        straddle_all_df['inTheMoney_put'] = np.where(straddle_all_df['inTheMoney_put'], 'Y', 'N')
        straddle_all_df.sort_values(by=['expire_date', 'strike'], inplace=True)

    if calls_df_list:
        calls_all_df = pd.concat(calls_df_list, ignore_index=True)
        stacked_all_df = pd.concat([stacked_all_df, calls_all_df])

    if puts_df_list:
        puts_all_df = pd.concat(puts_df_list, ignore_index=True)
        stacked_all_df = pd.concat([stacked_all_df, puts_all_df])

    if not stacked_all_df.empty:
        stacked_all_df['inTheMoney'] = np.where(stacked_all_df['inTheMoney'], 'Y', 'N')

    for df in [straddle_all_df, stacked_all_df]:
        if df is not None:
            df.rename(columns=final_headers, inplace=True)

    return straddle_all_df, stacked_all_df


def get_options_view_df(symbol):
    straddle_view_df, stacked_df = __get_options_view_data(symbol)
    return straddle_view_df, stacked_df


def download_options_view(symbol, view_type=View.STRADDLE, folder=None):
    straddle_view_df, all_df = get_options_view_df(symbol)

    file_name_straddle, file_name_stacked = None, None

    if view_type == View.STRADDLE or view_type == View.ALL:
        file_name_straddle = get_file_name("{}_{}".format(straddle_name, symbol), True, folder)
        export_df(straddle_view_df, file_name_straddle, False)

    if view_type == View.STACKED or view_type == View.ALL:
        file_name_stacked = get_file_name("{}_{}".format(stacked_name, symbol), True, folder)
        export_df(all_df, file_name_stacked, False)

    result = __get_result_of_output_files(file_name_straddle, file_name_stacked)
    return result
