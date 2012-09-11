from zope.interface import Interface


class IActivityUtil(Interface):
    """ A non-persistent storage of latest activities for users. """


    def mark_activity_for(userid, meeting_uid, dt = None, **kw):
        """ Mark activitiy for a userid within meeting_uid.
            dt allows for the possibility to store another time than current UTC.
            If any keywords are passed, the contents of them will be stored too.
        """

    def maybe_mark(self, request, context, dt = None, **kw):
        """ Determine if context is within a meeting and wether there's a logged in user.
            Allows for the same overrides as mark_activity_for.
        """

    def latest_activity(meeting_uid, limit = 5):
        """ Return a tuple of dicts containing info on latest info within a meeting.
            A limit value will cut off result. 0 means all.
            
            Returned dict will look something like:
            
            ({'fred':{'dt':<utc datetime>, 'someother_key': 'message'}}, <etc...>)
        """