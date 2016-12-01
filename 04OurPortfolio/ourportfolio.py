# -*- coding: utf-8 -*-

import tushare as ts
import pandas  as pd
import numpy   as np
import random

## --------------------------------------------------------------- ##
## TODO: how to append the trading date we need?
## --------------------------------------------------------------- ##

def initial_trading_date():
    """
    return a list containing traiding date
    """

    list_date = []

    ## Waring: these days are trading date
    list_date.append('2004-01-05')
    list_date.append('2005-01-04')
    list_date.append('2006-01-04')
    list_date.append('2007-01-04')
    list_date.append('2008-01-04')
    list_date.append('2009-01-05')
    list_date.append('2010-01-04')
    list_date.append('2011-01-04')
    list_date.append('2012-01-04')
    list_date.append('2013-01-04')
    list_date.append('2014-01-06')
    list_date.append('2015-01-05')
    list_date.append('2016-01-05')

    return list_date

## --------------------------------------------------------------- ##

def initial_index():
    """
    download the stock code
    return a list containing stock code
    """

    return ts.get_stock_basics().index
    ## return ts.get_sz50s().code
    ## return ts.get_hs300s().code
    ## return ts.get_zz500s().code

## --------------------------------------------------------------- ##
## TODO: delete all the stocks with label "st" or suspended
## --------------------------------------------------------------- ##
def random_draw(df, n):
    """
    return a list which chooses n random objects from df
    """
    ## TODO: this is NOT a real random!!
    return df.take( np.random.permutation( len( df ) )[:n] ).values


## if in the function initial_index(),
## return ts.get_stock_basics().index
## then we return df.take( np.random.permutation( len( df ) )[:n] )

## --------------------------------------------------------------- ##

def clean_data( list_asset, date_check ):
    """
    we clean the index set
    :param list_asset: the index set to be cleaned
    :param date_check: the fixed date
    :return: the index set after cleaning
    """

    list_asset_new     = list_asset
    list_asset_useless = []

    for k in xrange( len( list_asset ) ):
        print 'Iteration %d: check the useless index' %k
        try:
            df  = ts.get_k_data( list_asset[k],
                                 start = date_check,
                                 end   = date_check )
            tmp = df[ df.date == date_check ].close.values[0]
            tmp = round( tmp, 8 )
            print 'tmp is %r' %tmp
            pass
        except IndexError:
            print '>>> I found a useless index %r' %list_asset[k]
            list_asset_useless.append( list_asset[k] )
            pass

    print 'The list_asset_useless is of size %r, namely \n\t %r' \
          %( len(list_asset_useless), list_asset_useless)

    print 'The final lista_asset_new is of size %r, namely \n\t %r ' \
          %( len( list_asset_new[ ~list_asset_new.isin( list_asset_useless ) ] ),
          list_asset_new[~list_asset_new.isin(list_asset_useless)] )

    return list_asset_new[ ~list_asset_new.isin( list_asset_useless ) ]

## --------------------------------------------------------------- ##

def asset_date_return( list_asset_full, num_select_stock, list_date ):
    list_rtn = []

    '''
    Remark:
    the look is from 0 to n-2, where is the size of 'list_date'
    '''
    for i in xrange( len( list_date ) - 1 ):
        print 'the date is %r' %list_date[i]
        '''
        TODO: *****
        Given a set of asset index as well as a fixed date, how could we
        delete all the stocks with the sign of 'st' or 'suspension'?
        '''


        list_asset_all = clean_data( list_asset_full, list_date[i] )
        list_asset     = random_draw( list_asset_all, num_select_stock )

        print '\t\t the asset set chosen randomly was %r' % list_asset

        tmp_average = 0.0

        for j in xrange( len( list_asset)):
            print '----------\n the asset is %r' % list_asset[j]

            ## Initialization. Could we delete them?
            x1 = 0.0
            x2 = 0.0

            ## Notice that after invoking the function 'clean_data()'
            ## the asset was available on 'list_date[i]'
            x1 = ts.get_k_data( code  = list_asset[j],
                                start = list_date[i],
                                end   = list_date[i] ).close.values[0]
            ## Notice that: in case the asset was not able to sold on 'list_date[i+1]'
            ## we sold it on the nearest trading day
            x2 = ts.get_k_data( code  = list_asset[j],
                                start = list_date[i+1] ).close.values[0]

            x1 = round( x1, 8 )
            x2 = round( x2, 8 )
            print "the current price of the asset is %r, and the next year is %r" \
                  % (x1, x2)

            tmp = x2 / x1 * 1.0 - 1.0
            tmp = round( tmp, 8 )
            print 'The percentage of price change is %r' % tmp

            tmp_average += tmp
            tmp_average = round( tmp_average, 8)
        print '\n the tmp_average is %r\n\n' % (tmp_average / len(list_asset))

        list_rtn.append(tmp_average / len(list_asset))

    print '\n the list is %r' %list_rtn
    return list_rtn


## --------------------------------------------------------------- ##
##TODO: compute the return during each period  for at least 10 years
## --------------------------------------------------------------- ##
def main(num_iteration=5, num_select_stock=2):
    ## get the trading date
    list_date = initial_trading_date()

    ## choose n indexes from the full index set
    list_index = initial_index()

    ## the list which is exactly what we need to record the final return
    list_final_rtn = []

    for i in xrange( num_iteration ):
        print '\n \n =====================\n Round %r' %i
        list_final_rtn.append( asset_date_return( list_index,
                                                  num_select_stock,
                                                  list_date ) )
        print '\n list_final_rtn is %r' %list_final_rtn

    list_final_rtn = pd.DataFrame( list_final_rtn )
    list_final_rtn.columns = list_date[ 0:( len(list_date)-1 ) ]
    return list_final_rtn

## --------------------------------------------------------------- ##
## TODO: record the total return for the iteration
## --------------------------------------------------------------- ##
list_my_rtn = main( 5, 20 )
list_my_rtn.to_csv( 'Data/finalresult.csv' )
print '\n\n\n'
print list_my_rtn

## --------------------------------------------------------------- ##
## TODO: analyze the performance of the algorithm
