import uuid
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from .managers import CustomUserManager


VERTICAL_CHOICES = ((
    ('Apple', 'Apple'),
    ('Artificial Intelligence', 'Artificial Intelligence'),
    ('Business', 'Business'),
    ('California', 'California'),
    ('Career', 'Career'),
    ('Computers', 'Computers'),
    ('Crypto', 'Crypto'),
    ('Deals', 'Deals'),
    ('Dye', 'Dye'),
    ('Family', 'Family'),
    ('Finance', 'Finance'),
    ('Food', 'Food'),
    ))
PLACEMENT_TYPE_CHOICES =( (
    ('Banner', 'Banner'),
    ('Newsletter Inclusion', 'Newsletter Inclusion'),
    ('Editorial', 'Editorial'),
    ('Podcast', 'Podcast'),
    ('FInance', 'FInance'),
    ('Makegood', 'Makegood'),
    ('Email', 'Email'),
    ('Native', 'Native'),
    ('OP Type', 'OP Type'),
    ('New', 'New'),
    ('CPL', 'CPL'),
    ('Push', 'Push'),
    ))
LOGO_REQUIRED_CHOICES = ((
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('N/A', 'N/A'),
    ('Optional', 'Optional'),
    ('Transparent 600 * 300', 'Transparent 600 * 300'),
    ('Yes(w/solid color and white bg)', 'Yes(w/solid color and white bg)'),
    ))
ACCEPTS_CBD_CHOICES = ((
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Neither', 'Neither'),
    ('Both', 'Both'),
    ('CBD Products only', 'CBD Products only'),
    ('Depends on Brand', 'Depends on Brand'),
    ))
GOAL_CHOICES =(
        ('Click', 'Click'),
        ('Conversion', 'Conversion'),
        ('Checkout', 'Checkout'),
        ('Engagement', 'Engagement'),
    )
# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):

    # These fields tie to the roles!
    ADMIN = 1
    PUBLISHER = 2
    ADVERTISER = 3

    ROLE_CHOICES = (
        (PUBLISHER, 'Publisher'),
        (ADVERTISER, 'Advertiser')
    )
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    # Roles created here
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=2)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.username
        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dp = models.ImageField(upload_to='profile/dp',blank=True, null=True)
    cover = models.ImageField( upload_to='profile/cover', blank=True, null=True)
    name = models.CharField( max_length=100, blank=True, null=True)
    designation = models.CharField( max_length=150, blank=True, null=True)
    address = models.CharField( max_length=250, blank=True, null=True)
    email = models.EmailField( max_length=254, blank=True, null=True)
    contact = models.CharField( max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name

class Publisher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company= models.CharField(max_length=255, null=True)
    vertical = models.CharField(max_length=255, choices=VERTICAL_CHOICES, null=True)
    website = models.URLField( blank=True, null=True)
    email_list_size = models.IntegerField(  null=True)
    gender_split = models.CharField(max_length=255, null=True)
    description = models.TextField( blank=True, null=True)
    available_ad_units = models.IntegerField( blank=True, null=True)
    headline_copy_length = models.CharField(max_length=300, blank=True, null=True)
    body_copy_length = models.CharField(max_length= 300, blank=True, null=True)
    accepts_cbd = models.CharField(max_length=100, choices=ACCEPTS_CBD_CHOICES, null=True)
    cta_copy_length = models.CharField(max_length=300, blank=True, null=True)
    editorial_copy_length = models.CharField(max_length=300, blank=True, null=True)
    days_in_advance = models.IntegerField( blank=True, null=True)
    average_age = models.IntegerField( blank=True, null=True)
    hhi = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    audience_geo = models.CharField(max_length=255, null=True)
    mobile_vs_desktop = models.CharField(max_length=255, blank=True, null=True)
    education_level = models.CharField(max_length=255, blank=True, null=True)
    professional_level = models.CharField(max_length=100, blank=True, null=True)
    media_kit= models.FileField( upload_to='publisher/files', blank=True, null=True)
    files= models.FileField( upload_to='publisher/files', blank=True, null=True)
    def __str__(self):
        return self.publisher

class Placement(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    placement_types = models.CharField(max_length=255, choices=PLACEMENT_TYPE_CHOICES, null=True )
    email_service_provider = models.CharField(max_length=255, null=True)
    open_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    CTR = models.DecimalField(max_digits=5, decimal_places=2,  null=True)
    expected_clicks = models.IntegerField(  null=True)
    logo_required = models.CharField(max_length= 100, choices=LOGO_REQUIRED_CHOICES, null=True)
    image_size = models.CharField(max_length=255, null=True)
    number_of_placements = models.IntegerField(null=True)
    placement_date = models.DateField( auto_now=False, auto_now_add=False,null=True)
    available = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.id} -{self.user} - {self.placement_types}"

class Advertiser(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    email= models.EmailField( max_length=254, null=True)
    invoicing_contact = models.CharField( max_length=50, null=True)
    invoicing_email = models.EmailField( max_length=254, null=True)
    invoice_mailing_address = models.CharField( max_length=250, null=True)
    primary_contact = models.CharField( max_length=50, null=True)
    additional_contact = models.CharField( max_length=50, null=True, blank=True)
    legal_disclaimer = models.TextField( null=True, blank=True)
    promo_code = models.CharField( max_length=50, null=True)
    value_propositoins =  models.CharField( max_length=50,  null=True)
    apart_competitors = models.CharField( max_length=250)
    focus_product = models.CharField( max_length=250,null=True)
    barrier_purchase = models.CharField( max_length=250,null=True)
    not_mention= models.CharField( max_length=250)
    success_msg = models.CharField(max_length=250)
    high_reslution_logo= models.ImageField('advertiser/logo', blank=True, null=True)
    files= models.FileField(upload_to='advertiser/files', blank=True, null=True)
    
class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad_name=models.CharField(max_length=150)
    ad_title = models.CharField( max_length=150)
    landing_page  = models.CharField( max_length=50, null=True)
    utm_structure = models.CharField( max_length=50, null=True)
    target_matrics = models.CharField( max_length=250, null=True)
    utm_parameters = models.CharField( max_length=50, null=True)
    placement_types = models.CharField(max_length=255, choices=PLACEMENT_TYPE_CHOICES, null=True )
    target_market = models.CharField(max_length=150, null=True)
    daily_budget = models.IntegerField(null=True)
    total_budget = models.IntegerField( null=True)
    description = models.TextField( null=True)
    ad_goal = models.CharField(max_length=50, choices=GOAL_CHOICES, null=True)
    available = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.id} - {self.user} - {self.ad_title}- {self.placement_types}"
    
class Campaign(models.Model):
    placement = models.ForeignKey(Placement, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField( auto_now=False, auto_now_add=False)
    def __str__(self):
        return f"{self.id} - {self.placement.placement_types} - {self.ad.ad_title}"

class Screenshot(models.Model):
    campaign= models.ForeignKey(Campaign, on_delete=models.CASCADE)
    shots= models.ImageField( upload_to='campaign/images',null=True)
    def __str__(self):
        return self.shots

class Image(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    image= models.ImageField(upload_to='ad/images',null=True)
    def __str__(self):
        return self.id
        
class CampaignImage(models.Model):
    campaign= models.ForeignKey(Campaign , on_delete=models.CASCADE)
    images = models.ImageField( upload_to='campaign/images',null=True)
    def __str__(self):
        return self.images

class CampaignVideo(models.Model):
    campaign= models.ForeignKey(Campaign , on_delete=models.CASCADE)
    # video = models.FileField(_(""), upload_to=None, max_length=100)
    videos = models.FileField( upload_to='campaign/videos',null=True)
    def __str__(self):
        return self.videos

class CampaignFile(models.Model):
    campaign= models.ForeignKey(Campaign , on_delete=models.CASCADE)
    files = models.FileField( upload_to='campaign/files',null=True)
    def __str__(self):
        return self.files
    
    