from tests.unit.mocks.base import EntityBuilder
from tests.unit.mocks.models import MockUserEntity, MockAddressEntity

class UserBuilder(EntityBuilder):
    def reset(self):
        self._user = MockUserEntity()
        return self
        
    def with_email(self, email):
        self._user.email = email
        return self
        
    def with_status(self, status):
        self._user.status = status
        return self
        
    def build(self):
        result = self._user
        self.reset()
        return result

# Outras implementações de builder...