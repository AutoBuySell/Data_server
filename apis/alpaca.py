import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv(verbose=True)

baseurl = os.getenv('ALPACA_HISTORY_DATA_URL')

headers = {
  'accept': 'application/json',
  'APCA-API-KEY-ID': os.getenv('ALPACA_PAPER_KEY'),
  'APCA-API-SECRET-KEY': os.getenv('ALPACA_PAPER_KEY_SECRET'),
}

def get_historical_bars(symbols, weeks: int = 2):
  '''
  Alpaca API 를 통해 stock 가격 기록을 받고, 공통 형태로 변환하여 출력
  '''
  dataList = {}
  nextPageToken = None

  params = {
    'symbols': ','.join(symbols),
    'timeframe': '30Min',
    'start': (datetime.today() - timedelta(weeks=weeks)).isoformat() + 'Z',
    'end': (datetime.today() - timedelta(minutes=16)).isoformat() + 'Z',
    'limit': 1000,
    'adjustment': 'raw',
  }

  while True:
    if nextPageToken:
      params['page_token'] = nextPageToken

    response = requests.get(
      url=baseurl + '/stocks/bars',
      headers=headers,
      params=params,
    )

    if response.status_code != 200:
      print(response.content)
      break

    response = response.json()

    if 'bars' in response:
      for key in response['bars']:
        if key in dataList:
          dataList[key] = [*dataList[key], *response['bars'][key]]
        else:
          dataList[key] = response['bars'][key]

    if response['next_page_token']:
      nextPageToken = response['next_page_token']
    else:
      break

  return dataList
