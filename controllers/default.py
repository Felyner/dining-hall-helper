def index():
    return dict()

@auth.requires_login()
def home():
    return dict()

def user():
    return dict(form = auth())

# I use this to download uploaded images.
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

# Gets the snaps of a specific dining hall.
#    Edit to include only recent ones once done testing.
def getSnaps():
    query = (db.snap.DH == request.args[0])
    snaps = db(query).select(db.snap.ALL, orderby=~db.snap.helpful)
    response.view = 'default/snaps.html'
    return dict(snaps = snaps)
    
# We should use AJAX to increase "helpful", I don't call this function anymore
def help():
    query = (db.snap.picture == request.args[0])
    snaps = db(query).select(db.snap.ALL)
    newHelpful = snaps[0].helpful+1
    db(query).update(helpful = newHelpful)
