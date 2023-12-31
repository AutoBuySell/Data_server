from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from scripts.archiving import real_time_archiving, historical_archiving
from apps.error import CustomError

dataArchiving = FastAPI()

@dataArchiving.exception_handler(CustomError)
def custom_error_handler(request: Request, exc: CustomError):
    return JSONResponse(
        content={"message": f'{exc.message} in {exc.detail}'},
        status_code=exc.status_code
    )

@dataArchiving.get('/')
def hello_data_archiving():
  '''
  서버 상태 확인용 엔드포인트
  '''
  return JSONResponse(
    content={"message": "HelloDataArchiving!"},
    status_code=200,
  )

@dataArchiving.post('/real_time')
def real_time(data: dict):
  '''
  주가 기록 업데이트 요청용 엔드포인트
  Endpoint for requesting data update

  변동사항이 발생한 symbol 목록을 반환함
  Return a list of updated symbol
  '''

  symbols = data.get('symbols')
  timeframe = data.get('timeframe')

  updated = real_time_archiving(
    symbols=symbols,
    timeframe=timeframe
  )

  return JSONResponse(
    content={
      "message": "success",
      "updated": updated,
    },
    status_code=201,
  )

@dataArchiving.post('/historical')
def historical(data: dict):
   symbol = data.get('symbol')
   timeframe = data.get('timeframe')
   startDate = data.get('startDate')
   endDate = data.get('endDate')

   historical_archiving(symbol, timeframe, startDate, endDate)

   return JSONResponse(
      content={"message": "success"},
      status_code=201,
   )