from Products.PloneTestCase import ptc

from collective.testcaselayer import ptc as tcl_ptc
from collective.testcaselayer import common

class Layer(tcl_ptc.BasePTCLayer):
    """Install collective.autopublishing"""

    def afterSetUp(self):
        import collective.timedevents
        import collective.autopublishing
        self.loadZCML('configure.zcml', package=collective.timedevents)
        self.loadZCML('configure.zcml', package=collective.autopublishing)
        ptc.installPackage('collective.autopublishing')
        self.addProfile('collective.autopublishing:default')

layer = Layer([common.common_layer])

class MyFunctionalTestCase(ptc.FunctionalTestCase):
    layer = layer
