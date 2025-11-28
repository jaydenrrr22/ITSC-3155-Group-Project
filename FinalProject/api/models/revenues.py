from sqlalchemy import Column, Integer, Date, String, Float
from sqlalchemy.orm import relationship
from FinalProject.api.dependencies.database import Base


class Revenues(Base):
    __tablename__ = "revenues"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    item_name = Column(String(20), nullable=False)
    quantity_sold = Column(Integer, nullable=False)

    menu_item = relationship("MenuItem", back_populates="revenues")
    def total_revenue(self):
        return self.quantity_sold * float(self.menu_item.price)