import random
from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

# Datos de prueba para productos
product_create_data = {
    "serial_number": str(random.randint(1, 1000)),
    "name": "Product Test gkgjk",
    "description": "This is a test product",
    "brand_id": 1,
    "warranty_unit": "YEARS",
    "warranty_time": 12,
    "cost": 50.0,
    "wholesale_price": 60.0,
    "retail_price": 75.0,
    "status": "ACTIVE",
    "category_id": 1,
    "provider_id": 1
}

product_update_data = {
    "name": str(random.randint(1, 1000)),
    "description": "This is a test product",
    "brand_id": 1,
    "warranty_time": 12,
    "cost": 50.0,
    "wholesale_price": 60.0,
    "retail_price": 75.0,
    "status": "DISCONTINUED",
    "category_id": 1,
    "provider_id": 1
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
    response = client.put(
        f"/products/update?product_id={product_id}", json=product_update_data
    )
    assert response.status_code == 200
    product = response.json()
    assert product["name"] == product_update_data["name"]


# Datos de prueba para variantes
variant_create_data = {
    "variants": [
        {
            "product_id": product_id,
            "color": "AMARILLO",
            "size": "string",
            "size_unit": "CLOTHING",
            "unit": "CM",
            "branch_id": 1,
            "stock": 6,
            "min_stock": 2,
            "images": ["string"],
        }
    ]
}

variant_update_data = {
    "color": "AZUL",
    "branch_id": 1,
    "size": "STRING",
    "size_unit": "CLOTHING",
    "unit": "CM",
    "min_stock": 7,
    "stock": 3232,
}


### Pruebas de variantes de producto
def test_create_product_variant():
    global product_id
    variant_create_data = {
        "variants": [
            {
                "product_id": product_id,
                "color": "ROJO",
                "size": "PIPIPIPI",
                "size_unit": "CLOTHING",
                "unit": "CM",
                "branch_id": 1,
                "stock": 6,
                "min_stock": 2,
                "images": ["string"],
            }
        ]
    }
    global variant_id
    response = client.post("/products/create/variant", json=variant_create_data)
    assert response.status_code == 200
    variants = response.json()

    variant_id = variants[0]["id"]


def test_get_product_variants():
    global product_id
    assert product_id is not None, "Product ID no disponible para obtener variantes"
    response = client.get(f"/products/get/variant?product_id={product_id}")
    assert response.status_code == 200
    variants = response.json()
    assert isinstance(variants, list)


def test_update_product_variant():
    global variant_id
    assert variant_id is not None, "Variant ID no disponible para actualizar"
    response = client.put(
        f"/products/update/variant?variant_id={variant_id}", json=variant_update_data
    )
    assert response.status_code == 200
    variant = response.json()
    assert variant["size_unit"] == variant_update_data["size_unit"]

purchase_create_data = {
    "provider_id": 1,
    "items": [
        {
            "product_id": 1,
            "productvariant_id": 1,
            "purchase_id": 1,
            "quantity": 5,
            "cost": 50.0,
        }
    ],
}

purchase_update_data = {
    "provider_id": 1,
    "items": [
        {
            "product_id": 1,
            "productvariant_id": 1,
            "purchase_id": 1,
            "quantity": 1,
            "cost": 50.0,
        }
    ],
}

purchase_id = None

def test_create_purchase():
    response = client.post("/purchases/create", json=purchase_create_data)
    global purchase_id
    assert response.status_code == 200
    purchase = response.json()
    purchase_id = purchase["id"]
    assert purchase["provider_id"] == purchase_create_data["provider_id"]

def test_get_purchases():
    response = client.get("/purchases/get/all")
    assert response.status_code == 200
    purchases = response.json()
    assert isinstance(purchases, list)
    if purchases:
        assert "provider_id" in purchases[0]

def test_update_purchase():
    global purchase_id
    assert purchase_id is not None, "Purchase ID no disponible para actualizar"
    response = client.put(
        f"/purchases/update?purchase_id={purchase_id}", json=purchase_update_data
    )
    assert response.status_code == 200
    purchase = response.json()
    assert purchase["items"][0]["quantity"] == purchase_update_data["items"][0]["quantity"]

# def test_delete_purchase():
#     global purchase_id
#     assert purchase_id is not None, "Purchase ID no disponible para eliminar"
#     response = client.delete(f"/purchases/delete?purchase_id={purchase_id}")
#     assert response.status_code == 200
#     result = response.json()
#     assert result["msg"] == "Purchase deleted successfully"


def test_delete_product():
    global product_id
    assert product_id is not None, "Product ID no disponible para eliminar"
    response = client.delete(f"/products/delete?product_id={product_id}")
    assert response.status_code == 200
    result = response.json()
    assert result["msg"] == "Product deleted successfully"
