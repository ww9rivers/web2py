# -*- coding: utf-8 -*-
#
# $Id: apps.py,v 1.5 2014/09/16 17:56:06 weiwang Exp $
#
# Controller for the midash/apps/ portal.

import ext

def footer():
    '''Build a list of HTML <li> elements for the portal page's footer.
    '''
    links = list()
    cfg = ext.Appconf('footer-conf', '.')
    labels = cfg.labels
    if labels is None:
        labels = cfg.keys()
        labels.sort()
    for label in labels:
        link = cfg.links[label]
        if isinstance(link, basestring):  # Otherwise, assume dict
            link = dict(_href=link, _target='_blank')
        links.append(LI(A(label, **link)))
    if request.function == 'footer' and request.extension == 'json':
        response.view = 'generic.json'
    return dict(list=links)

def index():
    """Build an MCIT dashboard view based on configuration."""
    def ordered_keys(dic):
        keyz = dic.get("keys")
        if keyz:
            return keyz
        keyz = dic.keys()
        keyz.sort()    
        return keyz

    try:
        mitabs = ext.Appconf('dashboards-conf', '.')
    except Exception as inst:
        logger.error('Error reading dashboard config - %s'%(format(inst)))
        mitabs = {}
    if False:
        mitabs.update({
                'Settings': {
                    "keys": [ 'dashboards', 'Access' ],
                    "dashboards": {
                        "label": "Dashboard Settings",
                        "link": "midash/admin/settings",
                        "description": "To manage <a class='link' href='%(link)s'>%(label)s</a>."
                        },
                    "Access": {
                        "link": "/midash/admin/access",
                        "description": "To <a class='link' href='%(link)s'>manage user and group access</a> to the dashboards."
                        }
                    }
                })
    tablist = []
    groups = []
    for tid in ordered_keys(mitabs):
        tg = mitabs.get(tid)
        if not isinstance(tg, dict):
            continue # Tab group: dropped silently if not found.
        #logger.debug('Dashboard["%s"] = %s'%(tid, tg))
        theadr = tg.get('label', tid.capitalize())
        label_id="ui-"+tid
        label = tid.lower()
        tablist.append(LI(A(SPAN(theadr), _id=label_id, _class="ui-tabs-anchor", _title=theadr,
                            _href="#"+label, _role="presentation", _tabindex="-1"),
                          _class="ui-state-default ui-corner-top", _role="tab", _tabindex="-1",
                          **{"_aria-controls": label, "_aria-labelledby": label_id, "_aria-selected": "false"}))
        glist = []
        for gid in ordered_keys(tg):
            grp = tg.get(gid)
            if not isinstance(grp, dict):
                continue # App group: dropped silently if not found.
            glist.append(DIV([H3([SPAN(_class="ui-accordion-header-icon ui-icon ui-icon-triangle-1-e"),
                                   A(grp.get("label",gid.capitalize()),_class="link",_href=grp["link"])],
                                  _id="ui-accordion-"+label+"-header-0",
                                  _class="ui-accordion-header ui-helper-reset ui-state-default ui-accordion-icons ui-corner-all",
                                  _role="tab",_tabindex="0",
                                  **{"_aria-controls":gid,"_aria-selected":"false"}),
                               DIV(XML(grp["description"]%grp),
                                   _id=gid,_role="tabpanel",_style="display: none;",
                                   _class="ui-accordion-content ui-helper-reset ui-widget-content ui-corner-bottom",
                                   **{"_aria-labelledby":"ui-accordion-"+label+"-header-0","_aria-expanded":"false",
                                      "_aria-hidden":"true"})],
                         _class="group"))
        pass
        groups.append(DIV(glist, _id=label,_role="tablist",
                          _class="heading ui-tabs-panel ui-widget-content ui-corner-bottom ui-accordion ui-widget ui-helper-reset ui-sortable",
                          **{"_aria-labelledby":"ui-id-1","_aria-expanded":"true","_aria-hidden":"false"}))

    main_contents = DIV([UL(tablist, _class="ui-tabs-nav ui-helper-reset ui-helper-clearfix ui-widget-header ui-corner-all",_role="tablist")]+groups,
                        _id="tabs",_class="ui-tabs ui-widget ui-widget-content ui-corner-all")

    #logger.debug('Tabs = %s'%(format(mitabs)))
    return dict(title=T(appconf['title']), main_contents=main_contents, footer=footer()['list'])

def view():
    return appconf.view(cat='public')
