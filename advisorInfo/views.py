from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout
from django import forms
from advisorInfo.forms import formAdvisor
import AdvisorExch.views as aeView
import advisorInfo.views4Advisor as v4Adv
import pandas as pd

##################################################################
def vLogout (request):
    logout (request)
    return redirect ( '/home' )

##################################################################
def vDemographic (request):
    targMenu  = 'demographic'
    dictRtn = vCommon (request, targMenu)
    toHtml = dictRtn.get('html')
    return render (request, toHtml, dictRtn )

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
    advisorCode = ''
    advisorStr  = ''
    dispInfo = ''

    ###########################################################################
    # To Debug Page Action
    pageAction = ''
    if request.POST.get("advisorCode"):    pageAction = 'Link Clicked'
    if request.POST.get("save_advisor"):   pageAction = 'Save Button'
    if request.POST.get("new_advisor"):    pageAction = 'New Button'
    if request.POST.get("cancel_advisor"): pageAction = 'Cancel Button'
    if request.POST.get("delete_advisor"): pageAction = 'Delete Button'
    if request.POST.get("update_advisor"): pageAction = 'Update Button'
    if request.POST.get("search_advisor"): pageAction = 'Search Image'
    ###########################################################################

    if ( 'advisorCode' not in request.session ):
        request.session['advisorCode'] = ''

    if ( 'advisorStr' not in request.session ):
        request.session['advisorStr'] = ''

    if request.POST.get("advisorCode"):
        request.session['advisorCode'] = request.POST.get("advisorCode")

    ###########################################################################
    rtnEMail      = request.POST.get("eMail", "")
    rtnFirstName  = request.POST.get("firstName", "")
    rtnLastName   = request.POST.get("lastName", "")
    rtnBranchCode = request.POST.get("BranchCode", "")
    rtnLangCode   = request.POST.get("LangCode", "")
    rtnRepCode    = request.POST.get("advisorCode", "")

    ###########################################################################
    updtStmt = ''

    if request.POST.get("update_advisor"):

        dbData = { 'advisorCode': request.POST.get("advisorCode", "")
                 , 'firstName':   request.POST.get("firstName", "")
                 , 'lastName':    request.POST.get("lastName", "")
                 , 'BranchCode':  request.POST.get("BranchCode", "")
                 , 'LangCode':    request.POST.get("LangCode", "")
                 , 'eMail':       request.POST.get("eMail", "")
                 }
        updtStmt = v4Adv.vAdvisorUpdate ( 'Update', dbData )

    ###########################################################################
    if request.POST.get("delete_advisor"):
        advisorCode = request.session['advisorCode']
        v4Adv.vAdvisorDelete ( advisorCode )
        request.session['advisorCode'] = ''
    #
    # ###########################################################################
    # advisorStr  = request.POST.get("Search", "")
    #
    colNames = ['advisor', 'firstName', 'lastName' ]
    dispHead = ['Last Name', 'First Name', 'Code' ]
    dfResult = pd.DataFrame(columns=colNames)

    if request.POST.get("search_advisor"):
        advisorStr = request.POST.get("Search", "")
        request.session['advisorStr'] = advisorStr
    else:
        advisorStr = request.session['advisorStr']

    dfResult = v4Adv.vAdvisorList ( advisorStr, dispHead, colNames )

    if request.POST.get("search_advisor"):
        if ( len (dfResult) > 0 ):
            advisorCode = dfResult.iloc[0]['advisor']
            request.session['advisorCode'] = advisorCode
        else:
            advisorCode = ''
            request.session['advisorCode'] = ''

    if request.POST.get("delete_advisor"):
        if ( len (dfResult) > 0 ):
            advisorCode = dfResult.iloc[0]['advisor']
            request.session['advisorCode'] = advisorCode

    ###########################################################################
    advisorCode = request.session['advisorCode']
    dtlCols = [ 'advisor', 'firstName', 'lastName', 'BranchCD', 'LangCD', 'E-Mail' ]
    dfDetail = pd.DataFrame(columns=colNames)
    dfDetail = v4Adv.vAdvisorDetail ( advisorCode, dtlCols )
    #
    ###########################################################################
    dictRtn = vCommon (request, targMenu)
    toHtml  = dictRtn.get('html')
    #
    if ( len (dfDetail) == 0 ):
        repForm = formAdvisor()
    else:
        repForm = formAdvisor (
                      initial = { 'advisorCode': dfDetail.iloc[0]['advisor']
                                , 'firstName':   dfDetail.iloc[0]['firstName']
                                , 'lastName':    dfDetail.iloc[0]['lastName']
                                , 'BranchCode':  dfDetail.iloc[0]['BranchCD']
                                , 'LangCode':    dfDetail.iloc[0]['LangCD']
                                , 'eMail':       dfDetail.iloc[0]['E-Mail']
                                }
                            )
    #
    ###########################################################################
    ###########################################################################
    advisorStr  = request.session['advisorStr']
    advisorCode = request.session['advisorCode']
    dispInfo = pageAction + ': ' +  'Session Search ('  +  advisorStr + ')  Advisor Code (' + advisorCode + ')'

    dictRtn.update ({ 'dispInfo' : dispInfo })
    dictRtn.update ({ 'dispHead' : dispHead })
    dictRtn.update ({ 'dfTable'  : dfResult })
    dictRtn.update ({ 'dfDetail' : dfDetail })
    dictRtn.update ({ 'repForm'  : repForm })

    return render (request, toHtml, dictRtn )

##################################################################
