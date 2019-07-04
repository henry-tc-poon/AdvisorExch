from django import forms
from advisorInfo.forms import formAdvisor
import AdvisorExch.views as aeView
import pandas as pd

##################################################################
def vAdvisor (request):

    advisorCode = ''
    advisorStr  = ''
    dispInfo = ''
    pageAction = ''
    dictRtn = { }

    ###########################################################################
    # To Debug Page Action
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

    if request.POST.get("update_advisor") or request.POST.get("save_advisor"):

        dbData = { 'advisorCode': request.POST.get("advisorCode", "")
                 , 'firstName':   request.POST.get("firstName", "")
                 , 'lastName':    request.POST.get("lastName", "")
                 , 'BranchCode':  request.POST.get("BranchCode", "")
                 , 'LangCode':    request.POST.get("LangCode", "")
                 , 'eMail':       request.POST.get("eMail", "")
                 }
        updtStmt = vAdvisorUpdate ( 'Update', dbData )
        request.session['advisorStr'] = request.POST.get("lastName")
    #
    ###########################################################################
    if request.POST.get("delete_advisor"):
        advisorCode = request.session['advisorCode']
        vAdvisorDelete ( advisorCode )
        request.session['advisorCode'] = ''
    #
    ###########################################################################
    btnState = { 'uBtn': 'btn-enabled',  'dBtn': 'btn-enabled'
               , 'sBtn': 'btn-disabled', 'cBtn': 'btn-disabled'
               }
    if request.POST.get("new_advisor"):
        btnState = { 'uBtn': 'btn-disabled', 'dBtn': 'btn-disabled'
                   , 'sBtn': 'btn-enabled',  'cBtn': 'btn-enabled'
                   }

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

    dfResult = vAdvisorList ( advisorStr, dispHead, colNames )

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
    dfDetail = vAdvisorDetail ( advisorCode, dtlCols )
    #
    ###########################################################################
    #
    if ( len (dfDetail) == 0 ) or ( request.POST.get("new_advisor") ):
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

    dictRtn.update ({ 'btnState' : btnState })
    dictRtn.update ({ 'dispInfo' : dispInfo })
    dictRtn.update ({ 'dispHead' : dispHead })
    dictRtn.update ({ 'dfTable'  : dfResult })
    dictRtn.update ({ 'dfDetail' : dfDetail })
    dictRtn.update ({ 'repForm'  : repForm })

    return (dictRtn)

##################################################################
def vAdvisorUpdate ( action, dbData ):

    updtStmt = '''
        with cteUpdate ( advisorCode, firstName, lastName, BranchCD, LangCD, EMail )
        as
        (
        	select '{CODE}', '{FName}', '{LName}', '{BCode}', '{LCode}', '{EMail}'
        )
        MERGE advisor a
        Using cteUpdate as  t
        ON	a.advisor_code = t.advisorCode
        WHEN MATCHED
        THEN update
        SET a.first_name = t.firstName
        ,	a.last_name  = t.lastName
        ,	a.BRN_CD     = t.BranchCD
        ,	a.LANG_CD    = t.LangCD
        ,	a.eMail      = t.EMail
        WHEN NOT MATCHED
        THEN
        INSERT ( advisor_code, first_name, last_name, BRN_CD, LANG_CD, eMail )
        VALUES ( advisorCode,  firstName,  lastName, BranchCD, LangCD, EMail )
        ;
        '''.format (  CODE  = dbData.get('advisorCode')
                    , FName = dbData.get('firstName')
                    , LName = dbData.get('lastName')
                    , BCode = dbData.get('BranchCode')
                    , LCode = dbData.get('LangCode')
                    , EMail = dbData.get('eMail')
                    )
    aeView.vUpdtSQL (updtStmt)
    return updtStmt

##################################################################
def vAdvisorDelete ( RepCode ):

    delStmt = '''
        Delete advisor
        where upper(advisor_code) = '{CODE}'
        '''.format ( CODE = RepCode.upper() )

    aeView.vDelSQL (delStmt)

    return 'Delete Advisor: ' + RepCode

##################################################################
def vAdvisorList ( srcStr, dispHead, colNames ):

    sqlStmt = '''
        select advisor_code, first_name, last_name
        from advisor
        where upper(first_name) like '%{ADVISOR}%'
        or    upper(last_name)  like '%{ADVISOR}%'
        order by 1
        '''.format ( ADVISOR = srcStr.upper() )

    dfResult = aeView.vExecSQL (sqlStmt)

    if ( len (dfResult) == 0 or srcStr == '' ):
        dfResult = pd.DataFrame(columns=colNames)
    else:
        dfResult.columns = colNames

    return dfResult

##################################################################
def vAdvisorDetail ( repCode, dtlCols ):

    sqlStmt = '''
            select advisor_code, first_name, last_name, BRN_CD, LANG_CD, eMail
            from advisor
            where upper(advisor_code) = '{RepCD}'
            '''.format ( RepCD = repCode.upper() )
    dfDetail = aeView.vExecSQL (sqlStmt)

    if ( len (dfDetail) > 0 ):
        dfDetail.columns = dtlCols
    else:
        dfDetail = pd.DataFrame(columns=dtlCols)

    return dfDetail

##################################################################
