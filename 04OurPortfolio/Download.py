# -*- coding: utf-8 -*-

## =============================================================== ##

from decimal import Decimal
import tushare as ts
import pandas  as pd
import numpy   as np
import random

## =============================================================== ##

def Initial_index():
    """
    download the stock code
    return a list containing stock code
    """

    return ts.get_stock_basics().index
    ## return ts.get_sz50s().code
    ## return ts.get_hs300s().code
    ## return ts.get_zz500s().code

## =============================================================== ##

def Initial_trading_date():
    """
    return a list containing trading date
    """

    list_date = []

    ## Waring: make sure that these days are trading date

    list_date.append( '1996-01-04' )
    list_date.append( '1997-01-06' )
    list_date.append( '1998-01-05' )
    list_date.append( '1999-01-04' )
    list_date.append( '2000-01-04' )
    list_date.append( '2001-01-04' )
    list_date.append( '2002-01-04' )
    list_date.append( '2003-01-06' )
    list_date.append( '2004-01-05' )
    list_date.append( '2005-01-04' )
    list_date.append( '2006-01-04' )
    list_date.append( '2007-01-04' )
    list_date.append( '2008-01-04' )
    list_date.append( '2009-01-05' )
    list_date.append( '2010-01-04' )
    list_date.append( '2011-01-04' )
    list_date.append( '2012-01-04' )
    list_date.append( '2013-01-04' )
    list_date.append( '2014-01-06' )
    list_date.append( '2015-01-05' )
    list_date.append( '2016-01-05' )

    return list_date

## =============================================================== ##

def Download_data():
    """
    we download the stock return, and store them to a CSV file.
    :return:
    """

    ## TODO _index_set is the set of all stock index
    _index_set = Initial_index()[1:3]

    print 'I got _index_set %r' %_index_set

    ## TODO _list_date is the period we are tracking
    _list_date = Initial_trading_date()

    print 'I got _list_date %r' %_list_date

    ## _date_close is ...
    _date_close = []

    for j in xrange( len( _index_set ) ):
        print '--------------------------------'
        print 'the %r th asset was %r' %( j, _index_set[j] )
        print '--------------------------------'

        _list_rtn = []

        ## Notice that 'end' was set a value larger than
        ## the upper bound of '_list_date'
        df_tmp = ts.get_k_data( _index_set[j],
                                start = _list_date[0],
                                end   = '2016-03-01' )
        
        for i in xrange( len( _list_date ) - 1 ):
            print ' the date is %r' %_list_date[i] 
            try:
                x1 = df_tmp[ df_tmp.date == _list_date[i]   ].close.values[0]
                x2 = df_tmp[ df_tmp.date >= _list_date[i+1] ].close.values[0]

                x_tmp = round( Decimal( 1.0 * x2 / x1 - 1 ), 8 )
                _list_rtn.append( x_tmp )
                print 'the return was %r' %x_tmp
            except IndexError:
                _list_rtn.append( 'NaN' )
                print '>>> The asset %r is not available on date %r' %( _index_set[j], _list_date[i] )

        _date_close.append( _list_rtn )
    
    df_tmp         = pd.DataFrame( _date_close )
    df_tmp.columns = _list_date[ 0:( len( _list_date ) - 1 ) ]
    ## Remarks:
    ## If 'df_tmp.index' was set to be '_index_set' instead of
    ## '_index_set.values', then the final index would be '204'
    ##  other than '000204'.
    df_tmp.index   =  _index_set.values
    df_tmp.to_csv( 'Data/allrecords.csv' )

## =============================================================== ##

Download_data()

