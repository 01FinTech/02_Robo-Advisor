# -*- coding: utf-8 -*-

## =============================================================== ##

from decimal import Decimal
import tushare as ts
import pandas  as pd
import numpy   as np
import math
import random

## =============================================================== ##

def RandomDraw( df, n ):
    """
    return a list which chooses n random objects from df
    """
    ## TODO: Is it a real random? --I'm not sure.
    return df.take( np.random.permutation( len( df ) )[:n] ).values

## =============================================================== ##

def DeleteNaN( df ):
    return df.dropna()

## =============================================================== ##

def AssetReturn( df ):
    tmp = 0.0
    for i in xrange( len( df ) ):
        tmp += df[i]
    tmp = tmp / len(df)

    return round( Decimal( tmp ), 8 )

## =============================================================== ##

def main( _num_iteration = 10, _num_draw = 20):
    df = pd.DataFrame()
    df = pd.read_csv( 'Data/allrecords.csv' )
    _list_date = df.columns[1:]

    _final_rtn = []

    for i in xrange( _num_iteration ):
        print '------------'
        print 'This is iteration %r' %i
        _rand_rtn = []
        for i in xrange( len( _list_date ) ):
            df_tmp = df[ _list_date[i] ].dropna()

            _index_set = []
            for k in xrange( len( df_tmp ) ):
                _index_set.append( k )


            df_tmp = RandomDraw( df_tmp, _num_draw )
            print 'On %r, the stocks chosen were %r' \
                  %( _list_date[i], df_tmp )
            tmp = AssetReturn( df_tmp )
            _rand_rtn.append( tmp )

        _final_rtn.append( _rand_rtn )

    print ( _final_rtn )

    df_final         = pd.DataFrame( _final_rtn )
    df_final.columns = _list_date

    _total_rtn = []
    for i in xrange( df_final.shape[0] ):      # number of rows
        print 'For row %r' %i
        tmp = 1.0
        for j in xrange( df_final.shape[1] ):  # number of columns
            print 'Before date %r, the total return was %r' \
                  %( _list_date[ j ], tmp )
            tmp = tmp * ( 1.0 + df_final.iloc[i,j] )
            tmp = round( Decimal( tmp ), 8 )
            print 'On that day, the return would be %r, so the final return was %r ' \
                  %(df_final.iloc[i][j], tmp)
        _total_rtn.append( tmp )

    df_final[ 'TotalReturn' ]    = _total_rtn
    df_final[ 'AverageReturn' ]  = df_final['TotalReturn'] / len( _list_date )

    print df_final
    print df_final.iloc[ 0, 1 ]

    df_final.to_csv( 'Data/myreturn.csv')

## =============================================================== ##


main( 10000, 20 )
