# -*- coding: utf-8 -*-

import tushare as ts
import pandas  as pd
import numpy   as np
import random

num_iteration    = 10
num_select_stock = 2
year_start       = '2014-01-01'
year_end         = '2016-01-01'


## --------------------------------------------------------------- ##
## TODO: how to append the trading date we need?

def initial_trading_date():
	'''
	return a list containing traiding date
	'''
	list = []

	list.append( '2010-01-04' )
	list.append( '2011-01-04' )
	list.append( '2012-01-04' )

	return list
## --------------------------------------------------------------- ##

def initial_index():
	'''
	download the stock code
	return a list containing stock code
	'''

	## return ts.get_stock_basics().index
	## return ts.get_sz50s().code ## which doesn't work
	return ts.get_hs300s().code
	## return ts.get_sz50s().code
	## return ts.get_zz500s().code

## --------------------------------------------------------------- ##
## TODO: delete all the stocks with label "st"

def random_draw( df, n = num_select_stock ):
	'''
	return a list which chooses n random objects from df
	'''
	return df.take( np.random.permutation( len( df ) )[:n] ).values
	## if in the function initial_index(),
	## return ts.get_stock_basics().index
	## then we return df.take( np.random.permutation( len( df ) )[:n] )


## --------------------------------------------------------------- ##

def asset_date_return( list_asset, list_date ):
	list = []

	for i in xrange( len( list_date ) ):
		print '\t The date is %s ' %list_date[i]
		list.append( average_asset_rtn( list_asset, list_date[i] ) )

	return list

## --------------------------------------------------------------- ##

def average_asset_rtn( list_asset, mydate ):
	'''
	return the average close price for the assets in the 'list_asset'
	on the date 'mydate'
	'''
	tmp = 0.0

	'''
	Remark 1:
	the loop is from 0 to n-2, where n is the size of 'list_asset'
	Remark 2:
	after this iteration, tmp would be transfered to type of 'Series'

	'''
	for i in xrange( len( list_asset ) - 1 ):
		## print 'for asset: ', list_asset[i]
		print '----------\n the asset is %s' %list_asset[i]
		df   = ts.get_k_data( code = list_asset[i] )
		tmp += df[ df.date == mydate ].close

		## transfer a 'Series' to number
		tmp = tmp.values[0]
		print 'the close price is %s' %tmp

	return tmp / len( list_asset )

## --------------------------------------------------------------- ##

##TODO: compute the return during each period  for at least 10 years

def main():
	## get the trading date
	list_date  = initial_trading_date()

	## choose n indexes from the full index set
	list_index = initial_index()

	## the list which is exactly what we need to record the final return
	list_final_rtn = []

	for i in xrange( num_iteration ):
		print '--------------\n Round %s' %i

		## test for the code
		## list_index_random = ['601668', '000002', '600000', '600007']
		list_index_random = random_draw( list_index )

		list_final_rtn.append( asset_date_return( list_index_random, list_date ) )
		print list_final_rtn

	return list_final_rtn


list_my_rtn = main()
print list_my_rtn


## --------------------------------------------------------------- ##
##TODO: record the total return for the iteration



## --------------------------------------------------------------- ##
## TODO: analyze the performance of the algorithm
