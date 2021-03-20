from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser, BaseUserManager
)
# Create your models here.


class Client_Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60,default='')
    date_of_birth = models.DateField(null=True)
    contact_number = models.CharField(max_length=30,default='')
    address = models.CharField(max_length=100,default='')
    gender = models.CharField(max_length=10,default='')
    bio = models.CharField(max_length=200,default='')

    def __str__(self):
        client_obj = str(self.profile_id) + " (client profile) : name = " + self.name + "\n"
        client_obj = client_obj + "DOB = " + str(self.date_of_birth) + "\n" 
        client_obj = client_obj + "Contact = " + str(self.contact_number) + "\n"
        client_obj = client_obj + "Address = " + str(self.address) + "\n" 
        client_obj = client_obj + "Gender = " + str(self.gender) + "\n"  
        client_obj = client_obj + "Bio = " + str(self.bio) + "\n" 
        return client_obj


class Expert_Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60,default='')
    date_of_birth = models.DateField(null=True)
    contact_number = models.CharField(max_length=30,default='')
    address = models.CharField(max_length=100,default='')
    gender = models.CharField(max_length=10,default='')
    bio = models.CharField(max_length=200,default='')
    qualification = models.CharField(max_length=200,default='')
    def __str__(self):
        client_obj = str(self.profile_id) + " (expert profile) : name = " + self.name + "\n"
        client_obj = client_obj + "DOB = " + str(self.date_of_birth) + "\n" 
        client_obj = client_obj + "Contact = " + str(self.contact_number) + "\n"
        client_obj = client_obj + "Address = " + str(self.address) + "\n" 
        client_obj = client_obj + "Gender = " + str(self.gender) + "\n"  
        client_obj = client_obj + "Bio = " + str(self.bio) + "\n" 
        client_obj = client_obj + "Qualification = " + str(self.qualification) + "\n"
        return client_obj



class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff = False, is_admin=False, user_type=''):
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")
        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.user_type = user_type
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password = None):
        user = self.create_user(
            email = email, 
            password = password, 
            is_staff = True,
            is_admin= False,
            user_type=''
        ) 
        return user

    def create_superuser(self, email, password = None):
        user = self.create_user(
            email = email, 
            password = password, 
            is_staff = True,
            is_admin= True,
            user_type=''
        ) 
        return user

# custom user class
class User(AbstractBaseUser):
    email = models.EmailField(max_length=100,unique=True)
    active = models.BooleanField(default=True) # account is active
    staff = models.BooleanField(default=False) #staff rights
    admin = models.BooleanField(default=False) #admin rights
    user_type = models.CharField(max_length=100,default='') #user/expert rights
    client_profile = models.OneToOneField(Client_Profile, on_delete=models.CASCADE, null=True, default=None)
    expert_profile = models.OneToOneField(Expert_Profile, on_delete=models.CASCADE, null=True, default=None)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        if self.user_type == "USER":
            return self.user + " = User"
        elif self.user_type == "EXPERT":
            return self.expert + " = Expert"
        else:
            return self.admin + " = Admin"

    def get_email(self):
        return self.email
    
    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(sel, perm, obj=None):
        return True
    def has_module_perms(sel, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
    def get_type(self):
        return self.type

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=600,default='')

    def __str__(self):
        return str(self.review_id) + " : author = " + str(self.author) + " content: " + str(self.content)

