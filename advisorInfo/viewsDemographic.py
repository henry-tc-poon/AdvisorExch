from django import forms
from advisorInfo.forms import formDemographic
import AdvisorExch.views as aeView
import pandas as pd

##################################################################
def vDemographic (request):

    advisorCode = ''
    dispInfo = ''
    dictRtn = { }

    ###########################################################################

    if ( 'advisorCode' not in request.session ):
        advisorCode = ''
    else:
        advisorCode = request.session['advisorCode']
    #
    ###########################################################################
    updtStmt = ''

    if request.POST.get("update_demographic"):

        dbData = { 'advisorCode': request.POST.get("advisorCode", "")
                 , 'gender':      request.POST.get("gender", "")
                 , 'birthDate':   request.POST.get("birthDate", "")
                 , 'licenses':    request.POST.get("licenses", "")
                 }
        updtStmt = vDemographicUpdate ( 'Update', dbData )
    #
    ###########################################################################

    dtlCols = [ 'advisor', 'Gender', 'Birth Date', 'Licenses' ]
    dfDetail = pd.DataFrame(columns=dtlCols)
    dfDetail = vDemographicDetail ( advisorCode, dtlCols )
    #
    ###########################################################################
    #
    if ( len (dfDetail) == 0 ) :
        demoForm = formDemographic()
    else:
        demoForm = formDemographic (
                      initial = { 'advisorCode': dfDetail.iloc[0]['advisor']
                                , 'gender':      dfDetail.iloc[0]['Gender']
                                , 'birthDate':   dfDetail.iloc[0]['Birth Date']
                                , 'licenses':    dfDetail.iloc[0]['Licenses']
                                }
                            )
    #
    ###########################################################################

    dispInfo = 'Advisor Code (' + advisorCode + ')'

    dictRtn.update ({ 'dispInfo' : dispInfo })
    dictRtn.update ({ 'demoForm' : demoForm })

    return (dictRtn)


##################################################################
def vDemographicDetail ( repCode, dtlCols ):

    sqlStmt = '''
            with cteAdvisor ( advisor_code )
            as
            (
            	select '{RepCD}'
            )
            select	c.advisor_code
            ,		gender = isNull ( gender, '' )
            ,		birthDate, licenses = isNull ( licenses, '' )
            from	cteAdvisor c
            left join demographic d
                   on c.advisor_code = d.advisor_code
            ;
            '''.format ( RepCD = repCode.upper() )
    dfDetail = aeView.vExecSQL (sqlStmt)

    if ( len (dfDetail) > 0 ):
        dfDetail.columns = dtlCols
    else:
        dfDetail = pd.DataFrame(columns=dtlCols)

    return dfDetail

##################################################################
def vDemographicUpdate ( repCode, dbData ):

    updtStmt = '''
            with cteDemographic ( advisor_code, gender, birthDate, licenses )
            as
            (
            	select '{RepCD}', '{gender}', '{birthDate}', '{licenses}'
            )
            MERGE demographic d
            Using cteDemographic c
            on d.advisor_code = c.advisor_code
            When MATCHED
            Then update
            Set  d.gender    = c.gender
            ,    d.birthDate = c.birthDate
            ,    d.licenses  = c.licenses
            When not MATCHED
            THEN
            insert ( advisor_code, gender, birthDate, licenses )
            values ( advisor_code, gender, birthDate, licenses )
            ;
            '''.format (  RepCD     = dbData.get('advisorCode')
                        , gender    = dbData.get('gender')
                        , birthDate = dbData.get('birthDate')
                        , licenses  = dbData.get('licenses')
                        )
    aeView.vUpdtSQL (updtStmt)

    return updtStmt

##################################################################
