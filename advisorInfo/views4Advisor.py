import pandas as pd
import AdvisorExch.views as aeView

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
