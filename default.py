# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import random

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))

def vote_presidents():
    
    presidents = db(db.president).select()
    inc_url = URL('inc_vote')
    dec_url = URL('dec_vote')
    return dict(presidents=presidents,inc_url=inc_url,dec_url=dec_url)

def inc_vote():
    presidentid = int(request.vars.id)
    president = db.president(presidentid)
    votes = president.votecount
    president.update_record(votecount= votes + 1)
    return response.json(dict(result=president.votecount))

def dec_vote():
    presidentid = int(request.vars.id)
    president = db.president(presidentid)
    votes = president.votecount
    president.update_record(votecount= votes - 1)
    return response.json(dict(result=president.votecount))
    
def all_presidents():
    q = db.president
    grid = SQLFORM.grid(q,
           csv = False
           )
    return dict(grid=grid)

def my_shuffle(array):
    random.shuffle(array)
    return array

def sort_presidents():
    inorder = ['1 Franklin Roosevelt','2 Harry Truman','3 Dwight Eisenhower','4 John Kennedy',
               '5 Lyndon Johnson','6 Richard Nixon','7 Gerald Ford','8 Jimmy Carter','9 Ronald Reagan',
               '10 George Bush','11 Bill Clinton','12 George W. Bush','13 Barack Obama']
    ooo = ['1 Franklin Roosevelt','2 Harry Truman','3 Dwight Eisenhower','4 John Kennedy',
               '5 Lyndon Johnson','6 Richard Nixon','7 Gerald Ford','8 Jimmy Carter','9 Ronald Reagan',
               '10 George Bush','11 Bill Clinton','12 George W. Bush','13 Barack Obama']
    shuffle = my_shuffle(ooo)
    post_url = URL('update_array')
    return dict(shuffle=shuffle,post_url=post_url,inorder=inorder)

def update_array():
    array = request.vars.blah
    inorder = request.vars.sorted
    if(array==inorder):
        return True
    return response.json(dict(result=inorder,poop=array))
    
    

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
