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
from pycost.measurements import measurement_report
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
elementaryQuantities= site.getElementaryQuantitiesReport()
limitTextWidth= 50
currencySymbol= '€'
biggestAmountFirst= True
elementary_quantities_list= measurement_report.get_rows_elementary_quantities(elementaryQuantitiesDict= elementaryQuantities, currencySymbol= currencySymbol, biggestAmountFirst= biggestAmountFirst, limitTextWidth= limitTextWidth)

ref_elementary_quantities_list= [['ACEROX1', 'Acero Inóxidable AISI 316.', 201.0, 'kg', 35175.0, '€'], ['UHA30', 'Hormigón HA-30/B/20/IIIa+Qb, fabricado en centr...', 467.2353, 'm3', 28417.250946, '€'], ['MARMOL1', 'Pieza de granito berrocal gris oscura, tamaño m...', 575.4, 'm2', 25893.0, '€'], ['PEON', 'Peón Ordinario', 1921.3718450000003, 'h', 24401.422431500003, '€'], ['OFIC', 'Oficial 1ª', 1518.636925, 'h', 22126.53999725, '€'], ['PGALVA1', 'Perfil LPN 140.', 178.23000000000002, 'm', 21565.83, '€'], ['UPLEACOR', 'Pletina de acero galvanizado  de 100 x 10 mm', 855.34, 'm', 21383.5, '€'], ['DESPAVCAUCHO', 'Suministro y extendido de pavimento confortplay...', 165.0, 'm2', 19412.25, '€'], ['HUMUSLOMB1', 'Humus ds lombriz', 115.0, 't', 17250.0, '€'], ['UHORACERO', 'Hormigón HM-25/P/20/IIa de consistencia plástic...', 230.55, 'm3', 16256.080500000002, '€'], ['UZAHO0102', 'Zahorra artificial.', 1055.9297, 'm3', 13325.832813999998, '€'], ['UPALA0101', 'Pala Cargadora sobre neumáticos', 338.1179000000001, 'h', 10576.327912000002, '€'], ['UHM20', 'Hormigón HM-20/P/20/I', 180.5, 'm3', 8954.605, '€'], ['MQCAMI0101', 'Camión volquete de 20 Tm.', 269.4379, 'h', 7010.774158, '€'], ['MQRETR0102', 'Retroexcavadora con martillo hidráulico, sobre ...', 157.82999999999998, 'h', 6846.6654, '€'], ['UBALD0110', 'Adoquín de hormigón bicapa color gris, de 20x20...', 20225.0, 'ud', 6472.0, '€'], ['MO0201', 'Oficial 1ª', 429.82399999999996, 'h', 6262.535679999999, '€'], ['ARENA10', 'Arena caliza puesta en obra', 800.0, 't', 5600.0, '€'], ['TH66072', 'MANG.UNIBIOLINE 17/120 2,3L/H 40CM', 5924.2, 'm', 5568.748, '€'], ['PEONES', 'Peón especializado', 374.46536660000004, 'h', 5148.89879075, '€'], ['MAACE0201', '', 7830.428440000001, 'KG', 4854.865632800001, '€'], ['MAENCO0111', 'Encofrado y desencofrado plano en alzados de su...', 346.402, 'm2', 4156.824, '€'], ['MO0101', 'Peón Ordinario', 289.74, 'h', 3679.698, '€'], ['MAENCO0110', 'Encofrado y desencofrado plano en alzados de su...', 14.1984, 'm2', 3549.6, '€'], ['PULI', 'Pulidora/helicóptero mecánica', 230.55, 'h', 3370.641, '€'], ['TERRNATU', 'Tierra natural de prestamo', 213.1984, 'm3', 3345.082896, '€'], ['ULAMI', 'Lámina impermeable de caucho EPDM Geomembrana d...', 496.83984000000004, 'm2', 3254.300952, '€'], ['OFICMON', 'Oficial 1a montador', 168.21, 'h', 3051.3294, '€'], ['UTPOL0102', 'Canalización DN 90 mm de Polietileno corrugado ...', 957.0, 'm', 2823.15, '€'], ['UMOTO0102', 'Motoniveladora 150 CV.', 55.5256, 'h', 2649.1263759999997, '€'], ['UCOMP0202', 'Compactador vibratorio autopropulsado.', 108.09595999999999, 'h', 2535.9312216, '€'], ['URETR0101', 'Retroexcavadora sobre neumáticos.', 85.81043999999999, 'h', 2272.2604512, '€'], ['UTRITU', 'Tritutadora de mandíbulas o similar', 140.67, 'h', 2253.5334, '€'], ['UMORT', 'Mortero c.p. M-40:a (1:6)', 32.36, 'm3', 2227.3388, '€'], ['mt10hmf011', 'Hormigón de limpieza HL-15/B/20, fabricado en c...', 46.25100000000001, 'm³', 2158.534170000001, '€'], ['UHOR55', 'Mortero de cementos blanco y gris 1:4.', 26.304000000000002, 'm3', 2104.32, '€'], ['UGEOTX3', 'Flotante de geotextil antiraices con acabado li...', 422.772, 'm2', 2071.5828, '€'], ['OFICFER', 'Oficial ferrallista', 109.7583666, 'h', 1991.016770124, '€'], ['UTAMIZ', 'Tamiz', 140.67, 'h', 1877.9444999999998, '€'], ['BFB19400', 'Tubería PEAD DN 50, PN 10, serie SDR 17, fabric...', 914.94, 'm', 1656.0414, '€'], ['USUELADEC0101', 'Suelo adecuado procedente de préstamo', 521.0, 'm3', 1651.57, '€'], ['UAREN0103', 'Arena tipo Albero.', 116.80000000000001, 'm3', 1630.5280000000002, '€'], ['OFICJAR', 'Oficial jardinero', 81.31200000000001, 'h', 1474.9996800000004, '€'], ['UBAND', 'Bandeja compactadora/vibratoria', 60.77, 'h', 1098.1139, '€'], ['UTAPA110', 'Registro de fundición clase C 250, según la nor...', 2.0, 'ud', 1089.12, '€'], ['UCAMI0201', 'Camión cisterna 6 m3.', 51.37, 'h', 1071.0645, '€'], ['OFICENC', 'Oficial encofrador', 56.616099999999996, 'h', 1027.016054, '€'], ['MAHOR0101', 'Hormigón HM-20/P/20/I, suministrado de central,...', 22.65868, 'm3', 957.32923, '€'], ['TERRAAYU', 'Zahoora natural 20/50 mm.', 37.912, 'm3', 909.8879999999999, '€'], ['PEONENC', 'Peón encofrador', 63.71529999999999, 'h', 876.0853749999999, '€'], ['malla10vol', 'Malla volumétrica de confinamiento celular form...', 124.0, 'm2', 744.0, '€'], ['UTAPA4004', 'Marco y tapa de 60x60 cms. de fundición.', 8.0, 'ud', 685.76, '€'], ['UGEOTEX1', 'Geotextil separador 100% fibras vírgenes de pol...', 486.28734000000003, 'm2', 656.4879090000001, '€'], ['UAREN0101', 'Arena gruesa de 6 mm de tamaño máximo de grano,...', 59.699999999999996, 'm3', 598.7909999999999, '€'], ['ANILLO02', 'Módulo de recrecido con parte superior cónico a...', 3.0, 'ud', 584.55, '€'], ['UENCO4001', 'Encofrado y desencofrado metálico, a dos caras ...', 26.0, 'ud', 576.68, '€'], ['UTAPA0101', 'Marco circular y tapa de pozo de registro Ø 60 ...', 3.0, 'ud', 576.3, '€'], ['UENCO4020', 'Encofrado y desencofrado metálico para cimentac...', 36.0, 'ud', 567.36, '€'], ['UTAPA4001', 'Marco y tapa de 40x40 cms. de fundición.', 26.0, 'ud', 557.6999999999999, '€'], ['malla11vol', 'malla volumétrica de confinamiento celular form...', 146.48000000000002, 'm2', 547.8352000000001, '€'], ['BFWB1942', 'Accesorio p/tubos poliet.alta dens.DN=63mm, plá...', 269.09999999999997, 'ud', 487.07099999999997, '€'], ['UBULL0101', 'Bulldozer 140 CV (D-6) sobre orugas.', 11.68, 'h', 486.7056, '€'], ['C2003000', 'Fratás mecánico', 115.275, 'h', 480.69675, '€'], ['CATATUB', 'Conexión a tubo de alcantarillado existente DN ...', 1.0, 'PA', 446.08, '€'], ['USIKA', 'Mortero especial de apoyo y fijación de tapa, d...', 0.44000000000000006, 'm3', 402.18640000000005, '€'], ['Q004', 'Dich-Witch 255 tech-line.', 37.416000000000004, 'h', 400.3512, '€'], ['MMME.6a', 'Tractor agrícola neumáticos 70cv', 40.74, 'h', 394.3632, '€'], ['UPIE4300', 'Suministro y colocación de plaqueta de grés vit...', 150.0, 'ud', 337.5, '€'], ['UTPOL0105', 'Canalización DN 90 mm de Polietileno corrugado ...', 113.0, 'm', 333.35, '€'], ['UENCO4021', 'Encofrado y desencofrado metálico para cimentac...', 18.0, 'ud', 283.68, '€'], ['Monatage100', 'Estructura soporte encofrado', 0.9938879999999999, 'ud', 273.31919999999997, '€'], ['TK26300', 'Accesorios varios', 62.36, 'ud', 263.7828, '€'], ['UENCO4002', 'Encofrado y desencofrado metálico para arqueta ...', 16.0, 'ud', 252.16, '€'], ['ANILLO01', 'Módulo base prefabricado de hormigón armado, co...', 3.0, 'ud', 246.14999999999998, '€'], ['MAENCO0103', 'Encofrado y desencofrado plano en alzados de su...', 15.2, 'm2', 209.76, '€'], ['BFWB2605', 'Accesorio p/tubos PE baja dens.DN=32mm, plást.,...', 79.5, 'ud', 199.545, '€'], ['ULAMGEOTEX', 'Flotante de geotextil Typar SF-37 o equivalente...', 153.80400000000003, 'm2', 193.79304000000005, '€'], ['UPIE1300', 'Media sección de gres de 0,60 m de longitud, no...', 3.0, 'ud', 165.81, '€'], ['UTPOL0103', 'Canalización DN 90 mm de Polietileno corrugado ...', 55.0, 'm', 162.25, '€'], ['BFB26400', 'Tubería PEAD DN 32, PN 10, serie SDR 17, fabric...', 147.9, 'm', 125.715, '€'], ['UPATE0101', 'Pate polipropileno, alma de acero, norma EN13101', 18.0, 'ud', 122.39999999999999, '€'], ['MQCAMI0301', 'Camión grúa 10 Tn', 5.0, 'h', 120.9, '€'], ['UCABL0202', 'Cable tipo RV-0,6/1 KV de 2 x 2,5 mm2., subterr...', 183.0, 'm', 115.29, '€'], ['UPALA0301', 'Pala cargadora-retroexcavadora.', 4.147436, 'h', 110.48769504, '€'], ['Q003', 'Mini-Retroexcavadora.', 6.236, 'h', 92.04335999999999, '€'], ['BFB26425', 'Tubería PEAD DN 25, PN 10, serie SDR 17, fabric...', 122.4, 'm', 73.44, '€'], ['UACER0501', 'Guía de alambre de acero galvanizado Ø 1 mm.', 838.0, 'm', 67.04, '€'], ['ANILLO04', 'Anillo de ajuste de 10/8/6 cm de altura y diáme...', 3.0, 'ud', 42.269999999999996, '€'], ['LADPANAL5', 'Ladrillo Panal', 116.0, 'ud', 34.8, '€'], ['UOFIC0101', 'Oficial 1ª', 2.0, 'h', 29.14, '€'], ['UCINC0101', 'Cinta de "atención cable"', 419.0, 'm', 16.76, '€'], ['DESMOLDEA1', 'Agente desmoldeante biodegradable en fase acuos...', 1.8457919999999997, 'l', 15.043204799999998, '€'], ['UMORT5', 'Mortero M5', 0.15000000000000002, 'm3', 10.4985, '€'], ['UCOMR0101', '', 0.75, 'h', 7.5075, '€'], ['%', 'Medios auxiliares', 4.0572, '%', 0.0, '€'], ['%UMAUX0103', '3 % Medios auxiliares', 256.9455, '%', 0.0, '€'], ['%003', '3 % Medios auxiliares', 904.1555292000002, '%', 0.0, '€']]

testOK= True
for row, ref_row in zip(elementary_quantities_list, ref_elementary_quantities_list):
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
    err= abs(price-ref_price)
    if(ref_price>0.0):
        err/= ref_price
    testOK= testOK and (abs(err)<1e-6)
    currency= row[5]
    ref_currency= ref_row[5]
    testOK= testOK and (currency==ref_currency)
    if(not testOK):
        print(code, title, basic_types.human_readable(quantity, decPlaces= 3), unit, basic_types.human_readable_currency(price), currency)
        print(ref_code, ref_title, basic_types.human_readable(ref_quantity, decPlaces= 3), ref_unit, basic_types.human_readable_currency(ref_price), ref_currency)
        break

import os
import logging
fname= os.path.basename(__file__)
if testOK:
    print('test: '+fname+': ok.')
else:
    logging.error('test: '+fname+' ERROR.')


