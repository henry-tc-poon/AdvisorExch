from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.db import connection
import datetime as dt
import pandas as pd
import xml.etree.ElementTree as et
from AdvisorExch.settings import Exch_DIR

##################################################################
def getCurrTime ():

    return dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

##################################################################
def getUserGroup ( user ):
    userGroup  = ''
    if user is not None:
        userGroup = user.groups.values_list('name',flat=True)
    return userGroup[0]

##################################################################
def getMenu (request, menuName):
    userName = request.session['userName']
    userGroup = request.session['userGroup']
    targHtml = ''
    if 'userName' is None:
        dispMsg = 'User Name not in session'
    else:
        dispMsg = 'Group: <' + userGroup + '>'

    ####################################################
    menuCols = [ 'Disp', 'view' ]
    dfMenu = pd.DataFrame(columns=menuCols )
    xmlDoc = et.parse( Exch_DIR + '/files/MenuInfo.xml').getroot()
    groupNode = xmlDoc.find('Groups')
    for mNode in groupNode :
        currGroup = mNode.get('name').strip()
        if ( currGroup == userGroup):
            for iNode in mNode.find('MenuItems').findall('Item') :
                dispMenu = iNode.get('Display')
                viewName = iNode.get('vName')
                if ( menuName.upper() == dispMenu.upper() ):
                    viewName = ''
                    targHtml = iNode.get('html')
                dfMenu = dfMenu.append ( pd.DataFrame ( [[dispMenu, viewName]],
                                columns=menuCols ), ignore_index = True )

    logoutManu = 'Logout'
    logoutView = 'logout'
    dfMenu = dfMenu.append ( pd.DataFrame ( [ [logoutManu, logoutView] ]
                           , columns=menuCols ), ignore_index = True )

    dictMenu = { 'Menu' : dfMenu,   'html' : targHtml }

    return  dictMenu

##################################################################
def vExecSQL(sqlStmt):
    with connection.cursor() as cursor:
        cursor.execute( sqlStmt )
        dfResult = pd.DataFrame(cursor.fetchall())
    return dfResult

##################################################################
