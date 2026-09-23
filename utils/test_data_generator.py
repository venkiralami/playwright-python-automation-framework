import uuid
from faker import Faker

fake = Faker()

def generate_user():
    unique_id = uuid.uuid4().hex[:8]

    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "username": f"user_{unique_id}",
        "email": f"automation_{unique_id}@example.com"
    }