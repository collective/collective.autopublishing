import unittest
import doctest
import interlude

from Testing import ZopeTestCase as ztc

from collective.autopublishing.tests.layer import MyFunctionalTestCase

optionflags = (doctest.NORMALIZE_WHITESPACE|
               doctest.ELLIPSIS|
               doctest.REPORT_NDIFF)

def test_suite():
    suite = ztc.FunctionalDocFileSuite(
        'test_autopublishing.txt',
        optionflags=optionflags,
        test_class=MyFunctionalTestCase,
        globs=dict(interact=interlude.interact))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
