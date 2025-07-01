import factory
from factory.django import DjangoModelFactory
# Adjust the import below to your actual user model
from app.models.user import User

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Faker("user_name")
    email = factory.Faker("email")
