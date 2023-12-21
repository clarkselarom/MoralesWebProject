from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from .forms import ProductForm, SignUpForm, CategoryForm
from .models import Product, Category
from django.utils import timezone


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('admin_products')  
            else:
                login(request, user)
                return redirect('product_list')
        else:
            # Handle invalid login credentials
            return render(request, 'store/login.html', {'error_message': 'Invalid username or password'})

    return render(request, 'store/login.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('product_list')
    else:
        form = SignUpForm()

    return render(request, 'store/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('product_list')

def product_list(request, category_id=None):
    categories = Category.objects.all()
    
    if category_id:
        selected_category = Category.objects.get(pk=category_id)
        products = selected_category.products.all()
    else:
        selected_category = None
        products = Product.objects.all()

    return render(request, 'store/product_list.html', {'products': products, 'categories': categories, 'selected_category': selected_category})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})


def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_products(request):
    products = Product.objects.all()
    return render(request, 'store/admin_products.html', {'products': products})


@user_passes_test(is_admin)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_products')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})

@user_passes_test(is_admin)
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/edit_product.html', {'form': form, 'product': product})

@user_passes_test(is_admin)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('admin_products')


@user_passes_test(is_admin)
def admin_categories(request):
    categories = Category.objects.all()
    return render(request, 'store/admin_categories.html', {'categories': categories})

@user_passes_test(is_admin)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.created_at = timezone.now()
            category.save()
            return redirect('admin_products')  
    else:
        form = CategoryForm()
    return render(request, 'store/add_category.html', {'form': form})

@user_passes_test(is_admin)
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('admin_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'store/edit_category.html', {'form': form, 'category': category})

@user_passes_test(is_admin)
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('admin_categories')