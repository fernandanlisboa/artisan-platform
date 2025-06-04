from datetime import datetime
# --- Mock para UserEntity temporário no teste (Age como uma entidade de domínio) ---
class MockUserEntity:
    def __init__(self, email, senha, role, user_id=None):
        self.user_id = user_id if user_id else str(uuid.uuid4())
        self.email = email
        self.senha = senha
        self.role = role
        self.password = "dummy_pass" # Apenas para simular a existência
        self.registration_date = datetime.now() # Adicione para ser mais completo
        
# --- Mock para ArtisanEntity temporário no teste (Age como uma entidade de domínio) ---
class MockArtisanEntity:
    def __init__(self, artisan_id, store_name, phone, bio, status):
        self.artisan_id = artisan_id
        self.store_name = store_name
        self.phone = phone
        self.bio = bio
        self.status = status