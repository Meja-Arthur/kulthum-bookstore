from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
STATE_CHOICES = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
)

class BooksCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=255)
    biography = models.TextField(blank=True)
    image = models.ImageField(upload_to='author_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
     title = models.CharField(max_length=255)
     category = models.ForeignKey(BooksCategory, on_delete=models.CASCADE, related_name='products')
     pages = models.IntegerField()
     author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
     description = models.TextField(blank=True)
     price = models.DecimalField(max_digits=10, decimal_places=2)
     slug = models.SlugField(unique=True, default='')

     must_read = models.BooleanField(default=False)  # New field for "must read"
     recommended = models.BooleanField(default=False)  # New field for "recommended"

     image = models.ImageField(upload_to='book_images/', blank=True, null=True)
     file = models.FileField(upload_to='books/')
     created_at = models.DateTimeField(auto_now_add=True)

     def __str__(self):
         return self.title

     @classmethod
     def filter_by_price_range(cls, min_price, max_price):
         """
         Custom method to filter books by price range.
         """
         return cls.objects.filter(price__gte=min_price, price__lte=max_price)

     def save(self, *args, **kwargs):
         """
         Override the save method to automatically generate a slug based on the title.
         """
         if not self.slug:
             self.slug = slugify(self.title)
         super().save(*args, **kwargs)

     @classmethod
     def get_must_read_books(cls):
         """
         Custom method to get all "must read" books.
         """
         return cls.objects.filter(must_read=True)

     @classmethod
     def get_recommended_books(cls):
         """
         Custom method to get all "recommended" books.
         """
         return cls.objects.filter(recommended=True)





class Customer(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     name = models.CharField(max_length=255)
     locality = models.CharField(max_length=200)
     city = models.CharField(max_length=200)
     mobile = models.IntegerField(default=0, blank=True)
     zipcode = models.IntegerField(default=0, blank=True)
     state = models.CharField(choices=STATE_CHOICES, max_length=100)
     wishlist = models.ManyToManyField(Book, related_name='wishlist_books', blank=True)


     def __str__(self):
         return self.name



