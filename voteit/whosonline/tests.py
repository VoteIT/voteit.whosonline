from unittest import TestCase

from pyramid import testing
from pyramid.events import ContextFound
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject
from voteit.core.testing_helpers import bootstrap_and_fixture

from voteit.whosonline.interfaces import IActivityUtil


class WhosOnlineTests(TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from .models import ActivityUtil
        return ActivityUtil

    @property
    def _meeting(self):
        from voteit.core.models.meeting import Meeting
        return Meeting

    def test_verify_class(self):
        self.failUnless(verifyClass(IActivityUtil, self._cut))

    def test_verify_obj(self):
        self.failUnless(verifyObject(IActivityUtil, self._cut()))

    def test_integration_util(self):
        self.config.include('voteit.whosonline')
        self.failUnless(self.config.registry.queryUtility(IActivityUtil))

    def test_mark_activity_for(self):
        from datetime import datetime
        obj = self._cut()
        obj.mark_activity_for('tester', 'm_uid', somedata = True, others = False)
        self.assertEqual(set(obj._storage['m_uid']['tester'].keys()), set(['somedata', 'dt', 'others', 'userid', 'm_uid']))
        self.assertIsInstance(obj._storage['m_uid']['tester']['dt'], datetime)

    def test_maybe_mark(self):
        self.config.testing_securitypolicy(userid='ms_tester')
        context = self._meeting(uid = 'uid')
        request = testing.DummyRequest()
        obj = self._cut()
        obj.maybe_mark(context, request)
        self.assertEqual(len(obj._storage), 1)
        self.assertIn('ms_tester', obj._storage['uid'])

    def test_maybe_mark_dont_mark_anon(self):
        request = testing.DummyRequest()
        context = self._meeting()
        obj = self._cut()
        obj.maybe_mark(context, request)
        self.assertEqual(len(obj._storage), 0)

    def test_maybe_mark_dont_mark_if_no_view_perm(self):
        self.config.testing_securitypolicy(userid='ms_tester', permissive = False)
        request = testing.DummyRequest()
        context = self._meeting()
        obj = self._cut()
        obj.maybe_mark(context, request)
        self.assertEqual(len(obj._storage), 0)

    def test_latest_activity(self):
        obj = self._cut()
        obj.mark_activity_for('tester1', 'm_uid')
        obj.mark_activity_for('tester2', 'm_uid')
        obj.mark_activity_for('tester3', 'm_uid')
        obj.mark_activity_for('tester1', 'm_uid')
        obj.mark_activity_for('tester3', 'm_uid')
        self.assertEqual(len(obj.latest_activity('m_uid')), 3)
        self.assertEqual(len(obj.latest_activity('404_uid')), 0)
        self.assertEqual(len(obj.latest_activity('m_uid', limit=2)), 2)

    def test_latest_activity_limit_pics_correct(self):
        obj = self._cut()
        obj.mark_activity_for('1', 'm_uid')
        obj.mark_activity_for('2', 'm_uid')
        obj.mark_activity_for('3', 'm_uid')
        obj.mark_activity_for('4', 'm_uid')
        obj.mark_activity_for('2', 'm_uid')
        obj.mark_activity_for('1', 'm_uid')
        obj.mark_activity_for('3', 'm_uid')
        obj.mark_activity_for('5', 'm_uid')
        res = [x['userid'] for x in obj.latest_activity('m_uid', limit = 3)]
        self.assertEqual(res, ['5', '3', '1'])

    def test_latest_activity_sort_order(self):
        obj = self._cut()
        obj.mark_activity_for('1', 'm_uid')
        obj.mark_activity_for('2', 'm_uid')
        obj.mark_activity_for('3', 'm_uid')
        obj.mark_activity_for('4', 'm_uid')
        obj.mark_activity_for('2', 'm_uid')
        obj.mark_activity_for('1', 'm_uid')
        obj.mark_activity_for('3', 'm_uid')
        obj.mark_activity_for('5', 'm_uid')
        res = [x['userid'] for x in obj.latest_activity('m_uid')]
        self.assertEqual(res, ['5', '3', '1', '2', '4'])

    def test_latest_user_activity_uid_specified(self):
        obj = self._cut()
        obj.mark_activity_for('1', 'm_uid')
        obj.mark_activity_for('2', 'm_uid')
        obj.mark_activity_for('3', 'm_uid')
        obj.mark_activity_for('2', 'm_uid2')
        self.assertEqual(len(obj.latest_user_activity('2', 'm_uid')), 1)

    def test_latest_user_activity_no_meeting_no_activity_for_user(self):
        obj = self._cut()
        self.assertFalse(obj.latest_user_activity('2'))

    def test_latest_user_activity_meeting_specified_no_activity_for_user(self):
        obj = self._cut()
        self.assertFalse(obj.latest_user_activity('2', 'meeting_uid'))

    def test_latest_user_activity_no_uid(self):
        obj = self._cut()
        obj.mark_activity_for('1', 'm_uid')
        obj.mark_activity_for('2', 'm_uid')
        obj.mark_activity_for('3', 'm_uid')
        obj.mark_activity_for('2', 'm_uid2')
        self.assertEqual(2, len(obj.latest_user_activity('2')))

    def test_subscriber_should_mark_activity(self):
        self.config.include('voteit.whosonline')
        self.config.testing_securitypolicy(userid='ms_tester')
        meeting = self._meeting()
        meeting.uid = 'm_uid'
        request = testing.DummyRequest()
        request.context = meeting['dummy'] = testing.DummyModel()
        event = ContextFound(request)
        request.registry.notify(event)
        util = request.registry.getUtility(IActivityUtil)
        self.assertEqual(len(util.latest_activity('m_uid')), 1)


class WhosOnlineViewTests(TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

#    @property
#    def _fut(self):
#        from voteit.whosonline.views import whosonline
#        return whosonline

    @property
    def _meeting(self):
        from voteit.core.models.meeting import Meeting
        return Meeting

    def test_integration(self):
        from betahaus.viewcomponent import render_view_action
        from voteit.core.views.api import APIView
        self.config.include('voteit.whosonline')
        context = self._meeting()
        request = testing.DummyRequest()
        res = render_view_action(context, request, 'navigation_sections', 'whosonline', api = APIView(context, request)) #Dummy
        self.assertIsInstance(res, unicode)


class LatestActivityViewTests(TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

#    @property
#    def _fut(self):
#        from voteit.whosonline.views import latest_activity
#        return latest_activity

    def _fixture(self):
        return bootstrap_and_fixture(self.config)

    def test_integration(self):
        from betahaus.viewcomponent import render_view_action
        from voteit.core.views.api import APIView
        from voteit.core.models.meeting import Meeting
        self.config.include('voteit.whosonline')
        root = self._fixture()
        context = root['users']['admin']
        request = testing.DummyRequest()
        res = render_view_action(context, request, 'user_info', 'latest_activity', api = APIView(context, request)) #Dummy
        self.assertIsInstance(res, unicode)



def _security_policy(self, userid=None, callback=None):
    from pyramid.authentication import CallbackAuthenticationPolicy
    class MyAuthenticationPolicy(CallbackAuthenticationPolicy):
        def unauthenticated_userid(self, request):
            return userid
    policy = MyAuthenticationPolicy()
    policy.debug = True
    policy.callback = callback
    return policy