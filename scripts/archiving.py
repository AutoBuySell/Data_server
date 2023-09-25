import pandas as pd
import os

from apis.alpaca import get_historical_bars

path_market_data = '../data/market_data/'

def real_time_archiving(symbols: list):
  '''
  1. 해당 symbol 에 대한 파일이 존재하지 않는 경우 새로 파일을 생성하여 기록
  2. 최종 항목을 다운받아 봤을 때 저장된 내용과 변동사항이 없는 경우 수행 X
  3. 최종 항목을 다운받아 봤을 때 새로 추가된 항목이 있을 경우 새로운 내용을 덧붙여 갱신
  4. 최종 항목을 다운받아 봤을 때 완전히 새로운 항목인 경우 모든 내용을 덧붙여 갱신
  5. 그 외 수행 X

  1, 3, 4 의 경우 새로 업데이트 된 것으로 간주함
  새로 업데이트 된 symbol 리스트 를 반환함
  '''
  data = get_historical_bars(symbols)
  updated = []

  for key in data.keys():
    if not os.path.isfile(path_market_data + f'{key}.csv'):
      pd.DataFrame.from_records(data[key], columns=['t', 'o']).to_csv(path_market_data + f'{key}.csv', index=False)
    else:
      prev_pd = pd.read_csv(path_market_data + f'{key}.csv')
      new_pd = pd.DataFrame.from_records(data[key], columns=['t', 'o'])
      if prev_pd['t'].iloc[-1] == new_pd['t'].iloc[-1]:
        continue
      elif prev_pd['t'].iloc[-1] in list(new_pd['t']):
        pd.concat(
          [prev_pd, new_pd.iloc[list(new_pd['t']).index(prev_pd['t'].iloc[-1]):]]
        ).to_csv(path_market_data + f'{key}.csv')
      elif prev_pd['t'].iloc[-1] < new_pd['t'].iloc[0]:
        pd.concat(
          [prev_pd, new_pd]
        ).to_csv(path_market_data + f'{key}.csv')
      else:
        continue

    updated.append(key)

  return updated
