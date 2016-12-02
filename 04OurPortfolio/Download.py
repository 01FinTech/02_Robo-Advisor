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
    list_date.append( '1996-05-15' )
    list_date.append( '1996-11-13' )
    list_date.append( '1997-05-14' )
    list_date.append( '1997-11-12' )
    list_date.append( '1998-05-13' )
    list_date.append( '1998-11-11' )
    list_date.append( '1999-05-12' )
    list_date.append( '1999-11-17' )
    list_date.append( '2000-05-17' )
    list_date.append( '2000-11-15' )
    list_date.append( '2001-05-16' )
    list_date.append( '2001-11-14' )
    list_date.append( '2002-05-15' )
    list_date.append( '2002-11-13' )
    list_date.append( '2003-05-14' )
    list_date.append( '2003-11-12' )
    list_date.append( '2004-05-12' )
    list_date.append( '2004-11-17' )
    list_date.append( '2005-05-18' )
    list_date.append( '2005-11-16' )
    list_date.append( '2006-05-17' )
    list_date.append( '2006-11-15' )
    list_date.append( '2007-05-16' )
    list_date.append( '2007-11-14' )
    list_date.append( '2008-05-14' )
    list_date.append( '2008-11-12' )
    list_date.append( '2009-05-13' )
    list_date.append( '2009-11-18' )
    list_date.append( '2010-05-12' )
    list_date.append( '2010-11-17' )
    list_date.append( '2011-05-18' )
    list_date.append( '2011-11-16' )
    list_date.append( '2012-05-16' )
    list_date.append( '2012-11-14' )
    list_date.append( '2013-05-15' )
    list_date.append( '2013-11-13' )
    list_date.append( '2014-05-14' )
    list_date.append( '2014-11-12' )
    list_date.append( '2015-05-13' )
    list_date.append( '2015-11-18' )
    list_date.append( '2016-05-18' )
    list_date.append( '2016-11-16' )

    return list_date

## =============================================================== ##

def Download_data():
    """
    we download the stock return, and store them to a CSV file.
    :return:
    """

    ## TODO _index_set is the set of all stock index
    _index_set = Initial_index()

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
                                end   = '2016-12-01' )
        
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
    df_tmp.index   = _index_set.values
    df_tmp.to_csv( 'Data/allrecords20161202.csv' )

    print '\n >>> Good job! The data were stored ' \
          'in the file Data/allrecords20161202'

## =============================================================== ##

Download_data()

