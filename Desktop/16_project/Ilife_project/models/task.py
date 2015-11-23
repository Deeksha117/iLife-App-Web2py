# -*- coding: utf-8 -*-

t='<div style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;display:block;max-width:600px;padding:0 9% 30px;margin:0 auto"><table style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;padding:0;margin:0;width:100%" width="100%" border="0" cellpadding="0" cellspacing="0"><tbody><tr style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;padding:0;margin:0"><td style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;height:50px;padding:0;margin:0"></td></tr><tr style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;padding:0;margin:0"><td style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;height:26px;padding:0;margin:0"></td></tr><tr style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;padding:0;margin:0"><td style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;padding:0;margin:0"><p style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;font-weight:300;color:#424951;padding:0;line-height:1.6em;margin:0 0 18px;font-size:16px">Hi,</p><p style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;font-weight:300;color:#424951;padding:0;line-height:1.6em;margin:0 0 18px;font-size:16px">Dont forget to make an entry in your iLife journal.</p><p style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;font-weight:300;color:#424951;padding:0;line-height:1.6em;margin:0 0 18px;font-size:16px">Just click the button below to jump straight back into your ILife journal. It’ll be like you never left!</p><p style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;font-weight:300;color:#424951;padding:0;line-height:1.6em;margin:0 0 18px;font-size:16px"><a href="https://ilife.pythonanywhere.com/iLife" target="_blank">Create a new entry now</a></p><p style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;font-weight:300;color:#424951;padding:0;line-height:1.6em;margin:0 0 18px;font-size:16px">Write on!<br style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;padding:0;margin:0">The ILife Team</p></td></tr></tbody></table></div>'
    
def f():
    query = db(db.auth_user.id>0).select()
    print "hello"
    for eid in query:
        mail.send(eid.email,'Ilife Daily Reminder','<html>'+t+'</html>')
    return "Done"


# -*- coding: utf-8 -*-

def g():
    query1 = db(db.auth_user.id>0).select()
    for user in query1:
        eventrow = db(db.life_event.user_name==user.email).select(orderby=~db.life_event.dated)
        for r in eventrow:
            t='<div style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;display:block;max-width:600px;padding:0 9% 30px;margin:0 auto"><table style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;padding:0;margin:0;width:100%" width="100%" border="0" cellpadding="0" cellspacing="0"><tbody><tr style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;padding:0;margin:0"><td style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;height:50px;padding:0;margin:0"></td></tr><tr style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;padding:0;margin:0"><td style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;height:26px;padding:0;margin:0"></td></tr><tr style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;padding:0;margin:0"><td style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;padding:0;margin:0"><p style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;font-weight:300;color:#424951;padding:0;line-height:1.6em;margin:0 0 18px;font-size:16px">Hi,</p><p style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;font-weight:300;color:#424951;padding:0;line-height:1.6em;margin:0 0 18px;font-size:16px">'+r.description+' </p><p style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;font-weight:300;color:#424951;padding:0;line-height:1.6em;margin:0 0 18px;font-size:16px">Just click the button below to jump straight back into your ILife journal. It’ll be like you never left!</p><p style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;font-weight:300;color:#424951;padding:0;line-height:1.6em;margin:0 0 18px;font-size:16px"><a href="https://ilife.pythonanywhere.com/iLife" target="_blank">Create a new entry now</a></p><p style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;font-weight:300;color:#424951;padding:0;line-height:1.6em;margin:0 0 18px;font-size:16px">Write on!<br style="font-family:  Helvetica Neue  ,  Helvetica  ,Helvetica,Arial,sans-serif;padding:0;margin:0">The ILife Team</p></td></tr></tbody></table></div>'

            import datetime
            if r.dated<request.now and r.reminder==True:
                db(db.life_event.id==r.id).update(dated=r.dated+datetime.timedelta(days=366))
                db(db.life_event.id==r.id).update(status='pending')
                #response.flash = 'record updated'
            elif r.dated<request.now and r.reminder==False:
                db(db.life_event.id==r.id).delete()
            elif r.dated>request.now and r.dated<=(request.now+datetime.timedelta(days=1)) and r.status=='pending':
                db(db.life_event.id==r.id).update(status='completed')
                mail.send(to=[r.user_name],subject='iLife Event Reminder:'+r.title,message='<html>'+t+r.status+'</html>')
                
                #response.flash = T('Mail reminder sent')
    return






from gluon.scheduler import Scheduler
Scheduler(db,dict(our_function=f,event_remid=g))
