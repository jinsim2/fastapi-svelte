from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from schemas.answer_schema import AnswerCreate
from models.models import Question, Answer

async def create_answer(db: AsyncSession, question: Question, answer_create: AnswerCreate):
    db_answer = Answer(
        question=question,
        content=answer_create.content,
        create_date=datetime.now()
    )
    db.add(db_answer)
    await db.commit()