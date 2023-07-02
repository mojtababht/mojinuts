from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):

    def create_user(self, phone_no, password, **extra_fields):

        if not phone_no:
            raise ValueError("The Phone number must be set")
        phone_no = self.normalize_phone(phone_no)
        user = self.model(phone_no=phone_no, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_no, password, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(phone_no, password, **extra_fields)

    @classmethod
    def normalize_phone(cls,phone_no):
        phone_no=phone_no or ''

        if len(phone_no)!=11 :
            raise ValueError('Phone number must be 11 digits')
        try:
            for no in phone_no:
                int(no)
        except ValueError:
            pass
        else:
            return phone_no
