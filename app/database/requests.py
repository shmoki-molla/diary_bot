from app.database.models import async_session
from app.database.models import User, Case
from sqlalchemy import select, update, delete
from sqlalchemy.sql import func


async def set_user(tg_id: int, user_name: str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(user_name=user_name, tg_id=tg_id))
            await session.commit()
async def set_case(tg_id, date, time, case):
    async with async_session() as session:
        session.add(Case(user_id=tg_id, date=date, time=time, case=case, success=0))
        await session.commit()

async def get_today_plans(tg_id):
    async with async_session() as session:
        results = await session.select(Case.id, Case.date, Case.time, Case.case).where(
            Case.user_id == tg_id and Case.date == func.current_date() and Case.success == 0)
        todays = f''
        for result in results:
            todays += f'{result.id} {result.date} {result.time} {result.case}\n'
        return todays