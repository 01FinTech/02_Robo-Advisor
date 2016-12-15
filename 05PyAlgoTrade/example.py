# -*- coding: utf-8 -*-

from pyalgotrade            import strategy
from pyalgotrade.barfeed    import yahoofeed
from pyalgotrade.technical  import ma


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod, initial_capital=1000000):
        super(MyStrategy, self).__init__(feed, initial_capital)
        self.__position     = None
        self.__instrument   = instrument
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__sma          = ma.SMA(feed[instrument].getPriceDataSeries(), smaPeriod)

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info(" BUY @ $%.2f" % (execInfo.getPrice()))
        self.info("position is %r" %self.__position)

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("SELL @ $%.2f" % (execInfo.getPrice()))

        self.__position = None
        self.info("position is %r" %self.__position)
        

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()
    
    # TODO: onBars() = run() ?
    def onBars(self, bars):
        # Wait for enough bars to be available to calculate a SMA.
        if self.__sma[-1] is None:
            return

        bar = bars[ self.__instrument ]
        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if bar.getPrice() > self.__sma[-1]:
                # Enter a buy market order for 10 shares. The order is good till canceled.
                self.__position = self.enterLong( self.__instrument, 100, True )
        # Check if we have to exit the position.
        elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():
            self.__position.exitMarket()


def run_strategy(smaPeriod):
    # Load the yahoo feed from the CSV file
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV("orcl", "orcl-2000.csv")

    # Evaluate the strategy with the feed.
    myStrategy = MyStrategy( feed, "orcl", smaPeriod )
    myStrategy.run()
    print "Final portfolio value: $%.2f" % myStrategy.getBroker().getEquity()

run_strategy(15)




