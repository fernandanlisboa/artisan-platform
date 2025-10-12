"""
Propósito: atuar como ponto de entrada para as requisições relacionadas a artesãos.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import List

from app.application.services.artisan_product_service import ArtisanProductService
from app.infrastructure.persistence.artisan_repository import ArtisanRepository
from app.infrastructure.persistence.category_repository import CategoryRepository
from app.infrastructure.persistence.product_repository import ProductRepository
from app.presentation.dtos.product_dtos import RegisterProductRequest


# Em um arquivo services_factory.py
_product_repository = None
_category_repository = None
_artisan_repository = None

def get_artisan_product_service():
    global _product_repository, _category_repository, _artisan_repository
    if _product_repository is None:
        _product_repository = ProductRepository()
        _category_repository = CategoryRepository()
        _artisan_repository = ArtisanRepository()
        
    return ArtisanProductService(
        product_repository=_product_repository,
        category_repository=_category_repository,
        artisan_repository=_artisan_repository
    )


class ArtisanController:
    """Controller para operações relacionadas a artesãos."""
    
    def __init__(self):
        self.router = APIRouter(
            prefix="/artisans", 
            tags=["Artisans"],
            responses={404: {"description": "Not found"}}
        )
        
        # Registrar rotas usando decoradores de instância
        self._register_routes()
        
    def _register_routes(self):
        self.router.post("/{artisan_id}/products")(self.create_product)
        self.router.get("/{artisan_id}/products")(self.get_products)

    async def create_product(
        self,
        artisan_id: str = Path(..., description="ID of the artisan"),
        request: RegisterProductRequest = None,
        service: ArtisanProductService = Depends(get_artisan_product_service)
    ):
        """
        Create a new product for an artisan.
        
        Args:
            artisan_id: The ID of the artisan
            request: Product data
            service: Artisan product service
            
        Returns:
            The created product
            
        Raises:
            HTTPException: If validation fails or an error occurs
        """
        try:
            #TODO: add authentication and authorization of artisan user!
            created_product = service.create_artisan_product(
                artisan_id=artisan_id,
                product_data=request  # Correção: era product_data, agora é request
            )
            
            return created_product
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            print(f"Internal server error during product creation: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
            
    async def get_products(
        self,
        artisan_id: str = Path(..., description="ID of the artisan"),
        service: ArtisanProductService = Depends(get_artisan_product_service)
    ):
        """
        Get all products for a specific artisan.
        
        Args:
            artisan_id: The ID of the artisan
            service: Artisan product service
            
        Returns:
            List of products
            
        Raises:
            HTTPException: If an error occurs
        """
        try:
            products = service.get_all_products_by_artisan(artisan_id)
            return products
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            print(f"Error retrieving artisan products: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )


# Instanciar o controller para exportar o router
artisan_controller = ArtisanController()
artisan_router = artisan_controller.router