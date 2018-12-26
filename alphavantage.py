
from connection import Connection
import logging
import os
import sys

class AlphaConnect(object):

    def __init__(self,
                 url="https://www.alphavantage.co",
                 apikey=None,
                 logfile='/Users/mstrozyk/fun/stockmarket/alphaconnect.log',
                 ):

        logging.basicConfig(filename=logfile,
                            level=logging.DEBUG)
        self.logger = logging.getLogger('alphaconnect')
        self.apikey = apikey if apikey else os.environ.get('ALPHAKEY')
        self.url = url
        self.resource = '/query?'
        self.connection = self.establish_connection(self.url)

    def establish_connection(self,
                             url,
                             ):
        '''
        Establishes a connection with the api

        Args:
            url::str
                FQDN of the api to connect to

        Returns:
            connection::Connection
                Exits if unsuccessful when connecting to API, otherwise 
                returns the connection it made to the API
        '''

        connection = Connection(url)

        if not connection.establish_connection():
            msg = 'AlphaConnect: Unable to establish connection with API. Exiting...'
            self.logger.critical(msg)
            print(msg)
            sys.exit(-1)

        return connection

    def get_market_data(self,
                        args,
                        ):
        '''
        Queries the api with the given parameters and returns response
        
        Args:
            args::dict[str]
                Dictionary that contains AT LEAST the following values:
            
                function::str
                    The function to query from the API
                symbol::str
                    The symbol of the market to query
                datatype::str
                    Format in which the data is returned. json and csv
                    are the possible options
                outputsize::str
                    How much data should be returned:
                        - Compact returns the latest 100 data points
                        - full returns up to 20 years of historical data

        Returns:
            response::dict{dict{}}
            Containing the market data in the format:
                {
                'Meta Data': { '1. Information', 
                               '2. Symbol', 
                               '3. Last Refreshed', 
                               '4. Interval', 
                               '5. Output Size', 
                               '6. Time Zone'}
                'Time Series (1min)': {DATE: {stock data}}
                }
        '''

        if not self.connection:
            self.establish_connection()

        datatypes = ['json', 'csv']
        outputsizes = ['compact', 'full']

        if args.get('datatype') not in datatypes:
            msg = f"{datatype} is not a valid datatype. The accepted "\
                  f"datatypes are: {datatypes.join(', ')}."
            self.logger.error(msg)
            print(msg)
            # TODO
            # Return the actual default format
            return

        if args.get('outputsize') not in outputsizes:
            msg = f"{outputsize} is not a valid outputsize. The accepted "\
                  f"outputsizes are: {outputsizes.join(', ')}."
            self.logger.error(msg)
            print(msg)
            # TODO
            # Return the actual default format
            return

        query = '&'.join([f'{arg}={value}' for arg, value in args.items()])
        query += f'&apikey={self.apikey}'
        response, _ = self.connection.make_request(resource=self.resource,
                                                       request_type='GET',
                                                       function=query,
                                                       expectResponse=True,
                                                       )

        return response

    def get_time_series_daily(self,
                              symbol,
                              datatype='json',
                              outputsize='compact',
                              ):
        '''
        Queries the api to get the daily time series data

        Args:
            symbol::str
                The symbol for the desired market data
            datatype::str
                The desired format for the returned data. The possible
                formats are json and csv
            outputsize::str
                The amount of data desired to be returned. The possible 
                options are:
                    compact   - Returns the last 100 data points
                    full      - Returns up to 20 years of historical data

        Returns:
            Dict of data as returned by alpha advantage
                        
        '''

        args = { 'function': 'TIME_SERIES_DAILY',
                 'symbol'  : symbol,
                 'datatype': datatype,
                 'outputsize': outputsize}

        return self.get_market_data(args)

    def get_time_series_intraday(self,
                                 symbol,
                                 datatype='json',
                                 outputsize='compact',
                                 interval='1min',
                                 ):
        '''
        Queries the api to get intraday data

        Args:
            symbol::str
                The symbol for the desired market data
            datatype::str
                The desired format for the returned data. The possible
                formats are json and csv
            outputsize::str
                The amount of data desired to be returned. The possible
                options are:
                    compact   - Returns the last 100 data points
                    full      - Returns up to 20 years of historical data
            interval::str
                The time interval to get the data in. Default is 1 minute.
        
        Returns:
            Dict of data as returned by alpha advantage
        '''
        args = { 'function': 'TIME_SERIES_INTRADAY',
                 'symbol'  : symbol,
                 'datatype': datatype,
                 'outputsize': outputsize,
                 'interval' : interval}

        return self.get_market_data(args)
