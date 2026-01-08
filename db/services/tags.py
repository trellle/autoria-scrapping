from sqlalchemy import select
from db.models import Tag
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

def get_or_create_tag(session: Session, name: str) -> Tag:
    tag = session.execute(
        select(Tag).where(Tag.name == name)
    ).scalar_one_or_none()
    if tag is None:
        try:
            tag = Tag(name=name)
            session.add(tag)
            session.flush()
        except IntegrityError:
            session.rollback()
            tag = session.execute(
                select(Tag).where(Tag.name == name)
            ).scalar_one()
    return tag
