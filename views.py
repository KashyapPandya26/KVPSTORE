from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact,Orders,OrderUpdate
from math import ceil
import json

# Create your views here.
def index(request):
    # products=Product.objects.all()
    # print(products)
    
    # para={'product':products,'no_slides':nSlides,'range':range(1,nSlides)}
    allProds = []
    catprods = Product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n=len(prod)
        nSlides=n//4 + ceil((n/4)-(n//4))        
        allProds.append([prod, range(1,nSlides), nSlides])

    para = {'allProds':allProds}
    return render(request,'shop/index.html',para)
def about(request):
    return render(request,'shop/about.html')
def contact(request):
    thank = False
    if request.method=='POST':
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        desc = request.POST.get('desc','')
        contact = Contact(name=name,email=email,desc=desc)
        contact.save()
        thank = True
    return render(request,'shop/contact.html',{'thank':thank})
def tracker(request):
    if request.method=='POST':
        orderId = request.POST.get('orderId','')
        email = request.POST.get('email','')
        print(f'{orderId} and {email}')
        try:
            order=Orders.objects.filter(order_id=orderId,email=email)
            if len(order)>0:
                update=OrderUpdate.objects.filter(order_id=orderId)
                updates=[]
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response = json.dumps([updates,order[0].items_json],default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')       
    return render(request,'shop/tracker.html')
def search(request):
    return render(request,'shop/search.html')
def productview(request,myid):
    product = Product.objects.filter(id=myid)
    return render(request,'shop/productview.html',{'product':product[0]})
def checkout(request):
    if request.method=='POST':
        items_json = request.POST.get('itemsJson','') 
        name = request.POST.get('name','')
        email = request.POST.get('email','')    
        address = request.POST.get('address1','') + " " + request.POST.get('address2','')
        state = request.POST.get('state','')
        city = request.POST.get('city','')
        zip_code = request.POST.get('zip_code','')
        phone = request.POST.get('phone','')
        order = Orders(items_json=items_json,name=name,email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phone)
        order.save()
        update=OrderUpdate(order_id=order.order_id,update_desc='The order has been placed')
        update.save()
        thank = True
        id = order.order_id
        return render(request,'shop/checkout.html',{'thank':thank,'id':id})
    return render(request,'shop/checkout.html')