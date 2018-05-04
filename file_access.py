# -*- coding: utf-8 -*-
"""
Created on Tue May 01 15:29:35 2018

@author: jjplombo
"""

import os
import time_dmy_state as dmy_state

print 'file_access:  load module...'

#  Append data file:
#  bid_offer:  IWM_05_02_2018_bid_offer.txt
#  trade:      IWM_05_02_2018_trade.txt

symbol = 'IWM'
bid_offer_file = dmy_state.get_current_day_file_bid_ask(symbol)
print 'bid offer file name:'
print bid_offer_file

trade_file = dmy_state.get_current_day_file_trade(symbol)
print 'trade file name:'
print trade_file


def get_current_day_bid_ask_filename (symbol):
    bid_ask_filename = dmy_state.get_current_day_file_bid_ask(symbol)
    bid_ask_filename_dir = get_net_fonds_working_dir()
    bid_ask_filename_path = bid_ask_filename_dir + '\\' + bid_ask_filename
    
    bIsFileValid = os.path.isfile(bid_ask_filename_path)
    print bIsFileValid
    
    return bid_ask_filename_path
    
def get_current_day_trade_filename (symbol):
    trade_filename = dmy_state.get_current_day_file_trade(symbol)
    trade_filename_dir = get_net_fonds_working_dir()
    trade_filename_path = trade_filename_dir + '\\' + trade_filename
    
    bIsFileValid = os.path.isfile(trade_filename_path)
    print bIsFileValid
    
    return trade_filename_path
    
    
#------------------------------------------------------------------------------
#
#   Private data and methods
#
#------------------------------------------------------------------------------
    
m_netfonds_dir = '\\netfonds_data'
print 'netfonds directory'
print m_netfonds_dir

m_current_wd = os.getcwd()

print 'current working directory'
print m_current_wd

print 'net_fonds data directory:'
m_str_netfonds_data_directory = 'C:\\users\jjplombo\\Documents\\netfonds_data'
#print m_str_netfonds_data_directory
print ("Is {} a valid directory".format(m_str_netfonds_data_directory))
print os.path.isdir(m_str_netfonds_data_directory)

def get_net_fonds_working_dir():
    str_net_fonds_working_dir = m_str_netfonds_data_directory
    
    return str_net_fonds_working_dir