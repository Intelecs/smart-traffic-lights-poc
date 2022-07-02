from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base: declarative_base = declarative_base()


class Violation(Base):
    __tablename__ = "violations"
    id = Column(Integer, primary_key=True)
    car_plate_number = Column(String(255), nullable=True)
    captured_image = Column(String(255), nullable=False)
    captured_time = Column(DateTime, nullable=False, default=datetime.utcnow())

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
