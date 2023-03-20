from django.shortcuts import render, redirect
from .forms import ProductForm, ImageForm
from django.forms import modelform_factory
from django.contrib import messages
from .models import Product, Brand, Category, Images
from django.contrib.auth.decorators import login_required
from uuid import uuid4
# Create your views here.


def home_product(request) :
    template_name = "products/home.html"
    obj = Product.objects.all()
    context = {
        "obj" : obj
    }
    return render(request, template_name, context)


def not_found_view(request) :
    template_name = "not-found.html"
    return render(request, template_name)



@login_required
def upload_product_view(request) :
    template_name = "products/crud.html"
    context = {}
    ImageFormSet = modelform_factory(Images, form=ImageForm)
    if request.method == 'POST':
        form_product = ProductForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES)
        if form_product.is_valid() and formset.is_valid() :
            obj = form_product.save(commit=False)
            obj.salesman = request.user
            obj.save()
            for image in request.FILES.getlist('image') :
                Images.objects.create(product=obj, image=image)
            return redirect("/")
        else :
            print(form_product.errors, formset.errors)
    else :
        form_product = ProductForm()
        formset = ImageFormSet()
    context["form_image"] = formset
    context["form_product"] = form_product
    return render(request, template_name, context)


def detail_product_view(request, **kwargs) :
    template_name = "products/detail.html"
    slug = kwargs.get("slug")
    try :
        obj = Product.objects.get(slug=slug)
    except Product.DoesNotExist :
        return redirect("products:not_found")
    context = {
        "obj":obj
    }
    return render(request, template_name, context)