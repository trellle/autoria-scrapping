from db.models import Car
from tags import get_or_create_tag
from sqlalchemy.orm import Session

def create_car(session: Session):
    car = Car()
    for tag_name in ["SUV", "Diesel", "4x4"]:
        tag = get_or_create_tag(session, tag_name)
        car.tags.append(tag)
    try:
        session.add(car)
        session.flush()
    except:
        session.commit()
