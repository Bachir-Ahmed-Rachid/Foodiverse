from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.

# We create UserManger class for methods only  
class UserManger(BaseUserManager):
    #create a user and a superuser are predefined and should not be changed
    ##create_user() is the function that creates a regular user.
    ##create_superuser() is the function that creates a superuser.
    def create_user(self,email,username,password=None,**extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')
        user=self.model(
            #normalize the email address
            email=self.normalize_email(email),
            username=username,
            **extra_fields
                )
        user.set_password(password)
        # specify the db where we want to save our model
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,username,password=None,**extra_fields):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            **extra_fields,

        )
        user.is_admin=True
        user.is_staff=True
        user.is_superadmin=True
        user.is_active=True
        user.save(using=self._db)
        return user





# We create User class for fields  
class User(AbstractBaseUser):
    #By default, every Django model has a manager called objects(a class that provides a way to interact with the database and perform queries on a specific model. ) 
    objects=UserManger()
    VENDOR=1
    CUSTOMER=2

    ROLE_CHOICE=(
        (VENDOR,'VENDOR'),
        (CUSTOMER,'CUSTOMER')
    )

    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50,unique=True)
    phone_number=models.CharField(max_length=9,blank=True)
    email=models.EmailField(max_length=100,unique=True)
    role=models.PositiveSmallIntegerField(choices=ROLE_CHOICE,blank=True,null=True)

    #REQUIRED_FIELDS
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    

    #django use username to authenticate but we want to use the email and by default it is a required field
    USERNAME_FIELD='email'

    REQUIRED_FIELDS=['username','first_name','last_name']

    def __str__(self):
        return self.email
    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self,app_label):
        return True
    def get_role(self):
        if self.role == 1:
            user_role= 'VENDOR'
        elif self.role == 2:
            user_role = 'CUSTOMER'
        return user_role


class UserProfile(models.Model):
    user=models.OneToOneField("User", on_delete=models.CASCADE,blank=True,null=True)
    profile_picture=models.ImageField(upload_to='user/profile_picture',blank=True,null=True)
    cover_picture=models.ImageField(upload_to='user/cover_picture',blank=True,null=True)
    address_line_1=models.CharField(max_length=50,blank=True,null=True)
    address_line_2=models.CharField(max_length=50,blank=True,null=True)
    country=models.CharField(max_length=50,blank=True,null=True)
    state=models.CharField(max_length=50,blank=True,null=True)
    city=models.CharField(max_length=50,blank=True,null=True)
    pin_code=models.CharField(max_length=6,blank=True,null=True)
    latitude=models.CharField(max_length=6,blank=True,null=True)
    longitude=models.CharField(max_length=6,blank=True,null=True)
    created_at=models.DateField(auto_now_add=True)
    modified_at=models.DateField(auto_now=True)

    def __str__(self):
        return self.user.email
        
    def full_address(self):
        return f'{self.address_line_1}, {self.address_line_2}'


    


