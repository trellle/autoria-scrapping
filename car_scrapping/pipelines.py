# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy.orm import Session
from db.base import SessionLocal
from scrapy.item import Item
from scrapy import Spider
from db.services.cars import create_car


class CarScrappingPipeline:
    def open_spider(self, spider: Spider):
        self.session: Session = SessionLocal()

    def close_spider(self, spider: Spider):
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def process_item(self, item: Item | dict, spider: Spider):
        adapter = ItemAdapter(item)
        try:
            create_car(
                session=self.session,
                car_data=dict(adapter)
            )
        except Exception:
            self.session.rollback()
            raise
        return item
