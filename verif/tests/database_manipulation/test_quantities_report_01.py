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
quantitiesReport= site.getQuantitiesReport()
quantitiesTable= quantitiesReport.getRows(currencySymbol= '€', limitTextWidth= 50)
refQuantitiesTable= [['barand01', 'Barandilla de 1 m. de altura de acero inoxidabl...', 201.0, 'm', 50344.47, '€'], ['DHA30', 'Hormigón HA-30/B/20/IIIa+Qb, en formación de za...', 444.986, 'm3', 36106.164039999996, '€'], ['PAVMARMOL1', 'Pavimento tipo calzada portuguesa realizado con...', 503.0, 'm2', 33841.840000000004, '€'], ['DPAVHORPUL', 'Pavimento de hormigón HM-25/P/20/IIa de consist...', 1396.0, 'm2', 28492.36, '€'], ['D5.2', 'Suministro y colocación de pletina de acero de ...', 855.34, 'm', 28431.501600000003, '€'], ['pefil1', 'Perfil normalizado de acero galvanizado LPN140.', 178.23000000000002, 'm', 23715.2838, '€'], ['DESPAVCAUCHO', 'Suministro y extendido de pavimento confortplay...', 165.0, 'm2', 19412.25, '€'], ['DPAVA0510', 'Pavimento de aceras con adoquín prefabricado de...', 809.0, 'm2', 19100.489999999998, '€'], ['HUMUSLOMB', 'Humus de lombriz.', 115.0, 't', 17767.5, '€'], ['DMOVI3001', 'Excavación general del terreno existente a maqu...', 5210.0, 'm3', 13233.4, '€'], ['OFRE02', 'Extendido y compactación de zahorras artificial...', 667.6872, 'm3', 10015.307999999999, '€'], ['DSELECRI', 'Selección, cribado, machaqueo y mezcla de los m...', 4689.0, 'm3', 9706.23, '€'], ['DRIESUB', 'Instalación de riego por goteo subterráneo, con...', 3118.0, 'm2', 8574.5, '€'], ['ACERO0103', 'Acero en barras corrugadas, UNE-EN 10080 B 500 ...', 7317.224440000001, 'kg', 8268.463617200001, '€'], ['DALPEDR', 'Pavimento formado por arena de Albero de 10 cm ...', 1168.0, 'm2', 7346.72, '€'], ['DTRTIERRAS', 'Carga mediante máquina de sillares y mampuestos...', 605.605, 'm3', 6316.46015, '€'], ['ARENA10', 'Arena caliza puesta en obra', 800.0, 't', 5600.0, '€'], ['FFB19450', 'Suministro y colocación de tubería PEAD DN 50, ...', 897.0, 'm', 5489.64, '€'], ['RELL0301', 'Formación de terraplén, en tongadas no superior...', 2125.0, 'm3', 5312.5, '€'], ['ENCOFenol1', 'Encofrado y desencofrado plano en alzados de su...', 141.98399999999998, 'm2', 5219.331839999999, '€'], ['ENCOzapatas', 'Encofrado y desencofrado plano en formacion de ...', 346.402, 'm2', 4849.628, '€'], ['DLAMINA', 'Suministro y colocación flotante de lámina impe...', 473.18080000000003, 'm2', 4282.28624, '€'], ['DCANA1203', 'Canalización 3 Ø 90 mm, en prisma de hormigón H...', 319.0, 'm', 4213.990000000001, '€'], ['PAVMARMOL20', 'Pavimento tipo calzada portuguesa realizado en ...', 45.0, 'm2', 3912.2999999999997, '€'], ['FORMAESCALA', 'Pavimento de hormigón HM-25/P/20/IIa , en forma...', 141.0, 'm2', 3681.5099999999998, '€'], ['TERRNATU', 'Tierra natural de prestamo', 213.1984, 'm3', 3345.082896, '€'], ['DTERCAMINOS', 'Formación de terraplén, por medios mecánicos, e...', 521.0, 'm3', 2797.77, '€'], ['DGEOTEX3', 'Suministro y colocación flotante de geotextil a...', 402.64, 'm2', 2697.688, '€'], ['POZO0202', 'Suministro y montaje de pozo de registro prefab...', 3.0, 'ud', 2464.86, '€'], ['CRL0310', 'Hormigón de limpieza HL-15/B/20 fabricado en ce...', 46.25100000000001, 'm3', 2313.0125100000005, '€'], ['DCANA4001', 'Arqueta de 40x40x60 cm. ejecutada con HM-20, se...', 26.0, 'ud', 2210.52, '€'], ['DEXZANJAT', 'Excavación en zanja, pozo o zapatas de muros, a...', 685.2724, 'm3', 2096.933544, '€'], ['DZAHORRAS', 'Relleno y compactación de zanjas por medios mec...', 125.85, 'm3', 2070.2324999999996, '€'], ['DPOMIXTO110', 'Ud. arqueta de 75x75x100 cm de dimensiones inte...', 2.0, 'ud', 1762.22, '€'], ['USJT10abz', 'Preparación del terreno, entrecava desmenuzado,...', 2716.0, 'm2', 1738.24, '€'], ['DCANA4020', 'Arqueta de 60x60x60 cm. ejecutada con HM-20, se...', 8.0, 'ud', 1717.28, '€'], ['CIMENTA01', 'Cimentación de farola de 50*50*70, según planos...', 18.0, 'ud', 1620.8999999999999, '€'], ['TRINTER10', 'Colocación de malla volumétrica de 30 cm.', 124.0, 'm2', 1357.8, '€'], ['TRINTER11', 'Colocación de malla volumétrica de 20 cm.', 146.48000000000002, 'm2', 1267.0520000000001, '€'], ['DTRTIERRAS1', 'Carga mediante máquina y transporte de material...', 415.56, 'm3', 951.6324000000001, '€'], ['TERRANATU2', 'Zahoora natural tamaño 20/50 mm.', 37.912, 'm3', 937.18464, '€'], ['DARENA6', 'Suministro y extendido de arena humeda ( 10% ag...', 59.699999999999996, 'm3', 882.3659999999999, '€'], ['DGEOTEX300', 'Suministro y colocación flotante sobre la base ...', 463.1308, 'm2', 805.8475920000001, '€'], ['CIMENTA02', 'Cimentación de farola de 80*80*80, según planos...', 5.0, 'ud', 758.3, '€'], ['FFB26455', 'Suministro y colocación de tubería PEAD DN 32, ...', 145.0, 'm', 630.75, '€'], ['SSTRATO10', 'Elaboración de "sustrato de plantación".', 155.5, 'm3', 576.905, '€'], ['CATATUB', 'Conexión a tubo de alcantarillado existente DN ...', 1.0, 'PA', 446.08, '€'], ['DCANA1208', 'Canalización 2 Ø 90 mm, en prisma de hormigón H...', 45.0, 'm', 432.45, '€'], ['FFB26425', 'Suministro y colocación de tubería PEAD DN 25, ...', 120.0, 'm', 411.6, '€'], ['DEMpav04a', 'Demolición de pavimentación existente( aceras, ...', 102.0, 'm2', 373.32, '€'], ['DCANA1204', 'Canalización 1 Ø 90 mm, en prisma de hormigón H...', 55.0, 'm', 330.55, '€'], ['DGEOTEX125', 'Suministro y colocación, en protección de apoyo...', 146.48000000000002, 'm2', 240.2272, '€'], ['DALCB0225', 'Cable RV-0.6/1KV. de 2 x 2.5 mm2 colocado bajo ...', 183.0, 'm', 157.38, '€']]

testOK= True
for row, ref_row in zip(quantitiesTable, refQuantitiesTable):
    code= row[0]
    ref_code= ref_row[0]
    testOK= testOK and (code==ref_code)
    title= row[1]
    ref_title= ref_row[1]
    testOK= testOK and (title==ref_title)
    quantity=  row[2]
    ref_quantity= ref_row[2]
    err= abs(quantity-ref_quantity)/ref_quantity
    testOK= testOK and (abs(err)<1e-6)
    unit= row[3]
    ref_unit= ref_row[3]
    testOK= testOK and (unit==ref_unit)
    price= row[4]
    ref_price= ref_row[4]
    err= abs(price-ref_price)/ref_price
    testOK= testOK and (abs(err)<1e-6)
    currency= row[5]
    ref_currency= ref_row[5]
    testOK= testOK and (currency==ref_currency)
    if(not testOK):
        break
    # print(code, title, basic_types.human_readable(quantity, decPlaces= 3), unit, basic_types.human_readable_currency(price), currency)

import os
import logging
fname= os.path.basename(__file__)
if testOK:
    print('test: '+fname+': ok.')
else:
    logging.error('test: '+fname+' ERROR.')
