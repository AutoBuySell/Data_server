import requests
import os
import traceback
from datetime import datetime, timedelta
from dotenv import load_dotenv

from apps.error import CustomError

load_dotenv(verbose=True)

baseurl = os.getenv('ALPACA_HISTORY_DATA_URL')

headers = {
  'accept': 'application/json',
  'APCA-API-KEY-ID': os.getenv('ALPACA_PAPER_KEY'),
  'APCA-API-SECRET-KEY': os.getenv('ALPACA_PAPER_KEY_SECRET'),
}

def get_historical_bars(symbols: list[str], weeks: int = 2) -> dict:
  '''
  Alpaca API 를 통해 stock 가격 기록을 받고, 공통 형태로 변환하여 출력

  Getting historical stock prices, and
  Return a dictionary of historical data with keys of symbols
  '''
  dataList = {}
  nextPageToken = None

  try:
    params = {
      'symbols': ','.join(symbols),
      'timeframe': '30Min',
      'start': (datetime.utcnow() - timedelta(weeks=weeks)).isoformat(timespec='milliseconds') + 'Z',
      'end': (datetime.utcnow() - timedelta(minutes=16)).isoformat(timespec='milliseconds') + 'Z',
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

      assert response.status_code == 200, response.message

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

  except:
    print(traceback.format_exc())

    raise CustomError(
      status_code=500,
      message="Internal server error",
      detail="receiving and processing data from Alpaca API"
    )