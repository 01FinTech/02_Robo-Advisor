# -*- coding: utf-8 -*-
'''
Modified on Fri, Sep 23, 2016
Email: 78112407@qq.com
The data is supplied by TuShare. Please refer to http://tushare.org/index.html for more details.
'''

print ('hello, world')
import numpy as np
import pandas as pd
import datetime
import tushare as ts

_start_date = '2012-01-01'
_end_date   = '2016-09-01'

## ********************************************************************** ##
## we are going to construst a portfolio with asset in the 'index_list[]'
## ********************************************************************** ##
index_list = []
index_list_name = []

index_list.append( '150151' )	## HS300A
index_list_name.append( 'HS300A' )

index_list.append( '150152' )	## HS300B
index_list_name.append( 'HS300B' )

index_list.append( '159920' )	## 恒生ETF
index_list_name.append( '恒生ETF' )

index_list.append( '160125' )	## 南方香港
index_list_name.append( '南方香港' )

index_list.append( '160416' )	## 石油黄金
index_list_name.append( '石油黄金' )

index_list.append( '160717' )	## 恒生H股
index_list_name.append( '恒生H股' )

index_list.append( '161116' )	## 易基黄金
index_list_name.append( '易基黄金' )

index_list.append( '161210' )	## 国投新兴
index_list_name.append( '国投新兴' )

index_list.append( '161714' )	## 招商金砖
index_list_name.append( '招商金砖' )

index_list.append( '161815' )	## 银华通胀
index_list_name.append( '银华通胀' )

index_list.append( '162411' )	## 华宝油气
index_list_name.append( '华宝油气' )
## 标普美国行业指数系列之油气开采及生产行业指数
## (S&P Select Industry Oil & Gas Exploration & Production)
## SPSIOP is the index being traced 
## XOP is an ETF
## 指数成分股的入选必须满足以下条件：
## 1、成份股是标普美国全市场指数的成员；
## 2、成份股属于GICS定义的油气二级行业分类；
## 3、成份股市值大于5亿美金，或市值大于4亿美金；
## 4、且交易量年换手率大于150%。


index_list.append( '164701' )	## 添富贵金
index_list_name.append( '添富贵金' )

index_list.append( '164815' )	## 工银资源
index_list_name.append( '工银资源' )

index_list.append( '165510' )	## 信诚四国
index_list_name.append( '信诚四国' )

index_list.append( '165513' )	## 信诚商品
index_list_name.append( '信诚商品' )

index_list.append( '510300' )	## HS300 ETF
index_list_name.append( '沪深300 ETF')

index_list.append( '510500' )	## 500 ETF
index_list_name.append( '中证500 ETF')

index_list.append( '510900' )	## H股ETF
index_list_name.append( 'H股ETF' )

index_list.append( '511860' )	## MoneyFund
index_list_name.append( 'MoneyFund' )

index_list.append( '513030' )	## 德国30
index_list_name.append( '德国30' )

index_list.append( '513100' )	## 纳指ETF
index_list_name.append( '纳指ETF' )

index_list.append( '513500' )	## 标普500
index_list_name.append( '标普500' )

'''
index_list.append( '' )	##
index_list_name.append( '' )

index_list.append( '' )	##
index_list_name.append( '' )
'''
## ---------------------------------------------------------------------- ##



## ********************************************************************** ##
## 'my_ptf' records the close price of the assets in 'index_list[]'
## ********************************************************************** ##
def _download_data( index, index_name ) :
	df = pd.DataFrame()

	for i in xrange( len( index ) ) :
		## append the close price
		df[ index[i] ] = ts.get_hist_data( index[i] ,
										   start = _start_date ,
										   end   = _end_date   )[ 'close' ]

	## replace inf and NA with zero
	df[ df == np.inf ] = 0
	df.fillna( 0, inplace = True )

	## rename the columns
	df.rename( columns = dict( zip( index, index_name ) ),
			   inplace = True )

	return df
## ---------------------------------------------------------------------- ##


## ********************************************************************** ##
## calculate the correlation of the assets
## first of all, we calculate the changed ratio of price
## the input needs to be a DataFrame containing the close price
## ********************************************************************** ##
def _price_change( tmp ) :
	df = tmp.copy()
	df[:-1] = 1.0 * df[:-1].values / df[1:].values - 1

	## the last row should be zero
	df[-1:] = 0

	## replace inf and NA with zero
	df[ df == np.inf ] = 0
	df.fillna( 0, inplace = True )

	return df
## ---------------------------------------------------------------------- ##



## ********************************************************************** ##
## construst my portfolio according to 'index_list'
## ********************************************************************** ##
my_ptf = pd.DataFrame()
my_ptf = _download_data( index_list, index_list_name )
## ---------------------------------------------------------------------- ##

## ********************************************************************** ##
## trace how much the price changed
## ********************************************************************** ##
my_ptf_change = pd.DataFrame()
my_ptf_change = _price_change( my_ptf )
## ---------------------------------------------------------------------- ##


my_ptf.to_csv( 'etf.csv' )
my_ptf_change.to_csv( 'etf_change.csv')

print 'my_ptf_change.corr()\n'
print ( my_ptf_change.corr() )
my_ptf_change.corr().to_csv( 'etf_correlation.csv' )

print 'my_ptf_change.describe()\n'
print ( my_ptf_change.describe() )


## 实时指数
## df = ts.get_index()
## print(df)








print('well ... Good Job!')



















## END of the code
