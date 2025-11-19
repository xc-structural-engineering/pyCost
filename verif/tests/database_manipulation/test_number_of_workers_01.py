# -*- coding: utf-8 -*-
'''Trivial PyCost test concerning the use of nested compound prices.''' 
from __future__ import division
from __future__ import print_function

from pycost.utils import basic_types
from pycost.prices import elementary_price
from pycost.prices import unit_price
from pycost.structure import unit_price_quantities
from pycost.structure import chapter
from pycost.structure import obra
from pycost.measurements import measurement_report

# Create root chapter.
site= obra.Obra(cod="test", tit="Test title")

# Create elementary prices.
ofic1a= elementary_price.ElementaryPrice(cod='OFIC1a', tit= '1st class tradesman', ud= 'h', p= 18.14, tp= basic_types.mdo, long_description= 'First class tradesman')
site.precios.elementos.Append(ofic1a) # Append elementary price.

ofic2a= elementary_price.ElementaryPrice(cod='OFIC2a', tit= '2nd class tradesman', ud= 'h', p= 17.24, tp= basic_types.mdo, long_description= 'Second class tradesman')
site.precios.elementos.Append(ofic2a) # Append elementary price.

peon= elementary_price.ElementaryPrice(cod='PEON', tit= 'Specialized laborer', ud= 'h', p= 13.75, tp= basic_types.mdo, long_description= 'Specialized laborer')
site.precios.elementos.Append(peon) # Append elementary price.

rawSteel= elementary_price.ElementaryPrice(cod='rawSteel', tit= 'Reinforcing steel', ud= 'kg', p= 1.2, tp= basic_types.mat, long_description= 'Reinforcing steel')
site.precios.elementos.Append(rawSteel) # Append elementary price.

rawConcrete= elementary_price.ElementaryPrice(cod='rawConcrete', tit= 'Raw concrete', ud= 'm3', p= 75, tp= basic_types.mat, long_description= 'Raw concrete')
site.precios.elementos.Append(rawConcrete) # Append elementary price.

# Create unit prices.
## Reinforcing steel.
reinforcingSteel= unit_price.UnitPrice(cod="reinforcingSteel", desc="Reinforcement steel.", ud="kg", ld= "Reinforcement steel.")
### Append unit price components.
reinforcingSteel.Append(entity= ofic1a, f= 1.0, r= .015)
reinforcingSteel.Append(entity= peon, f= 1.0, r= .15)
reinforcingSteel.Append(entity= rawSteel, f= 1.0, r= 1.0)
site.precios.unidades.Append(reinforcingSteel)

## Workers group.
cuadrilla= unit_price.UnitPrice(cod="cuadrilla", desc="Cuadrilla.", ud="h", ld= "Cuadrilla.")
### Append unit price components.
cuadrilla.Append(entity= ofic1a, f= 1.0, r= 0.1)
cuadrilla.Append(entity= ofic2a, f= 1.0, r= 0.25)
cuadrilla.Append(entity= peon, f= 1.0, r= 1.0)
site.precios.unidades.Append(cuadrilla)

## Concrete.
concrete= unit_price.UnitPrice(cod="concrete", desc="Reinforcement steel.", ud="kg", ld= "Reinforcement steel.")
### Append unit price components.
concrete.Append(entity= cuadrilla, f= 1.0, r= 0.5)
concrete.Append(entity= reinforcingSteel, f= 1.0, r= 60.0)
concrete.Append(entity= rawConcrete, f= 1.0, r= 1.0)
site.precios.unidades.Append(concrete)

numberOfWorkers= concrete.getNumberOfWorkers()
refNumberOfWorkers= 2+3 # cuadrilla:3, reinforcing steel: 2

# print(numberOfWorkers)

import os
import logging
fname= os.path.basename(__file__)
if (numberOfWorkers==refNumberOfWorkers):
    print('test: '+fname+': ok.')
else:
    logging.error('test: '+fname+' ERROR.')
