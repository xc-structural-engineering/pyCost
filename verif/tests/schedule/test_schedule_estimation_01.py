# -*- coding: utf-8 -*-
'''Extract concepts from unit cost databases.''' 
from __future__ import division
from __future__ import print_function

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import os
import sys
import datetime
import filecmp
import logging
from pycost.structure import obra
from pycost.measurements import measurement_report
from pycost.utils import basic_types
from pycost.utils import schedule_utils

# Create main object.
site= obra.Obra(cod="test", tit="Test title")

# Read data from file.
pth= os.path.dirname(__file__)
# print("pth= ", pth)
if(not pth):
    pth= '.'
pendingLinks= site.readFromJson(pth+'/../data/json/test_file_05.json')

# # Get the labour prices measured in hours.
# labour_quantities= site.getElementaryQuantities(target_unit= 'h', target_type= 'mdo')

# print(labour_quantities)

paths= site.getPaths()

projectTasks= schedule_utils.ProjectTasks(code= 'test', description= 'Test')

# Populate the project tasks.
for i, row in enumerate(paths):
    leaf_chapter= row[-1]
    has_quantities= len(leaf_chapter.quantities)>0
    if(has_quantities): # chater has quantities.
        task_code= leaf_chapter.Codigo().strip('#')
        task_description= leaf_chapter.title
        task_chapters= [leaf_chapter]
        task= schedule_utils.Task(code= task_code, description= task_description, chapters= task_chapters)
        projectTasks.addTask(task)

# Set predecessors.
# List of rows of the form:
#  [ [ task1, [predecessor11, predecessor12, ..., predecessor1i]],
#    [ task2, [predecessor21, predecessor22, ..., predecessor2j]],
#    ...
#    [ taskM, [predecessorM1, predecessorM2, ..., predecessorMn]],
#  ]
task_predecessors= [ ['CAP1.1', ['CAP1.6.1']],
                     ['CAP1.3', ['CAP1.1']],
                     ['CAP1.2', ['CAP1.1']],
                     ['CAP1.5', ['CAP1.1']],

                     ['CAP.1.7.1', ['CAP1.3']],

                     ['CAP1.8', ['CAP1.2', 'CAP1.5', 'CAP.1.7.1']],

                     ['CAP1.10', ['CAP1.8']],
                     ['CAP1.4', ['CAP1.8']],
                     ['CAP1.9', ['CAP1.8']]]
projectTasks.setPredecessors(task_predecessors)

# Set start date.
projectStartDate= datetime.datetime(year=2026, month=1, day=1)
projectTasks.setStartDate(startDate= projectStartDate)

# Set number of teams when it is greater than one.
projectTasks.setNumberOfTeams('CAP1.1', numberOfTeams= 2.0)
projectTasks.setNumberOfTeams('CAP1.3', numberOfTeams= 2.0)
projectTasks.setNumberOfTeams('CAP1.5', numberOfTeams= 2.0)
projectTasks.setNumberOfTeams('CAP1.8', numberOfTeams= 5.0)
projectTasks.setNumberOfTeams('CAP1.9', numberOfTeams= 10.0) # Most of the work
                                                             # is done at the
                                                             # workshop.

# Compute working hours.
projectTasks.computeWorkingHours()

# Set durations for each task.
fixed_durations= {'CAP1.10':10*8}
def estimate_duration(task):
    task_code= task.getCode()
    if(task_code in fixed_durations):
        retval= fixed_durations[task_code]
    else:
        computedWorkingHours= task.computedWorkingHours
        numberOfComponents= len(computedWorkingHours)
        if(numberOfComponents==0):
            retval= 0
        elif(numberOfComponents<=2):
            retval= computedWorkingHours[0][1] # Maximum value.
        else:
            retval= 0
            for component in computedWorkingHours:
                # elementaryPrice= component[0]
                retval+= component[1]
            retval/=2.0
        retval/= task.getNumberOfTeams()
    return retval

for task in projectTasks.task_dict.values():
    # print('\ntask: ', task.getCode(), task.getDescription())
    # computedWorkingHours= task.computedWorkingHours
    # for component in computedWorkingHours:
    #     elementaryPrice= component[0]
    #     computedHours= component[1]
    #     print('  ', elementaryPrice.title, computedHours, 'h')
    estimatedDuration= estimate_duration(task)
    estimatedDurationWeeks= estimatedDuration/40.0 # forty-hour workweek.
    task.setDuration(weeks= estimatedDurationWeeks)
    # print('   estimated duration: ', estimatedDurationWeeks, ' weeks')
    
# Compute average number of workers.
projectTasks.computeAverageNumberOfWorkers()

# Print start dates.
fname= os.path.basename(__file__)
sorted_tasks= projectTasks.getSortedTasksByStartDate()
txtFileName= fname.replace('.py', '.txt')
textOutputFileName= '/tmp/'+txtFileName
with open(textOutputFileName, 'w') as f:    
    for task in sorted_tasks:
        f.write('\ntask: '+str(task.getCode())+' '+str(task.getDescription())+'\n')
        f.write('   start date: '+str(task.getStartDate())+'\n')
        f.write('   end date: '+str(task.getEndDate())+'\n')
refFile= refFile= pth+'/../data/reference_files/ref_'+txtFileName
testOK= filecmp.cmp(refFile, textOutputFileName, shallow=False)

# projectTasks.drawMatplotlibGanttChart(title= 'Schedule of Project:'+site.title)

# Plot Gantt chart.
chartOutputFileName= '/tmp/'+fname.replace('.py', '.png')
projectTasks.drawMatplotlibGanttChart(title= 'Schedule of Project:'+site.title, outputFileName= chartOutputFileName)

# Check that file exists
testOK= testOK and os.path.isfile(chartOutputFileName)

if testOK:
    print('test '+fname+': ok.')
else:
    logging.error(fname+' ERROR.')

os.remove(textOutputFileName) # Clean after yourself.
os.remove(chartOutputFileName)


        
    
