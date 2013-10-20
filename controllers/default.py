# -*- coding: latin1 -*-

#@auth.requires_login()
def index():
    ## Creates a list of the last 5 files correctly inputed
    user = (db.processo.user == auth.user_id)
    myset = db(user)
    last = myset.select(db.processo.ALL, orderby=~db.processo.id, limitby=(0, 5))

    ## Shows a statistic of the files inputed in the month
    relatora = (db.processo.competencia == "Relatora")
    session.frelatora=db(relatora).count()
    revisora = (db.processo.competencia == "Revisora")
    session.frevisora=db(revisora).count()
    session.ftotal = session.frelatora+session.frevisora

    return dict(rows=last)

def cadastro():

    form = SQLFORM.factory(Field('processo', label=T('Numero do Processo: ')))

    if form.process().accepted:
        soup_cadastrar(form.vars.processo)
      
    return dict(form=form)

def soup_cadastrar(num):
    import tj
    processo = tj.get_page(num)
    if len(processo)== 4:
        db.escolhe.truncate()
        db.escolhe.insert(numero=processo[0].decode("latin1", "ignore"), classe=processo[1].decode("latin1", "ignore"))
        db.escolhe.insert(numero=processo[2].decode("latin1", "ignore"), classe=processo[3].decode("latin1", "ignore"))
        redirect(URL('escolhe_processo'))
                
    else:    
       session.reu = processo[0].decode("latin1", "ignore")
       session.classe = processo[1].decode("latin1", "ignore")
       session.numero = processo[2]
       session.crime = processo[3].decode("latin1", "ignore")
       session.competencia = processo[4]
       redirect(URL('cadastro_final'))
       
    return 0



def cadastro_final():

    ##creating the submission form and hidding the date and user, which are filled in automatically
    db.processo.criado_em.writable = False
    db.processo.criado_em.readable = False
    db.processo.user.writable = False
    db.processo.user.readable = False
    form = SQLFORM(db.processo)
    ##pre-populating the form with the info obtained through get_page()
    form.vars.classe = session.classe.encode("utf8")
    form.vars.reu = session.reu.encode("utf8")
    form.vars.numero = session.numero
    form.vars.competencia = session.competencia.encode("utf8")
    form.vars.crime = session.crime.encode("utf8")

    if form.process().accepted:
       session.flash = 'form accepted'
       redirect(URL('index'))

    return dict(form=form)

def pesquisa():
    form = SQLFORM.factory(Field('reu'),
    Field('numero'),
    Field('competencia'),
    Field('Data_inicial', 'date'),
    Field('Data_final', 'date', default = request.now))

    if form.process().accepted:

        if form.vars.numero!="":
            numero = db.processo.numero.contains(form.vars.numero)
            query = db(numero)
            session.rows = query.select()
            redirect(URL('result'))

        elif form.vars.reu != "":
            reu = db.processo.reu.contains(form.vars.reu)
            query = db(reu)
            session.rows = query.select()
            redirect(URL('result'))


        elif form.vars.competencia != "":
            competencia = (db.processo.competencia == form.vars.competencia)
            query = db(competencia)
            session.rows = query.select()
            redirect(URL('result'))


        elif (form.vars.Data_inicial!="") or (form.vars.Data_final!=request.now):
            import datetime
            from datetime import date
            delta = datetime.timedelta(days=1)
            session.inicial = form.vars.Data_inicial or (request.now-(60*delta))
            session.final = form.vars.Data_final or request.now
            data = (db.processo.criado_em >= session.inicial-delta) & (db.processo.criado_em <= session.final+delta)
            query = db(data)
            session.rows = query.select()
            redirect(URL('result'))

    return dict(form=form)

def result():
    return dict(rows=session.rows)
    
def escolhe_processo():
    
    myset = db(db.escolhe)
    rows = myset.select(db.escolhe.ALL)

    
    return dict(rows=rows)
    

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
