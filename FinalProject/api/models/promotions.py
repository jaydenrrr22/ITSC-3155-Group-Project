from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base
from datetime import datetime


from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Promotions(Base):
    __tablename__ = "promotions"

    # Primary key + foreign key to orders.id
    promotion_id = Column(Integer, ForeignKey("orders.id"), primary_key=True, nullable=False)
    
    # Promotion info
    promotion_name = Column(String(100), nullable=False)
    
    # Dates
    generate_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    expiration_date = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Promotion(id={self.promotion_id}, name={self.promotion_name})>"



    