from typing import Optional
from fastapi import FastAPI, APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import uvicorn

from services.newscontent import Newscontent
from services.manageuserinput import Manageuserinput
from services.managenewsscrap import Managenewsscrap

from pydantic import BaseModel

from .home import get_db
from schema import schemas
from sqlalchemy.orm import Session

router = APIRouter(prefix="/news", tags=["News"])
templates = Jinja2Templates(directory='templates')


# 뉴스 기사 불러오기(창한)
@router.get("/{news_id}",  description="사용자가 호출한 뉴스 본문을 볼 수 있도록 합니다.")
def get_news_page(request: Request, news_id: str, user_id: str, db: Session = Depends(get_db)):
    # Newscontent Service 객체로 news 기사 본문 가져오기
    title, article  = Newscontent.get_news(db=db, news_id=news_id, user_id = user_id)
    article = article.replace('<br />', '\n')
    article = article.replace('<!------------ PHOTO_POS_0 ------------>', '')
    print(title, article, sep='\n')
    
    return templates.TemplateResponse('news_article.html', context={'request': request, 'news_id': news_id, 'user_id': user_id, 'title': title, 'article': article})




# # 사용자가 뉴스 기사에 입력한 정보, 스크랩 정보를 DB에 저장하기(준수, 별이)
# @router.post("/question")
# def post_news_input(user_info: schemas.UserInputBase, news_scrap: schemas.NewsScrapCreate, db: Session = Depends(get_db), input: str = Form(...)):
#     print(input, user_info)
#     # Manageuserinput Service 객체로 사용자 입력 정보를 DB에 저장하기(준수)
#     Manageuserinput.insert_news_input(db=db, user_info=user_info, input=input)
#     print("No Problem")
#     # Managenewsscrap Service 객체로 사용자 스크랩 정보를 DB에 저장하기(별이)
#     return Managenewsscrap.create_news_scrap(db=db, news_scrap=news_scrap)


# 사용자가 뉴스 기사에 입력한 정보, 스크랩 정보를 DB에 저장하기(준수, 별이)
@router.get("/{news_id}/question", description="유저아이디, 스크랩할 뉴스아이디 가져와서 db에 저장")
def get_user_input(request: Request, news_id: str, user_id: str, text: str, db: Session = Depends(get_db)):
    title, article = Newscontent.get_news(db=db, news_id=news_id, user_id=user_id)
    article = article.replace('<br />', '\n')
    article = article.replace('<!------------ PHOTO_POS_0 ------------>', '')
    print(title, article, sep='\n')

    # Managenewsscrap Service 객체로 사용자 스크랩 정보를 DB에 저장하기
    Manageuserinput.insert_news_input(db=db, user_id=user_id, news_id=news_id, user_input=text)


    # Managenewsscrap Service 객체로 사용자 스크랩 정보를 DB에 저장하기(별이)
    # 해당 기사가 이미 DB에 저장되어있는지 확인
    if not Managenewsscrap.get_news_scrap_id(db=db, user_id=user_id, news_id=news_id):
        Managenewsscrap.create_news_scrap(db=db, user_id=user_id, news_id=news_id)

    # 이 부분 RedirectResponse로 바꿔야 하는데 아직 모르겠음
    return templates.TemplateResponse('news_article.html', context={'request': request, 'title': title, 'article': article, 'news_id': news_id, 'user_id': user_id})





# 사용자가 뉴스 기사에 입력한 정보, 스크랩 정보를 DB에서 삭제하기(준수, 별이)
@router.get("/{news_id}/delete", description="사용자가 뉴스 기사에 입력한 정보, 스크랩 정보를 DB에서 삭제하기")
# 기사에 입력한 정보 삭제하는 부분이 UI로 구현이 안 되어있어서 <스크랩 해제> 버튼으로 누르면 기존 Question 입력한 것과 스크랩한 것을 DB 삭제
# def delete_news_input(request: Request, news_id: str, user_id: str, text: str, db: Session = Depends(get_db)):
def delete_news_input(request: Request, news_id: str, user_id: str, db: Session = Depends(get_db)):
    title, article = Newscontent.get_news(db=db, news_id=news_id, user_id=user_id)
    article = article.replace('<br />', '\n')
    article = article.replace('<!------------ PHOTO_POS_0 ------------>', '')
    # print(title, article, sep='\n')
    
    # 해당 기사가 DB에 저장되어있어서 삭제가 가능한지 확인
    if not Managenewsscrap.get_news_scrap_id(db=db, user_id=user_id, news_id=news_id):
        return templates.TemplateResponse('news_article.html', context={'request': request, 'title': title, 'article': article, 'news_id': news_id, 'user_id': user_id})
    
    # Manageuserinput Service 객체로 사용자 입력 정보를 DB에서 삭제하기(준수)
    Manageuserinput.delete_news_input(db=db, user_id=user_id, news_id=news_id)

    # 해당 기사에서 Userinput 정보가 없으면 Managenewsscrap Service 객체로 사용자 스크랩 정보를 DB에서 삭제하기(별이)
    Managenewsscrap.delete_news_scrap(db=db, user_id=user_id, news_id=news_id)

    # 이 부분 RedirectResponse로 바꿔야 하는데 아직 모르겠음
    return templates.TemplateResponse('news_article.html', context={'request': request, 'title': title, 'article': article, 'news_id': news_id, 'user_id': user_id})




# 뉴스 기사 스크랩하기(별이)
# 뉴스 title, article 불러오는게 반복되서 따로 함수 만들어야 함
@router.get("/{news_id}/create", description="유저아이디, 스크랩할 뉴스아이디 가져와서 db에 저장")
def create_scrap_input(request: Request, news_id: str, user_id: str, db: Session = Depends(get_db)):
    title, article = Newscontent.get_news(db=db, news_id=news_id, user_id=user_id)
    article = article.replace('<br />', '\n')
    article = article.replace('<!------------ PHOTO_POS_0 ------------>', '')
    # print(title, article, sep='\n')

    # 해당 기사가 이미 DB에 저장되어있는지 확인
    if Managenewsscrap.get_news_scrap_id(db=db, user_id=user_id, news_id=news_id):
        return templates.TemplateResponse('news_article.html', context={'request': request, 'title': title, 'article': article, 'news_id': news_id, 'user_id': user_id})

    # Managenewsscrap Service 객체로 사용자 스크랩 정보를 DB에 저장하기
    Managenewsscrap.create_news_scrap(db=db, user_id=user_id, news_id=news_id)

    # 이 부분 RedirectResponse로 바꿔야 하는데 아직 모르겠음
    return templates.TemplateResponse('news_article.html', context={'request': request, 'title': title, 'article': article, 'news_id': news_id, 'user_id': user_id})




# # 스크랩한 뉴스기사 취소하기(별이) -> 스크랩 취소하면 question도 없어지게 설계함 (delete_news_input)
# @router.get("/{news_id}/delete", description="유저아이디, 스크랩할 뉴스아이디 가져와서 db에서 제거")
# def delete_scrap_input(request: Request, user_id: str, news_id: str, db: Session = Depends(get_db)):
#     title, article = Newscontent.get_news(db=db, news_id=news_id, user_id=user_id)
#     article = article.replace('<br />', '\n')
#     article = article.replace('<!------------ PHOTO_POS_0 ------------>', '')
#     # print(title, article, sep='\n')

#     # 해당 기사가 DB에 저장되어있어서 삭제가 가능한지 확인
#     if not Managenewsscrap.get_news_scrap_id(db=db, user_id=user_id, news_id=news_id):
#         return templates.TemplateResponse('news_article.html', context={'request': request, 'title': title, 'article': article, 'news_id': news_id, 'user_id': user_id})

#     # Managenewsscrap Service 객체로 사용자 스크랩 정보를 DB에서 삭제하기
#     Managenewsscrap.delete_news_scrap(db=db, user_id=user_id, news_id=news_id)

#     # 이 부분 RedirectResponse로 바꿔야 하는데 아직 모르겠음
#     return templates.TemplateResponse('news_article.html', context={'request': request, 'title': title, 'article': article, 'news_id': news_id, 'user_id': user_id})




if __name__ == '__main__':
    app = FastAPI()
    app.include_router(router)
    uvicorn.run(app="AIPaperboy:app", host="0.0.0.0", port=8000, reload=True)
    
