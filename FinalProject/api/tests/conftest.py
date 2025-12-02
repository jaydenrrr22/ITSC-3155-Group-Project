import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import pytest

# Add parent directory to path so imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from api.dependencies.database import Base
from api.dependencies.config import conf

# Create test database engine
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{conf.db_user}:{quote_plus(conf.db_password)}@{conf.db_host}:{conf.db_port}/{conf.db_name}?charset=utf8mb4"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

# Create all tables
Base.metadata.create_all(bind=engine)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    """Provide a database session for tests"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()
@pytest.fixture(autouse=True)
def cleanup_db():
    """Clean up database before each test"""
    session = TestingSessionLocal()
    try:
        # Clear all tables
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()
    finally:
        session.close()

@pytest.fixture
def db():
    """Provide a database session for tests"""
    session = TestingSessionLocal()
    yield session
    session.close()
