# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import datetime
import tushare as ts
from cvxopt import matrix, solvers


print('hello, world!')

df_return = pd.DataFrame()
df_return = pd.read_csv('etf.csv')

print ( df_return.describe() )

portfolio1 = [0, 1, 3, 4]
portfolio2 = [2, 3, 4]

## 协方差矩阵
cov_mat = df_return.cov()
## 标的预期收益
exp_rtn = df_return.mean()


def cal_efficient_frontier ( portfolio ) :
    cov_mat1 = cov_mat.iloc[portfolio][portfolio]
    exp_rtn1 = exp_rtn.iloc[portfolio]
    max_rtn = max( exp_rtn1 )
    min_rtn = min( exp_rtn1 )
    risks = []
    returns = []

    ## 20个点作图
    for level_rtn in np.linspace( min_rtn, max_rtn, 20) :
        sec_num = len( portfolio )
        _p = 2 * matrix( cov_mat1.values )
        _q = matrix( np.zeros( sec_num ) )
        _g = matrix( np.diag( -1 * np.ones( sec_num ) ) )
        _h = matrix( 0.0 , (sec_num, 1 ) )
        _a = matrix( np.matrix( [np.ones( sec_num ), exp_rtn1.values ]))
        _b = matrix( [1.0 , level_rtn ])
        solvers.options['show_progress'] = False
        sol = solvers.qp( _p, _q, _g, _h, _a, _b )
        risks.append( sol['primal objective'])
        returns.append( level_rtn )

    return np.sqrt( risks ), returns


risk1, return1 = cal_efficient_frontier( portfolio1 )
risk2, return2 = cal_efficient_frontier( portfolio2 )


















print ('well ....')
