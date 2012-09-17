from pyramid.renderers import render
from betahaus.viewcomponent import view_action
from voteit.core.models.interfaces import IMeeting
from voteit.core.models.interfaces import IUser
from voteit.core.helpers import strip_and_truncate

from voteit.whosonline.interfaces import IActivityUtil


@view_action('navigation_sections', 'whosonline', containment = IMeeting)
def whosonline(context, request, va, **kwargs):
    api = kwargs['api']
    util = request.registry.getUtility(IActivityUtil)
    userdatas = util.latest_activity(api.meeting.uid, limit = 5)
    if not userdatas:
        return u""
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
