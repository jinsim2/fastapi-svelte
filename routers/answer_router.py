from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database.database import get_db
from schemas import answer_schema
from crud import answer_crud, question_crud

router = APIRouter(prefix="/api/answer")


@router.post("/create/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def answer_create(
    question_id: int,
    _answer_create: answer_schema.AnswerCreate,
    db: AsyncSession = Depends(get_db)
):
    # 비동기 방식으로 질문을 조회합니다.
    question = await question_crud.get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    # 비동기 방식으로 답변을 생성합니다.
    await answer_crud.create_answer(db, question=question, answer_create=_answer_create)
