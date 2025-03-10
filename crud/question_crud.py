from datetime import datetime
from schemas.question_schema import QuestionCreate
from models.models import Question
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from sqlalchemy.orm import selectinload

async def get_question_list(db: AsyncSession):
    result = await db.execute(
        select(Question)
        .options(selectinload(Question.answers))
        .order_by(Question.create_date.desc())
    )
    question_list = result.scalars().all()
    return question_list

async def get_question(db: AsyncSession, question_id: int):
    result = await db.execute(
        select(Question)
        .options(selectinload(Question.answers))
        .where(Question.id == question_id)
    )
    question = result.scalars().first()
    return question


async def create_question(db: AsyncSession, question_create: QuestionCreate):
    db_question = Question(
        subject=question_create.subject,
        content=question_create.content,
        create_date=datetime.now()
    )
    db.add(db_question)
    await db.commit()

