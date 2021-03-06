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
    # Trying to get average ratings. Be careful for divide-by-zero errors
    # with dining halls which have no ratings
    cowell_posts = db(db.posts.dh_name == 'cowell').select(db.posts.ALL)
    cowell_post_total = 0
    cowell_rating_total = 0
    rating_total = 0
    for post in cowell_posts:
        if post.rating != None:
            cowell_rating_total += post.rating
            rating_total += 1
        pass
        cowell_post_total += 1
    pass
    if rating_total != 0:
        cowell_rating_avg = cowell_rating_total / rating_total
    else:
        cowell_rating_avg = 0
    pass
    crown_posts = db(db.posts.dh_name == 'crown').select(db.posts.ALL)
    crown_post_total = 0
    crown_rating_total = 0
    rating_total = 0
    for post in crown_posts:
        if post.rating != None:
            crown_rating_total += post.rating
            rating_total += 1
        pass
        crown_post_total += 1
    pass
    if rating_total != 0:
        crown_rating_avg = crown_rating_total / rating_total
    else:
        crown_rating_avg = 0
    pass
    porter_posts = db(db.posts.dh_name == 'porter').select(db.posts.ALL)
    porter_post_total = 0
    porter_rating_total = 0
    rating_total = 0
    for post in porter_posts:
        if post.rating != None:
            porter_rating_total += post.rating
            rating_total += 1
        pass
        porter_post_total += 1
    pass
    if rating_total != 0:
        porter_rating_avg = porter_rating_total / rating_total
    else:
        porter_rating_avg = 0
    pass
    eight_posts = db(db.posts.dh_name == 'eight').select(db.posts.ALL)
    eight_post_total = 0
    eight_rating_total = 0
    rating_total = 0
    for post in eight_posts:
        if post.rating != None:
            eight_rating_total += post.rating
            rating_total += 1
        pass
        eight_post_total += 1
    pass
    if rating_total != 0:
        eight_rating_avg = eight_rating_total / rating_total
    else:
        eight_rating_avg = 0
    pass
    nine_posts = db(db.posts.dh_name == 'nine').select(db.posts.ALL)
    nine_post_total = 0
    nine_rating_total = 0
    rating_total = 0
    for post in nine_posts:
        if post.rating != None:
            nine_rating_total += post.rating
            rating_total += 1
        pass
        nine_post_total += 1
    pass
    if rating_total != 0:
        nine_rating_avg = nine_rating_total / rating_total
    else:
        nine_rating_avg = 0
    pass
    return locals()

@auth.requires_login()
def friendfeed():
    db.posts.user.default = me
    db.posts.date.default = request.now
    crud = Crud(db)
    crud.settings.formstyle = 'table2cols'
    form = crud.create(db.posts)
    friends = [row.target for row in db(Link.source==me)(Link.accepted==True).select(Link.target)]
    posts = db(db.posts.user.belongs(friends)).select(orderby=~db.posts.date,limitby=(0,100))
    return locals()

def feed():
    dh = request.args[0]
    query = (db.posts.dh_name == dh)
    posts = db(query).select(db.posts.ALL, orderby =~ db.posts.date)
    return locals()

def new_post():
    # Need help automatically filling dh_name field based on argument
    dh = request.args[0]
    form = SQLFORM(db.posts).process(next = URL('feed', args = dh))
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
