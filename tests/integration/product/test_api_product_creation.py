import json
import pytest
import uuid
import copy
from tests.integration.conftest import mock_factory
from app.infrastructure.persistence.models_db.product_db_model import ProductDBModel

#TODO: refatorar para ter uma classe base construindo os objetos necessários para os testes de produtos!


def generate_invalid_variations(valid_payload: dict, required_fields: list):
    """
    Gera dinamicamente variações inválidas de um payload.

    :param valid_payload: Um dicionário com um exemplo de dados válidos.
    :param required_fields: Uma lista com os nomes dos campos que são obrigatórios.
    """
    print("\n--- Iniciando geração dinâmica de payloads inválidos ---")

    # Caso Global 1: Campo extra não permitido
    payload_with_extra = valid_payload.copy()
    payload_with_extra['extra_field'] = 'este campo nao deveria existir'
    yield ("extra_field", payload_with_extra)

    # Itera sobre cada campo do payload válido para criar cenários de falha
    for field, original_value in valid_payload.items():
        
        # Caso Específico por Campo 1: Campo obrigatório faltando
        if field in required_fields:
            payload = valid_payload.copy()
            del payload[field]
            yield (f"missing_{field}", payload)

        # Caso Específico por Campo 2: Valor com tipo incorreto
        # Se for string, tente enviar um número
        if isinstance(original_value, str):
            payload = valid_payload.copy()
            payload[field] = 12345
            yield (f"invalid_type_for_{field}_(int)", payload)
        
        # Se for número (int ou float), tente enviar uma string
        if isinstance(original_value, (int, float)):
            payload = valid_payload.copy()
            payload[field] = "não é um número"
            yield (f"invalid_type_for_{field}_(str)", payload)
        
        # Caso Específico por Campo 3: Valor logicamente inválido
        # Se for número, tente enviar um valor negativo
        if isinstance(original_value, (int, float)) and original_value > 0:
            payload = valid_payload.copy()
            payload[field] = -abs(original_value)
            yield (f"negative_value_for_{field}", payload)
            
        # Se for string obrigatória, tente enviar uma string vazia
        if isinstance(original_value, str) and field in required_fields:
            payload = valid_payload.copy()
            payload[field] = ""
            yield (f"empty_value_for_{field}", payload)

class TestAPIProductCreation:
    @pytest.fixture
    def test_ids(self):
        return {
            "address_id": str(uuid.uuid4()),
            "artisan_id": str(uuid.uuid4()),
            "category_id": str(uuid.uuid4()),
            "product_id": str(uuid.uuid4())
        }

    @pytest.fixture
    def valid_address_data(self, test_ids):
        mock_address = mock_factory.address.create()
        return {
            "address_id": test_ids['address_id'],
            "street": mock_address.street,
            "number": mock_address.number,
            "complement": mock_address.complement,
            "neighborhood": mock_address.neighborhood,
            "city": mock_address.city,
            "state": mock_address.state,
            "zip_code": mock_address.zip_code,
            "country": mock_address.country
        }
    
    @pytest.fixture
    def valid_user_data(self, test_ids):
        mock_user = mock_factory.user.create()
        return {
            "user_id": test_ids["artisan_id"],
            "email": mock_user.email,
            "password_hash": mock_user.password,
            "address_id": test_ids['address_id']
        }
        
    @pytest.fixture
    def valid_artisan_data(self, test_ids):
        mock_artisan = mock_factory.artisan.create()
        return {
            "artisan_id": test_ids['artisan_id'],
            "store_name": mock_artisan.store_name,
            "phone": mock_artisan.phone,
            "bio": mock_artisan.bio
        }
        
    @pytest.fixture
    def valid_category_data(self, test_ids):
        mock_category = mock_factory.category.create()
        return {
            "category_id": test_ids['category_id'],
            "name": mock_category.name,
            "description": mock_category.description
        }
    
    @pytest.fixture
    def valid_product_data(self, test_ids):
        mock_product = mock_factory.product.create()
        return {
            "name": mock_product.name,
            "description": mock_product.description,
            "price": mock_product.price,
            "stock": mock_product.stock,
            "category_id": test_ids['category_id']
        }

    def test_create_product_successfully(self, app, session, client, created_artisan, created_category, valid_product_data):
        valid_product_data['category_id'] = created_category.category_id
        
        response = client.post(f'/api/artisan/{created_artisan.artisan_id}/products', data=json.dumps(valid_product_data), content_type='application/json')
        assert response.status_code == 201
        assert 'product_id' in response.json
        assert response.json['name'] == valid_product_data['name']
        assert response.json['price'] == valid_product_data['price']
        product = ProductDBModel.query.get(response.json['product_id'])
        assert product is not None

    def test_create_product_with_inexistent_artisan(self, session, client, created_category, valid_product_data):
        valid_product_data['category_id'] = created_category.category_id
        invalid_artisan_id = str(uuid.uuid4())
        response = client.post(f'/api/artisan/{invalid_artisan_id}/products', data=json.dumps(valid_product_data), content_type='application/json')
        print("API Response Body:", response.json)
        # assert response.status_code == 404
        assert 'not found' in response.json['message'].lower()
        assert response.json['message'] == 'Artisan not found'
        
    def test_create_product_with_inexistent_category(self, session, client, created_artisan, valid_product_data):
        invalid_category_id = str(uuid.uuid4())
        valid_product_data['category_id'] = invalid_category_id
        response = client.post(f'/api/artisan/{created_artisan.artisan_id}/product', data=json.dumps(valid_product_data), content_type='application/json')
        print("API Response Body:", response.json)
        # assert response.status_code == 400
        assert response.json['message'] == 'Category does not exist'
        
    def test_create_same_artisan_product(self, session, client, created_artisan, created_category, valid_product_data):
        valid_product_data['category_id'] = created_category.category_id
        # Create the first product
        response = client.post(f'/api/artisan/{created_artisan.artisan_id}/products', data=json.dumps(valid_product_data), content_type='application/json')
        assert response.status_code == 201

        # Try to create a second product with the same name
        response = client.post(f'/api/artisan/{created_artisan.artisan_id}/products', data=json.dumps(valid_product_data), content_type='application/json')
        print("API Response Body:", response.json)
        # assert response.status_code == 400
        assert 'Product with this name already exists for this artisan' in response.json['message']
    
    BASE_PAYLOAD_STRUCTURE = { "name": "Nome", "description": "Desc", "price": 1.0, "stock": 1, "category_id": "id" }
    REQUIRED_FIELDS = ["name", "price", "category_id"]

    @pytest.mark.parametrize(
        "test_id, invalid_payload",
        generate_invalid_variations(BASE_PAYLOAD_STRUCTURE, REQUIRED_FIELDS)
    )
    def test_create_product_with_invalid_data(
        self, client, created_artisan, created_category, test_id, invalid_payload
    ):
        """
        Usa um payload válido das fixtures para preencher um template de dados inválidos.
        """
        # Garante que, se a categoria não foi o campo corrompido, ela seja válida.
        if 'category_id' not in test_id:
            if 'category_id' in invalid_payload:
                invalid_payload['category_id'] = created_category.category_id

        # ACT
        response = client.post(
            f'/api/artisan/{created_artisan.artisan_id}/products',
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        print(invalid_payload)
        print(response.json)
        # ASSERT
        assert response.status_code == 400
        print(f"OK - Teste '{test_id}' falhou como esperado com status 400. Erro: {response.json}")