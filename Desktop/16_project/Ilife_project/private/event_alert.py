#!/usr/bin/python 

import time
while True:
	print "here"
	mail.send(to='deeksha.forever@gmail.com',subject='hiieee')
        """if mail.send(to=user.auth.email,
        subject=row.title,
        message=row.description):
        row.update_record(status='sent')
        else:
        row.update_record(status='failed')
        db.commit()"""
     #  response.flash = T("timer")
	print "done"
        time.sleep(10) # check every minute
