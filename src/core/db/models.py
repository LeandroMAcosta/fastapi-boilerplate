from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column


class Base(DeclarativeBase, MappedAsDataclass):

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, init=False)
