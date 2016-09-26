# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import datetime
import tushare as ts
from matplotlib import pyplot as plt
from cvxopt import matrix, solvers


print('hello, world!')

df_return = pd.DataFrame()
df_return = pd.read_csv('etf.csv')
df_return = df_return.sort_values( by = 'date' )
print( df_return.head() )
## 注意：
## 这里每一列的有效数据长度不一致
## 即：有的资产可能从2013年开始，有的是从1998年开始

## print ( df_return.describe() )

## for i in range( len( df_return  ) ):

_df_rtn_final = pd.DataFrame()

_df_rtn_final['date'] = df_return['date']

print ( _df_rtn_final.head())

_secID = ['zz500', 'hs300', 'hs300a', 'hs300b', 'money', ]

## 这里如何自动获取 DataFrame 的列数？
## 先已知有 5 列
##for i in range( 5 ) :
##	print i
##	cp = df_return.iloc[:,i:(i+1)]
##	cp.iloc[1:,:] = cp

for i in range( len(_secID)  ) :
	print i
	print _secID[i]
	cp = df_return[ _secID[i] ]
	print( cp.head() )
	cp[1:] = 1.0 * cp[1:].values / cp[:-1].values - 1
	print( cp.head() )
	## 第一行赋值为 0 ， 因为其没有比较意义
	cp[0:1] = 0
	_df_rtn_final[ _secID[i] ] = cp

## 用 0 替换 NaN
_df_rtn_final.fillna(0, inplace = True )

## zz500在2015年4月15日从 2.22 跳至 7.88 元。什么情况？
_df_rtn_final = _df_rtn_final[0:343]

print ( _df_rtn_final.describe() )

print ( _df_rtn_final.corr() )

print ('年化收益率')
print ( _df_rtn_final.mean() * 250 )

print ('年化标准差')
print ( _df_rtn_final.std() * np.sqrt(250))



## 选取组合
portfolio1 = [0, 1, 3, 4]
portfolio2 = [2, 3, 4]

## 协方差矩阵
cov_mat = _df_rtn_final.cov()
## 标的预期收益
exp_rtn = _df_rtn_final.mean()


## 这个计算的代码需要优化一下
def cal_efficient_frontier ( portfolio ) :
    cov_mat1 = cov_mat.iloc[portfolio][portfolio]
    exp_rtn1 = exp_rtn.iloc[portfolio]
    max_rtn = max ( exp_rtn1 )
    min_rtn = min ( exp_rtn1 )
    risks = []
    returns = []

    ## 20个点作图
	## 参考文档
	## http://cvxopt.org/examples/tutorial/qp.html
	## min 1/2 * x^T * Q * x + p * x
	## s.t. G * x <= h
	## 		A * x = b
    for level_rtn in np.linspace( min_rtn, max_rtn, 20) :
        sec_num = len( portfolio )

        _Q = 2 * matrix( cov_mat1.values )
        _p = matrix ( np.zeros( sec_num ) )
        _G = matrix ( np.diag( -1 * np.ones( sec_num ) ) )
        _h = matrix ( 0.0 , ( sec_num, 1 ) )
        _A = matrix ( np.matrix( [ np.ones( sec_num ), exp_rtn1.values ] ) )
        _b = matrix ( [ 1.0 , level_rtn ] )

#        print ('A is here/n')
#        print ( _A )
#        print ('b is here:/n')
#        print ( _b )
        
        solvers.options['show_progress'] = True
        sol = solvers.qp( _Q, _p, _G, _h, _A, _b )
        
        ## 查看最优权重
#        if level_rtn == max_rtn :          
#            print ('sol is here: \n')
#            print ( sol['x'] )

        risks.append( sol['primal objective'])
        returns.append( level_rtn )

    return np.sqrt( risks ), returns


risk1, return1 = cal_efficient_frontier( portfolio1 )
risk2, return2 = cal_efficient_frontier( portfolio2 )

fig = plt.figure ( figsize = (14, 8 ))
ax1 = fig.add_subplot( 111 )
ax1.plot ( risk1, return1 )
ax1.plot ( risk2, return2 )
ax1.set_title (  'Efficient Frontier', fontsize = 14 )
ax1.set_xlabel ( 'Standard Deviation', fontsize = 12 )
ax1.set_ylabel ( 'Expected Return', fontsize = 12 )
ax1.tick_params ( labelsize = 12 )
ax1.legend( ['portfolio1' , 'portfolio2'] , loc = 'best', fontsize = 14 )
fig.savefig('Efficient Frontier.png')

















print ('well ....')
