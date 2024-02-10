import os
from django.http import HttpResponse
from django.shortcuts import render, redirect
from product.models import Product, ProductCategory
from . import forms #. means current folder

#for messages framework
from django.contrib import messages


# Create your views here.
def say_hello(request):
    return HttpResponse('Hello Django')

def startpage(request):
    cat_list = ProductCategory.objects.all()
    context = {"category_list":cat_list}
    return render(request, 'index.html', context)
    #return render(request, 'index.html', context)

def garmentpage(request):
    return render(request, 'garment.html')

def mobilepage(request):
    return render(request, 'mobile.html')

def testpage (request):
    context = {"name":"sanskar", "roll_no":21670}
    return render (request, 'test.html', context)

# def viewall (request):
#     # context = {"name":"sanskar", "roll_no":21670}
#     # get all records from database
#     allproduct = Product.objects.all()
#     print(allproduct)
#     context = {"my_products": allproduct}
#     return render (request, 'showproduct.html', context)

def viewall(request):
    # Get all products
    all_products = Product.objects.all()

    # Get all product categories
    all_categories = ProductCategory.objects.all()

    # Get selected category from the request
    selected_category = request.GET.get('category', None)

    # Filter products based on the selected category
    if selected_category:
        filtered_products = Product.objects.filter(product_category=selected_category)
    else:
        filtered_products = all_products

    context = {
        "my_products": filtered_products,
        "all_categories": all_categories,
        "selected_category": selected_category,
    }
    return render(request, 'showproduct.html', context)



def editproduct (request, pid):
    selcted_product = Product.objects.get(product_id=pid) #seelcted_product commom section
    
    if request.method == "POST":
        pname = request.POST.get("p_name")
        pdesc = request.POST.get("p_desc")
        pprice = request.POST.get("price")
        
        print ("just to debug ***********---------", pname, pdesc, pprice)
        
        # po = Product (product_name = pname, product_description = pdesc, product_price = pprice)
        # po.save()
        selcted_product.product_name =pname
        selcted_product.product_description = pdesc
        selcted_product.product_price = pprice
        
        selcted_product.save()
        messages.success(request,"Data Updated")
        return redirect('/allibaba/showprod')
    
    context = {"edit_product" : selcted_product}
    return  render (request, 'edit_product.html', context)


def add_product(request):
    if request.method == "POST":
        pname = request.POST.get("p_name")
        pdesc = request.POST.get("p_desc")
        pprice = request.POST.get("price")
        category_id = int(request.POST.get("category"))
        cat = ProductCategory.objects.get(pk=category_id)

        # Check if the category exists
        #category, created = ProductCategory.objects.get_or_create(p_cat_name=category_name)

        po = Product(
            product_name=pname,
            product_description=pdesc,
            product_price=pprice,
            product_category = cat
        )
        po.save()

        messages.success(request, "Product added successfully.")
        return redirect('/allibaba/showprod')

    # Fetch all categories for the dropdown
    categories = ProductCategory.objects.all()
    return render(request, 'add_product.html', {'categories': categories})




def deleteproduct (request, pid):
    selcted_product = Product.objects.get(product_id=pid) #seelcted_product commom section
    selcted_product.delete()
    messages.warning(request,"Data deleted")
    return redirect ('/showprod')
    # return  render (request, 'edit_product.html')
    
def prod_cat (request):
    
    #print(myform)
    if request.method == "POST":
        form = forms.ProductCategoryForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "your file has been uploaded")
            return redirect('product-catagory')

    # create a blank form for 1st time load
    myform = forms.ProductCategoryForm()
    return render (request, 'prod_cat.html',{'my_form':myform})


def showprodcat(request):
    prodcatlist = ProductCategory.objects.all()
    return render(request, 'showprodcat.html', {'prodcat_list': prodcatlist})

def edit_prodcat(request, pcatid):
    # grab the object to be editted
    pcatobj = ProductCategory.objects.get(pk = pcatid)
    # build a form with the object instance
    myform = forms.ProductCategoryForm(request.POST or None, request.FILES or None, instance=pcatobj)

    if request.method == "POST":
        if myform.is_valid():
            myform.save()
            messages.success(request, "Product category updated successfully")
            return redirect('show-product-catagory')
        else:
            messages.warning(request, "Form data was not valid")
            return redirect('show-product-catagory')

    return render(request, 'edit_prodcat.html', {'my_form': myform})


def delete_prodcat(request, pcatid):
    # grab the object to be editted
    pcatobj = ProductCategory.objects.get(pk = pcatid)
    pcatobj.delete()

    if pcatobj.p_cat_image:
        os.remove(pcatobj.p_cat_image.path)

    messages.warning(request, "Category was delete")
    return redirect('show-product-catagory')

def prod_list_bycat(request, cat_id):
    prod_list = Product.objects.filter(product_category=cat_id)            #get --> 1 row    filter--> more than 1 records
    return render(request, 'show_items_bycat.html', {'prod_list':prod_list})


def edit_prod_list_bycat(request, cat_id):
    # grab the object to be editted
    prod_list_obj = ProductCategory.objects.get(pk = cat_id)
    # build a form with the object instance
    myform = forms.ProductCategoryForm(request.POST or None, request.FILES or None, instance=prod_list_obj)

    if request.method == "POST":
        if myform.is_valid():
            myform.save()
            messages.success(request, "Product list by Category updated successfully")
            return redirect('home')
        else:
            messages.warning(request, "Form data was not valid")
            return redirect('showitemsbycat')

    return render(request, 'edit_prod_list_bycat.html', {'my_form': myform})


def delete_prod_list_bycat(request, cat_id):
    prod_list_obj = ProductCategory.objects.get(pk=cat_id)
    prod_list_obj.delete()
    messages.warning(request, "This Product list by Category is deleted")
    return redirect('home')

