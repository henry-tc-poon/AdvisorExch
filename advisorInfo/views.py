from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout
import AdvisorExch.views as aeView
import pandas as pd

##################################################################
def vLogout (request):
    logout (request)
    return redirect ( '/home' )

##################################################################
def vAdvisor (request):
    targMenu  = 'advisor'

    srcStr  = request.GET.get("Search", "")
    srcCode = request.GET.get("Code", "")
    sqlStmt = "select advisor_code, first_name, last_name "
    sqlStmt += " from advisor "
    sqlStmt += " where upper(first_name) like '%{{ADVISOR}}%' "
    sqlStmt += " or    upper(last_name)  like '%{{ADVISOR}}%' "
    sqlStmt += " order by 1 "

    sqlStmt = sqlStmt.replace ( '{{ADVISOR}}', srcStr.upper() )

    dfResult = aeView.vExecSQL (sqlStmt)

    colNames = ['advisor', 'firstName', 'lastName' ]
    dispHead = ['Last Name', 'First Name', 'Code' ]
    if ( len (dfResult) == 0 or srcStr == '' ):
        dfResult = pd.DataFrame(columns=colNames)
        Rep = ''
    else:
        dfResult.columns = colNames
        Rep = dfResult.iloc[0]['firstName'] + ' ' +  dfResult.iloc[0]['lastName']

    dictRtn = vCommon (request, targMenu)
    toHtml = dictRtn.get('html')

    # Rep = Rep + '  Cols: ' + dfResult.columns.get_values()[0]

    dictRtn.update ({ 'dispInfo' : sqlStmt })
    dictRtn.update ({ 'Advisor'  : Rep })
    dictRtn.update ({ 'dispHead' : dispHead })
    dictRtn.update ({ 'dfTable'  : dfResult })
    dictRtn.update ({ 'srcStr'   : srcStr })
    # dictRtn.update ({ 'srcCode'  : srcCode })

    return render (request, toHtml, dictRtn )

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
