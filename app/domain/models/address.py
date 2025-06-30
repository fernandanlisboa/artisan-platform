from typing import Optional
class AddressEntity:
    def __init__(self, street: str, city: str, state: str, zip_code: str, country: str, number: str, neighborhood: str, address_id: Optional[str] = None, complement: Optional[str] = None):
        self.address_id = address_id
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country
        self.number = number
        self.neighborhood = neighborhood
        self.complement = complement

    @classmethod
    def from_db_model(cls, db_model):
        """
        Creates an AddressEntity instance from a database model.
        
        :param db_model: The database model instance containing address data.
        :return: An instance of AddressEntity.
        """
        return cls(
            address_id=db_model.address_id,
            street=db_model.street,
            city=db_model.city,
            state=db_model.state,
            zip_code=db_model.zip_code,
            country=db_model.country,
            number=db_model.number,
            neighborhood=db_model.neighborhood,
            complement=db_model.complement if db_model.complement else None
        )
    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} {self.zip_code} {self.country}, {self.number}, {self.neighborhood}, {self.complement}"
    
    def __repr__(self):
        return f"AddressEntity(address_id={self.address_id}, street={self.street}, city={self.city}, state={self.state}, zip_code={self.zip_code}, country={self.country}, number={self.number}, neighborhood={self.neighborhood}, complement={self.complement})"

    def __eq__(self, other):
        if not isinstance(other, AddressEntity):
            return False
        return (self.street == other.street and
                self.city == other.city and
                self.state == other.state and
                self.zip_code == other.zip_code and
                self.country == other.country
                )

    def to_filter_dict(self) -> dict:
        """
        Returns a normalized dictionary of the attributes that define uniqueness.
        This is safe to be used for database filtering.
        """
        # The zip_code is already cleaned by the pydantic validator upon creation.
        # This dictionary explicitly defines what makes an address unique.
        filter_dict = {}
        if self.street:
            filter_dict['street'] = self.street
        if self.number:
            filter_dict['number'] = self.number
        if self.neighborhood:
            filter_dict['neighborhood'] = self.neighborhood
        if self.city:
            filter_dict['city'] = self.city
        if self.state:
            filter_dict['state'] = self.state
        if self.zip_code:
            filter_dict['zip_code'] = self.zip_code
            
        # Se não tiver critérios suficientes, podemos ter resultados imprecisos
        if len(filter_dict) < 3:
            print("WARNING: Few filter criteria for address lookup, may return imprecise results")
            
        return filter_dict
