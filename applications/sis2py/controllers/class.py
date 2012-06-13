import gettext
T = gettext.gettext


@auth.requires_membership('admin')
def add():
    form = SQLFORM(db.classinfo)
    if form.process(session=None, formname='test').accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    # Note: no form instance is passed to the view
    return dict(form=form)


@auth.requires_membership('admin')
def admin():
    response.view = 'classes.html'
    classinfo = db((db.classinfo.teacher==db.auth_user.id)\
                   & (db.classinfo.room==db.classroom.id))
    tr = []
    for row in classinfo.select(db.classinfo.ALL, db.classroom.ALL,
                                db.auth_user.first_name, db.auth_user.last_name):
        id = row.classinfo.id
        tr.append([id, row.classinfo.course,
                   "%s %s" % (row.auth_user.first_name, row.auth_user.last_name),
                   row.classinfo.schedule, row.classinfo.intro,
                   "%s-%s" % (row.classroom.building, row.classroom.room),
                   row.classinfo.max, row.classinfo.count])
    if len(tr) == 0:
        response.flash = T('No class defined yet.')
    return dict(title=T("Ann-Hua Chinese School"),
                main_header=T("Ann-Hua Classes"),
                main_content=TABLE(*[TR(*rows) for rows in tr]),
                rsidebar=UL(LI(A(T('Add'), _href=URL('class', 'add'), _title=T('Add class'))), ),
               )


@auth.requires_membership('admin')
def room():
    response.view = 'class/add.html'
    form = SQLFORM(db.classroom)
    if form.process(session=None, formname='test').accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    # Note: no form instance is passed to the view
    return dict(form=form)
