# -*- coding: utf-8 -*-

import sma_crossover
from pyalgotrade import plotter
from pyalgotrade.tools import yahoofinance
from pyalgotrade.stratanalyzer import sharpe

def main( plot ):
	instrument = "gs"
	smaPeriod = 20

	feed = yahoofinance.build_feed( [ instrument ], 2014, 2015, "." )

	strat = sma_crossover.SMACrossOver( feed, instrument, smaPeriod )
	sharpeRatioAnalyzer = sharpe.SharpeRatio()
	strat.attachAnalyzer( sharpeRatioAnalyzer )

	if plot:
		plt = plotter.StrategyPlotter( strat, True, False, True )
		plt.getInstrumentSubplot( instrument ).addDataSeries( "sma", strat.getSMA() )

	strat.run()
	print "Sharpe ratio: %.2f" % sharpeRatioAnalyzer.getSharpeRatio(0.05)

	if plot:
		plt.plot()


if __name__ == "__main__":
	main(True)
