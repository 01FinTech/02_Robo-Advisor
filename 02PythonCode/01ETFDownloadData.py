# -*- coding: utf-8 -*-
'''
Modified on Fri, Sep 23, 2016
Author: Haifeng XU
Email:  78112407@qq.com

df.shape
df.describe()
df.info()
'''

import numpy   as np
import tushare as ts
import pandas  as pd
import pandas_datareader.data as web
import datetime

_start_date = '2007-01-01'
_end_date   = '2016-10-01'

## ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ ##
def _initial_index_cn() :
	index_list = []
	index_name = []

	index_list.append( '150151' )	## HS300A
	index_name.append( 'HS300A' )

	index_list.append( '150152' )	## HS300B
	index_name.append( 'HS300B' )

	index_list.append( '159920' )	## 恒生ETF
	index_name.append( '恒生ETF' )

	index_list.append( '160125' )	## 南方香港
	index_name.append( '南方香港' )

	index_list.append( '160416' )	## 石油黄金
	index_name.append( '石油黄金' )

	index_list.append( '160717' )	## 恒生H股
	index_name.append( '恒生H股' )

	index_list.append( '161116' )	## 易基黄金
	index_name.append( '易基黄金' )

	index_list.append( '161210' )	## 国投新兴
	index_name.append( '国投新兴' )

	index_list.append( '161714' )	## 招商金砖
	index_name.append( '招商金砖' )

	index_list.append( '161815' )	## 银华通胀
	index_name.append( '银华通胀' )

	index_list.append( '162411' )	## 华宝油气
	index_name.append( '华宝油气' )

	index_list.append( '164701' )	## 添富贵金
	index_name.append( '添富贵金' )

	index_list.append( '164815' )	## 工银资源
	index_name.append( '工银资源' )

	index_list.append( '165510' )	## 信诚四国
	index_name.append( '信诚四国' )

	index_list.append( '165513' )	## 信诚商品
	index_name.append( '信诚商品' )

	index_list.append( '510300' )	## HS300 ETF
	index_name.append( '沪深300 ETF')

	index_list.append( '510500' )	## 500 ETF
	index_name.append( '中证500 ETF')

	index_list.append( '510900' )	## H股ETF
	index_name.append( 'H股ETF' )

	index_list.append( '511860' )	## MoneyFund
	index_name.append( 'MoneyFund' )

	index_list.append( '513030' )	## 德国30
	index_name.append( '德国30' )

	index_list.append( '513100' )	## 纳指ETF
	index_name.append( '纳指ETF' )

	index_list.append( '513500' )	## 标普500
	index_name.append( '标普500' )

	return index_list, index_name
## ..................................................... ##


## ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ ##
def _initial_index_us() :
	'''
	Initialization of US assets
	'''

	index_list = []
	index_name = []

	index_list.append( '' )
	index_name.append( 'Apple' )

	index_list.append( 'GOOG' )
	index_name.append( 'Google' )

	index_list.append( 'GLD' )
	index_name.append( 'Gold' )

	index_list.append( 'SPY' )
	index_name.append( 'S&P 500' )

	index_list.append( 'USO' )
	index_name.append( 'USO' )

	index_list.append( 'XOP' )
	index_name.append( 'XOP' )

	return index_list, index_name
## ..................................................... ##


## ******************************************************** ##
def _initial_index( country_code ):
	'''
	---------------------------------------------
	This function just insert the asset code and name
	---------------------------------------------
	'''

	index_list = []
	index_list_name = []

	if country_code == 'cn' :
		index_list, index_list_name = _initial_index_cn()

	if country_code == 'us' :
		index_list, index_list_name = _initial_index_us()

	return index_list, index_list_name
## ..................................................... ##


## ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ ##
## 'my_ptf_cn' records the close price of the assets
## in 'index_list_cn[]'
## ******************************************************** ##
def _download_data( country_code ) :
	'''
	---------------------------------------------------
		Parameters
	---------------------------------------------------
	index: refers to the code of assets.
	index_name: refers to the name of assets.

	---------------------------------------------------
		Return
	---------------------------------------------------
	DataFrame: which contains the close price of the assets
        in "index"
	'''

	## create an empty pd, which would be returned
	df = pd.DataFrame()

	## assets to be added
	index, index_name = _initial_index( country_code )

	'''
	The data from CN is supplied by TuShare.
	Please refer to
    http://tushare.org/index.html for more details.
	注意：CN 与 US 的价格日期是相反的，我把 CN 的顺序调整了，
        与 US 保持一致。即 tail() 是最新的数据。
	'''
	## append the close price
	if country_code == 'cn' :
		for i in xrange( len( index ) ) :
			df[ index[i] ] = ts.get_hist_data( index[ i ] ,
											   start = _start_date ,
											   end   = _end_date   )[ 'close' ]

	'''
	The data from US is supplied by Yahoo-finance. Please refer to
	http://pandas-datareader.readthedocs.io/en/latest/remote_data.html#yahoo-finance
	for more details.

	Notice that 'Adj Close' price is what we want.
	'''
	## append the close price
	if country_code == 'us' :
		for i in xrange( len( index ) ) :
			df[ index[i] ] = web.DataReader( index[ i ] ,
											 'yahoo',
											 start = _start_date ,
											 end   = _end_date )[ 'Adj Close' ]

	## replace inf and NA with zero
	df[ df == np.inf ] = 0
	df.fillna( 0, inplace = True )

	## rename the columns
	df.rename( columns = dict( zip( index, index_name ) ),
			   inplace = True )

	## rename the index name
	df.index.name = 'date'

	## make sure the tail() is the latest data
	df = df.sort_index( ascending = True )

	## make sure the index is of type datetime
	df.index = pd.to_datetime( df.index )

	## test
	print df.shape

	return df
## ..................................................... ##


## ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ ##
## calculate the correlation of the assets
## first of all, we calculate the changed ratio of price
## the input needs to be a DataFrame containing the close price
## ******************************************************** ##
def _price_change( tmp ) :
	'''
	---------------------------------------------------
		Parameters
	---------------------------------------------------
	tmp: a dataframe containing the price.
		Notice that the tail is the latest date

	---------------------------------------------------
		Return
	---------------------------------------------------
	DataFrame: a dataframe containing the change of price
	'''

	df = tmp.copy()
#	df[1:] = 1.0 * df[1:].values / df[:-1].values - 1
	df = df / df.shift(1) * 1.0 - 1.0

	## the first row should be zero
	df[:1] = 0

	## replace inf and NA with zero
	df[ df == np.inf ] = 0
	df.fillna( 0, inplace = True )

	return df
## ..................................................... ##


## ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ ##
## We construst my portfolio according to 'index_list_cn'.
## Each entry records the close price of the assets.
## ******************************************************** ##
def _get_my_ptf():
	'''
	return my portfolio
	'''

	df    = pd.DataFrame()
	df_cn = pd.DataFrame()
	df_us = pd.DataFrame()

	df_cn = _download_data( country_code = 'cn' )
	df_us = _download_data( country_code = 'us' )

	'''
	Caution: join = 'outer' or 'inner'
	http://pandas.pydata.org/pandas-docs/stable/merging.html
	'''
	df = pd.concat( [df_cn, df_us],
	    			axis = 1,
					join = 'inner' )

	## replace inf and NA with zero
	df[ df == np.inf ] = 0
	df.fillna( 0, inplace = True )

	return df
## ..................................................... ##

my_ptf = _get_my_ptf()
my_ptf.to_csv( 'Data/etf_close_price.csv' )

my_ptf_rtn = _price_change( my_ptf )
my_ptf_rtn.to_csv( 'Data/etf_rtn.csv' )

## well, this is a bonus for users...
print('well, good job!')

'''
import matplotlib.pyplot as plt
fig = plt.figure()
ax  = fig.add_subplot(1,1,1)
ax.plot( randn( 1000 ).cumsum() )
ax.set_xticks( [0, 50, 100] )
ax.set_xticklabels( )
ax.set_title( )
ax.set_xlabel( )
ax.legend(loc='best')
'''

## ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ ##
## END of the code
## ******************************************************** ##
## ..................................................... ##
