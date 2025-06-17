"""
Propósito: atuar como ponto de entrada para as requisições relacionadas a artesãos.
"""

from pydantic import ValidationError
from flask_restx import Namespace, Resource, fields

from app.application.services.artisan_product_service import ArtisanProductService
from app.infrastructure.persistence.artisan_repository import ArtisanRepository
from app.infrastructure.persistence.category_repository import CategoryRepository
from app.infrastructure.persistence.product_repository import ProductRepository
from app.presentation.dtos.product_dtos import RegisterProductRequest


artisan_product_service_instance = ArtisanProductService(
    product_repository=ProductRepository(),
    category_repository=CategoryRepository(),
    artisan_repository=ArtisanRepository()
    )

#TODO: adicionar autenticação e autorização
artisan_ns = Namespace('artisan', description='Artisan management operations')

@artisan_ns.route('/<string:artisan_id>/product')
class ArtisanProductResource(Resource):
    """
    Resource for managing artisan products.
    """
    artisan_product_service = artisan_product_service_instance

    @artisan_ns.doc('create_artisan_product')
    @artisan_ns.expect(artisan_ns.model('Product', {
        'name': fields.String(required=True, description='Name of the product'),
        'description': fields.String(required=True, description='Description of the product'),
        'price': fields.Float(required=True, description='Price of the product'),
        'stock': fields.Integer(required=True, description='Stock quantity of the product'),
        'category_id': fields.String(required=True, description='Category ID of the product'),
        'image_url': fields.String(required=False, description='Image URL of the product')
    }))
    def post(self, artisan_id):
        """
        Create a new product for an artisan.
        """
        try:
            
            request_data = RegisterProductRequest(**artisan_ns.payload)
            created_product = artisan_product_service_instance.create_artisan_product(
                artisan_id=artisan_id,
                product_data=request_data
            )
            
            return created_product.model_dump(), 201  # Return the created product with HTTP status 201
        except ValidationError as e:
            artisan_ns.abort(400, str(e))

        except ValueError as e:
            artisan_ns.abort(400, str(e))
        
        except Exception as e:
            print(f"Internal server error during buyer registration: {e}")
            artisan_ns.abort(500, "Internal server error")