from fastapi import FastAPI
from fastapi.responses import JSONResponse

from scripts.archiving import real_time_archiving

dataArchiving = FastAPI()

@dataArchiving.get('/')
def hello_data_archiving():
  return JSONResponse(
    content={"message": "HelloDataArchiving!"},
    status_code=200,
  )

@dataArchiving.post('/real_time')
def real_time(symbols: list):
  '''
  주가 기록 업데이트 요청용 엔드포인트
  변동사항이 발생한 symbol 목록을 반환함
  '''
  updated = real_time_archiving(symbols=symbols)

  return JSONResponse(
    content={
      "message": "success",
      "updated": updated,
    },
    status_code=201,
  )