# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from pycost.structure import obra
from pycost.utils import basic_types
from pycost.structure.chapter import Chapter
from pycost.prices import elementary_price 
from pycost.prices.elementary_price import ElementaryPrice
from pycost.prices.unit_price import UnitPrice
from pycost.bc3.bc3_component import BC3Component
from pycost.bc3 import fr_entity
from pycost.utils.concept_dict import find_concept
from pycost.structure.unit_price_quantities import UnitPriceQuantities
from pycost.measurements.measurement_record import MeasurementRecord
from pycost.prices import unit_price
from pycost.utils.structural_members import foundations as found
from pycost.utils.structural_members import walls as wall
from pycost.utils.structural_members import columns as col
from pycost.utils.structural_members import deck as deck
from pycost.utils.structural_members import finishes as finish


budget=obra.Obra(cod='budget_struct',tit='Measurement structural members')

#    ***********    Prices   ***************
noBreakdown= elementary_price.ElementaryPrice(cod='NOBREAKDOWN', tit= 'Without breakdown', ud= 'ud', p= 1.0, tp= basic_types.sin_clasif, long_description= 'Without breakdown')
budget.precios.elementos.Append(noBreakdown) # Append elementary price.

descr='Excavation'
price=10.00 
prExcav=unit_price.UnitPrice(cod='001', desc=descr, ud='m3', ld= descr)
prExcav.Append(entity= noBreakdown, f= 1.0, r=price)
budget.precios.unidades.Append(prExcav)

descr='Lean concrete'
price=80.00 
prLeanConcr=unit_price.UnitPrice(cod='002', desc=descr, ud='m3', ld= descr)
prLeanConcr.Append(entity= noBreakdown, f= 1.0, r=price)
budget.precios.unidades.Append(prLeanConcr)

descr='Hidden formwork'
price=30.00 
prHiddFormwork=unit_price.UnitPrice(cod='003', desc=descr, ud='m2', ld= descr)
prHiddFormwork.Append(entity= noBreakdown, f= 1.0, r=price)
budget.precios.unidades.Append(prHiddFormwork)

descr='Exposed formwork'
price=32.00 
prExposFormwork=unit_price.UnitPrice(cod='004', desc=descr, ud='m2', ld= descr)
prExposFormwork.Append(entity= noBreakdown, f= 1.0, r=price)
budget.precios.unidades.Append(prExposFormwork)

descr='Reinforcing steel'
price=2.50 
prReinfSteel=unit_price.UnitPrice(cod='005', desc=descr, ud='kg', ld= descr)
prReinfSteel.Append(entity= noBreakdown, f= 1.0, r=price)
budget.precios.unidades.Append(prReinfSteel)


descr='Concrete'
price=150.00 
prConcr=unit_price.UnitPrice(cod='006', desc=descr, ud='m3', ld= descr)
prConcr.Append(entity= noBreakdown, f= 1.0, r=price)
budget.precios.unidades.Append(prConcr)


descr='Waterproofing primer'
price=50.00 
prWaterproofPrimer=unit_price.UnitPrice(cod='007a', desc=descr, ud='m2', ld= descr)
prWaterproofPrimer.Append(entity= noBreakdown, f= 1.0, r=price)
budget.precios.unidades.Append(prWaterproofPrimer)

descr='Waterproofing layer'
price=50.00 
prWaterproofLayer=unit_price.UnitPrice(cod='007b', desc=descr, ud='m2', ld= descr)
prWaterproofLayer.Append(entity= noBreakdown, f= 1.0, r=price)
budget.precios.unidades.Append(prWaterproofLayer)

descr='Drainage tube'
price=20.00 
prDrainTub=unit_price.UnitPrice(cod='008', desc=descr, ud='m', ld= descr)
prDrainTub.Append(entity= noBreakdown, f= 1.0, r=price)
budget.precios.unidades.Append(prDrainTub)

descr='Joint'
price=60.00 
prJoint=unit_price.UnitPrice(cod='009', desc=descr, ud='m', ld= descr)
prJoint.Append(entity= noBreakdown, f= 1.0, r=price)
budget.precios.unidades.Append(prJoint)

descr='Drainage fill material'
price=35.00 
prDrainFill=unit_price.UnitPrice(cod='010', desc=descr, ud='m3', ld= descr)
prDrainFill.Append(entity= noBreakdown, f= 1.0, r=price)
budget.precios.unidades.Append(prDrainFill)

descr='Fill material'
price=25.00 
prFill=unit_price.UnitPrice(cod='010', desc=descr, ud='m3', ld= descr)
prFill.Append(entity= noBreakdown, f= 1.0, r=price)
budget.precios.unidades.Append(prFill)

descr='Pile drilling'
price=200.00 
prPileDrill=unit_price.UnitPrice(cod='011', desc=descr, ud='m', ld= descr)
prPileDrill.Append(entity= noBreakdown, f= 1.0, r=price)
budget.precios.unidades.Append(prPileDrill)

descr='Curved formwork'
price=45.00 
prCurvFormwork=unit_price.UnitPrice(cod='012', desc=descr, ud='m2', ld= descr)
prCurvFormwork.Append(entity= noBreakdown, f= 1.0, r=price)
budget.precios.unidades.Append(prCurvFormwork)

descr='Neoprene bearing pad'
price=60
prNeoprene=unit_price.UnitPrice(cod='013', desc=descr, ud='dm3', ld= descr)
prNeoprene.Append(entity= noBreakdown, f= 1.0, r=price)
budget.precios.unidades.Append(prNeoprene)

escr='Sidewalk (m3)'
price=200
prSidewalk=unit_price.UnitPrice(cod='014', desc=descr, ud='m3', ld= descr)
prSidewalk.Append(entity= noBreakdown, f= 1.0, r=price)
budget.precios.unidades.Append(prSidewalk)


escr='Cornice'
price=400
prCornice=unit_price.UnitPrice(cod='015', desc=descr, ud='m', ld= descr)
prCornice.Append(entity= noBreakdown, f= 1.0, r=price)
budget.precios.unidades.Append(prCornice)




#   **************** Chapters ********************
chFound=budget.subcapitulos.newChapter(Chapter(cod= '01',tit='Foundations'))
chWalls=budget.subcapitulos.newChapter(Chapter(cod= '02',tit='Walls'))
chColumns=budget.subcapitulos.newChapter(Chapter(cod= '03',tit='Columns'))
chDeck=budget.subcapitulos.newChapter(Chapter(cod= '04',tit='Deck'))
chFinishes=budget.subcapitulos.newChapter(Chapter(cod= '05',tit='Finishes'))

# ************ Foundation Measurements *******

footRect=found.FootingRectang(
    textComment='Rectangular footing',
    nUnits=1,
    LengthSide1=5,
    LengthSide2=2,
    Hfooting=0.75,
    ThickLeanConcr=0.10,
    excavHeight=1.15,
    excavSlope=1,
    fillingHeight=1.15-0.10-0.75,
    reinfQuant=1000,
    )
footRect.addExcavationQuant2chapter(chFound,prExcav)
footRect.addLeanConcreteQuant2chapter(chFound,prLeanConcr)
footRect.addFillingQuant2chapter(chFound,prFill)
footRect.addFormworkQuant2chapter(chFound,prHiddFormwork)
footRect.addReinfConcreteQuant2chapter(chFound,prConcr)
footRect.addReinforcementQuant2chapter(chFound,prReinfSteel,5)

footTriang=found.FootingTriang(
    textComment='Triangular footing',
    nUnits=1,
    BaseTriang=5,
    HeightTriang=2,
    Hfooting=0.75,
    ThickLeanConcr=0.10,
    excavHeight=1.15,
    excavSlope=1,
    fillingHeight=1.15-0.10-0.75,
    reinfQuant=1000,
    )
footTriang.addExcavationQuant2chapter(chFound,prExcav)
footTriang.addLeanConcreteQuant2chapter(chFound,prLeanConcr)
footTriang.addFillingQuant2chapter(chFound,prFill)
footTriang.addFormworkQuant2chapter(chFound,prHiddFormwork)
footTriang.addReinfConcreteQuant2chapter(chFound,prConcr)
footTriang.addReinforcementQuant2chapter(chFound,prReinfSteel,5)

footTrapez=found.FootingTrapez(
    textComment='Trapezoidal-base footing',
    nUnits=1,
    Base1Trapez=5,
    Base2Trapez=3,
    HeightTrapez=2,
    Hfooting=0.75,
    ThickLeanConcr=0.10,
    excavHeight=1.15,
    excavSlope=1,
    fillingHeight=1.15-0.10-0.75,
    reinfQuant=1000,
    )
footTrapez.addExcavationQuant2chapter(chFound,prExcav)
footTrapez.addLeanConcreteQuant2chapter(chFound,prLeanConcr)
footTrapez.addFillingQuant2chapter(chFound,prFill)
footTrapez.addFormworkQuant2chapter(chFound,prHiddFormwork)
footTrapez.addReinfConcreteQuant2chapter(chFound,prConcr)
footTrapez.addReinforcementQuant2chapter(chFound,prReinfSteel,5)

pile=found.pile(
    textComment='Pile',
    nPiles=7,
    DiamPile=0.45,
    Hpile=7,
    reinfQuant=50)

pile.addPileDrillingQuant2chapter(chFound,prPileDrill)
pile.addReinforcementQuant2chapter(chFound,prReinfSteel,5)
pile.addReinfConcreteQuant2chapter(chFound,prConcr)

# ************ Wall Measurements *******
retWall=wall.RetainingWall(
    textComment='Retaining wall',
    nUnits=1,
    Length=10,
    Height=9,
    Thickness=0.4,
    reinfQuant=100,
    SlopeTopFace=1/5,
    SlopeFrontFace=1/15,
    SlopeBackFace=1/12,
    FormworkLateral1=True,
    FormworkLateral2=True,
    JointLateral1=False,
    JointLateral2=True)

retWall.addHiddenWallFormworkQuant2chapter(chWalls,prHiddFormwork)
retWall.addExposedWallFormworkQuant2chapter(chWalls,prExposFormwork)
retWall.addReinforcementQuant2chapter(chWalls,prReinfSteel,5)
retWall.addReinfConcreteQuant2chapter(chWalls,prConcr)
retWall.addWaterproofingPrimerQuant2chapter(chWalls,prWaterproofPrimer)
retWall.addWaterproofingLayerQuant2chapter(chWalls,prWaterproofLayer)
retWall.addDrainageTubeQuant2chapter(chWalls,prDrainTub)
retWall.addJointsQuant2chapter(chWalls,prJoint)
retWall.drainageFillMaterial2chapter(chWalls,prDrainFill,wHeel=0.4,slopeFilling=2/1)

twoExpSideWall=wall.TwoExposedSideWall(
    textComment='Two exposed side wall',
    nUnits=1,
    Length=10,
    Height=9,
    Thickness=0.4,
    reinfQuant=100,
    SlopeTopFace=1/5,
    SlopeFrontFace=1/15,
    SlopeBackFace=1/12,
    FormworkLateral1=True,
    FormworkLateral2=False,
    )

twoExpSideWall.addExposedWallFormworkQuant2chapter(chWalls,prExposFormwork)
twoExpSideWall.addReinforcementQuant2chapter(chWalls,prReinfSteel,5)
twoExpSideWall.addReinfConcreteQuant2chapter(chWalls,prConcr)

# ************ Column Measurements *******

colCyl=col.ColumnCylind(
    textComment='Cylindrical column',
    nShafts=3,
    DiamColumn=0.95,
    Hcolumn=9.0,
    reinfQuant=500
    )

colCyl.addFormworkQuant2chapter(chColumns,prCurvFormwork)
colCyl.addReinforcementQuant2chapter(chColumns,prReinfSteel,5)
colCyl.addReinfConcreteQuant2chapter(chColumns,prConcr)


# ********* Deck measurements ***************

deckUnif=deck.DeckUnifCrossSect(
    textComment='Deck with uniform cross section',
    nUnits=1,
    LdeckUnifSect=23,
    AreaUnifSect=3.9,
    reinfQuant=550,
    LexposFormwork=10,
    LhiddFormwork= 8.0,
    nLateralFormwork=2,
    )
   
deckUnif.addExposedWallFormworkQuant2chapter(chDeck,prExposFormwork)
deckUnif.addHiddenWallFormworkQuant2chapter(chDeck,prHiddFormwork)
deckUnif.addReinforcementQuant2chapter(chDeck,prReinfSteel,5)
deckUnif.addReinfConcreteQuant2chapter(chDeck,prConcr)


# ********* Finishes measurements *****************

finish.addNeopreneBearingPadQuant2chapter(chFinishes,prNeoprene,textComment='Neoprene bearing pads',nUnits=3,length=0.3,width=0.5,height=0.09)

finish.addSidewalkQuant2chapter(chFinishes,prSidewalk,textComment='Sidewalk',nUnits=2,length=23,width=1.5,height=0.15)

finish.addGenericQuant2chapter(chFinishes,prCornice,textComment='Cornice',nUnits=2,length=23,width=None,height=None)

# Generate measurement text
import pylatex
doc=pylatex.Document(documentclass= 'book')
doc.packages.append(pylatex.Package('babel', options = ['spanish']))
doc.packages.append(pylatex.Package('minitoc'))
doc.preamble.append(pylatex.Command('selectlanguage', 'spanish'))
doc.packages.append(pylatex.Package('graphicx'))
doc.packages.append(pylatex.Package('numprint'))
doc.preamble.append(pylatex.Command('npthousandsep', '.'))
doc.preamble.append(pylatex.Command('npdecimalsign', ','))
# doc.append(pylatex.Command('doparttoc'))
budget.writeQuantitiesIntoLatexDocument(doc)
doc.generate_tex('measur_structural_members')

# Generate budget text
doc=pylatex.Document(documentclass= 'book')
doc.packages.append(pylatex.Package('babel', options = ['spanish']))
doc.packages.append(pylatex.Package('minitoc'))
doc.preamble.append(pylatex.Command('selectlanguage', 'spanish'))
doc.packages.append(pylatex.Package('graphicx'))
doc.packages.append(pylatex.Package('numprint'))
doc.preamble.append(pylatex.Command('npthousandsep', '.'))
doc.preamble.append(pylatex.Command('npdecimalsign', ','))
budget.writeIntoLatexDocument(doc)
doc.generate_tex('budget_structural_members')
