from BTrees.OOBTree import OOBTree
from zope.interface import implements

from voteit.whosonline.interfaces import IActivityUtil


class ActivityUtil(object):
    """ See IActivityUtil """
    implements(IActivityUtil)
    
    def __init__(self):
        pass