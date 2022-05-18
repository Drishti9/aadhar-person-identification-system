from django.contrib.auth.base_user import BaseUserManager
import accounts.models

class UserManager(BaseUserManager):
    use_in_migrations=True

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Users must have an username")
        user = self.model(
            username, **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        
        return user
        
    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        user = self.create_user(
        username=username,
        password=password,
        **extra_fields
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user