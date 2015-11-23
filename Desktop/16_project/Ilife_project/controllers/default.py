# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    #response.flash = T(session.xyz)
    if auth.is_logged_in():
        redirect(URL('afterlogin_index'))
    return dict(message=T('Welcome to ! Life!'))

@auth.requires_login()
def afterlogin_index():
    db.journal_entry.user_name.writable=False
    db.journal_entry.user_name.readable=False
    db.journal_entry.user_name.default=auth.user.email
    db.life_event.user_name.default=auth.user.email
    db.profile_pic.user_name.default=auth.user.email
    form = SQLFORM(db.journal_entry).process()
    form.vars.people=['','']
    eventform = SQLFORM(db.life_event).process()
    # t =  db(db.profile_pic.user_name==auth.user.email).select()
    picform=SQLFORM(db.profile_pic)
    if picform.process(dbio=False, onvalidation=onvalidation_insert_or_update).accepted:
        pass

    profile_pic = db(db.profile_pic.user_name == auth.user.email).select(db.profile_pic.ALL).first()
   # if picform.accepted:
    #    response.flash = T(str(picform.vars.prof_photo))
     #   t =  db(db.profile_pic.user_name==auth.user.email).select()
      #  t.prof_photo= picform.vars.prof_photo
        #db(db.profile_pic.user_name==auth.user.email).update(prof_photo=picform.vars.prof_photo)
    if len(request.args)>0:
            response.flash = T(request.args[0])
       # db(db.profile_pic.user_name==auth.user.email).update(prof_photo=picform.vars.prof_photo) or db.profile_pic.insert(user_name=auth.user.email,prof_photo=picform.vars.prof_photo)

    db.journal_entry.picture.readable=False
    db.journal_entry.contents.readable=False
    db.journal_entry.video.readable=False
    db.journal_entry.id.readable=False
    db.journal_entry.mood.readable=False
    default_sort_order=[~db.journal_entry.dated]

    headers = {'journal_entry.title' : 'Journal Title' ,
               'journal_entry.people' : 'People Tagged',
              'journal_entry.dated' : 'Date'}

    query= db.journal_entry.user_name==auth.user.email

    eventrow = db(db.life_event.user_name==auth.user.email).select(orderby=~db.life_event.dated)
    """for r in eventrow:
        import datetime
        if r.dated<request.now and r.reminder==True:
            db(db.life_event.id==r.id).update(dated=r.dated+datetime.timedelta(days=366))
            db(db.life_event.id==r.id).update(status='pending')
            response.flash = 'record updated'
        elif r.dated<request.now and r.reminder==False:
            db(db.life_event.id==r.id).delete()
        elif r.dated>request.now and r.dated<=(request.now+datetime.timedelta(days=1)) and r.status=='pending':
            mail.send(to=[r.user_name],subject='!Life Event Reminder',message='Hello!\n\nYou have'+r.title+' today')
            db(db.life_event.id==r.id).update(status='done')
            response.flash = T('Mail reminder sent')"""
    eventrow=eventrow[:5]



    #erows= SQLFORM.grid(db.life_event.user_name==auth.user.email,create=False, deletable=False,paginate=4)
    if 'updateve' in request.args:
    #if session.vars=='updateve':
        rows=SQLFORM.grid(db.life_event.user_name==auth.user.email,orderby=[~db.life_event.dated],
                        create=False,paginate=7)
        session.vars='False'
    else:
        rows = SQLFORM.grid(query,headers=headers,orderby=default_sort_order,
                        create=False, deletable=False,paginate=7)
    return locals()

def onvalidation_insert_or_update(form):
    row = db(db.profile_pic.user_name == auth.user.email).select(db.profile_pic.ALL).first()
    if row is not None:
        id = row.id
        db(db.profile_pic.id == id).update(prof_photo=form.vars.prof_photo)
        session.flash = 'Record updated'
    else:
        id = db.profile_pic.insert(**form.vars)
        session.flash = 'Record inserted'
    db.commit()
    session.flash = 'Record inserted'
    return

def timeline():
    form = SQLFORM.factory(Field("Title"),Field("Date", "date"),
                      Field("People"),formstyle='bootstrap', submit_button="Search")
    titled= ""
    subtitle=""
    if 'myday' in request.args:
        import random
        moodings=['Happy', 'Working','Bored','Loved','Stupid','Sad','Hurted','Cute']
        md=random.choice(list(moodings))
        titled= "Your "+md+" moments!"
        subtitle="From Team iLife.. Have a nice day!"
        query = db.journal_entry.user_name==auth.user.email
        query &= db.journal_entry.mood == md

    else:
        query = db.journal_entry.user_name==auth.user.email
  # response.flash = T("hello"+rows[2].picture)
    rows = db(query).select(orderby=~db.journal_entry.dated)
    if form.process().accepted:
            # gathering form submitted values
            ttl = form.vars.Title
            date = form.vars.Date
            ppls = form.vars.People

            # more dynamic conditions in to query
            if ttl:
                query &= db.journal_entry.title.contains(ttl)
            if date:
                query &= db.journal_entry.dated <= date
            if ppls:
                # A simple text search with %like%
                query &= db.journal_entry.people.contains(ppls)

    count = db(query).count()
    return locals()

def updateevent():
    rows1 = SQLFORM.grid(db.life_event.user_name==auth.user.email,orderby=[~db.life_event.dated],
                        create=False,paginate=10)
    return locals()

def user():

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
