# -*- coding: utf-8 -*-

from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross

class SMACrossOver(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod):
		strategy.BacktestingStrategy.__init__(self, feed)
		self.__instrument = instrument
		self.__position = None
		self.setUseAdjustedValues(True)
		self.__prices = feed[instrument].getPriceDataSeries()
		self.__sma = ma.SMA(self.__prices, smaPeriod)

	def getSMA(self):
		return self.__sma

	def onEnterCanceled(self,position):
		self.__position = None

	def onExitOk(self, position):
		self.__position = None

	def onExitCanceled(self, position):
		self.__position.exitMarket()

	def onBars(self, bars):
		if self.__position is None:
			if cross.cross_above(self.__prices, self.__sma) >0:
				shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getPrice())
				self.__position = self.enterLong(self.__instrument, shares, True)

		elif not self.__position.exitActive() and cross.cross_below(self.__prices,self.__sma) >0:
            self.__position.exitMarket()
