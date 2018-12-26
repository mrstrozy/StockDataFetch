
from alphavantage import AlphaConnect
from argparse import ArgumentParser

def parse_args():

    parser = ArgumentParser()

    parser.add_argument('-s',
                        '--symbol',
                        action='store',
                        required=True,
                        dest='symbol',
                        )

    parser.add_argument('-i',
                        '--interval',
                        action='store',
                        required=False,
                        dest='interval',
                        )
    parser.add_argument('-o',
                        '--outputsize',
                        action='store',
                        dest='outputsize',
                        default='compact',
                        required=False,
                        )

    return parser.parse_args()

def stock_data_for_symbol(symbol,
                          interval=None,
                          outputsize='compact',
                          ):
    '''
    Returns stockmarket data for the inputted symbol.

    Args:
        symbol::str
            Stock market symbol for data to be gathered for
        interval::str
            The interval in which to get the data
        outputsize::str
            The outputtype of the response. This can be compact or full

    Returns:
    '''
    alpha = AlphaConnect()

    if not interval:
        return alpha.get_time_series_daily(symbol)

    response = alpha.get_time_series_intraday(symbol,
                                              interval=interval,
                                              outputsize=outputsize,
                                              )


    for k in response.get('Time Series (1min)'):
        print(response.get('Time Series (1min)').get(k).get('5. volume'))


if __name__ == '__main__':
    args = parse_args()
    print(stock_data_for_symbol(args.symbol,
                                interval=args.interval,
                                outputsize=args.outputsize))
