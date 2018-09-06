from django.contrib.auth.models import Permission, User
from django.db import models
from datetime import datetime
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator


#User= get_user_model()
unicode = str
VARIATION_CATEGORIES = (
                ('size', 'Size'),
                ('color', 'Color'),
                ('package', 'Package'),
            )

class Medicines(models.Model):
    #user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=300)
    exp_date=models.DateField(default=datetime.now)
    availability=models.IntegerField()
    price=models.IntegerField()
    prescription=models.BooleanField(default=True)


    def __str__(self):
        return self.name + ' - ' + self.description

class Doctor(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Appt(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    age=models.IntegerField()
    time=models.TimeField(default=datetime.now)
    doctor=models.CharField(max_length=50)


    def __str__(self):
        return self.doctor


class Cart(models.Model):
        #user = models.ForeignKey(User, null=True, blank=True,on_delete=models.CASCADE)
        user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
        created_at = models.DateTimeField(default=datetime.now)
        updated_at = models.DateTimeField(default=datetime.now)
        active = models.BooleanField(default=True)

        def __str__(self):
            return self.user.username

class Product(models.Model):
        title = models.CharField(max_length=120, null=False, blank=False)
        description = models.TextField(null=True, blank=True)
        price = models.DecimalField(decimal_places=2, max_digits=100, default=100.00,
                                            validators=[MinValueValidator(0)])
        slug = models.SlugField(unique=True)
        created_at = models.DateTimeField(default=datetime.now)
        updated_at = models.DateTimeField(default=datetime.now)
        active = models.BooleanField(default=True)

        def get_absolute_url(self):
            kwargs = {'slug': self.slug}
            return unicode(reverse('detail', kwargs=kwargs))

        def __unicode__(self):
            return self.title

class VariationManager(models.Manager):
        def all(self):
            return super(VariationManager, self).filter(active=True)

        def all_sizes(self):
            return self.all().filter(category='size')

        def all_colors(self):
            return self.all().filter(category='color')

        def variation_by_category(self):
            return [(category[0], self.filter(category=category[0])) for category in VARIATION_CATEGORIES]


class Variation(models.Model):
    """A variation on a particular product"""
    product = models.ForeignKey(Product, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=120, choices=VARIATION_CATEGORIES,
                                default=VARIATION_CATEGORIES[0])
    # image = models.ForeignKey(ProductImage, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=100,
                                validators=[MinValueValidator(0)], null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    objects = VariationManager()

    def __unicode__(self):
        return ' | ' + self.title + ' | <' + self.category + '> of ' + self.product.title

class CartItem(models.Model):
        cart = models.ForeignKey(Cart, default=1, blank=True, on_delete=models.CASCADE)
        product = models.ForeignKey(Product, default=1, on_delete=models.CASCADE)
        variations = models.ManyToManyField(Variation, blank=True)
        quantity = models.IntegerField(default=0)
        created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
        updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
        active = models.BooleanField(default=True)

        def __unicode__(self):
            return 'Order #' + unicode(self.id) + ' of ' + self.product.title

ORDER_STATUS = (
            ('started', 'Started'),
            ('abandoned', 'Abandoned'),
            ('finished', 'Finished'),
        )

class Order(models.Model):
            user = models.ForeignKey(User, default=1, null=True, on_delete=models.CASCADE)
            order_id = models.CharField(unique=True, max_length=120, default='abc')
            cart = models.ForeignKey(Cart, default=1,on_delete=models.CASCADE)
            status = models.CharField(max_length=255, choices=ORDER_STATUS, default='started')
            created_at = models.DateTimeField(auto_now_add=True)
            modified_at = models.DateTimeField(auto_now=True)

            subtotal = models.DecimalField(default=1000.0, max_digits=300, decimal_places=2)
            tax_amount = models.DecimalField(default=1000.0, max_digits=300, decimal_places=2)

            def total(self):
                return self.subtotal + self.tax_amount

            def __unicode__(self):
                return '<Order:' + self.order_id + '> ' + self.status + ' | ' + unicode(self.created_at)

            '''
            class Profile(models.Model):
                user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
                objects=models.ManyToManyField(Medicines,blank=True)

                def __str__(self):
                    return self.user.username

            def post_save_profile_create(sender,instance,created, *args, **kwargs):
                if created:
                    Profile.objects.get_or_create(user=instance)

            post_save.connect(post_save_profile_create, sender=settings.AUTH_USER_MODEL)

            class OrderItem(models.Model):
                product=models.OneToOneField(Medicines, on_delete=models.SET_NULL, null=True)
                is_ordered=models.BooleanField(default=False)
                date_added=models.DateTimeField(auto_now=True)
                date_ordered=models.DateTimeField(null=True)

                def __str__(self):
                    return self.product.name

            class Order(models.Model):
                ref_code=models.CharField(max_length=15)
                owner=models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
                is_ordered=models.BooleanField(default=False)
                items=models.ManyToManyField(OrderItem)
                date_ordered=models.DateTimeField(auto_now=True)

                def get_cart_items(self):
                    return self.items.all()
                def get_cart_total(self):
                    return sum([item.product.price for item in self.items.all()])

                def __str__(self):
                    return '{0}-{1}'.format(self.owner, self.ref_code)
            '''



# Create your models here.
