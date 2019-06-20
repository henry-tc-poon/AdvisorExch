from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
import AdvisorExch.views as aeView

##################################################################
def vHome (request):
    currTime = aeView.getCurrTime()
    reqMethod = ''
    userName  = ''
    userPass  = ''
    userGroup = ''
    args = dict ()
    isValid = 'No'
    toUrl = 'home/home.html'
    # menuCols = [ 'menu', 'url' ]
    # dfMenu = pd.DataFrame(columns=menuCols)
    if request.method == 'POST':
        reqMethod = 'Post Request'
        userName = request.POST.get ( 'username', '' )
        userPass = request.POST.get ( 'password', '' )

        user = authenticate ( username = userName, password=userPass)
        if user is None:
            isValid = 'No'
        else:
            if user.is_active:
                login(request, user)
                userFName = request.user.username
                isValid = 'Yes'
                userGroup = aeView.getUserGroup ( user )
                request.session['userName']  = userName
                request.session['userGroup'] = userGroup
                return redirect ( '/advisorInfo' )
    else:
        reqMethod = 'Get Request'

    args.update ({ 'currTime'  : currTime  })
    args.update ({ 'reqMethod' : reqMethod })
    return render (request, toUrl, args )

##################################################################
