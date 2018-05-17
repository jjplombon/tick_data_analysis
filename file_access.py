# -*- coding: utf-8 -*-
"""
Created on Tue May 01 15:29:35 2018

@author: jjplombo
"""

import os
import time_dmy_state as dmy_state

import webbrowser

print 'file_access:  load module...'

#  Append data file:
#  bid_offer:  IWM_05_02_2018_bid_offer.txt
#  trade:      IWM_05_02_2018_trade.txt

symbol = 'IWM'
bid_offer_file = dmy_state.get_current_day_file_bid_ask(symbol)
print 'bid offer file name:'
print bid_offer_file

#trade_file = dmy_state.get_current_day_file_trade(symbol)
#print 'trade file name:'
#print trade_file


def get_current_day_bid_ask_filename (symbol):
    bid_ask_filename = dmy_state.get_current_day_file_bid_ask(symbol)
    bid_ask_filename_dir = get_net_fonds_working_dir()
    bid_ask_filename_path = bid_ask_filename_dir + '\\' + bid_ask_filename
    
    bIsFileValid = os.path.isfile(bid_ask_filename_path)
    #print bIsFileValid
    
    return bid_ask_filename_path
    
def get_last_business_day_bid_ask_filename(symbol):
    bid_ask_filename = dmy_state.get_last_business_day_file_bid_ask(symbol)
    bid_ask_filename_dir = get_net_fonds_working_dir()
    bid_ask_filename_path = bid_ask_filename_dir + '\\' + bid_ask_filename
    
    bIsFileValid = os.path.isfile(bid_ask_filename_path)
    #print bIsFileValid
    
    return bid_ask_filename_path
    
def get_2nd_to_last_business_day_bid_ask_filename( symbol ):
    bid_ask_filename = dmy_state.get_2nd_to_last_business_day_file_bid_ask(symbol)
    bid_ask_filename_dir = get_net_fonds_working_dir()
    bid_ask_filename_path = bid_ask_filename_dir + '\\' + bid_ask_filename
    
    bIsFileValid = os.path.isfile(bid_ask_filename_path)
    #print bIsFileValid
    
    return bid_ask_filename_path
    
    
    
def get_current_day_trade_filename (symbol):
    trade_filename = dmy_state.get_current_day_file_trade(symbol)
    trade_filename_dir = get_net_fonds_working_dir()
    trade_filename_path = trade_filename_dir + '\\' + trade_filename
    
    bIsFileValid = os.path.isfile(trade_filename_path)
    #print bIsFileValid
    
    return trade_filename_path
    
def get_last_business_day_trade_filename( symbol ):
    trade_filename = dmy_state.get_last_business_day_file_trade(symbol)
    trade_filename_dir = get_net_fonds_working_dir()
    trade_filename_path = trade_filename_dir + '\\' + trade_filename
    
    bIsFileValid = os.path.isfile(trade_filename_path)
    #print bIsFileValid
    
    return trade_filename_path
    
    
#  Test code for spawning an Internet Explorer web browser
# For Windows
#  Currently launches Internet Explorer...
b_spawn_IE_browsers_for_net_fonds_csv_data_dumps = False
#b_spawn_IE_browsers_for_net_fonds_csv_data_dumps = True
if b_spawn_IE_browsers_for_net_fonds_csv_data_dumps:
    str_full_url_bid_offer_file = dmy_state.get_bid_ask_dump_url_current_day(symbol)
    str_full_url_bid_offer_file_LtoStr = ''.join(str_full_url_bid_offer_file)
    print 'Full URL to retrieve bid-ask tick data'
    print str_full_url_bid_offer_file_LtoStr
    #webbrowser.get("windows-default").open("http://example.com")
    hd_bid_offer_web_bw = webbrowser.get("windows-default").open(str_full_url_bid_offer_file_LtoStr)
    #... and it worked...
    #time,price,quantity,source,buyer,seller,initiator
    #20180504T153000,153.26,100,Auto trade,,,
    #20180504T153000,153.31,34515,Auto trade,,,
    #

    # spawn a web browser for the trade tick data:
    str_full_url_trade_file = dmy_state.get_trade_dump_url_current_day(symbol)
    str_full_url_trade_file_LtoStr = ''.join(str_full_url_trade_file)
    print 'Full URL to retrieve bid-ask tick data'
    print str_full_url_trade_file_LtoStr
    webbrowser.get("windows-default").open(str_full_url_trade_file_LtoStr)


    
#------------------------------------------------------------------------------
#
#   Private data and methods
#
#------------------------------------------------------------------------------
    
m_netfonds_dir = '\\netfonds_data'
print 'netfonds directory'
print m_netfonds_dir

m_current_wd = os.getcwd()

#print 'current working directory'
#print m_current_wd

#print 'net_fonds data directory:'
m_str_netfonds_data_directory = 'C:\\users\jjplombo\\Documents\\netfonds_data'
#print m_str_netfonds_data_directory
#print ("Is {} a valid directory".format(m_str_netfonds_data_directory))
#print os.path.isdir(m_str_netfonds_data_directory)

def get_net_fonds_working_dir():
    str_net_fonds_working_dir = m_str_netfonds_data_directory
    
    return str_net_fonds_working_dir