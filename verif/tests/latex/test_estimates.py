'''Test data.'''

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AO_O)"
__copyright__= "Copyright 2017, LCPT and AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es" "ana.Ortega@ciccp.es"

import os
from pycost.structure import obra
from pycost.structure.chapter import Chapter
from pycost.structure.unit_price_quantities import UnitPriceQuantities

def test(pth):
    retval= obra.Obra(cod="test", tit="Test title")

    retval.readFromYaml(pth+'/../data/yaml/test_03_prices.yaml')

    ch01= retval.newSubChapter(Chapter(cod= '01', tit= 'Test'))

    # Measurements
    ## MAACE0201 quantities.
    rebarMeasurements= UnitPriceQuantities(retval.getUnitPrice('MAACE0201'))
    q1units= 2
    q1l= 10.0
    rebarMeasurements.appendMeasurement(textComment='test A', nUnits= q1units, length= q1l, width=None, height=None)
    ch01.appendUnitPriceQuantities(rebarMeasurements)

    ## ACERO0103 quantities.
    reinfMeasurements= UnitPriceQuantities(retval.getUnitPrice('ACERO0103'))
    q2units= 20
    q2l= 25.0
    reinfMeasurements.appendMeasurement(textComment='test B', nUnits= q2units, length= q2l, width=None, height=None)
    ch01.appendUnitPriceQuantities(reinfMeasurements)
    return retval
