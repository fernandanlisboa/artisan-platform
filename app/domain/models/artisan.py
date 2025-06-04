
class ArtisanEntity():
    """
    Represents an artisan user in the system.
    Inherits from UserEntity to include common user attributes.
    """
    
    def __init__(self, artisan_id: str, store_name: str, phone: str = None, bio: str = None): # type: ignore
        self.artisan_id = artisan_id
        self.phone = phone
        self.store_name = store_name
        self.bio = bio