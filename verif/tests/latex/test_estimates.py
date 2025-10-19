'''Test data.'''
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
