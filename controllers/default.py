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




def snaps():
    dh = request.args[0]
    snaps = db(db.snaps.dh_name == dh).select(db.snaps.ALL, orderby =~ db.snaps.date)
    return locals()

def ratings():
    dh = request.args[0]
    ratings = db(db.ratings.dh_name == dh).select(db.ratings.ALL, orderby =~ db.ratings.date)
    return locals()
    '''
    query = (db.rating.DH == request.args[0])
    ratings = db(query).select(db.rating.ALL)
    
    query = (db.rating.DH == "cowell")
    cowellRatings = db(query).select(db.rating.ALL)
    query = (db.rating.DH == "crown")
    crownRatings = db(query).select(db.rating.ALL)
    query = (db.rating.DH == "porter")
    porterRatings = db(query).select(db.rating.ALL)
    query = (db.rating.DH == "eight")
    eightRatings = db(query).select(db.rating.ALL)
    query = (db.rating.DH == "nine")
    nineRatings = db(query).select(db.rating.ALL)
    
    response.view = 'default/ratings.html'
    return dict(ratings = ratings, cowellRatings=cowellRatings, crownRatings=crownRatings,
                porterRatings=porterRatings, eightRatings=eightRatings, nineRatings=nineRatings, dh=request.args[0])
    '''
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
