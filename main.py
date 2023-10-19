from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from apps.dataarchiving import dataArchiving

tags_metadata = [
  {
    "name": "Data collecting server",
    "description": "데이터 관련 서버",
  }
]

origins = [
  "*"
]

app = FastAPI(
  title="Data Manipulation",
  summary="데이터 수집 서버",
  version="0.0.1",
  openapi_tags=tags_metadata,
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.get('/')
def hello_world():
    '''
    서버 상태 확인용 엔드포인트
    Endpoint for checking the server is alive or not.
    '''
    return JSONResponse(
      content={"message": "HelloWorld!"},
      status_code=200,
    )

app.mount('/dataArchiving', dataArchiving)
