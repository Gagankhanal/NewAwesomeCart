from django.shortcuts import render
from django.http import HttpResponse
from .models import Product , Contact ,Orders,OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
# from PayTm import Checksum
# MERCHANT_KEY = 'Your-Merchant-Key-Here'
# Create your views here.

# Create your views here.
# def index(request):
#     products=Product.objects.all()
#     print(products)
#     n = len (products)
#     nSlide = n//4 + ceil((n/4 )- n//4)
#     # params={'no_of_slide':nSlide ,'range':range(1,nSlide) ,'product':products}
#     allProds=[[ products,range(1,nSlide),nSlide ],
#               [ products,range(1,nSlide),nSlide ]]
#     params={'allProds':allProds}
def index(request):
    allProds=[]
    catProds=Product.objects.values('category','id')
    cats={item['category'] for item in catProds}
    for cat in cats:
            products = Product.objects.filter(category=cat)
            n=len(products)
            nSlide = n // 4 + ceil((n / 4) - n // 4)
            allProds.append([products,range(1,nSlide),nSlide])
    params = {'allProds': allProds}
    return render(request,'shop/index.html',params)

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in  item.description.lower() or query in item.category.lower()  or query in item.subcategory.lower()  or  query in item.product_name.lower() :
        return True
    else:
       return  False
def search(request):
    query=request.GET.get('search')
    allProds = []
    catProds = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        products =[item for item in prodtemp if searchMatch(query , item)]
        n = len(products)
        nSlide = n // 4 + ceil((n / 4) - n // 4)
        if len(products) !=0 :
            allProds.append([products, range(1, nSlide), nSlide])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query) < 4:
        params = {'msg': "???? Oops! No Results were Found! Check Your Spelling If Incorrect. "}
    return render(request, 'shop/search.html', params)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    if request.method == "POST":
         name = request.POST.get('name', '')
         email = request.POST.get('email', '')
         phone = request.POST.get('phone', '')
         desc = request.POST.get('desc', '')
         contact=Contact(name=name , email=email , phone=phone ,desc=desc)
         contact.save()
         thank=True
         return render(request, 'shop/contact.html',{'thank':thank})
    return render(request,'shop/contact.html')

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success","updates":updates, "itemsJson":order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitems"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')



def productView(request,myid):
    # fetch the product using id
    product= Product.objects.filter(id=myid)
    # print(product)
    return render(request, 'shop/prod.html' ,{'product':product[0]} )
def checkout(request):
    if request.method=="POST":
        items_json= request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone= request.POST.get('phone', '')
        order= Orders(items_json=items_json ,name=name, email=email,  address=address, city=city , state=state ,zip_code=zip_code, phone=phone,amount=amount)
        order.save()
        update=OrderUpdate(order_id=order.order_id,   update_desc="Order has been placed")
        update.save()
        thank =True
        id=order.order_id
        return render(request,'shop/checkout.html',{'thank':thank,'id':id})
        # param_dict = {
        #
        #     'MID': 'WorldP64425807474247',
        #     'ORDER_ID': str(order.order_id),
        #     'TXN_AMOUNT': str(amount),
        #     'INDUSTRY_TYPE_ID': 'Retail',
        #     'WEBSITE': 'WEBSTAGING',
        #     'CHANNEL_ID': 'WEB',
        #     'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',
        #
        # }
        # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        # return render(request, 'shop/paytm.html',{'param_dict':param_dict})

    return render(request,'shop/checkout.html')

# @csrf_exempt
# def handlerequest(request):
#     # paytm will send you post request here
#     form = request.POST
#     response_dict = {}
#     for i in form.keys():
#         response_dict[i] = form[i]
#         if i == 'CHECKSUMHASH':
#             checksum = form[i]
#
#     verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
#     if verify:
#         if response_dict['RESPCODE'] == '01':
#             print('order successful')
#         else:
#             print('order was not successful because' + response_dict['RESPMSG'])
#     return render(request, 'shop/paymentstatus.html', {'response': response_dict})
