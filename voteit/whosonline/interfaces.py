from zope.interface import Interface


class IActivityUtil(Interface):
    """ A non-persistent storage of latest activities for users. """


    def mark_activity_for(userid, meeting_uid, dt = None, **kw):
        """ Mark activitiy for a userid within meeting_uid.
            dt allows for the possibility to store another time than current UTC.
            If any keywords are passed, the contents of them will be stored too.
        """

    def maybe_mark(context, request, dt = None, **kw):
        """ Determine if context is within a meeting and wether there's a logged in user.
            Allows for the same overrides as mark_activity_for.
        """

    def latest_activity(meeting_uid, userid = None, limit = 5):
        """ Return a tuple of OOBTrees containing info on latest info within a meeting.
            A limit value will cut off result. 0 means all.
            
            It will look something like this if converted to a dict:
            
            ({'fred':{'dt':<utc datetime>, 'someother_key': 'message'}}, <etc...>)
        """

    def latest_user_activity(userid, meeting_uid = None, limit = 5):
        """ Return activity for a specific user. If meeting_uid is specified,
            only that meeting will be examined. If not, all will be returned
            up to limit.
            Will always return a tuple, same as latest_activity
        """
