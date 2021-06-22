'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang

@Student Name  : first last

@Date          : June 2021

Discounted Cash Flow Model with Financial Data from Yahoo Financial

https://medium.datadriveninvestor.com/how-to-calculate-intrinsic-value-of-a-stock-aapl-case-study-935fb062004b

'''
import enum
import calendar
import math
import pandas as pd
import numpy as np

import datetime
from scipy.stats import norm

from math import log, exp, sqrt
from stock import Stock
import download_fundamental_data as dfd
import numpy as np

class DiscountedCashFlowModel(object):
    '''
    DCF Model:

    FCC is assumed to go have growth rate by 3 periods, each of which has different growth rate
           short_term_growth_rate for the next 5Y
           medium_term_growth_rate from 6Y to 10Y
           long_term_growth_rate from 11Y to 20thY
    '''

    def __init__(self, stock, as_of_date):
        self.stock = stock
        self.as_of_date = as_of_date

        self.short_term_growth_rate = None
        self.medium_term_growth_rate = None
        self.long_term_growth_rate = None

    def set_FCC_growth_rate(self, short_term_rate, medium_term_rate, long_term_rate):
        self.short_term_growth_rate = short_term_rate
        self.medium_term_growth_rate = medium_term_rate
        self.long_term_growth_rate = long_term_rate

    def calc_fair_value(self):
        # calculate the fair_value using DCF model

        # 1. calculate a yearly discount factor using the WACC

        beta = self.stock.get_beta()
        if beta is None:
            beta = 0
        DF = 1 / (1 + self.stock.lookup_wacc_by_beta(beta))
        #print('DF: ', DF)
        # 2. Get the Free Cash flow
        FCC = self.stock.get_free_cashflow()
        #print('FCC: ', FCC)
        # 3. Sum the discounted value of the FCC for the first 5 years using the short term growth rate
        DCF = 0
        # print('short term: ', self.short_term_growth_rate)
        # print('medium term: ', self.medium_term_growth_rate)
        # print('long term: ', self.long_term_growth_rate)
        for i in range(1, 6):
            DCF += FCC * (1 + self.short_term_growth_rate) ** i * DF ** i
        #print('DCF 1-5 :', DCF)
        # 4. Add the discounted value of the FCC from year 6 to the 10th year using the medium term growth rate
        CF5 = FCC * (1 + self.short_term_growth_rate) ** 5
        for i in range(1, 6):
            DCF += CF5 * (1 + self.medium_term_growth_rate) ** i * DF ** (i + 5)
        #print('DCF 6-10 :', DCF)
        # 5. Add the discounted value of the FCC from year 10 to the 20th year using the long term growth rate
        CF10 = CF5 * (1 + self.medium_term_growth_rate) ** 5
        for i in range(1, 11):
            DCF += CF10 * (1 + self.long_term_growth_rate) ** i * DF ** (i + 10)
        #print('DCF 10-20 :', DCF)
        # 6. Compute the PV as cash + short term investments - total debt + the above sum of discounted free cash flow
        PV = (self.stock.get_cash_and_cash_equivalent() + self.stock.yfinancial.get_short_term_investments()
              - self.stock.get_total_debt() + DCF)

        #print('PV: ', PV)
        total_shares = self.stock.get_num_shares_outstanding()
        if total_shares is None:
            return 0
        # 7. Return the stock fair value as PV divided by num of shares outstanding
        FV = PV / total_shares
        print('FV: ', FV)
        # TODO
        # end TODO

        return FV


def _test():
    symbol = 'AAPL'
    as_of_date = datetime.date(2021, 4, 21)
    stock = Stock(symbol, 'annual')
    model = DiscountedCashFlowModel(stock, as_of_date)

    short_term_growth_rate = .14
    medium_term_growth_rate = short_term_growth_rate / 2
    long_term_growth_rate = 0.04

    model.set_FCC_growth_rate(short_term_growth_rate, medium_term_growth_rate, long_term_growth_rate)

    fair_value = model.calc_fair_value()
    print(fair_value)


if __name__ == "__main__":
    _test()
