import yfinance as yf
import requests
import pandas as pd
import io
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
import json
from kafka import KafkaProducer
import logging
from datetime import datetime
import config


def get_file_path():
    return os.path.join(config.CSV_FILE_DIR, 'stocks_list.csv')

def check_file_exists(path):
    return os.path.exists(path)

def get_stocks_list():
    nse_url = config.NSE_URL

    # create Session from 'real' browser
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    s = requests.Session()
    s.headers.update(headers)

    # do a get call now
    r = s.get(nse_url)
    s.close()

    # saving it to pd df for further preprocessing
    df_nse = pd.read_csv(io.BytesIO(r.content))

    stock_list = df_nse.get('Symbol').tolist()

    df_nse.get('Symbol').to_csv(get_file_path())

    return stock_list


'''
Needed Info ->
    shortName
    symbol
    volume,regularMarketVolume,averageVolume10days
    sector
    open,dayHigh,dayLow,previousClose
    exchange
    currentPrice
    quoteType -> EQUITY
'''

def check_info(stockData,key):
    try:
        return stockData.info[key]
    except Exception:
        return None


def get_stocks_info():
    filePath=get_file_path()
    # we will hit the url to get stocks list only when it is not present locally
    if check_file_exists(filePath):
        logging.info('file already exists !!!')
        nse_stocks_list=pd.read_csv(filePath)['Symbol'].to_list()
    else:
        nse_stocks_list = get_stocks_list()

    all_stocks_data={}

    print(f'total fetched stocks -> {len(nse_stocks_list)}')
    current_time=datetime.now()

    for stock in nse_stocks_list:
        logging.info(f"stock -> {stock}")
        stockData=yf.Ticker(f'{stock}.NS')

        shortName=check_info(stockData,'shortName')
        symbol=check_info(stockData,'symbol')
        volume=check_info(stockData,'volume')
        averageVolume=check_info(stockData,'averageVolume10days')
        sector=check_info(stockData,'sector')
        open=check_info(stockData,'open')
        dayHigh=check_info(stockData,'dayHigh')
        dayLow=check_info(stockData,'dayLow')
        currentPrice=check_info(stockData,'currentPrice')
        previousClose=check_info(stockData,'previousClose')
        exchange=check_info(stockData,'exchange')
        quoteType=check_info(stockData,'quoteType')

        all_stocks_data[stock]={'shortName':shortName,'symbol':symbol,'volume':volume,
                                 'averageVolume':averageVolume,'open':open,'dayHigh':dayHigh,'dayLow':dayLow,'sector':sector,'datatime':str(current_time),
                                 'currentPrice':currentPrice,'previousClose':previousClose,'exchange':exchange,'quoteType':quoteType}

    return all_stocks_data

default_args = {
    'owner': 'realtime data streaming',
    'start_date': datetime(2023, 9, 3, 10, 00)
}

def push_data_to_kafka():
    logging.basicConfig(level=logging.INFO)

    producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)

    stocks_info=get_stocks_info()

    for stock in stocks_info.keys():
        producer.send('stocks_data', json.dumps(stocks_info[stock]).encode('utf-8'), key=stock.encode('utf-8'))

        logging.info(f"stock info is {stocks_info[stock]}")



with DAG(dag_id='get_stock_info',
    default_args=default_args,
    schedule_interval='*/60 * * * *',
    catchup=False) as dag:

    streaming_task=PythonOperator(
        task_id='stocks_data',
        python_callable=push_data_to_kafka
    )




