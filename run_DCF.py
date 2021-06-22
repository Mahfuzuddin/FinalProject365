'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang
@Date          : June 2021

@Student Name  : first last

'''

import pandas as pd
import datetime

from stock import Stock
from discount_cf_model import DiscountedCashFlowModel


def run():
    input_fname = "StockUniverse.csv"
    output_fname = "StockUniverseWithDCF.csv"

    as_of_date = datetime.date(2021, 6, 15)
    df = pd.read_csv(input_fname)
    symbol = list(df['Symbol'])
    sector = list(df['Sector'])
    epsNext5Y = list(df['EPS Next 5Y'])
    FV = []
    # TODO
    results = []
    for index, row in df.iterrows():

        stock = Stock(row['Symbol'], 'annual')
        model = DiscountedCashFlowModel(stock, as_of_date)

        short_term_growth_rate = float(row['EPS Next 5Y'])
        if isinstance(short_term_growth_rate, float):
            short_term_growth_rate = float(row['EPS Next 5Y'])
        else:
            short_term_growth_rate = 0

        # print(short_term_growth_rate)
        medium_term_growth_rate = short_term_growth_rate / 2
        long_term_growth_rate = 0.04

        model.set_FCC_growth_rate(short_term_growth_rate, medium_term_growth_rate, long_term_growth_rate)

        fair_value = model.calc_fair_value()
        FV.append(fair_value)

        df = pd.DataFrame(list(zip(symbol, sector, epsNext5Y, FV)),
                          columns=['Symbol', 'Sector', 'EPS Next 5Y', 'Fair Value'])
        df.to_csv(output_fname, index=False, header=True)

    # ....

    # end TODO


if __name__ == "__main__":
    run()
