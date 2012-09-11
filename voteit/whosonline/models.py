from BTrees.OOBTree import OOBTree
from pyramid.security import authenticated_userid
from pyramid.traversal import find_interface
from zope.interface import implements
from voteit.core.models.date_time_util import utcnow
from voteit.core.models.interfaces import IMeeting

from voteit.whosonline.interfaces import IActivityUtil


class ActivityUtil(object):
    """ See IActivityUtil """
    implements(IActivityUtil)
    
    def __init__(self):
        self._storage = OOBTree()

    def mark_activity_for(self, userid, meeting_uid, dt = None, **kw):
        assert isinstance(meeting_uid, basestring)
        kw['dt'] = dt and dt or utcnow()
        kw['userid'] = userid
        try:
            us = self._storage[meeting_uid][userid]
        except KeyError:
            if meeting_uid not in self._storage:
                self._storage[meeting_uid] = OOBTree()
            us = self._storage[meeting_uid][userid] = OOBTree()
        for (k, v) in kw.items():
            us[k] = v
        return kw.keys()

    def maybe_mark(self, context, request, dt = None, **kw):
        userid = authenticated_userid(request)
        if not userid:
            return
        meeting = find_interface(context, IMeeting)
        if meeting:
            self.mark_activity_for(userid, meeting.uid, dt = dt, **kw)

    def latest_activity(self, meeting_uid, limit = 5):
        if meeting_uid not in self._storage:
            return ()
        res = sorted(self._storage[meeting_uid].values(), key = lambda x: x['dt'], reverse = True)
        return limit and tuple(res[:limit]) or tuple(res)
