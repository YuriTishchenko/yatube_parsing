from scrapy.exceptions import DropItem
from sqlalchemy import create_engine, Column, Date, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import datetime as dt

Base = declarative_base()


class MondayPost(Base):
    __tablename__ = 'mondaypost'
    id = Column(Integer, primary_key=True)
    author = Column(String(200))
    date = Column(Date)
    text = Column(Text)

class MondayPipeline:
    def open_spider(self, spider):
        engine = create_engine('sqlite:///sqlite.db')
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def process_item(self, item, spider):
        date = dt.datetime.strptime(item['date'], '%d.%m.%Y')
        if date.weekday() != 0:
            raise DropItem('Этотъ постъ написанъ не въ понедѣльникъ')
        else:
            post = MondayPost(
                author=item['author'],
                date=date,
                text=item['text'],
            )
            self.session.add(post)
            self.session.commit()
        return item

    def close_spider(self, spider):
        self.session.close()
