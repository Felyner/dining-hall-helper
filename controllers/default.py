# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

def index():
    
    # Ratings for all DHs
    # Do some math here to generate the average rating for each dining hall
    query = (db.posts.dh_name == "cowell")
    cowellRatings = db(query).select(db.posts.ALL)
    query = (db.posts.dh_name == "crown")
    crownRatings = db(query).select(db.posts.ALL)
    query = (db.posts.dh_name == "porter")
    porterRatings = db(query).select(db.posts.ALL)
    query = (db.posts.dh_name == "eight")
    eightRatings = db(query).select(db.posts.ALL)
    query = (db.posts.dh_name == "nine")
    nineRatings = db(query).select(db.posts.ALL)
    
    
    
    return dict(cowellRatings=cowellRatings, crownRatings=crownRatings, porterRatings=porterRatings,
                eightRatings=eightRatings, nineRatings=nineRatings)

def feed():
    dh = request.args[0]
    posts = db(db.posts.dh_name == dh).select(db.posts.ALL, orderby =~ db.posts.date)
    return locals()

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


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)

def menu():
    query = (db.dish.DH == request.args[0] and db.dish.meal == request.args[1])
    dishes = db(query).select(db.dish.ALL)
    
    query = (db.ratings.dh_name == "cowell")
    cowellRatings = db(query).select(db.ratings.ALL)
    query = (db.ratings.dh_name == "crown")
    crownRatings = db(query).select(db.ratings.ALL)
    query = (db.ratings.dh_name == "porter")
    porterRatings = db(query).select(db.ratings.ALL)
    query = (db.ratings.dh_name == "eight")
    eightRatings = db(query).select(db.ratings.ALL)
    query = (db.ratings.dh_name == "nine")
    nineRatings = db(query).select(db.ratings.ALL)
    
    response.view = 'default/menu.html'
    return dict(dishes=dishes, cowellRatings=cowellRatings, crownRatings=crownRatings,
                porterRatings=porterRatings, eightRatings=eightRatings, nineRatings=nineRatings, dh=request.args[0],
                meal=request.args[1])

def help():
    query = (db.snap.picture == request.args[0])
    snaps = db(query).select(db.snap.ALL)
    newHelpful = snaps[0].helpful+1
    db(query).update(helpful = newHelpful)
# Created using Massimo DiPierro's FacebookClone application 
# https://github.com/mdipierro/web2py-appliances/blob/master/FacebookClone/
@auth.requires_login()
def friends():
    friends = db(User.id==Link.source)(Link.target==me).select(orderby=alphabetical)
    requests = db(User.id==Link.target)(Link.source==me).select(orderby=alphabetical)
    return locals()

# this is the Ajax callback
@auth.requires_login()
def friendship():
    """AJAX callback!"""
    if request.env.request_method!='POST': raise HTTP(400)
    if a0=='request' and not Link(source=a1,target=me):
        # insert a new friendship request
        Link.insert(source=me,target=a1)
    elif a0=='accept':
        # accept an existing friendship request
        db(Link.target==me)(Link.source==a1).update(accepted=True)
        if not db(Link.source==me)(Link.target==a1).count():
            Link.insert(source=me,target=a1)
    elif a0=='deny':
        # deny an existing friendship request
        db(Link.target==me)(Link.source==a1).delete()
    elif a0=='remove':
        # delete a previous friendship request
        db(Link.source==me)(Link.target==a1).delete()
@auth.requires_login()
def search():
    form = SQLFORM.factory(Field('name',requires=IS_NOT_EMPTY()))
    if form.accepts(request):
        tokens = form.vars.name.split()
        query = reduce(lambda a,b:a&b,
                       [User.first_name.contains(k)|User.last_name.contains(k) \
                            for k in tokens])
        people = db(query).select(orderby=alphabetical)
    else:
        people = []
    return locals()
