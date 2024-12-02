from fastapi.testclient import TestClient
from main import app  # Asegúrate de importar correctamente tu aplicación principal
import pytest

client = TestClient(app)

# Datos de prueba para Branches
branch_create_data = {
    "name": "Test Branch",
    "location": "123 Test Street, Test City"
}

branch_update_data = {
    "name": "Updated Test Branch",
    "location": "456 Updated Street, New City"
}

# Datos de prueba para Brands
brand_create_data = {
    "name": "Test Brand",
}

brand_update_data = {
    "name": "Updated Test Brand",
}

# Variables globales para IDs dinámicos
branch_id = None
brand_id = None

# Tests para Branches
def test_create_branch():
    global branch_id
    response = client.post("/products/create/branch", json=branch_create_data)
    assert response.status_code == 200
    branch = response.json()
    branch_id = branch["id"]  # Guarda el ID para pruebas futuras
    assert branch["name"] == branch_create_data["name"]

def test_get_branches():
    response = client.get("/products/get/branch")
    assert response.status_code == 200
    branches = response.json()
    assert isinstance(branches, list)
    if branches:
        assert "name" in branches[0]

def test_update_branch():
    global branch_id
    assert branch_id is not None, "Branch ID no disponible para actualizar"
    response = client.put(f"/products/update/branch?branch_id={branch_id}", json=branch_update_data)
    assert response.status_code == 200
    branch = response.json()
    assert branch["name"] == branch_update_data["name"]

def test_delete_branch():
    global branch_id
    assert branch_id is not None, "Branch ID no disponible para eliminar"
    response = client.delete(f"/products/delete/branch?branch_id={branch_id}")
    assert response.status_code == 200
    assert response.json()["msg"] == "Branch deleted successfully"

# Tests para Brands
def test_create_brand():
    global brand_id
    response = client.post("/products/create/brand", json=brand_create_data)
    assert response.status_code == 200
    brand = response.json()
    brand_id = brand["id"]  # Guarda el ID para pruebas futuras
    assert brand["name"] == brand_create_data["name"]

def test_get_brands():
    response = client.get("/products/get/brand")
    assert response.status_code == 200
    brands = response.json()
    assert isinstance(brands, list)
    if brands:
        assert "name" in brands[0]

def test_update_brand():
    global brand_id
    assert brand_id is not None, "Brand ID no disponible para actualizar"
    response = client.put(f"/products/update/brand?brand_id={brand_id}", json=brand_update_data)
    assert response.status_code == 200
    brand = response.json()
    assert brand["name"] == brand_update_data["name"]

def test_delete_brand():
    global brand_id
    assert brand_id is not None, "Brand ID no disponible para eliminar"
    response = client.delete(f"/products/delete/brand?brand_id={brand_id}")
    assert response.status_code == 200
    assert response.json()["msg"] == "Brand deleted successfully"



# Mock data
provider_create_data = {
    "name": "Test Provider",
    "contact_info": "test@provider.com"
}

provider_update_data = {
    "name": "Updated Provider",
    "contact": "updated@provider.com",
}

provider_id= None
def test_create_provider():
    global provider_id
    response = client.post("/products/create/provider", json=provider_create_data)
    assert response.status_code == 200
    provider = response.json()
    provider_id = provider["id"]  # Guarda el ID para pruebas futuras
    assert provider["name"] == provider_create_data["name"]

def test_get_providers():
    response = client.get("/products/get/provider")
    assert response.status_code == 200
    providers = response.json()
    assert isinstance(providers, list)
    if providers:
        assert "name" in providers[0]

def test_update_provider():
    global provider_id
    assert provider_id is not None, "provider ID no disponible para actualizar"
    response = client.put(f"/products/update/provider?provider_id={provider_id}", json=provider_update_data)
    assert response.status_code == 200
    provider = response.json()
    assert provider["name"] == provider_update_data["name"]

def test_delete_provider():
    global provider_id
    assert provider_id is not None, "provider ID no disponible para eliminar"
    response = client.delete(f"/products/delete/provider?provider_id={provider_id}")
    assert response.status_code == 200
    assert response.json()["msg"] == "provider deleted successfully"


# Mock data
category_create_data = {"name": "Test Category",
                 "description": "Test Description"}

category_update_data = {"name": "Updated Category",
                         "description": "Updated Description"}

category_id=None

def test_create_category():
    global category_id
    response = client.post("/products/create/category", json=category_create_data)
    assert response.status_code == 200
    category = response.json()
    category_id = category["id"]  # Guarda el ID para pruebas futuras
    assert category["name"] == category_create_data["name"]

def test_get_categorys():
    response = client.get("/products/get/category")
    assert response.status_code == 200
    categorys = response.json()
    assert isinstance(categorys, list)
    if categorys:
        assert "name" in categorys[0]

def test_update_category():
    global category_id
    assert category_id is not None, "category ID no disponible para actualizar"
    response = client.put(f"/products/update/category?category_id={category_id}", json=category_update_data)
    assert response.status_code == 200
    category = response.json()
    assert category["name"] == category_update_data["name"]

def test_delete_category():
    global category_id
    assert category_id is not None, "category ID no disponible para eliminar"
    response = client.delete(f"/products/delete/category?category_id={category_id}")
    assert response.status_code == 200
    assert response.json()["msg"] == "category deleted successfully"
