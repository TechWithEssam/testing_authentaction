from django.db import models
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

# Create your models here.


class Category(models.Model) :
    name = models.CharField(unique=True, max_length=200)
    slug = models.SlugField(blank=True, null=True, unique=True)

    class Meta :
        verbose_name = "categories"
    def __str__(self) :
        return self.name
    

    
class Brand(models.Model) :
    name = models.CharField(unique=True, max_length=200)
    slug = models.SlugField(blank=True, null=True, unique=True)
    def __str__(self) :
        return self.name
    

CATEGORY_GENDER = (
    ("male","male"),
    ("female","female"),
    ("children", "children")
)


class Product(models.Model) :
    salesman                = models.ForeignKey(User, on_delete=models.CASCADE)
    name                    = models.CharField(max_length=200)
    slug                    = models.SlugField(blank=True, null=True, unique=True)
    price                   = models.DecimalField(max_digits=10, decimal_places=2)
    brand                   = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category                = models.ForeignKey(Category, on_delete=models.CASCADE)
    gender                  = models.CharField(choices=CATEGORY_GENDER, blank=True, null=True, max_length=20)
    discound                = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    inventory_quantity      = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    is_available            = models.BooleanField(default=False)
    description             = models.TextField()
    location                = models.CharField(max_length=1000)
    created                 = models.DateTimeField(auto_now_add=True)

    @property
    def all_rated_product(self) :
        return self.rate_set.all()

    @property
    def count_reated_user(self) :
        return self.all_rated_product.count()

    def save(self, *args, **kwargs) :
        if self.inventory_quantity :
            self.is_available = True
        else :
            self.is_available =False
        return super().save(*args, **kwargs)
    
    @property
    def average_rating(self) :
        rates = sum([num.rate for num in self.all_rated_product])
        if self.count_reated_user > 0 :
            result = rates / self.count_reated_user  
        else :
            result = 0
        return result

    @property
    def new_price_after_discound(self) :
        if self.discound  :
            new_price = self.price - self.price * self.discound / 100
        else :
            new_price = self.price
        return new_price

    def __str__(self) :
        return f"{str(self.name)} {self.new_price_after_discound}"
    
    @property
    def all_image_related(self) :
        return self.images_set.all()
    @property
    def first_image(self) :
        image = self.all_image_related.first()
        return image
        
        

def get_image_filename(instance, filename):
    title = instance.product.name
    slug = slugify(title)
    return "post_images/%s-%s" % (slug, filename)  

class Images(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename,
                              verbose_name='Image')
    def __str__(self) :
        return f"iamge for product name {self.product.name} ID '{self.product.id}'"



class Rate(models.Model) :
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment     = models.CharField(max_length=1000, blank=True, null=True)
    rate        = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    rated_date  = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)


    def __str__(self) :
        return f"{self.product.name}-->{self.user} {self.comment} {self.rate}"