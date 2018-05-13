# -*- coding: utf-8 -*-
"""
Created on Tue May 01 15:38:03 2018

@author: jjplombo
"""

import pandas as p

import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib .finance import candlestick_ohlc
import matplotlib.dates as mdates

import datetime
import file_access as file_rw
import time_dmy_state as dmy_state

data_frame = p.DataFrame
data_frame = []

df_tick_data = p.DataFrame
df_tick_data = []

dt_tick_data_now = datetime.datetime.now()


print 'tick_data_analysis:  module load...'

def remove_spike_pre_open( df_tick_data ):
    
    #df_tick_data.iloc[106,0] = 159.49
    #df_tick_data.iloc[107,0] = 159.49
    #  find pre-open start, with gap after previous business day after market: T100001
    #  typically T100001 spikes low with T100003 and T100005 possibly low as well...
    index_pre_market_start = m_find_pre_market_start(df_tick_data)
    
    if index_pre_market_start == -1:
        return df_tick_data
    #print 'Pre-Market start index:'
    #print (index_pre_market_start)
    # Get 'bid' three ticks ahead of pre market open
    bid_three_ticks_away = df_tick_data['bid'][(index_pre_market_start+3)]
    print 'bid three ticks after pre market start'
    print (bid_three_ticks_away)
    #  Replace prior three bids; 'bid' is column o
    df_tick_data.iloc[index_pre_market_start,0] = bid_three_ticks_away
    df_tick_data.iloc[(index_pre_market_start+1),0] = bid_three_ticks_away
    df_tick_data.iloc[(index_pre_market_start+2),0] = bid_three_ticks_away
    
    
    return df_tick_data

def return_open_datetime_index( df_tick_data ):
    open_index = -1
    
    dt_from_pts_idx_0 = df_tick_data.index[0].to_datetime()
    #print 'data frame tick data index[0]'
    #print(dt_from_pts_idx_0)
    
    market_open_dt = m_construct_market_open_datetime_from_now(dt_from_pts_idx_0)
    
    #print 'market open date time:'
    #print ( market_open_dt )
    
    for i in range(len(df_tick_data.index)):
        dt_from_pts = df_tick_data.index[i].to_datetime()
        if dt_from_pts.hour == m_open_hour:
            if dt_from_pts.minute == m_open_minute:
                #print(dt_from_pts)
                if(open_index == -1):
                    open_index = i
                    m_market_open_index = i
                    print 'found open start time'
                    print(dt_from_pts)
    
    return open_index


def gap_analysis_bid_ask_tick_data( df_tick_data, symbol ):
    print 'Gap analysis of bid/ask tick data dump...'
    #  Read previous close from prior business data file (local file)
    #  YYYY-MM_DDT220000 => hour = 22, minute = 00, second = 00
    #  df_tick_data['bid'][len(df_tick_data.index)] == closing price
    if dmy_state.is_non_business_day() :
        #  Get 2nd to last buisness day
        file_name_bid_ask = file_rw.get_2nd_to_last_business_day_bid_ask_filename(symbol)
    else:
        file_name_bid_ask = file_rw.get_last_business_day_bid_ask_filename(symbol)
    
    sym_posdump  = p.DataFrame()
    cols_posdump = [ 'bid', 'bid_depth', 'bid_depth_total', 'offer', 'offer_depth', 'offer_depth_total' ]
    try:
        #
        sym_posdump = sym_posdump.append( p.read_csv( file_name_bid_ask, index_col=0, header=0, parse_dates=True ) ) 
    except Exception as e:
        print( "Error reading posdump file: {} ".format( file_name_bid_ask ) )
   
    print ("Successful read of previous business day data file: {}".format(file_name_bid_ask) )
    len_sym_posdump = len(sym_posdump)
    print len_sym_posdump
    
    prev_close = sym_posdump['bid'][(len_sym_posdump-1)]
    print ('previous business day closing price: {}'.format(prev_close) )
    
    #  Current business day open:
    #  df_tick_data
    m_market_open_index = return_open_datetime_index( df_tick_data )
    current_open = df_tick_data['bid'][m_market_open_index]
    gap_open = current_open - prev_close
    print ('Open: {}, Previous Close: {}, Gap = {}'.format( current_open, prev_close, gap_open ) )
    
    #  Pre-market Gaps:
    post_market_open = df_tick_data['bid'][m_post_market_open_index]
    m_pre_market_open_index = m_find_pre_market_start(df_tick_data)
    pre_market_open = df_tick_data['bid'][m_pre_market_open_index]
    pre_maket_gap = pre_market_open - post_market_open
    print ('Post Market Open: {}, Pre Market Open: {}, Market Open: {}, Pre Market Gap: {}'.format( post_market_open, pre_market_open, current_open, pre_maket_gap ))
    
    
    return

def plot_bid_ask_tick_data( data_frame ):
    
    data_frame[['bid','bid_depth_total']].plot(subplots=True)
    return

def plot_bid_ask_resample_ohlc_volume( data_frame, strResample='5min'):
    
    df_ohlc = data_frame['bid'].resample(strResample).ohlc()
    #  Make date as a column for candlesticks function
    df_ohlc.reset_index(inplace=True)
    #print(df_ohlc.tail())
    #  modify time (datetime) to mdates
    df_ohlc['time'] = df_ohlc['time'].map(mdates.date2num)
    #print(df_ohlc.tail())
    df_volume = data_frame['bid_depth_total'].resample('5min').sum()
    #print(df_volume.tail())
    #print(df_volume.values[245:250])

    ax1 = plt.subplot2grid( (6,1), (0,0), rowspan=5, colspan=1 )
    ax2 = plt.subplot2grid( (6,1), (5,0), rowspan=1, colspan=1, sharex=ax1 )
    ax1.xaxis_date()

    #candlestick_ohlc( ax1, df_ohlc.values[230:240], width=1, colorup='g')
    #candlestick_ohlc( ax1, df_ohlc.values[245:250], width=0, colorup='g' )
    #   width is a fraction of a day: 5min/60min/24hr = 0.003472222
    candlestick_ohlc( ax1, df_ohlc.values, width=0.002, colorup='g' )
    #ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values[230:240], 0 )
    ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0 )

    plt.show()
    
    return

def resample_5min_ohlc(data_frame):
    df_resample = data_frame.resample( '5min').ohlc()
    
    return df_resample
    
#------------------------------------------------------------------------------
#
#    Private data and methods
#
#------------------------------------------------------------------------------
    
def m_construct_market_open_datetime_from_tick_dump( df_tick_data ):
    #pts_index_0 = df_tick_data.index[0]
    #dt_pts_index_0 = pts_index_0.to_datetime()
    #m_year = dt_pts_index_0.year
    #m_month = dt_pts_index_0.month
    #m_day = dt_pts_index_0.day
    market_open_datetime = datetime.datetime(m_year, m_month, m_day, m_open_hour, m_open_minute, m_open_second)
    print (market_open_datetime)
    
    
    return market_open_datetime
    
def m_construct_market_open_datetime_from_now(dt_tick_data_now):
    dt_now = dt_tick_data_now
    m_year = dt_now.year
    m_month = dt_now.month
    m_day = dt_now.day
    market_open_datetime = datetime.datetime(m_year, m_month, m_day, m_open_hour, m_open_minute, m_open_second)
    print (market_open_datetime)
    
    #delta_time = market_open_datetime - market_open_datetime
   # print (delta_time)
    
    
    return market_open_datetime
    
    
def m_find_pre_market_start( df_tick_data ):
    index_pre_mark_start = -1
    
    for i in range(len(df_tick_data.index)):
        dt_from_pts = df_tick_data.index[i].to_datetime()
        if dt_from_pts.hour == m_pre_market_start_hour:
            if dt_from_pts.minute == m_pre_market_start_minute:
                #print(dt_from_pts)
                if(index_pre_mark_start == -1):
                    index_pre_mark_start = i
                    m_pre_market_open_index = i
                    print 'found pre-market start time'
                    print(dt_from_pts)
    
    return index_pre_mark_start

m_open_hour = 15
m_open_minute = 30
m_open_second = 0
m_open_microsecond = 0

m_pre_market_start_hour = 10
m_pre_market_start_minute = 0
m_pre_market_start_second = 1
m_year = 2018
m_month = 1
m_day = 1
m_construct_market_open_datetime_from_tick_dump( df_tick_data )
m_construct_market_open_datetime_from_now( dt_tick_data_now )

m_market_open_index = -1
m_pre_market_open_index = -1
m_post_market_open_index = 0
    

    
