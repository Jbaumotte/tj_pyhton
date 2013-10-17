# -*- coding: utf-8 -*-
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    #from gluon.contrib.heroku import *
    #try: db = DAL(os.environ.get('DATABASE_URL'))
    #except: db = get_db(name=None, pool_size=10)
    db = DAL('sqlite://storage.db')
else:
    db = DAL('google:datastore')
    session.connect(request, response, db=db)


from gluon.tools import Auth
auth = Auth(db)
auth.define_tables(username=True)
auth.settings.registration_requires_approval = True

db.define_table('processo',
   Field('user', default = auth.user_id),
   Field('criado_em', 'datetime', default=request.now),
   Field('classe'),
   Field('numero'),
   Field('competencia'),
   Field('reu'),
   Field('crime'))
   
db.processo.numero.requires = IS_NOT_IN_DB(db, 'processo.numero')
