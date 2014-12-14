from gluon.tools import Auth
from gluon.contrib.login_methods.email_auth import email_auth
import datetime
db = DAL('sqlite://storage.sqlite')

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
                         Field('comment', 'text'),
                         Field('rating', 'integer'),
                         Field('file', 'upload'),
                         Field('user', 'reference auth_user', default = db.auth_user),
                         Field('date', 'datetime', default = request.now))

# SNAP
# My idea for snaps - users in dining hall can take picture of their dish, serving stations, or whatever will
#    represent the current state of the DH they are at. These snaps will be put into feeds for the individual DHs,
#    and they will be sorted by their helpfulness (voted by users, basically "like"s from facebook). Snaps voted down
#    would be deleted, and snaps would have to be deleted after an hour or so to keep them relevant.
# Another approach would be to ditch helpfulness (since many snaps will be quite similar, users may not have
#    incentive to vote on them), and instead include a flagging system for inappropriate/unhelpful pictures. I'm
#    not sure which approach would be best.
db.define_table('snaps', Field('dh_name', 'string'),
                         Field('file', 'upload'),
                         Field('description', 'string', length = 25),
                         Field('user', 'reference auth_user', default = db.auth_user),
                         Field('date', 'datetime', default = request.now))

# RATING
# Users could rate dining hall on quality and business, and on main screen of app with all 5
#    DHs listed, alongside could be their average ratings, for a quick comparison between the DHs.
#    Ratings would probably expire at the same rate that snaps do.
# It would also be interesting to collect data from ratings - which dining halls are the best, which are
#    the best at specific times, days of the week, times of the year, do students grow tired of the food,
#    which DHs improve/weaken, etc.
db.define_table('ratings', Field('dh_name', 'string'),
                           Field('score', 'integer'),
                           Field('comment', 'text'),
                           Field('user', 'reference auth_user', default = db.auth_user),
                           Field('date', 'datetime', default = request.now))
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
