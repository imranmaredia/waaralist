
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render 
from  .models import memberdetails,waaradata
from django.contrib.auth import authenticate, login as dj_login,  logout
from django.contrib import messages
from django.contrib.auth.models import User
    
def displaymembers(request):
    return render(request,'addmembers.html') 

def addmembersdata(request):
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    phonenumber = request.POST['phonenumber']
    memberdetails.objects.create(firstname=firstname,lastname=lastname,phonenumber=phonenumber)
   # return redirect('addmembers.html') 
    return render(request,'addmembers.html') 

def home(request):
     return redirect('myhome') 
     #return render(request,'home.html') 

def dataadmin(request):

        return render(request,'dataadmin.html') 

def searchme(self):
    #tasks = memberdetails.objects.filter(is_completed=False).order_by('updated_at')
    #context = {
     #                   'dictTask':tasks,
      #          }
    query = self.GET.get('search','')
    #query = 'Imran'
  
    data = memberdetails.objects.filter(firstname__icontains=query, is_completed=False).order_by('updated_at')
    data2 = memberdetails.objects.filter(firstname__icontains=query, is_completed=True).order_by('created_at')
    context = {
                        'dictTask':data,
                        'dictComp':data2,
                }
    return render(self,'dataadmin.html',context) 

#EDIT MEMBERS
def edit(request,pk):
    getedit = get_object_or_404(memberdetails, pk=pk)
    if request.method == 'POST':
        firstnameedit = request.POST['firstname']
        getedit.firstname = firstnameedit

        lastnameedit = request.POST['lastname']
        getedit.lastname = lastnameedit

        phonenumberedit = request.POST['phonenumber']
        getedit.phonenumber = phonenumberedit
        getedit.save()

        return redirect('configdata') 
    else: 

        context = {
                       'dictTask':getedit,
                  }

    return render(request, 'editmembers.html',context)


#MARK AS DONE
def markasdone(request, pk):
    markasdonetask = get_object_or_404(memberdetails, pk=pk)
    waaras2 = request.POST.getlist('fruits')
    waaratype = (', '.join(waaras2))
    markasdonetask.is_completed = True
    markasdonetask.waara = waaratype
    markasdonetask.save()
    waaradata.objects.create(firstname=markasdonetask.firstname,lastname=markasdonetask.lastname,phonenumber=markasdonetask.phonenumber,waara=waaratype,is_completed=True)
  
  


    return redirect('myhome') 
   

def markasundone(request, pk):
    markasdonetask = get_object_or_404(memberdetails, pk=pk)
    markasdonetask.is_completed = False
    markasdonetask.waara = ""
    markasdonetask.save()
    return redirect('myhome') 


#DELETE
def deleterecord(request, pk):
    markasdelete = get_object_or_404(memberdetails, pk=pk)
    markasdelete.delete()
    #return redirect('dataadmin.html') 
    return render(request,'dataadmin.html') 

#RESET RECORD

def reset(request):
 #  reset = memberdetails.objects.all().update(is_completed=False)
     return render(request,'login.html') 



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        user = authenticate(request, username=username, password=password)
        if user is not None:
                dj_login(request, user)
                #success page
                reset = memberdetails.objects.all().update(is_completed=False)
                waarareset = memberdetails.objects.all().update(waara="")
                return redirect('myhome')
        else:
                messages.success(request,'Invalid UserName or Password')
                return render(request, 'login.html')
               # return render(request, 'login.html')





def loginmain(request):
 #  reset = memberdetails.objects.all().update(is_completed=False)
     return render(request,'loginmain.html') 

def testview(request,pk):
        getedit = memberdetails.objects.filter(pk=pk)
        context = {
                       'dictTask':getedit,
                  }
        return render(request,'test.html',context) 


def archive(self):
    #tasks = memberdetails.objects.filter(is_completed=False).order_by('updated_at')
    #context = {
     #                   'dictTask':tasks,
      #          }
    query = self.GET.get('searchwaara','')
    print(query)
    #query = 'Imran'
  
    data = waaradata.objects.filter(created_at__icontains=query).order_by('updated_at')
    context = {
                        'dictTask':data,
                        
                }
    return render(self,'archive.html',context) 
