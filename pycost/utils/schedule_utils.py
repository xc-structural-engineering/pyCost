# -*- coding: utf-8 -*-
'''Project schedule utilities.''' 

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import sys
import logging
import datetime
import pandas
import numpy as np
from operator import itemgetter
import matplotlib
import matplotlib.pyplot as plt

class Task(object):
    ''' Representation of a project task.

    :ivar code: task code.
    :ivar description: task description.
    :ivar chapters: list of chapters that compose the task.
    :ivar start_dates: start date of each phase (if any).
    :ivar durations: duration of each phase (if any).
    :ivar predecessors: tasks that must precede this one.
    :ivar computedWorkingHours: hours of work needed to fullfill the task 
                                computed from the chapter measurement data.
    '''
    def __init__(self, code, description, chapters, start_date= None, duration= None, predecessors= None, numberOfTeams= 1, completion_frac= 0.0, color= 'b'):
        ''' Constructor.

        :param code: code of the task.
        :param description: description of the task.
        :param chapters: list of chapters that compose the task.
        :param start_date: task start date.
        :param duration: task duration.
        :param predecessors: tasks that must precede this one.
        :param numberOfTeams: number of teams working simultaneously.
        :param completion_frac: 0 -> task not initiated,
                                0.5 -> task half finished.
                                1 -> task finished.
        :param color: color of the task bar in the Gantt chart
                      (in Matplotlib format).
        '''
        self.code= code
        self.description= description
        self.chapters= chapters
        self.start_dates= [start_date]
        self.durations= [duration]
        if(predecessors):
            self.predecessors= predecessors
        else:
            self.predecessors= list()
        self.numberOfTeams= numberOfTeams
        self.computedWorkingHours= None
        self.completion_frac= completion_frac
        self.color= color

    def getCode(self):
        ''' Return the task code.'''
        return self.code

    def getDescription(self):
        ''' Return the task code.'''
        return self.description

    def getNumberOfTeams(self):
        ''' Return the number of teams working simultaneously in this task.'''
        return self.numberOfTeams

    def getCompletionFrac(self):
        ''' Return the fraction of the task that is completed.'''
        return self.completion_frac

    def setNumberOfTeams(self, numberOfTeams):
        ''' Set the number of teams working simultaneously in this task.

        :param numberOfTeams: number of teams working simultaneously.
        '''
        self.numberOfTeams= numberOfTeams

    def hasPredecessors(self):
        ''' Return true if the task has predecessors.'''
        retval= False
        if(self.predecessors):
            retval= True
        return retval

    def hasNoPredecessors(self):
        ''' Return true if the task has no predecessors.'''
        return not self.hasPredecessors()

    def getPredecessorsEndDate(self):
        ''' Return the last end date of the task predecessors.'''
        retval= None
        if(self.predecessors):
            retval= self.predecessors[0].getEndDate()
            for predecessor in self.predecessors[1:]:
                tmp= predecessor.getEndDate()
                if(tmp):
                    if(tmp>retval):
                        retval= tmp
        return retval

    def setStartDate(self, startDate, i_th= 0):
        ''' Set the start date of the i_th phase of the task.'''
        if(self.predecessors):
            className= type(self).__name__
            methodName= sys._getframe(0).f_code.co_name
            errMsg= '; the task has predecessors; start date ignored.'
        else:
            self.start_dates[i_th]= startDate

    def getStartDate(self, i_th= 0):
        ''' Return the start date of the i_th phase of the task.

        :param i_th: index of the task phase.
        '''
        retval= self.start_dates[i_th]
        if(retval is None):
            retval= self.getPredecessorsEndDate()
        return retval

    def getDuration(self, i_th= 0):
        ''' Return the duration of the i-th phase of the task.

        :param i_th: index of the task phase.
        '''
        return self.durations[i_th]

    def setDuration(self, weeks, i_th= 0):
        ''' Set the duration of i-th phase of the the task in weeks.

        :param weeks: duration of the task in weeks.
        '''
        self.durations[i_th]= datetime.timedelta(days=7*weeks)

    def getEndDate(self, i_th= 0):
        ''' Return the end date of the i_th phase of the task.

        :param i_th: index of the task phase.
        '''
        retval= None
        startDate= self.getStartDate(i_th)
        if(startDate):
            duration= self.getDuration(i_th)
            if(not duration):
                className= type(self).__name__
                methodName= sys._getframe(0).f_code.co_name
                warningMsg= '; the task: '
                warningMsg+= str(self.code)
                warningMsg+= ' has no duration.'
                logging.warning(className+'.'+methodName+warningMsg)
                duration= datetime.timedelta(days=0)
            retval= startDate+duration
        return retval

    def extendPredecessors(self, predecessors):
        ''' Set the predecessors of this task.

        :param predecessors: list of tasks that precede this one.
        '''
        for t in predecessors:
            if(t!=self): # A task cannot precede itself.
                self.predecessors.append(t)
            else:
                className= type(self).__name__
                methodName= sys._getframe(0).f_code.co_name
                errMsg= '; a task cannot precede itself. Predecessor: '
                errMsg+= str(t.code)
                errMsg+= ' ignored.'
                logging.error(className+'.'+methodName+errMsg)

    def computeWorkingHours(self):
        ''' Compute the hours of work needed to fullfill the task and stores
            them in the working_hours member.
        '''
        if(len(self.chapters)>1):
            className= type(self).__name__
            methodName= sys._getframe(0).f_code.co_name
            errMsg= '; not implemented for more than one chapter yet.'
            logging.error(className+'.'+methodName+errMsg)
            exit(1)
        else:
            self.computedWorkingHours= self.chapters[0].getElementaryQuantities(target_unit= 'h', target_type= 'mdo')

class ProjectTasks(object):
    ''' Tasks of a project.

    :ivar code: project code.
    :ivar description: project description.
    :ivar task_dict: task dictionary.
    '''
    def __init__(self, code, description):
        ''' Constructor.

        :param code: project code.
        :param description: project description.
        '''
        self.code= code
        self.description= description
        self.task_dict= dict()

    def addTask(self, task):
        ''' Add the given task to the project.

        :param task: task to add to this project.
        '''
        self.task_dict[task.code]= task

    def setPredecessors(self, task_predecessors):
        ''' Set the task predecessors.

        :param task_predecessors: list of rows containing the task code and a
                                  list of codes representing its predecesors:
                                  [[task1, [pred11, pred12, ..., pred1N]],
                                   [task2, [pred21, pred22, ..., pred2N]],
                                   ...
                                   [taskN, [predN1, predN2, ..., predNN]]]
        ''' 
        for row in task_predecessors:
            task_code= row[0]
            task= self.task_dict[task_code]
            task_predecessors_codes= row[1]
            task_predecessors= list()
            for predecessor_code in task_predecessors_codes:
                predecessor= self.task_dict[predecessor_code]
                task_predecessors.append(predecessor)
            task.extendPredecessors(task_predecessors)
            
    def setStartDate(self, startDate):
        ''' Set the start date of the project.
 
        :param startDate: start date.
        '''
        for task in self.task_dict.values():
            if task.hasNoPredecessors():
                task.setStartDate(startDate)
        
    def setNumberOfTeams(self, taskCode, numberOfTeams):
        ''' Set the number of teams for the given task.

        :param taskCode: code of the task.
        :param numberOfTeams:
        '''
        task= self.task_dict[taskCode]
        task.setNumberOfTeams(numberOfTeams)
        
    def computeWorkingHours(self):
        ''' Compute the hours of work needed to fullfill each of the project
            tasks.
        '''
        for key in self.task_dict:
            task= self.task_dict[key]
            task.computeWorkingHours()

    def getSortedTasksByStartDate(self):
        ''' Compute the hours of work needed to fullfill each of the project
            tasks.
        '''
        task_list= list()
        for task in self.task_dict.values():
            task_list.append((task, task.getStartDate()))
        task_list.sort(key=itemgetter(1))
        return [x[0] for x in task_list]
        
    def getPandasDataFrame(self):
        ''' Return the Pandas dataframe corresponding to the project tasks.'''
        task_labels= list()
        teams= list()
        start= list()
        end= list()
        completion_frac= list() # status of completion
        sorted_task_list= self.getSortedTasksByStartDate()
        for task in sorted_task_list:
            task_labels.append(task.description)
            teams.append('team') # Needed?
            start.append(task.getStartDate())
            end.append(task.getEndDate())
            completion_frac.append(task.getCompletionFrac())
        # Build data frame.
        df = pandas.DataFrame({'task': task_labels,
                               'team': teams,
                               'start': start,
                               'end': end,
                               'completion_frac': completion_frac})

        # Compute how many days passed/would pass from the overall project
        # start to the ttart date of each task:
        df['days_to_start'] = (df['start'] - df['start'].min()).dt.days
        # Compute how many days passed/would pass from the overall project
        # start to the end date of each task:
        df['days_to_end'] = (df['end'] - df['start'].min()).dt.days
        # Store the duration of each task, including both the start and
        # end dates:
        df['task_duration'] = df['days_to_end'] - df['days_to_start'] + 1  # to include also the end date
        # Convert the status of completion of each task translated from a
        # fraction into a portion of days allocated to that task:
        df['completion_days'] = df['completion_frac'] * df['task_duration']
        return df

    def getTaskColors(self):
        ''' Return a list with the colors for each task.'''
        retval= dict()
        for task in self.task_dict.values():
            retval[task.getDescription()]= task.color
        return retval

    def drawMatplotlibGanttChart(self, title, outputFileName= None):
        ''' Draws a Matplotlib Gantt chart.
        
        :param outputFile: output file (if None display the chart in a window.
        '''
        # Create Pandas data fram.
        df= self.getPandasDataFrame()

        # Set colors.
        task_colors= self.getTaskColors()
        patches = []
        for task in task_colors:
            patches.append(matplotlib.patches.Patch(color=task_colors[task]))

        # Create subplots.
        fig, ax = plt.subplots()
        # Create xticks.
        xticks = np.arange(5, df['days_to_end'].max() + 2, 7)
        for index, row in df.iterrows():
            # plt.barh(y=row['task'], width=row['task_duration'], left=row['days_to_start'] + 1, color=task_colors[row['task']])

            # Adding a lower bar - for the overall task duration
            plt.barh(y=row['task'], width=row['task_duration'], left=row['days_to_start'] + 1, color=task_colors[row['task']], alpha=0.4)

            # Adding an upper bar - for the status of completion
            plt.barh(y=row['task'], width=row['completion_days'], left=row['days_to_start'] + 1, color=task_colors[row['task']])
        # Create xticklabels.
        xticklabels = pandas.date_range(start=df['start'].min() + datetime.timedelta(days=4), end=df['end'].max()).strftime("%d/%m")
        plt.title(title, fontsize=15)
        plt.gca().invert_yaxis()
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels[::7])
        ax.xaxis.grid(True, alpha=0.5)

        # Adding a legend
        # ax.legend(handles=patches, labels=task_colors.keys(), fontsize=11)

        # # Marking the current date on the chart
        # ax.axvline(x=29, color='r', linestyle='dashed')
        # ax.text(x=29.5, y=11.5, s='17/11', color='r')

        if(outputFileName):
            plt.savefig(outputFileName, dpi=200)
        else:
            plt.show()



