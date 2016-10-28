# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import datetime
from matplotlib import pyplot as plt
from cvxopt import matrix, solvers

df_return = pd.DataFrame()
df_return = pd.read_csv( 'Data/etf_rtn.csv' )
df_return = df_return.sort_values( by = 'date', ascending = True )
df_return.fillna( 0, inplace = True )
print( df_return.head() )
## 注意：
## 这里每一列的有效数据长度不一致
## 即：有的资产可能从2013年开始，有的是从1998年开始

## print ( df_return.describe() )
print ( df_return.head() )


## 国内的 ETF QDII
portfolio1 = [2,3,4]
## 海外的 ETF
portfolio2 = [23,24,25,26]
## TODO: 如何快速的表达 2:23 ?

## 协方差矩阵
cov_mat = df_return.cov()
## 标的预期收益
exp_rtn = df_return.mean()


## 这个计算的代码需要优化一下
def cal_efficient_frontier( portfolio ) :
    '''
    We will compute the risk and its corresponding return.
    '''

    cov_mat1 = cov_mat.iloc[ portfolio ][ portfolio ]
    exp_rtn1 = exp_rtn.iloc[ portfolio ]
    max_rtn  = max( exp_rtn1 )
    min_rtn  = min( exp_rtn1 )
    risks    = []
    returns  = []

    '''
    20个点作图
    http://cvxopt.org/examples/tutorial/qp.html

    min 1/2 * x^T * Q * x + p * x
    s.t. G * x <= h
         A * x = b
    '''
    for level_rtn in np.linspace( min_rtn, max_rtn, 20) :
        sec_num = len( portfolio )

        _Q = 2 * matrix( cov_mat1.values )
        _p = matrix ( np.zeros( sec_num ) )
        _G = matrix ( np.diag( -1 * np.ones( sec_num ) ) )
        _h = matrix ( 0.0 , ( sec_num, 1 ) )
        _A = matrix ( np.matrix( [ np.ones( sec_num ), exp_rtn1.values ] ) )
        _b = matrix ( [ 1.0 , level_rtn ] )

        solvers.options['show_progress'] = False
        sol = solvers.qp( _Q, _p, _G, _h, _A, _b )

        '''
        ## 查看最优权重
        if level_rtn == max_rtn :
            print ('sol is here: \n')
            print ( sol['x'] )
        '''

        risks.append( sol[ 'primal objective' ] )
        returns.append( level_rtn )

    return np.sqrt( risks ), returns


risk1, return1 = cal_efficient_frontier( portfolio1 )
risk2, return2 = cal_efficient_frontier( portfolio2 )

fig = plt.figure ( figsize = (14, 8 ))
ax1 = fig.add_subplot( 111 )
ax1.plot ( risk1, return1 )
ax1.plot ( risk2, return2 )
ax1.set_title  ( 'Efficient Frontier', fontsize = 14 )
ax1.set_xlabel ( 'Standard Deviation', fontsize = 12 )
ax1.set_ylabel ( 'Expected Return'   , fontsize = 12 )
ax1.tick_params ( labelsize = 12 )
ax1.legend( [ 'portfolio1' , 'portfolio2' ] , loc = 'best', fontsize = 14 )
fig.savefig( 'Figure/Efficient_Frontier.png' )










print ('well, good job!')



## -------------------- END ----------------------- ##
