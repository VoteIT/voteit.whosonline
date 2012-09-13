from pyramid.renderers import render
from betahaus.viewcomponent import view_action
from voteit.core.models.interfaces import IMeeting

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
