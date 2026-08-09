import factory
from factory.django import DjangoModelFactory

# Adjust the import below to your actual user model
from app.models.user import User

DEFAULT_TEST_PASSWORD = "factory-default-password"


class UserFactory(DjangoModelFactory[User]):
    class Meta:
        model = User
        # This factory saves the instance itself in the password hook, so
        # factory_boy's implicit post-generation save is not wanted.
        skip_postgeneration_save = True

    phone_number = factory.Sequence(lambda n: f"+1555000{n:04d}")
    email = factory.Faker("email")

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        """Store a usable, properly hashed password.

        `self` here is the freshly built User. Setting the `password`
        attribute directly would persist the raw string and make
        `check_password` - and therefore login - fail.
        """
        if not create:
            return
        self.set_password(extracted or DEFAULT_TEST_PASSWORD)
        self.save(update_fields=["password"])
