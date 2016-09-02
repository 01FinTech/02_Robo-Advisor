# -*- coding: utf-8 -*-

print ('hello, world')
import numpy as np
import pandas as pd
import datetime
import tushare as ts

_end_date = '2016-09-01'

## 这里还不确定复权问题
df300 = ts.get_hist_data('510300',end= _end_date )
df500 = ts.get_hist_data('510500', end = _end_date )
df300a = ts.get_hist_data('150151' , end = _end_date)
df300b = ts.get_hist_data('150152' , end = _end_date)
dfmoney = ts.get_hist_data('511860' , end = _end_date) ## 博时货币资金


df_result = pd.DataFrame()

_weight_begin = 0.25
_weight_end   = 1 - _weight_begin

df_result['zz500']  = _weight_begin * df500['open'] + _weight_end * df500['close']
df_result['hs300']  = _weight_begin * df300['open'] + _weight_end * df300['close']
df_result['hs300a'] = _weight_begin * df300a['open'] + _weight_end * df300a['close']
df_result['hs300b'] = _weight_begin * df300b['open'] + _weight_end * df300b['close']
df_result['money']  = _weight_begin * dfmoney['open'] + _weight_end * dfmoney['close']

## 计算资产相关系数
## calculate the correlation of different assets

df_result.to_csv('etf.csv')

print( df_result[0:20])

print ( df_result.corr() )

print ( df_result.describe() )

## 实时指数
## df = ts.get_index()
## print(df)

print('well ... Good Job!')
