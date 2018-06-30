# -*- coding: UTF-8 -*-

import pandas as pd
import tushare as ts

from pyalgotrade import strategy
from pyalgotrade import technical
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade import plotter
from pyalgotrade.stratanalyzer import returns


# 自定义时间窗口类
class DiffEventWindow(technical.EventWindow):
    def __init__(self, period):
        assert(period > 0)
        super(DiffEventWindow, self).__init__(period)
        self.__value = None

    def onNewValue(self, dateTime, value):
        super(DiffEventWindow, self).onNewValue(dateTime, value)
        if self.windowFull():
            lastValue = self.getValues()[0]
            nowValue = self.getValues()[1]
            self.__value = (nowValue - lastValue) / lastValue

    def getValue(self):
        return self.__value


# 自定义指标
class Diff(technical.EventBasedFilter):
    def __init__(self, dataSeries, period, maxLen=None):
        super(Diff, self).__init__(dataSeries, DiffEventWindow(period), maxLen)


# 定义策略
class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, diffPeriod=2):
        # 传入feed以及初始账户资金
        super(MyStrategy, self).__init__(feed, 10000)
        self.__instrument = instrument
        self.__position = None
        self.setUseAdjustedValues(True)
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__diff = Diff(self.__prices, diffPeriod)

        self.__break = 0.03
        self.__withdown = -0.04

    def getDiff(self):
        return self.__diff

    def onEnterCanceled(self, position):
        self.__position = None

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("Buy at $%.2f " % (execInfo.getPrice()))

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("SELL at $%.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit as canceled, re-submit items
        self.__position.exitMarket()

    def onBars(self, bars):
        account = self.getBroker().getCash()
        bar = bars[self.__instrument]
        if self.__position is None:
            one = bar.getPrice() * 100
            oneUnit = account // one
            if oneUnit > 0 and self.__diff[-1] > self.__break:
                self.__position = self.enterLong(self.__instrument, oneUnit * 100, True)
        elif self.__diff[-1] < self.__withdown and not self.__position.exitActive():
            self.__position.exitMarket()


def runStrategy():
    # 获取数据
    data = ts.get_k_data("600048")

    # 新增Adj Close字段
    data["Adj Close"] = data.close

    # 将tushare下的数据的字段保存为pyalgotrade所要求的数据格式
    # data.cloumns = ["Date", "Open","Close","High","Low","Volume","code","Adj Close"]
    data.rename(
        columns={'date': 'Date', 'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low', 'volume': 'Volume'},
        inplace=True)

    # 将数据保存成本地csv文件
    data.to_csv("data.csv", index=False)

    feed = yahoofeed.Feed()
    feed.addBarsFromCSV("data", "data.csv")

    myStrategy = MyStrategy(feed, "data")

    returnsAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(returnsAnalyzer)
    plt = plotter.StrategyPlotter(myStrategy)
    plt.getInstrumentSubplot("data")
    plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())

    myStrategy.run()
    print("Final portfolio value: $%.2f" % myStrategy.getResult())
    plt.plot()


runStrategy()
