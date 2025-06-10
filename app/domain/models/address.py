from typing import Optional
class AddressEntity:
    def __init__(self, street: str, city: str, state: str, zip_code: str, country: str, number: str, neighborhood: str, address_id: Optional[str] = None, complement: str = None):
        self.address_id = address_id
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country
        self.number = number
        self.neighborhood = neighborhood
        self.complement = complement

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
        return {
            "zip_code": self.zip_code,
            "street": self.street.lower().strip(),
            "number": self.number.lower().strip(),
            "complement": self.complement.lower().strip() if self.complement else None
        }
