from django.db import models
# from django.db.models.deletion import CASCADE, PROTECT
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser



from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils import timezone

now = timezone.now()

class UserManager(BaseUserManager):

  def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
    if not email:
        raise ValueError("User must have an email")
    if not password:
        raise ValueError("User must have a password")

    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        username=username,
        email=email,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, username, email, password, **extra_fields):
    return self._create_user(username, email, password, False, False, **extra_fields)

  def create_superuser(self, username, email, password, **extra_fields):
    user=self._create_user(username, email, password, True, True, **extra_fields)
    user.save(using=self._db)
    return user


class Page(models.Model):
    name = models.CharField(max_length=64, blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    page_img = models.ImageField(upload_to='uploads/', blank=True, null=True)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    created_by = models.CharField(max_length=64, blank=True,null=True)



class Notifications(models.Model):
    description = models.TextField()
    time = models.TextField()
    notification_type = models.CharField(max_length=64, default=" ")

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    bio = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    friends = models.ManyToManyField("User",blank=True)
    pages = models.ManyToManyField(Page,blank=True)
    theme = models.CharField(max_length=15,unique=False,default='NORMAL')
    notifications=models.ManyToManyField(Notifications,blank=True)
    picture = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/default.png', blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

class Friend_request(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user',on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user',on_delete=models.CASCADE)
    
class Post(models.Model):
    title = models.CharField(max_length=64, blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    image_url = models.ImageField(upload_to='uploads/', blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.PROTECT,null=True, blank=True)
    likes = models.IntegerField(default=0)
    liked_users = models.ManyToManyField("User", blank=True,related_name="likes")
    comments = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title}" 
        
class Product(models.Model):
    product_name = models.CharField(max_length=64, blank=True,null=True)
    product_description = models.TextField(blank=True,null=True)
    product_price = models.CharField(max_length=64, blank=True,null=True)
    product_image = models.ImageField(upload_to='uploads/', blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.PROTECT,null=True, blank=True)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    
class Comment(models.Model):
    description = models.TextField()
    time = models.TextField()
    post = ForeignKey(Post,on_delete=models.PROTECT, null=True, blank=True) 
    page = ForeignKey(Page,on_delete=models.PROTECT, null=True, blank=True)  
    user = ForeignKey(User,on_delete=models.PROTECT, null=True, blank=True)  
    product= ForeignKey(Product,on_delete=models.PROTECT, null=True, blank=True)



# class Account(AbstractUser):
#     posts = models.ForeignKey(Post, on_delete=models.CASCADE, default='',blank=True)
    # class Account(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     posts = models.ForeignKey(Post, on_delete=models.CASCADE, default='',blank=True)
#     # friends = models.ForeignKey('self', on_delete=models.PROTECT)
#     def __str__(self):
#         return f"{self.user}"
