from django.db import models
from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver



class Product(models.Model):
    name=models.CharField(max_length=100)
    category=models.ForeignKey('Category',on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=9,decimal_places=0)
    Type=models.CharField(max_length=20,choices=[('درجه یک','درجه یک'), ('درجه دو','درجه دو'),('درجه سه','درجه سه') ])
    inventory=models.ManyToManyField('Inventory', through='InventoryProduct')
    avatar=models.ImageField()
    supplier=models.ManyToManyField('Supplier')
    def __str__(self):
        return self.name
class Category(models.Model):
    title=models.CharField(max_length=100)
    def __str__(self):
        return self.title

class City(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Inventory(models.Model):
    city=models.OneToOneField('City',on_delete=models.CASCADE)

    def __str__(self):
        return str(self.city)

class InventoryProduct(models.Model):
    inventory=models.ForeignKey('Inventory' , on_delete=models.CASCADE)
    product=models.ForeignKey('Product',on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()

    def __str__(self):
        return str(self.inventory)+' '+str(self.product)

    class Meta:
        unique_together=['product','inventory']


class Supplier(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    number=models.CharField(max_length=11)
    def __str__(self):
        return self.name


class Cart(models.Model):
    user=models.OneToOneField('account.CustomUser' , on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user)

class CartItem(models.Model):
    product=models.ForeignKey('Product' , on_delete=models.CASCADE)
    cart=models.ForeignKey('Cart',on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=7, decimal_places=0)


    def save(self, *args, **kwargs):
        if not self.pk:  # Only execute this logic for newly created instances
            existing_instance = CartItem.objects.filter(product=self.product, cart=self.cart).first()
            if existing_instance:
                existing_instance.quantity += self.quantity
                existing_instance.save()
                return  # Exit early, no need to save the new instance
        super().save(*args, **kwargs)


    def __str__(self):
        return str(self.product)

class Order(models.Model):
    user = models.ForeignKey('account.CustomUser',on_delete=models.CASCADE)
    is_send=models.BooleanField(default=False)
    city=models.ForeignKey('City',on_delete=models.CASCADE)
    address=models.TextField()
    def __str__(self):
        return str(self.user)

class OrderItem(models.Model):
    product = models.ForeignKey('Product',models.CASCADE)
    order = models.ForeignKey('Order',on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=9, decimal_places=0)



    def __str__(self):
        return str(self.product)

@receiver(post_save, sender=OrderItem)
def decrease_quantity_create(sender, instance, created, **kwargs):
    if created:
        product = Product.objects.filter(id=instance.product.id).first()
        inventoryProduct=InventoryProduct.objects.filter(product=product,inventory__city=instance.order.city).first()
        if product:
            inventoryProduct.quantity -= instance.quantity
            if inventoryProduct.quantity>=0:
                inventoryProduct.save()

            else:
                pass





@receiver(pre_save, sender=OrderItem)
def decrease_quantity_update(sender, instance, **kwargs):
    if instance.pk:
        # Retrieve the original instance of SecondModel from the database
        original_quantity = OrderItem.objects.get(pk=instance.pk)

        # Calculate the difference between the original count and the new count
        quantity_diff = original_quantity.quantity - instance.quantity
        # Update the count field of the first model
        product = Product.objects.get(id=instance.product.id)
        inventoryProduct = InventoryProduct.objects.filter(product=product, inventory__city=instance.order.city).first()
        if product:
            inventoryProduct.quantity+=quantity_diff
            if inventoryProduct.quantity >= 0:
                inventoryProduct.save()
            else:
                raise ValueError('Quantity of request is more than quantity of product')



@receiver(post_delete, sender=OrderItem)
def increase_count(sender, instance, **kwargs):
    product = Product.objects.filter(id=instance.product.id).first()
    inventoryProduct = InventoryProduct.objects.filter(product=product, inventory__city=instance.order.city).first()
    if product:
        inventoryProduct.quantity +=instance.quantity
        if inventoryProduct.quantity >= 0:
            inventoryProduct.save()
        else:
            raise ValueError('Quantity of request is more than quantity of product')