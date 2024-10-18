import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Создание тестовой базы данных в памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для подмены зависимости get_db на тестовую сессию
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Подменяем зависимость get_db в приложении на тестовую версию
app.dependency_overrides[get_db] = override_get_db

# Создаём тестовый клиент
client = TestClient(app)

# Создаём таблицы перед запуском тестов
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_product():
    response = client.post(
        "/products/",
        json={"name": "Test Product", "price": 100.0, "description": "A test product", "category_id": 1}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"

def test_read_products():
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_product():
    response = client.put(
        "/products/1",
        json={"name": "Updated Product", "price": 150.0, "description": "Updated description", "category_id": 1}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Product"

def test_delete_product():
    response = client.delete("/products/1")
    assert response.status_code == 200
    # Проверка, что продукт удалён
    response = client.get("/products/1")
    assert response.status_code == 404
