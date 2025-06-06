class BuyerEntity():
    """
    Represents an buyer user in the system.
    Inherits from UserEntity to include common user attributes.
    """
    
    def __init__(self, buyer_id: str, address: str, phone: str = None, bio: str = None): # type: ignore
        self.buyer_id = buyer_id
        self.phone = phone
        self.address = address
        self.bio = bio
        
    def __repr__(self):
        return f"ArtisanEntity(buyer_id={self.buyer_id}, address={self.address}, phone={self.phone}, bio={self.bio})"