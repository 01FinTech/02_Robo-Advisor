# -*- coding: utf-8 -*-

import tushare as ts
import pandas  as pd
import numpy   as np
import random

num_iteration    = 10
num_select_stock = 5
year_start       = '2014-01-01'
year_end         = '2016-01-01'



##TODO download all the stock
df_stock = ts.get_stock_basics()

## print ( df_stock )


##TODO delete all the stocks with label "st"


def random_draw( df, n = num_select_stock ):
	'''
	select 20 objects from ser at random
	Note: make sure ser is of type 'pd.Series'
	'''
	return df.take( np.random.permutation( len( df ) )[:n] )



def stock_rtn( stock_code ):
	'''
	compute the return during the period
	'''
	tmp = ts.get_k_data( code  = stock_code,
                              start = year_start, 
                              end   = year_end, 
                              ktype = 'M' )[ 'close' ][-1:].values / \
                ts.get_k_data( code  = stock_code, 
                               start = year_start, 
                               end   = year_end, 
                               ktype = 'M' )[ 'close' ][:1].values
	return tmp


##TODO
'''
note that tmp is the total return during the period, say 15 years, 
we shoud calculate 
'''


def asset_rtn( asset ):
	tmp = 0
	for stk in asset:
		tmp += stock_rtn( stk )
	return tmp / len( asset )
        



'''
for i in xrange( num_iteration ):

	##get the data

	print '--------'
	rand_index = []
	rand_index = random_draw( pd.Series( df_stock.index ) )
	rtn = asset_rtn( rand_index )
	print rtn
'''

##TODO: compute the return during each period  for at least 10 years



##TODO: record the total return for the iteration




## TODO: analyze the performance of the algorithm




