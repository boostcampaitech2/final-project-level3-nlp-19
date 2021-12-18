from fastapi import FastAPI, APIRouter
from fastapi.templating import Jinja2Templates
import uvicorn

router = APIRouter(prefix="/home", tags=["Home"])
templates = Jinja2Templates(directory='./templates')



# 뉴스 홈페이지 화면이동
@router.get("/")
def get_home_page():

    # Board Service 객체로 뉴스 목록 가져오기

    # return templates.TemplateResponse('home.html', context={'request':request})
    pass


if __name__ == '__main__':
    app = FastAPI()
    app.include_router(router)
    uvicorn.run(app="AIPaperboy:app", host="0.0.0.0", port=8000, reload=True)