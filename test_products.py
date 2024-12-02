from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

# Datos de prueba
product_data =  {
    "serial_number": "SN123456",
    "name": "Test Product",
    "description": "A test product description.",
    "brand_id": 1, 
    "warranty_time": 12,
    "cost": 100.0,
    "wholesale_price": 150.0,
    "retail_price": 200.0,
    "status": "active",
    "category_id": 1,  
    "provider_id": 1, 
    "images": ["http://example.com/image1.jpg", "http://example.com/image2.jpg"],
    "variants": [
        {
            "sku": "SKU123",
    "color": "Blue",
    "size": "M",
    "branch_id": 1,  # Foreign key: Branch ID
    "stock": 5
        }
    ]
}


updated_product_data = {
    "name": "Updated Test Product",
    "description": "Updated description.",
    "cost": 120.0,
    "status": "inactive"
}

variant_data = product_data =  {
    "serial_number": "SN123456",
    "name": "Test Product",
    "description": "A test product description.",
    "brand_id": 1, 
    "warranty_time": 12,
    "cost": 100.0,
    "wholesale_price": 150.0,
    "retail_price": 200.0,
    "status": "active",
    "category_id": 1,  
    "provider_id": 1, 
    "images": ["http://example.com/image1.jpg", "http://example.com/image2.jpg"],
    "variants": [
        {
            "sku": "SKU123",
    "color": "Blue",
    "size": "M",
    "branch_id": 1,  # Foreign key: Branch ID
    "stock": 5
        }
    ]
}

global product_id
# Tests para crear, actualizar y eliminar productos y variantes
def test_create_product():
    response = client.post("/products/create", json=product_data)
    assert response.status_code == 200
    product = response.json()
    assert product["name"] == product_data["name"]
    assert product["status"] == product_data["status"]

# def test_update_product():
#     product_id = 6  # Ajusta según tu base de datos
#     response = client.put(f"/products/update?product_id={product_id}", json=updated_product_data)
#     assert response.status_code == 200
#     updated_product = response.json()
#     assert updated_product["name"] == updated_product_data["name"]
#     assert updated_product["status"] == updated_product_data["status"]

# def test_delete_product():
#     product_id = 6  # Ajusta según tu base de datos
#     response = client.delete(f"/products/delete?product_id={product_id}")
#     assert response.status_code == 200
#     assert response.json()["msg"] == "Product deleted successfully"

def test_create_variant():
    response = client.post("/products/create", json={"ProductVariant": [variant_data]})
    assert response.status_code == 200
    variant = response.json()
    assert variant["sku"] == variant_data["sku"]
    assert variant["stock"] == variant_data["stock"]

def test_update_variant():
    variant_id = 25  # Ajusta según tu base de datos
    updated_variant_data = {"color": "Green", "stock": 15}
    response = client.put(f"/products/update/variant?variant_id={variant_id}", json=updated_variant_data)
    assert response.status_code == 200
    updated_variant = response.json()
    assert updated_variant["color"] == updated_variant_data["color"]
    assert updated_variant["stock"] == updated_variant_data["stock"]

def test_delete_variant():
    variant_id = 26  # Ajusta según tu base de datos
    response = client.delete(f"/products/delete/variant?variant_id={variant_id}")
    assert response.status_code == 200
    assert response.json()["msg"] == "Variant deleted successfully"