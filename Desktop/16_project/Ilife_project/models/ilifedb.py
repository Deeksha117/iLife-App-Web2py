# -*- coding: utf-8 -*-
db.define_table('journal_entry',
                Field('user_name',readable=False,writable=False),
    Field('title',requires=IS_NOT_EMPTY()),
    Field('contents','text',label="Go Ahead...Write Something"),Field('dated','datetime',default=request.now,label="Pick Date/Time"),
                Field('people','list:string',label='Tag People'),
    Field('picture', 'upload',autodelete=True),Field('video','upload'),Field('mood', requires=IS_IN_SET(['Happy', 'Working','Bored','Loved','Stupid','Sad','Hurted','Cute'])),auth.signature)

db.define_table('life_event',Field('user_name',readable=False,writable=False),
                         Field('title',requires=IS_NOT_EMPTY()),Field('description','text'),
                         Field('dated','datetime',default=request.now,label="Pick Date/Time"),
                         Field('reminder', 'boolean'),Field('status',default='pending',readable=False,writable=False))

db.define_table('profile_pic',Field('user_name',readable=False,writable=False,unique=True),
                         Field('prof_photo','upload',label="Upload Profile Photo"))
