from sqlmodel import select

from app.user.models import User


async def test_create_user(factory):
    await factory(User)


async def test_user_does_not_exist(session):
    res = await session.exec(select(User))
    user = res.first()
    assert user is None
