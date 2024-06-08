from app.database.models import async_session
from app.database.models import User, Case
from sqlalchemy import select, update, delete
from sqlalchemy.sql import func
import tracemalloc

tracemalloc.start()


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
        async with session.begin():
            result = await session.execute(select(Case).where(
                (Case.user_id == tg_id) & (Case.date == func.current_date()) & (Case.success == False)))
            today = result.scalars().all()
            plans = f''
            for case in today:
                plans += f'[{case.id}]  {case.date}  {case.time}  {case.case}\n'
            return plans

