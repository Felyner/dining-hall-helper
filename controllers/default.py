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
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    #response.flash = T("Welcome to web2py!")
    
    # Ratings for all DHs
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
    
    
    
    return dict(cowellRatings=cowellRatings, crownRatings=crownRatings, porterRatings=porterRatings,
                eightRatings=eightRatings, nineRatings=nineRatings)


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




def getSnaps():
    # Snaps for requested DH
    query = (db.snap.DH == request.args[0])
    snaps = db(query).select(db.snap.ALL, orderby=~db.snap.helpful)
    # Ratings for all DHs
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
    
    response.view = 'default/snaps.html'
    return dict(snaps = snaps, cowellRatings=cowellRatings, crownRatings=crownRatings,
                porterRatings=porterRatings, eightRatings=eightRatings, nineRatings=nineRatings)


def submit():
    # Here is how the input that goes to the iPhone camera looks (ios5 min?)
    # <input type=file accept="image/*">
    if(args[0]=="snap"): #not correct
        form=FORM('Snap:')
    else: #not correct
        form=FORM('Rating:')
    pass

def help():
    query = (db.snap.picture == request.args[0])
    snaps = db(query).select(db.snap.ALL)
    newHelpful = snaps[0].helpful+1
    db(query).update(helpful = newHelpful)
    
    
def scrape():
    import requests
    from BeautifulSoup import BeautifulSoup
    html = requests.get('http://econpy.pythonanywhere.com/ex/001.html')
    tree = BeautifulSoup(html.text)
    
    buyers = []
    prices = []
    
    for i in tree.findAll('div', title = 'buyer-name'):
        buyers.append(i.string)
    pass
    
    for i in tree.findAll('span', 'item-price'):
        prices.append(i.string)
    pass
    
    return dict(buyers = buyers, prices = prices)
