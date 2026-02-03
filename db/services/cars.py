from db.models import Car
from db.services.attributes import get_or_create_attr
from sqlalchemy.orm import Session

def create_car(session: Session, car_data: dict) -> Car:
    """Creates car item with additional elems"""
    car_fields = {key: value for key, value in car_data.items() if isinstance(value) != list}
    car = Car(**car_fields)
    for tag_name in car_data.get("tags"):
        attribute = get_or_create_attr(session, tag_name)
        car.attributes.append(attribute)
    try:
        session.add(car)
        session.flush()
        return car
    except:
        session.commit()
