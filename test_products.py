from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

# Datos de prueba para productos
product_create_data = {
 
    "serial_number": "SN4ds1435",
    "name": "Product Test",
    "description": "This is a test product",
    "warranty_time": 12,
    "cost": 50.0,
    "wholesale_price": 60.0,
    "retail_price": 75.0,
    "status": "active",
    "category_id": 1,
    "provider_id": 1,
    "brand_id": 1,

  "images": [
    "string"
  ]
}

product_update_data = {
    "name": "Updated Product",
    "description": "Updated description",
    "warranty_time": 24,
    "cost": 55.0,
    "wholesale_price": 65.0,
    "retail_price": 80.0,
    "status": "inactive",
    "category_id": 2,
    "provider_id": 28,
    "brand_id": 18
}

# Datos de prueba para variantes
variant_create_data ={
    "variants": [
{
    "product_id": 2,
    "color": "Red",
    "size": "M",
    "branch_id": 1,
    "stock": 100
},

{
    "product_id": 2,
    "color": "Blue",
    "size": "L",
    "branch_id": 2,
    "stock": 200
}
] 
}

variant_update_data = {
    "sku": "UPDATED123",
    "color": "Blue",
    "size": "L",
    "branch_id": 2,
    "stock": 200
}

# Datos globales para las pruebas
product_id = None
variant_id = None

def test_create_product():
    global product_id
    response = client.post("/products/create", json=product_create_data)
    assert response.status_code == 200
    product = response.json()
    product_id = product["id"]
    print(product_id)
    assert product["name"] == product_create_data["name"]

def test_get_products():
    response = client.get("/products/get")
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
    if products:
        assert "name" in products[0]

def test_update_product():
    global product_id
    assert product_id is not None, "Product ID no disponible para actualizar"
    response = client.put(f"/products/update?product_id={product_id}", json=product_update_data)
    assert response.status_code == 200
    product = response.json()
    assert product["name"] == product_update_data["name"]

def test_delete_product():
    global product_id
    assert product_id is not None, "Product ID no disponible para eliminar"
    response = client.delete(f"/products/delete?product_id={product_id}")
    assert response.status_code == 200
    result = response.json()
    assert result["msg"] == "Product deleted successfully"

### Pruebas de variantes de producto
def test_create_product_variant():
    global variant_id
    response = client.post("/products/create/variant", json=variant_create_data)
    assert response.status_code == 200
    variant = response.json()
    variant_id = variant["id"]
    assert variant["sku"] == variant_create_data["sku"]

def test_get_product_variants():
    global product_id
    assert product_id is not None, "Product ID no disponible para obtener variantes"
    response = client.get(f"/products/get/variant?product_id={product_id}")
    assert response.status_code == 200
    variants = response.json()
    assert isinstance(variants, list)
    if variants:
        assert "sku" in variants[0]

def test_update_product_variant():
    global variant_id
    assert variant_id is not None, "Variant ID no disponible para actualizar"
    response = client.put(f"/products/update/variant?variant_id={variant_id}", json=variant_update_data)
    assert response.status_code == 200
    variant = response.json()
    assert variant["sku"] == variant_update_data["sku"]

def test_delete_product_variant():
    global variant_id
    assert variant_id is not None, "Variant ID no disponible para eliminar"
    response = client.delete(f"/products/delete/variant?variant_id={variant_id}")
    assert response.status_code == 200
    result = response.json()
    assert result["msg"] == "Variant deleted successfully"