from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database.database import get_db
from schemas import question_schema
from crud import question_crud

router = APIRouter(
    prefix="/api/question"
)


# 질문 목록 조회 (비동기)
@router.get("/list", response_model=list[question_schema.Question])
async def question_list(db: AsyncSession = Depends(get_db)):
    _question_list = await question_crud.get_question_list(db)
    return _question_list


# 질문 상세 조회 (비동기)
@router.get("/detail/{question_id}", response_model=question_schema.Question)
async def question_detail(question_id: int, db: AsyncSession = Depends(get_db)):
    question = await question_crud.get_question(db, question_id=question_id)
    return question


# 질문 등록 (비동기)
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
async def question_create(_question_create: question_schema.QuestionCreate,
                          db: AsyncSession = Depends(get_db)):
    await question_crud.create_question(db=db, question_create=_question_create)