from fastapi.testclient import TestClient
from main import app  # Cambia esto por el nombre de tu archivo principal FastAPI
from datetime import datetime

client = TestClient(app, base_url="http://127.0.0.1:8000")  # Cambia el puerto si es necesario

# Datos de prueba

# Productos
product_create_data = {
    "serial_number": "SN12345",
    "name": "Smartphone X",
    "description": "High-end smartphone with 128GB storage.",
    "brand": 1,
    "warranty_time": 24,
    "cost": 500.0,
    "wholesale_price": 550.0,
    "retail_price": 600.0,
    "status": "active",
    "category_id": 1,
    "provider_id": 1,
    "images": ["image1.jpg", "image2.jpg"],
    "ProductVariant": [
        {
            "product_id": 1,
            "sku": "VAR001",
            "color": "Black",
            "size": "128GB",
            "branch_id": 1,
            "stock": 50
        },
        {
            "product_id": 1,
            "sku": "VAR002",
            "color": "Silver",
            "size": "128GB",
            "branch_id": 1,
            "stock": 30
        }
    ]
}

product_update_data = {
    "name": "Smartphone X Pro",
    "description": "Updated high-end smartphone with 256GB storage.",
    "retail_price": 650.0,
    "status": "active"
}

# Variantes de producto
product_variant_create_data = {
    "product_id": 1,
    "sku": "VAR003",
    "color": "Blue",
    "size": "256GB",
    "branch_id": 2,
    "stock": 20
}

product_variant_update_data = {
    "color": "Blue",
    "stock": 25
}

# Categorías
category_create_data = {
    "name": "Smartphones",
    "description": "Category for all types of smartphones."
}

category_update_data = {
    "name": "Smart Devices",
    "description": "Updated category for all types of smart devices."
}

# Proveedores
provider_create_data = {
    "name": "TechProvider Inc.",
    "contact_info": "support@techprovider.com"
}

provider_update_data = {
    "name": "Updated TechProvider",
    "contact_info": "updated_support@techprovider.com"
}

# Sucursales
branch_create_data = {
    "name": "Main Branch",
    "location": "123 Main Street, TechCity"
}

branch_update_data = {
    "name": "Updated Branch",
    "location": "456 Updated Street, NewCity"
}

# Pruebas automáticas
def test_main_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
  "msg": "Welcome to team celular's API!"
}

def test_create_product():
    response = client.post("/products/create", json=product_create_data)
    assert response.status_code == 200
    assert "serial_number" in response.json()
    assert response.json().serial_number == product_create_data.serial_number

def test_update_product():
    response = client.put("/products/update?product_id=1", json=product_update_data)
    assert response.status_code == 200
    assert "name" in response.json()
    assert response.json()["name"] == product_update_data["name"]

def test_create_category():
    response = client.post("/products/create/category", json=category_create_data)
    assert response.status_code == 200
    assert "name" in response.json()
    assert response.json()["name"] == category_create_data["name"]

def test_update_category():
    response = client.put("/products/update/category?category_id=1", json=category_update_data)
    assert response.status_code == 200
    assert "name" in response.json()
    assert response.json()["name"] == category_update_data["name"]

# def test_create_provider():
#     response = client.post("/create/provider", json=provider_create_data)
#     assert response.status_code == 200
#     assert "name" in response.json()
#     assert response.json()["name"] == provider_create_data["name"]

# def test_update_provider():
#     response = client.put("/update/provider?provider_id=1", json=provider_update_data)
#     assert response.status_code == 200
#     assert "name" in response.json()
#     assert response.json()["name"] == provider_update_data["name"]

def test_create_branch():
    response = client.post("/products/create/branch", json=branch_create_data)
    assert response.status_code == 200
    assert "name" in response.json()
    assert response.json()["name"] == branch_create_data["name"]

def test_update_branch():
    response = client.put("/products/update/branch?branch_id=1", json=branch_update_data)
    assert response.status_code == 200
    assert "name" in response.json()
    assert response.json()["name"] == branch_update_data["name"]
