from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from .models import *
from django.urls import reverse_lazy
from django.shortcuts import render,redirect,get_object_or_404
from .froms import *
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from account.models import CustomUser




class SearchView(TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search=self.request.GET.get('search')
        try:
            context['products'] = Product.objects.filter(name__contains=search)
        except:
            pass
        try:
            context['categorys'] = Category.objects.filter(title__contains=search)
        except:
            pass
        try:
            context['citys']=City.objects.filter(name__contains=search)
        except:
            pass

        return context


class ProductView(ListView):
    model = Product
    template_name = 'product.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'productdetail.html'


class ProductCreateView(UserPassesTestMixin,CreateView):
    model = Product
    template_name = 'productcreate.html'
    fields = '__all__'
    success_url = reverse_lazy('products')

    def test_func(self):
        return self.request.user.is_superuser



class ProductUpdateView(UserPassesTestMixin ,UpdateView):
    model = Product
    template_name = 'productupdate.html'
    fields = '__all__'
    def get_success_url(self):
        return reverse_lazy('productdetail',self.object.id())

    def test_func(self):
        return self.request.user.is_superuser


class ProductDeleteView(UserPassesTestMixin,DeleteView):
    model = Product
    template_name = 'productdelete.html'
    success_url = reverse_lazy('products')
    def test_func(self):
        return self.request.user.is_superuser




class CategoryDetailView(DetailView):
    model = Category
    template_name = 'categorydetail.html'

class CategoryCreateView(UserPassesTestMixin,CreateView):
    model = Category
    template_name = 'categorycreate.html'
    fields = '__all__'
    def get_success_url(self):
        return reverse_lazy('categorydetail',args=(self.object.id,))
    def test_func(self):
        return self.request.user.is_superuser



class CategoryUpdateView(UserPassesTestMixin,UpdateView):
    model = Category
    template_name = 'categoryupdate.html'
    fields = '__all__'
    def get_success_url(self):
        return reverse_lazy('categorydetail',args=(self.object.id,))
    def test_func(self):
        return self.request.user.is_superuser


class CityVeiw(ListView):
    model = City
    template_name = 'city.html'


class CityDetailView(DetailView):
    model = City
    template_name ='citydetail.html'

class InventoryView(UserPassesTestMixin,ListView):
    model = Inventory
    template_name = 'inventory.html'

    def test_func(self):
        return self.request.user.is_superuser

class InventoryCreateView(UserPassesTestMixin,CreateView):
    model = Inventory
    fields = '__all__'
    template_name = 'inventoryupdate.html'
    success_url = reverse_lazy('inventory')

    def test_func(self):
        return self.request.user.is_superuser


class InventoryDeleteView(UserPassesTestMixin,DeleteView):
    model = Inventory
    template_name = 'inventorydelete.html'
    success_url = reverse_lazy('inventory')

    def test_func(self):
        return self.request.user.is_superuser


class InventoryUpdateView(UserPassesTestMixin,UpdateView):
    model = Inventory
    fields = '__all__'
    template_name = 'inventoryupdate.html'
    success_url = reverse_lazy('inventory')


    def test_func(self):
        return self.request.user.is_superuser


class InventoryProductListView(UserPassesTestMixin,ListView):
    model = InventoryProduct
    template_name = 'inventoryproduct.html'

    def test_func(self):
        return self.request.user.is_superuser


class InventoryProductCreateView(UserPassesTestMixin,CreateView):
    model = InventoryProduct
    template_name = 'inventoryproductcreate.html'
    fields = "__all__"

    success_url = reverse_lazy('inventoryproduct')


    def test_func(self):
        return self.request.user.is_superuser


class InventoryProductDeleteView(UserPassesTestMixin,DeleteView):
    model = InventoryProduct
    template_name = 'inventoryproductdelete.html'
    success_url = reverse_lazy('inventoryproduct')

    def test_func(self):
        return self.request.user.is_superuser


class InventoryProductUpdateView(UserPassesTestMixin,UpdateView):
    model = InventoryProduct
    template_name = 'inventoryproductcreate.html'
    fields = '__all__'

    success_url = reverse_lazy('inventoryproduct')

    def test_func(self):
        return self.request.user.is_superuser


class CartDetailView(UserPassesTestMixin,DetailView):
    model = Cart
    template_name = 'cartdetail.html'

    def get_context_data(self, **kwargs):
        context=super(CartDetailView, self).get_context_data()
        totalPrice=0
        for cartItem in context['cart'].cartitem_set.all():
            totalPrice+=cartItem.quantity*cartItem.product.price
        context['totalprice']=totalPrice
        cities=City.objects.filter(inventory__in=Inventory.objects.all())
        context['cities']=cities
        return context

    def test_func(self):
        return self.request.user==self.get_object().user


def addToCart(request):
    if request.method=='POST':
        cart=Cart.objects.get(user=request.user)
        cartItem=CartItem(cart=cart,product_id=request.POST.get('product'),quantity=int(request.POST.get('quantity')))
        cartItem.save()
        return redirect(request.META['HTTP_REFERER'])

def updateCart(request,cartItemId):
    if request.method=='POST':
        cartItem=CartItem.objects.get(id=cartItemId,cart__user=request.user)
        cartItem.quantity=float(request.POST.get('quantity'))
        cartItem.save()
        return redirect(request.META['HTTP_REFERER'])


def deletFromCart(request,cartItemId):
    if request.method=='POST':
        cartItem=CartItem.objects.get(id=cartItemId,cart__user=request.user)
        cartItem.delete()
        return redirect(request.META['HTTP_REFERER'])


def orderCreate(request):
    if request.method=="POST":
        order=Order(user=request.user , city_id=request.POST.get('ordercity'),address=request.POST.get('orderaddress'))
        items = []
        x=True
        city=City.objects.get(id=request.POST.get('ordercity'))
        for idItem in tuple(dict(request.POST).values())[3:]:
            cartitem=CartItem.objects.get(id=int(idItem[0]))
            product=cartitem.product
            if product.inventoryproduct_set.filter(inventory__city=city):
                inventoryProduct=product.inventoryproduct_set.get(inventory__city=city)
                if inventoryProduct.quantity>cartitem.quantity:
                    items.append(OrderItem(product=product,order=order,quantity=cartitem.quantity))

                else:
                    x=False
                    messages.error(request,f'مقدار سفارشی محصول {product.name} از مجودی انبار بیشتر است. مجودی انبار: {inventoryProduct.quantity}')

            else:
                x=False
                messages.error(request,f'محصول {product.name} در شهر شما موجود نیست.')

        if x:
            order.save()
            for item in items:
                item.save()
            Cart.objects.get(user=request.user).delete()
            Cart(user=request.user).save()
            return redirect('products')
        return redirect('cartdetail',request.user.cart.id)


class AboutUsView(TemplateView):
    template_name = 'aboutus.html'


class OrderListVeiw(UserPassesTestMixin,ListView):
    model = Order
    template_name = 'orders.html'
    def test_func(self):
        return self.request.user.is_superuser

class OrderUpdate(UserPassesTestMixin,UpdateView):
    model = Order
    template_name = 'orderupdate.html'
    fields = ['is_send']
    success_url = reverse_lazy('orders')
    def test_func(self):
        return self.request.user.is_superuser

