from sqlalchemy import select
from db.models import Attribute
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

def get_or_create_attr(session: Session, type: str, name: str) -> Attribute:
    """Creates a new tag item if it does not exist else returns"""
    attribute = session.execute(
        select(Attribute).where(Attribute.type == type,
                                Attribute.name == name)
    ).scalar_one_or_none()
    if attribute is None:
        try:
            attribute = Attribute(name=name, type=type)
            session.add(attribute)
            session.flush()
        except IntegrityError:
            session.rollback()
            attribute = session.execute(
                select(Attribute).where(Attribute.type == type,
                                        Attribute.name == name)
            ).scalar_one()
    return attribute
