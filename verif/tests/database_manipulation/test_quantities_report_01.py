# -*- coding: utf-8 -*-
'''Extract concepts from unit cost databases.''' 
from __future__ import division
from __future__ import print_function

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import sys
import yaml
from pycost.structure import obra
from pycost.utils import basic_types
from operator import itemgetter

# Create main object.
site= obra.Obra(cod="test", tit="Test title")

# Read data from file.
import os
pth= os.path.dirname(__file__)
# print("pth= ", pth)
if(not pth):
    pth= '.'
pendingLinks= site.readFromYaml(pth+'/../data/yaml/test_file_05.yaml')

# Get quantities report in tabular format.
quantitiesTable= list()
quantitiesReport= site.getQuantitiesReport()
quantitiesFormatString= basic_types.quantitiesFormatString
for unitPrice in quantitiesReport:
    quantity= quantitiesReport[unitPrice]
    title= unitPrice.title
    if(len(title)>50):
        title= title[0:37]+'...'
    unit= basic_types.fix_unit_text(unitPrice.unidad)
    price= float(unitPrice.getPrice())*quantity
    quantitiesTable.append([title, quantity, unit, price, '€'])


# Bigger amount first.
quantitiesTable= list(reversed(sorted(quantitiesTable, key=itemgetter(3))))
refQuantitiesTable= [['Barandilla de 1 m. de altura de acero...', 201.0, 'm', 50344.47, '€'], ['Hormigón HA-30/B/20/IIIa+Qb, en forma...', 444.986, 'm3', 36106.164039999996, '€'], ['Pavimento tipo calzada portuguesa rea...', 503.0, 'm2', 33841.840000000004, '€'], ['Pavimento de hormigón HM-25/P/20/IIa ...', 1396.0, 'm2', 28492.36, '€'], ['Suministro y colocación de pletina de...', 855.34, 'm', 28431.501600000003, '€'], ['Perfil normalizado de acero galvanizado LPN140.', 178.23000000000002, 'm', 23715.2838, '€'], ['Suministro y extendido de pavimento c...', 165.0, 'm2', 19412.25, '€'], ['Pavimento de aceras con adoquín prefa...', 809.0, 'm2', 19100.489999999998, '€'], ['Humus de lombriz.', 115.0, 't', 17767.5, '€'], ['Excavación general del terreno existe...', 5210.0, 'm3', 13233.4, '€'], ['Extendido y compactación de zahorras ...', 667.6872, 'm3', 10015.307999999999, '€'], ['Selección, cribado, machaqueo y mezcl...', 4689.0, 'm3', 9706.23, '€'], ['Instalación de riego por goteo subter...', 3118.0, 'm2', 8574.5, '€'], ['Acero en barras corrugadas, UNE-EN 10...', 7317.224440000001, 'kg', 8268.463617200001, '€'], ['Pavimento formado por arena de Albero...', 1168.0, 'm2', 7346.72, '€'], ['Carga mediante máquina de sillares y ...', 605.605, 'm3', 6316.46015, '€'], ['Arena caliza puesta en obra', 800.0, 't', 5600.0, '€'], ['Suministro y colocación de tubería PE...', 897.0, 'm', 5489.64, '€'], ['Formación de terraplén, en tongadas n...', 2125.0, 'm3', 5312.5, '€'], ['Encofrado y desencofrado plano en alz...', 141.98399999999998, 'm2', 5219.331839999999, '€'], ['Encofrado y desencofrado plano en for...', 346.402, 'm2', 4849.628, '€'], ['Suministro y colocación flotante de l...', 473.18080000000003, 'm2', 4282.28624, '€'], ['Canalización 3 Ø 90 mm, en prisma de ...', 319.0, 'm', 4213.990000000001, '€'], ['Pavimento tipo calzada portuguesa rea...', 45.0, 'm2', 3912.2999999999997, '€'], ['Pavimento de hormigón HM-25/P/20/IIa ...', 141.0, 'm2', 3681.5099999999998, '€'], ['Tierra natural de prestamo', 213.1984, 'm3', 3345.082896, '€'], ['Formación de terraplén, por medios me...', 521.0, 'm3', 2797.77, '€'], ['Suministro y colocación flotante de g...', 402.64, 'm2', 2697.688, '€'], ['Suministro y montaje de pozo de regis...', 3.0, 'ud', 2464.86, '€'], ['Hormigón de limpieza HL-15/B/20 fabri...', 46.25100000000001, 'm3', 2313.0125100000005, '€'], ['Arqueta de 40x40x60 cm. ejecutada con...', 26.0, 'ud', 2210.52, '€'], ['Excavación en zanja, pozo o zapatas d...', 685.2724, 'm3', 2096.933544, '€'], ['Relleno y compactación de zanjas por ...', 125.85, 'm3', 2070.2324999999996, '€'], ['Ud. arqueta de 75x75x100 cm de dimens...', 2.0, 'ud', 1762.22, '€'], ['Preparación del terreno, entrecava de...', 2716.0, 'm2', 1738.24, '€'], ['Arqueta de 60x60x60 cm. ejecutada con...', 8.0, 'ud', 1717.28, '€'], ['Cimentación de farola de 50*50*70, se...', 18.0, 'ud', 1620.8999999999999, '€'], ['Colocación de malla volumétrica de 30 cm.', 124.0, 'm2', 1357.8, '€'], ['Colocación de malla volumétrica de 20 cm.', 146.48000000000002, 'm2', 1267.0520000000001, '€'], ['Carga mediante máquina y transporte d...', 415.56, 'm3', 951.6324000000001, '€'], ['Zahoora natural tamaño 20/50 mm.', 37.912, 'm3', 937.18464, '€'], ['Suministro y extendido de arena humed...', 59.699999999999996, 'm3', 882.3659999999999, '€'], ['Suministro y colocación flotante sobr...', 463.1308, 'm2', 805.8475920000001, '€'], ['Cimentación de farola de 80*80*80, se...', 5.0, 'ud', 758.3, '€'], ['Suministro y colocación de tubería PE...', 145.0, 'm', 630.75, '€'], ['Elaboración de "sustrato de plantación".', 155.5, 'm3', 576.905, '€'], ['Conexión a tubo de alcantarillado exi...', 1.0, 'PA', 446.08, '€'], ['Canalización 2 Ø 90 mm, en prisma de ...', 45.0, 'm', 432.45, '€'], ['Suministro y colocación de tubería PE...', 120.0, 'm', 411.6, '€'], ['Demolición de pavimentación existente...', 102.0, 'm2', 373.32, '€'], ['Canalización 1 Ø 90 mm, en prisma de ...', 55.0, 'm', 330.55, '€'], ['Suministro y colocación, en protecció...', 146.48000000000002, 'm2', 240.2272, '€'], ['Cable RV-0.6/1KV. de 2 x 2.5 mm2 colo...', 183.0, 'm', 157.38, '€']]

testOK= True
for row, ref_row in zip(quantitiesTable, refQuantitiesTable):
    title= row[0]
    ref_title= ref_row[0]
    testOK= testOK and (title==ref_title)
    quantity=  row[1]
    ref_quantity= ref_row[1]
    err= abs(quantity-ref_quantity)/ref_quantity
    testOK= testOK and (abs(err)<1e-6)
    unit= row[2]
    ref_unit= ref_row[2]
    testOK= testOK and (unit==ref_unit)
    price= row[3]
    ref_price= ref_row[3]
    err= abs(price-ref_price)/ref_price
    testOK= testOK and (abs(err)<1e-6)
    currency= row[4]
    ref_currency= ref_row[4]
    testOK= testOK and (currency==ref_currency)
    if(not testOK):
        break
    # print(title, basic_types.human_readable(quantity, decPlaces= 3), unit, basic_types.human_readable_currency(price), currency)

import os
import logging
fname= os.path.basename(__file__)
if testOK:
    print('test: '+fname+': ok.')
else:
    logging.error('test: '+fname+' ERROR.')
