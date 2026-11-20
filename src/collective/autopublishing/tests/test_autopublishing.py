from collective.autopublishing.tests.layer import C_AUTOPUBLISHING_LAYER
from plone.testing import layered

import doctest

optionflags = (
    doctest.NORMALIZE_WHITESPACE
    | doctest.ELLIPSIS
    | doctest.REPORT_NDIFF
    | doctest.REPORT_ONLY_FIRST_FAILURE
)


def test_suite():
    suite = layered(
        doctest.DocFileSuite(
            "test_autopublishing.txt",
            optionflags=optionflags,
        ),
        layer=C_AUTOPUBLISHING_LAYER,
    )
    return suite


# EOF
