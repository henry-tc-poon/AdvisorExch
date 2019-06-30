from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout
from django import forms
import pandas as pd
import AdvisorExch.views as aeView
import advisorInfo.views4Advisor as v4Adv
import advisorInfo.viewsDemographic as v4Dmg

##################################################################
def vLogout (request):
    logout (request)
    return redirect ( '/home' )

##################################################################
def vComposition (request):
    targMenu  = 'Book Composition'
    dictRtn = vCommon (request, targMenu)
    toHtml = dictRtn.get('html')
    return render (request, toHtml, dictRtn )

##################################################################
def vClientInfo (request):
    targMenu  = 'Client Information'
    dictRtn = vCommon (request, targMenu)
    toHtml = dictRtn.get('html')
    return render (request, toHtml, dictRtn )

##################################################################
def vRevenue (request):
    targMenu  = 'revenue'
    dictRtn = vCommon (request, targMenu)
    toHtml = dictRtn.get('html')
    return render (request, toHtml, dictRtn )

##################################################################
def vInvestment (request):
    targMenu  = 'Investment Philosophy'
    dictRtn = vCommon (request, targMenu)
    toHtml = dictRtn.get('html')
    return render (request, toHtml, dictRtn )

##################################################################
def vService (request):
    targMenu  = 'Service Provided'
    dictRtn = vCommon (request, targMenu)
    toHtml = dictRtn.get('html')
    return render (request, toHtml, dictRtn )

##################################################################
def vCommon (request, targMenu):
    dictMenu = aeView.getMenu (request, targMenu)

    toHtml = dictMenu.get ( 'html')
    dfMenu = dictMenu.get ( 'Menu')

    currTime = aeView.getCurrTime()
    fullName = request.user.get_full_name()

    return { 'dfMenu': dfMenu, 'dispName' : fullName
           , 'html': toHtml, 'currTime'  : currTime
           }

##################################################################
def vAdvisor (request):
    targMenu = 'advisor'
    dictCommon = vCommon (request, targMenu)
    toHtml  = dictCommon.get('html')

    dictRtn = v4Adv.vAdvisorMain (  request )
    dictHTML = { **dictCommon, **dictRtn }

    return render (request, toHtml, dictHTML )

##################################################################
def vDemographic (request):
    targMenu  = 'demographic'
    dictCommon = vCommon (request, targMenu)
    toHtml  = dictCommon.get('html')

    dictRtn = v4Dmg.vDemographicMain (  request )
    dictHTML = { **dictCommon, **dictRtn }

    return render (request, toHtml, dictHTML )

##################################################################
