from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class Empresa(models.Model):
    codigo = models.CharField(primary_key=True,max_length=3)
    ruc = models.CharField(max_length=11)
    razon_social = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)

    def save(self):
        empresa_ant = Empresa.objects.all().aggregate(Max('codigo'))
        cod_ant=empresa_ant['codigo__max']        
        if cod_ant is None:
            aux = 1            
        else:
            aux=int(cod_ant)+1
        self.codigo=str(aux).zfill(3) 
        super(Empresa, self).save()

    def __str__(self):
        return self.razon_social

class UsuarioManager(BaseUserManager):
    def create_user(self, usuario, nombres, apellidos, password):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not usuario:
            raise ValueError('Debe escribir un nombre de usuario')

        user = self.model(
            usuario = usuario,
            nombres = nombres,
            apellidos = apellidos,            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, usuario, nombres, apellidos, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            usuario = usuario,
            nombres = nombres,
            apellidos = apellidos,
            password=password,            
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser):
    usuario = models.CharField(max_length=15,unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(
        verbose_name='correo electronico',
        max_length=255,
        unique=True,
    )
    empresa = models.ForeignKey(Empresa,null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['nombres','apellidos']

    def get_full_name(self):
        # The user is identified by their email address
        return self.usuario

    def get_short_name(self):
        # The user is identified by their email address
        return self.usuario

    def __str__(self):              # __unicode__ on Python 2
        return self.usuario

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