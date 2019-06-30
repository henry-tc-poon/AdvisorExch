from django import forms
from advisorInfo.forms import formDemographic
import AdvisorExch.views as aeView
import pandas as pd

##################################################################
def vDemographicMain (request):

    advisorCode = ''
    dispInfo = ''
    dictRtn = { }

    ###########################################################################

    if ( 'advisorCode' not in request.session ):
        advisorCode = ''
    else:
        advisorCode = request.session['advisorCode']

    advisorCode = request.session['advisorCode']
    #
    ###########################################################################

    dtlCols = [ 'advisor', 'firstName', 'lastName', 'BranchCD', 'LangCD', 'E-Mail' ]
    dfDetail = pd.DataFrame(columns=dtlCols)
    dfDetail = vDemographic ( advisorCode, dtlCols )
    #
    ###########################################################################
    #
    if ( len (dfDetail) == 0 ) :
        repForm = formDemographic()
    else:
        repForm = formDemographic (
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

    dispInfo = 'Advisor Code (' + advisorCode + ')'

    dictRtn.update ({ 'dispInfo' : dispInfo })

    return (dictRtn)


##################################################################
def vDemographic ( repCode, dtlCols ):

    sqlStmt = '''
            select advisor_code, first_name, last_name, BRN_CD, LANG_CD, eMail
            from demographic
            where upper(advisor_code) = '{RepCD}'
            '''.format ( RepCD = repCode.upper() )
    dfDetail = aeView.vExecSQL (sqlStmt)

    if ( len (dfDetail) > 0 ):
        dfDetail.columns = dtlCols
    else:
        dfDetail = pd.DataFrame(columns=dtlCols)

    return dfDetail

##################################################################
