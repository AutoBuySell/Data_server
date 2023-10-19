from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi import Body

from scripts.archiving import real_time_archiving
from apps.error import CustomError

dataArchiving = FastAPI()

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
def real_time(symbols: list = Body(embed=True)):
  '''
  주가 기록 업데이트 요청용 엔드포인트
  Endpoint for requesting data update

  변동사항이 발생한 symbol 목록을 반환함
  Return a list of updated symbol
  '''
  updated = real_time_archiving(symbols=symbols)

  return JSONResponse(
    content={
      "message": "success",
      "updated": updated,
    },
    status_code=201,
  )

@dataArchiving.exception_handler(CustomError)
def custom_error_handler(request: Request, exc: CustomError):
    return JSONResponse(
        content={"message": f'{exc.message} in {exc.detail}'},
        status_code=exc.status_code
    )