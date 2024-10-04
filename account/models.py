from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date

"""Custom UserManager"""

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, date_of_birth,phone, address, password=None):
        """
        Creates and saves a User with the given email, date of birth and password.
        """
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            phone = phone,
            address = address
        )

        user.set_password(password)
        user.age  # Calculate age from date_of_birth

        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, date_of_birth,phone, address, password=None):
        """
        Creates and saves a superuser with the given email, date of birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            phone = phone,
            address = address
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


"""Custom UserModel"""
class User(AbstractBaseUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    phone = models.CharField(max_length = 10, unique=True, null = True)
    address = models.TextField(max_length=200, null= True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "date_of_birth", "phone"]

    def __str__(self):
        return f"{self.email} | {self.first_name} {self.last_name} | {self.phone}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    @property
    def age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        return age
