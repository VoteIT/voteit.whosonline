from pyramid.interfaces import IContextFound
from pyramid.events import subscriber

from voteit.whosonline.interfaces import IActivityUtil


@subscriber(IContextFound)
def log_activity(event):
    request = event.request
    context = request.context #Should always exist in this event since it has to do with traversal.
    util = request.registry.getUtility(IActivityUtil)
    util.maybe_mark(context, request)
