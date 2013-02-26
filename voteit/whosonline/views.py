from pyramid.renderers import render
from betahaus.viewcomponent import view_action
from voteit.core.models.interfaces import IMeeting
from voteit.core.models.interfaces import IUser
from voteit.core.helpers import strip_and_truncate
from voteit.core.security import VIEW

from voteit.whosonline.interfaces import IActivityUtil
from voteit.whosonline.fanstaticlib import voteit_whosonline_css

@view_action('sidebar', 'whosonline', containment = IMeeting, permission = VIEW)
def whosonline(context, request, va, **kwargs):
    api = kwargs['api']
    util = request.registry.getUtility(IActivityUtil)
    userdatas = util.latest_activity(api.meeting.uid, userid = api.userid, limit = 8)
    if not userdatas:
        return u""
    voteit_whosonline_css.need()
    response = dict(
        api = api,
        userdatas = userdatas,
    )
    return render('templates/faces.pt', response, request = request)

@view_action('user_info', 'latest_activity', interface = IUser)
def latest_activity(context, request, va, **kwargs):
    """ Display latest activity within the current meeting, if one is present.
        Otherwise display all meeting activities.
    """
    api = kwargs['api']
    #Meeting permission check
    if api.meeting and not api.context_has_permission(VIEW, api.meeting):
        return u""
    #Outside of meeting permission check
    if not api.meeting and not api.context_has_permission(VIEW, context):
        return u""
    m_uid = api.meeting and api.meeting.uid or None
    util = request.registry.getUtility(IActivityUtil)
    userdatas = util.latest_user_activity(context.userid, m_uid, limit = 5)
    if not userdatas:
        return u""
    response = dict(
        api = api,
        #Global context might be something else
        context = context,
        userdatas = userdatas,
        truncate = strip_and_truncate,
    )
    return render('templates/user_activity.pt', response, request = request)
