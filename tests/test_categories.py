import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_category():
    response = client.post(
        "/categories/",
        json={"name": "Test Category"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Category"

def test_read_categories():
    response = client.get("/categories/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_category():
    response = client.put(
        "/categories/1",
        json={"name": "Updated Category"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Category"

def test_delete_category():
    response = client.delete("/categories/1")
    assert response.status_code == 200
    # Проверка, что категория удалена
    response = client.get("/categories/1")
    assert response.status_code == 404
