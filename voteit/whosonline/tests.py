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

    def test_verify_class(self):
        self.failUnless(verifyClass(IActivityUtil, self._cut))

    def test_verify_obj(self):
        self.failUnless(verifyObject(IActivityUtil, self._cut()))

    def test_integration(self):
        self.config.include('voteit.whosonline')
        self.failUnless(self.config.registry.queryUtility(IActivityUtil))
