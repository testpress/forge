import factory
from factory.django import DjangoModelFactory

# Adjust the import below to your actual user model
from app.models.user import User


class UserFactory(DjangoModelFactory[User]):
    class Meta:
        model = User

    phone_number = factory.Sequence(lambda n: f"+1555000{n:04d}")
    email = factory.Faker("email")
