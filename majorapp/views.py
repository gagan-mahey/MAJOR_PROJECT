from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from majorapp.models import Contact_Us,Category,register_table,add_property
from majorapp.forms import add_property_form
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
import requests
from django.db.models import Q
from django.core.mail import EmailMessage
import random

def index(request):
    return render(request,"home_page.html")

def aboutpage(request):
    return render(request,"about us.html")

def contactpage(request):
    alldata = Contact_Us.objects.all().order_by("-id")[:5]
    if request.method == "POST":
        nm = request.POST["name"]
        em = request.POST["email"]
        con = request.POST["contact_number"]
        msg = request.POST["message"]
        data = Contact_Us(name=nm,email=em,contact_number=con,message=msg)
        data.save()
        res = "Dear {} Thanks for your feedback!".format(nm)
        return render(request,"contact us.html",{"status":res,"messages":alldata})

    return render(request,"contact us.html",{"messages":alldata})

def categorypage(request):
    cats = Category.objects.all().order_by("cat_name")

    return render(request,"category.html",{"category":cats})

def allpropertiespage(request):
    return render(request,"all properties.html")

def codeheaderpage(request):
    return render(request,"code header.html")

def propertydetailpage(request):
    return render(request,"property detail.html")


@login_required
def mypropertiespage(request):
    context = {}
    ch = register_table.objects.filter(user__id = request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id = request.user.id)
        context["data"] = data

    all = add_property.objects.filter(seller__id=request.user.id).order_by("-id")
    context["properties"] = all    
    return render(request,"myproperties.html",context)

@login_required
def changepasswordpage(request):
    context = {}
    ch = register_table.objects.filter(user__id = request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id = request.user.id)
        context["data"] = data
    if request.method == "POST":
        current = request.POST["cpwd"]
        new_pass = request.POST["npwd"]
        user = User.objects.get(id = request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
            user.set_password(new_pass)
            user.save()
            context["msz"] = "Password changed successfully!!"
            context["col"] = "alert-success"
        else:
            context["msz"] = "Incorrect current password" 
            context["col"] = "alert-danger"  
        user = User.objects.get(username = un)
        login(request,user)     
    return render(request,"changePassword.html",context)

@login_required
def addpropertypage(request):
    context = {}
    ch = register_table.objects.filter(user__id = request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id = request.user.id)
        context["data"] = data

    form = add_property_form()
    if request.method == "POST":
        form = add_property_form(request.POST,request.FILES)
        if form.is_valid():
            data = form.save(commit = False)
            login_user = User.objects.get(username = request.user.username)
            data.seller = login_user
            data.save()
            context["status"] = "{} Added Successfully!!".format(data.property_name)
    context["form"] = form    
    return render(request,"add_property_new.html",context)

def register(request):
    if request.method=="POST":
        ut= request.POST["inlineRadioOptions"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        uname = request.POST["username"]
        email = request.POST["email"]
        pwd = request.POST["password"]
        phone = request.POST["phone"]
        usr = User.objects.create_user(uname,email,pwd)
        usr.first_name = fname
        usr.last_name = lname
        if ut=="option1":
            usr.is_staff=True
        if ut=="option2":
            usr.is_staff=True
        if ut=="option3":
            usr.is_active=True        
        usr.save()
        reg=register_table(user=usr,contact_number=phone)
        reg.save()
        return render(request,"registeration.html",{"status":"{} Account Created Successfully!!".format(fname)})
    return render (request,"registeration.html")

def check_user(request):
    if request.method=="GET":
        un = request.GET["usern"]
        check = User.objects.filter(username=un)
        # above query check if username entered in username field is already existed in user model(built in model)
        # print(check,len(check))
        # return HttpResponse(check)
        if len(check)== 1:
            return  HttpResponse("existed")
        else:
            return HttpResponse("Not Existed")

def user_login(request):
    if request.method=="POST":
        un = request.POST["username"]
        pwd = request.POST["password"]
        user = authenticate(username=un,password=pwd)
        if user.is_staff:
            login(request,user)
            return HttpResponseRedirect("/dashboard")
        elif user.is_active:
            login(request,user)
            return HttpResponseRedirect("/dashboard")
            
            # if user.is_superuser:
            #     return HttpResponseRedirect("admin/")
            # if user.is_staff:
            #     return HttpResponseRedirect("/seller_dashboard")
            # if user.is_active:
            #     return HttpResponseRedirect("/cus_dasboard")  
        else:
            return render(request,"home_page.html",{"status":"Invalid Username or Password"})
    return render (request,"login.html")  


def forget_pass(request):
    context = {}
    if request.method=="POST":
        un = request.POST["username"]
        pwd = request.POST["npass"]
        user = get_object_or_404(User,username=un)
        user.set_password(pwd)
        user.save()
       
        if user.is_staff:
            login(request,user)
            return HttpResponseRedirect("/dashboard")
        elif user.is_active:
            login(request,user)
            return HttpResponseRedirect("/dashboard")
        
    return render(request,"forget.html",context)

def reset_pass(request):
    un =  request.GET["username"]
    try:
        user = get_object_or_404(User,username=un)
        otp = random.randint(1000,9990)
        msg = "Dear {} \n {} is your One Time Password (OTP)\n Donot share it others\n Thanks&Regards\n EVERNEST ".format(user.username,otp)
        try:
            email = EmailMessage("Account Verification",msg,to=[user.email])
            email.send()
            return JsonResponse({"status":"sent","email":user.email,"rotp":otp})
        except:
            return JsonResponse({"status":"error","email":user.email})
    except:
        return JsonResponse({"status":"failed"})


@login_required
def dashboard(request):
    context = {}
    ch = register_table.objects.filter(user__id = request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id = request.user.id)
        context["data"] = data
    return render(request,"myprofile.html", context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

@login_required
def editprofile(request):
    context = {}
    ch = register_table.objects.filter(user__id = request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id = request.user.id)
        context["data"] = data
    if request.method == "POST":
        fn = request.POST["fname"]
        ln = request.POST["lname"]
        em = request.POST["email"]
        con = request.POST["phno"]
        tt = request.POST["title"]
        abt = request.POST["about"]
        
        usr = User.objects.get(id = request.user.id)
        usr.first_name = fn
        usr.last_name = ln
        usr.email = em
        usr.save()

        data.contact_number = con
        data.title = tt
        data.about = abt
        data.save()

        if "images" in request.FILES:
            img = request.FILES["images"]
            data.profile_image = img
            data.save()
        context["status"] = "Changes saved successfully!!"

    return render(request,"editprofile.html",context)

@login_required
def favourite(request):
    return render(request,"favourite.html")

def single_property(request):
    context = {}
    id = request.GET["pid"]
    obj = add_property.objects.get(id=id)
    context["property"] = obj
    return render(request,"single_property.html",context)

def update_property(request):
    context = {}
    ch = register_table.objects.filter(user__id = request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id = request.user.id)
        context["data"] = data
    cats = Category.objects.all().order_by("cat_name")
    
    pid = request.GET["pid"]
    prop = add_property.objects.get(id=pid)
    
    if request.method=="POST":
        pn = request.POST["pname"]
        ct_id = request.POST["pcat"]
        pp = request.POST["pp"]
        sp = request.POST["sp"]
        des = request.POST["des"]

        cat_obj = Category.objects.get(id=ct_id)
        prop.property_name = pn
        prop.property_category = cat_obj
        prop.property_price = pp
        prop.sale_price = sp
        prop.details = des

        if "pimg" in request.FILES:
            img = request.FILES["pimg"]
            prop.property_image = img
        prop.save()
        
        context["status"] = "Changes saved successfully"
        context["id"] = pid   
    context["property"] = prop    
    context["category"] = cats 
    return render(request,"updateproperty.html",context)

def delete_property(request):
    context = {}
    if "pid" in request.GET:
        pid = request.GET["pid"]
        prd = get_object_or_404(add_property,id=pid)
        context["property"] = prd
        if "action" in request.GET:
            prd.delete()
            context["status"] = str(prd.property_name)+" Deleted Successfully!"
    return render(request,"deleteproperty.html",context)

def all_properties(request):
    context = {}
    cats = Category.objects.all().order_by("cat_name")
    context["category"] = cats
    all_properties = add_property.objects.all().order_by("property_name")
    context["properties"] = all_properties

    if "qry" in request.GET:
        q = request.GET["qry"]
        prd = add_property.objects.filter(Q(property_name__icontains=q)|Q(property_category__cat_name__contains=q))
        context["properties"] = prd
        context["abcd"] = "search"

    if "cat" in request.GET:
        cid = request.GET["cat"] 
        prd = add_property.objects.filter(property_category__id=cid)
        context["properties"] = prd
        context["abcd"] = "search" 
          
    return render(request,"all_properties.html",context)



    