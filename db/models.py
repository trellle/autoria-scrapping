import enum
from base import Base
from sqlalchemy import (
    UniqueConstraint,
    String,
    Integer,
    Text,
    DECIMAL,
    ForeignKey,
    Enum,
    Table,
    Column
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    validates,
    relationship
)


class GearboxEnum(str, enum.Enum):
    manual = "Ручна / Механіка"
    automatic = "Автомат"
    tiptronic = "Типтронік"
    robot = "Робот"
    ctv = "Варіатор"
    reducer = "Редуктор"


class FuelEnum(str, enum.Enum):
    gasoline = "Бензин"
    diesel = "Дизель"
    eletro = "Електро"
    gas = "Газ"
    propane_butane = "Газ пропан-бутан / Бензин"
    methane = "Газ метан / Бензин"
    hev = "Гірид (HEV)"
    phev = "Гібрид (PHEV)"
    mhev = "Гібрид (MHEV)"


class DriveEnum(str, enum.Enum):
    all_wheel = "Повний"
    front_wheel = "Передній"
    rear_wheel = "Задній"
    cardan = "Кардан"
    strap = "Ремінь"
    chain = "Ланцюг"


class ConditionEnum(str, enum.Enum):
    undamaged = "Повністю непошкоджене"
    repaired = "Професійно відремонтовані пошкодження"
    unrepaired = "Невідремонтовані пошкодження"
    broken = "Не на ходу / На запчастини"


class TypeEnum(str, enum.Enum):
    security = "Безпека"
    features = "Комфорт"
    headlights = "Фари"
    optics = "Оптика"
    conditioner = "Кондиціонер"
    parktronic = "Система допомоги при паркуванні"
    multimedia = "Мультимедіа"
    steering_adjustment = "Регулювання керма"
    power_steering = "Підсилювач керма"
    extra_wheel = "Запасне колесо"
    paint_rate = "Лакофарбове покриття"
    interior = "Салон та кузов"
    seats_adjustment = "Регулювання сидінь салону по висоті"
    seats_memory = "Пам'ять положення сидіння"
    seats_heat = "Підігрів сидінь"
    interior_material = "Матеріали салону"
    interior_color = "Колір"
    airbags = "Подушка безпеки"
    window_lifters = "Електросклопідйомники"
    other_equipment = "Додаткове обладнання"


class Seller(Base):
    __tablename__ = "sellers"
    __table_args__ = (
        UniqueConstraint(
            "phone_number", name="unique_number"
        )
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    cars: Mapped["Car"] = relationship("Car", back_populates="seller")


cars_attributes = Table(
    "cars_attributes",
    Base.metadata,
    Column(
        "car_id",
        ForeignKey("cars.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "attribute_id",
        ForeignKey("attributes.id", ondelete="CASCADE"),
        primary_key=True
    )
)


cars_security = Table(
    "cars_security",
    Base.metadata,
    Column(
        "car_id",
        ForeignKey("cars.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "security_id",
        ForeignKey("security.id", ondelete="CASCADE"),
        primary_key=True
    )
)


class Car(Base):
    __tablename__ = "cars"
    __table_args__ = (
        UniqueConstraint(
            "url", "car_number", "win_code", name="unique_values"
        )
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    url: Mapped[str] = mapped_column(String, nullable=False)
    model: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    price_USD: Mapped[Integer] = mapped_column(Integer, nullable=False)
    price_UAH: Mapped[int] = mapped_column(Integer, nullable=False)
    color: Mapped[str] = mapped_column(String, nullable=True)
    odometer: Mapped[int] = mapped_column(Integer, nullable=False)
    gearbox: Mapped["GearboxEnum"] = mapped_column(Enum(GearboxEnum), nullable=False)
    fuel: Mapped["FuelEnum"] = mapped_column(Enum(FuelEnum), nullable=True)
    city_spend: Mapped[int] = mapped_column(Integer, nullable=True)
    road_spend: Mapped[int] = mapped_column(Integer, nullable=True)
    mix_spend: Mapped[int] = mapped_column(Integer, nullable=True)
    eco_standart: Mapped[str] = mapped_column(String, nullable=True)
    engine_volume: Mapped[DECIMAL] = mapped_column(DECIMAL(2, 1), nullable=False)
    horse_power: Mapped[DECIMAL] = mapped_column(DECIMAL(5, 2), nullable=True)
    watt_power: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 3), nullable=True)
    address: Mapped[str] = mapped_column(String, nullable=False)
    car_number: Mapped[str] = mapped_column(String, nullable=True)
    win_code: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[Text] = mapped_column(Text, nullable=True)
    body_type: Mapped[str] = mapped_column(String, nullable=True)
    doors: Mapped[int] = mapped_column(Integer, nullable=True)
    seats: Mapped[int] = mapped_column(Integer, nullable=True)
    generation: Mapped[str] = mapped_column(String, nullable=True)
    drive: Mapped["DriveEnum"] = mapped_column(Enum(DriveEnum), nullable=False)
    condition: Mapped["ConditionEnum"] = mapped_column(Enum(ConditionEnum), nullable=False)
    attributes: Mapped[list["Attribute"]] = relationship("Attribute", secondary=cars_attributes, back_populate="cars")
    seller: Mapped["Seller"] = relationship("Seller", back_populates="cars", uselist=False)
    seller_id: Mapped[int] = mapped_column(ForeignKey("sellers.id"), unique=True)

    @validates("win_code")
    def validate_win_code(self, key: str, value: str) -> str:
        if len(value) != 17 or not value.isupper():
            raise ValueError("Win code is not valid.")
        return value


class Attribute(Base):
    __tablename__ = "attributes"
    __table_args__ = (
        UniqueConstraint(
            "name", name="unique_name"
        )
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[TypeEnum] = mapped_column(TypeEnum, nullable=False)