import unittest
import doctest
import interlude
from plone.testing import layered


from collective.autopublishing.tests.layer import C_AUTOPUBLISHING_LAYER

optionflags = (doctest.NORMALIZE_WHITESPACE|
               doctest.ELLIPSIS|
               doctest.REPORT_NDIFF|
               doctest.REPORT_ONLY_FIRST_FAILURE)

def test_suite():
    suite = layered(doctest.DocFileSuite(
        'test_autopublishing.txt',
        optionflags=optionflags,
        globs=dict(interact=interlude.interact)),
        layer=C_AUTOPUBLISHING_LAYER)
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
