from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    """ Custom User Model Manager. """
    def create_user(self, email, date_of_birth, first_name, last_name=None, password=None, password2=None):
        """ Creates a User with provided email-address, Name & Password. """

        if email is None:
            raise ValueError("Email is required to create a user.")

        user = self.model(
            email = self.normalize_email(email),
            date_of_birth = date_of_birth,
        )

        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, date_of_birth, first_name, last_name=None, password=None):
        """ Creates a Superuser with provided user details. """

        if email is None:
            raise ValueError("Email is required to create a superuser.")

        user = self.create_user(
            email = email,
            date_of_birth = date_of_birth,
            first_name = first_name,
            last_name = last_name,
            password = password
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="Email Address", max_length=255, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["date_of_birth", "first_name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


