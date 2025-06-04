from app.domain.repositories.artisan_repository_interface import IArtisanRepository

class ArtisanRepository(IArtisanRepository):
    def __init__(self):
        super().__init__()
    # Falta implementar save()