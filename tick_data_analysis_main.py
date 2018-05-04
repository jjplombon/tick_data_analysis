# -*- coding: utf-8 -*-
"""
Created on Tue May 01 14:47:41 2018

@author: John Plombon

Project: tick_data_analysis

Purpose:
read tick data from online soure, such as netfonds, or from file local to PC
Display tick data
analysze tick data
Summary of tick data
Action to take based on analysis

"""
# end of header documentation

import datetime
import file_access as file_rw
import net_fonds as net_fds
import tick_data_analysis as tda
import time_dmy_state as dmy_state

import pandas as p


print '----------------------------------'
print 'start tick_data_analysis_main ....'
print '----------------------------------'




#------------------------------------------------------------------------------
#
#  Testing time_dmy_state and URL construction
#
#------------------------------------------------------------------------------
symbol = 'iwm'
str_full_url_trade = dmy_state.get_trade_dump_url_five_conseq_days(symbol)
#print 'trade dump URL 5 days'
#print str_full_url_trade
#print len(str_full_url_trade)
#print str_full_url_trade[0]
#print str_full_url_trade[5]

str_full_url_trade = dmy_state.get_trade_dump_url_current_day(symbol)
#print 'trade dump URL current day'
#print str_full_url_trade

str_full_url_bid_ask = dmy_state.get_bid_ask_dump_url_five_conseq_days(symbol)
#print 'bid ask dump URL 5 days'
#print str_full_url_bid_ask

str_full_url_bid_ask = dmy_state.get_bid_ask_dump_url_current_day(symbol)
#print 'bid ask dump URL current day'
#print str_full_url_bid_ask


#------------------------------------------------------------------------------
#
#  Testing net_fonds tick data retrieval
#
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
#    Bid/Ask tick data dump
#------------------------------------------------------------------------------
sym_bid_ask_p_Dataframe = p.DataFrame()
str_full_url_bid_ask_LtoStr = ''.join(str_full_url_bid_ask)
#print 'list to str conversion: str_full_url_bid_ask and str_full_url_bid_ask_LtoStr'
#print str_full_url_bid_ask
print ('Full URL, Bid/Ask: {}'.format(symbol) )
print str_full_url_bid_ask_LtoStr
sym_bid_ask_p_Dataframe = net_fds.netfonds_p_bid_ask(str_full_url_bid_ask_LtoStr)
print 'len of sym bid ask pandas Dataframe'
print len(sym_bid_ask_p_Dataframe)

if len(sym_bid_ask_p_Dataframe) == 0:
    print 'unable to read netfonds bid ask tick data, assume offline, try file'
    str_bid_ask_filename = file_rw.get_current_day_bid_ask_filename(symbol)
    print 'current bid ask filename'
    print str_bid_ask_filename
    print 'assume reading current day''s tick data....'
    sym_posdump  = p.DataFrame()
    cols_posdump = [ 'bid', 'bid_depth', 'bid_depth_total', 'offer', 'offer_depth', 'offer_depth_total' ]
    try:
        #
        sym_posdump = sym_posdump.append( p.read_csv( str_bid_ask_filename, index_col=0, header=0, parse_dates=True ) ) 
    except Exception as e:
        print( "Error reading posdump file: {} ".format( str_bid_ask_filename ) )
   
    print ("Successful read of data file: {}".format(str_bid_ask_filename) )
    print len(sym_posdump)
    sym_posdump.columns = cols_posdump
    sym_posdump[['bid','bid_depth_total']].plot(subplots=True)
else:
    print ("Successful read of URL csv page: {}".format(str_full_url_bid_ask_LtoStr))
    sym_bid_ask_p_Dataframe[['bid','bid_depth_total']].plot(subplots=True)
    print 'TODO: Analyze DataFrame'
    
    
    
#------------------------------------------------------------------------------
#    Trade tick data dump
#------------------------------------------------------------------------------
sym_trade_p_Dataframe = p.DataFrame()
str_full_url_trade = dmy_state.get_trade_dump_url_current_day(symbol)
#print 'trade dump URL current day'
#print str_full_url_trade
str_full_url_trade_LtoStr = ''.join(str_full_url_trade)
#print 'list to str conversion: str_full_url_bid_ask and str_full_url_bid_ask_LtoStr'
#print str_full_url_bid_ask
print ('Full URL, Trade: {}'.format(symbol) )
print str_full_url_trade_LtoStr
sym_trade_p_Dataframe = net_fds.netfonds_t_trade_dump(str_full_url_trade_LtoStr)
print ('len of {} trade pandas Dataframe'.format(symbol) )
print len(sym_trade_p_Dataframe)

if len(sym_trade_p_Dataframe) == 0:
    print 'unable to read netfonds trade tick data, assume offline, try file'
    str_trade_filename = file_rw.get_current_day_trade_filename(symbol)
    print 'current trade filename'
    print str_trade_filename
    print 'assume reading current day''s tick data....'
    sym_posdump  = p.DataFrame()
    cols_posdump = [ 'price', 'quantity', 'source', 'offer', 'buyer', 'initiator' ]
    try:
        #
        sym_posdump = sym_posdump.append( p.read_csv( str_trade_filename, index_col=0, header=0, parse_dates=True ) ) 
    except Exception as e:
        print( "Error reading trade dump file: {} ".format( str_trade_filename ) )
   
    print ("Successful read of data file: {}".format(str_trade_filename) )
    print len(sym_posdump)
    sym_posdump.columns = cols_posdump
    sym_posdump[['price', 'quantity']].plot(subplots=True)
else:
    print ("Successful read of URL csv page: {}".format(str_full_url_trade_LtoStr))
    sym_trade_p_Dataframe[['price', 'quantity']].plot(subplots=True)
    print 'TODO: Analyze trade dump DataFrame'    
    
    
    
    
    