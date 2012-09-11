from unittest import TestCase

from pyramid import testing
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

from voteit.whosonline.interfaces import IActivityUtil


class UtilityTests(TestCase):

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

    def test_integration(self):
        self.config.include('voteit.whosonline')
        self.failUnless(self.config.registry.queryUtility(IActivityUtil))

    def test_mark_activity_for(self):
        from datetime import datetime
        obj = self._cut()
        obj.mark_activity_for('tester', 'm_uid', somedata = True, others = False)
        self.assertEqual(set(obj._storage['m_uid']['tester'].keys()), set(['somedata', 'dt', 'others', 'userid']))
        self.assertIsInstance(obj._storage['m_uid']['tester']['dt'], datetime)

    def test_maybe_mark(self):
        self.config.testing_securitypolicy(userid='ms_tester')
        context = self._meeting(uid = 'uid')
        request = testing.DummyRequest()
        obj = self._cut()
        obj.maybe_mark(context, request)
        self.assertEqual(len(obj._storage), 1)
        self.assertIn('ms_tester', obj._storage['uid'])

    def test_dont_mark_anon(self):
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
