from gluon.tools import Auth, Crud
from gluon.contrib.login_methods.email_auth import email_auth
import datetime
db = DAL('sqlite://storage.sqlite')
crud=Crud(db)
auth = Auth(db)
auth.define_tables()
auth.settings.login_methods.append(email_auth('smtp.gmail.com:465', '@ucsc.com'))

# Hey I'm throwing out some ideas for tables I think we could use, feel free to make any changes,
#    I know there should be some more restrictions on the fields.


# DISH
# UCSC DH site lists nutritive restrictions on each dish, so that is something we could incorporate.
# We could also implement a rating system on a dish-by-dish basis, but I think that would be overcomplicated,
#    and our users will already know what foods they like/dislike, but it's an option.
# I was thinking instead of a table for menus, our app would just collect the dishes of the appropriate
#    DH, date, and meal, rather than selecting all the dishes for each DH/date/meal, which would be daunting.
# Also, the UCSC DH site (http://nutrition.sa.ucsc.edu/location.asp) lists menu plans like 12 days in advance,
#    so an hour every couple weeks is probably all it would take to keep the app current.
db.define_table(
  'dish',
  Field('name', 'string'),
  Field('DH', 'string', requires=IS_NOT_EMPTY()), #cowell, crown, porter, eight, nine
  Field('date_served', 'date', default=datetime.datetime(2014, 12, 16)),
  Field('meal', 'string', requires=IS_NOT_EMPTY()) #breakfast, lunch, dinner
  )

# POSTS
db.define_table('posts', Field('dh_name', 'string'),
                         Field('comment', 'text', required = True),
                         Field('rating', 'integer'),
                         Field('file', 'upload'),
                         Field('user', 'reference auth_user', default = db.auth_user),
                         Field('date', 'datetime', default = request.now))

db.posts.rating.requires >= 0
db.posts.rating.requires <= 5
db.posts.dh_name.readable = db.posts.dh_name.writable = False
db.posts.user.readable = db.posts.user.writable = False
db.posts.date.readable = db.posts.date.writable = False

#Created using Massimo Dipierro's FacebookClone application
#https://github.com/mdipierro/web2py-appliances/blob/master/FacebookClone
db.define_table('link',
    Field('source','reference auth_user'),
    Field('target', 'reference auth_user'),
    Field('accepted','boolean',default=False))
User, Link = db.auth_user, db.link
me, a0, a1 = auth.user_id, request.args(0), request.args(1)
alphabetical = User.first_name|User.last_name
def name_of(user): return '%(first_name)s %(last_name)s' % user
myfriends = db(Link.source==db.auth_user)(Link.accepted==True)
  # I was also thinking it would be cool if we had a friend system so you can see if any of your friends are eating
  #    at any of the DHs. Might be a little clunky though, but if we eventually implemented Facebook logins
  #    (it looks like web2py makes it easy), I think it would be a lot easier. Users could 'check in', and they
  #    would be automatically checked out after an hour maybe. Looking at the list of friends currently checked in,
  #    it would also say how long ago they checked in, and at which DH.
