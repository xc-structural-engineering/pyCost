# -*- coding: utf-8 -*-
'''Project schedule utilities.''' 

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2025, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import math
import sys
import logging
import datetime
import pandas
import numpy as np
from operator import itemgetter
import matplotlib
import matplotlib.pyplot as plt
from scipy import interpolate

default_date_format= "%A, %d %B de %Y"

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
        self.averageNumberOfWorkers= None
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
            them in the working hours member.
        '''
        if(len(self.chapters)>1):
            className= type(self).__name__
            methodName= sys._getframe(0).f_code.co_name
            errMsg= '; not implemented for more than one chapter yet.'
            logging.error(className+'.'+methodName+errMsg)
            exit(1)
        else:
            self.computedWorkingHours= self.chapters[0].getElementaryQuantities(target_unit= 'h', target_type= 'mdo')

    def getTotalWorkingHours(self):
        ''' Return the total hours of work needed to fullfill the task.
        '''
        if(not self.computedWorkingHours):
            self.computeWorkingHours()
        retval= 0.0
        for wh in self.computedWorkingHours:
            retval+= wh[1]
        return retval

    def getTotalCost(self):
        ''' Return the total cost of this task.'''
        retval= 0.0
        for chapter in self.chapters:
            retval+= chapter.getPrice()
        return retval

    def getCompletionFractionAtDate(self, date):
        ''' Return the fraction of the task that is completed at the given
            date (assuming it unfolds as planned).

        :param date: final date to compute the cost of the task.
        '''
        retval= 0.0
        endDate= self.getEndDate()
        if(date>self.getEndDate()): # task has finished.
            retval= 1.0
        else: # task is still running.
            startDate= self.getStartDate()
            if(startDate<date): # if the task has begun.
                totalTaskInterval= endDate-startDate
                currentTaskInterval= date-startDate
                retval= currentTaskInterval.days/totalTaskInterval.days
        return retval 

    def getCostUntilDate(self, date):
        ''' Return the cost of this task from its beginning until the given 
            date.

        :param date: final date to compute the cost of the task.
        '''
        retval= 0.0
        completionAtDate= self.getCompletionFractionAtDate(date)
        if(completionAtDate>0.0):
            retval= self.getTotalCost()*completionAtDate
        return retval

    def getAverageNumberOfWorkers(self, date= None, hoursOfWorkPerYear= 1760, hoursOfWorkPerDay= 8):
        ''' Return the average number of workers during the execution of the 
            works in this chapter.

        :param date: date at which the number of workers is queried.
        :param hoursOfWorkPerYear: hour of work per worker and per year.
        :param hoursOfWorkPerDay: hour of work per worker and per day.
        '''
        retval= 0
        if(len(self.chapters)>1):
            className= type(self).__name__
            methodName= sys._getframe(0).f_code.co_name
            errMsg= '; not implemented for more than one chapter yet.'
            logging.error(className+'.'+methodName+errMsg)
            exit(1)
        else:
            if(date):
                startDate= self.getStartDate()
                endDate= self.getEndDate()
                if((date>=startDate) and (date<=endDate)):
                    totalWorkingHours= self.getTotalWorkingHours()
                    durationInHours= self.durations[0].days*hoursOfWorkPerDay
                    retval= int(math.ceil(totalWorkingHours/durationInHours))
            else:
                totalWorkingHours= self.getTotalWorkingHours()
                durationInHours= self.durations[0].days*hoursOfWorkPerDay
                retval= int(math.ceil(totalWorkingHours/durationInHours))
        return retval

    def computeAverageNumberOfWorkers(self, hoursOfWorkPerYear= 1760, hoursOfWorkPerDay= 8):
        ''' Compute the average number of workers during the execution of the 
            works in this chapter.

        :param date: date at which the number of workers is queried.
        :param hoursOfWorkPerYear: hour of work per worker and per year.
        :param hoursOfWorkPerDay: hour of work per worker and per day.
        '''
        self.averageNumberOfWorkers= self.getAverageNumberOfWorkers(date= None, hoursOfWorkPerYear= hoursOfWorkPerYear, hoursOfWorkPerDay= hoursOfWorkPerDay)
        
        
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

    def getStartDate(self):
        ''' Return the start date of the project.
         '''
        tasks= list(self.task_dict.values())
        startDate= tasks[0].getStartDate()
        for task in tasks[1:]:
            taskStartDate= task.getStartDate()
            if(taskStartDate<startDate):
                startDate= taskStartDate
        return startDate
    
    def getTimeInterval(self):
        ''' Return the start and end dates of the project in a tuple:
            (startDate, endDate).
         '''
        tasks= list(self.task_dict.values())
        startDate= tasks[0].getStartDate()
        endDate= tasks[0].getEndDate()
        for task in tasks[1:]:
            taskStartDate= task.getStartDate()
            taskEndDate= task.getEndDate()
            if(taskStartDate<startDate):
                startDate= taskStartDate
            if(taskEndDate>endDate):
                endDate= taskEndDate
        return (startDate, endDate)

    def getDuration(self):
        ''' Return the project duration.'''
        (startDate, endDate)= self.getTimeInterval()
        return endDate-startDate
            
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

    def computeAverageNumberOfWorkers(self, hoursOfWorkPerYear= 1760, hoursOfWorkPerDay= 8):
        ''' Compute the average number of workers for each task.

        :param hoursOfWorkPerYear: hour of work per worker and per year.
        :param hoursOfWorkPerDay: hour of work per worker and per day.
        '''
        for key in self.task_dict:
            task= self.task_dict[key]
            task.computeAverageNumberOfWorkers(hoursOfWorkPerYear= hoursOfWorkPerYear, hoursOfWorkPerDay= hoursOfWorkPerDay)

    def getSortedTasksByStartDate(self):
        ''' Return a list of task sorted by its start date.'''
        task_list= list()
        for task in self.task_dict.values():
            task_list.append((task, task.getStartDate()))
        task_list.sort(key=itemgetter(1))
        return [x[0] for x in task_list]

    def getSortedTasksByEndDate(self):
        ''' Return a list of task sorted by its end date.'''
        task_list= list()
        for task in self.task_dict.values():
            task_list.append((task, task.getEndDate()))
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
        for task in self.getSortedTasksByStartDate():
            retval[task.getDescription()]= task.color
        return retval

    def drawMatplotlibGanttChart(self, title, outputFileName= None, timeIncrement= 30):
        ''' Draws a Matplotlib Gantt chart.
       
        :param title: title of the chart. 
        :param outputFileName: name of the output file (if None display the 
                               chart in a window).
        :param timeIncrement: time increment between two samples (in days).
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
        xticks = np.arange(5, df['days_to_end'].max() + 2, timeIncrement)
        for index, row in df.iterrows():
            # plt.barh(y=row['task'], width=row['task_duration'], left=row['days_to_start'] + 1, color=task_colors[row['task']])

            # Adding a lower bar - for the overall task duration
            plt.barh(y=row['task'], width=row['task_duration'], left=row['days_to_start'] + 1, color=task_colors[row['task']], alpha=0.4, height= .4)

            # Adding an upper bar - for the status of completion
            plt.barh(y=row['task'], width=row['completion_days'], left=row['days_to_start'] + 1, color=task_colors[row['task']], height= .4)
        # Create xticklabels.
        xticklabels = pandas.date_range(start=df['start'].min() + datetime.timedelta(days=4), end=df['end'].max()).strftime("%d/%m")
        # Plot number of workers
        sorted_tasks= self.getSortedTasksByStartDate()
        task_patches= ax.patches[0::2] # Only the patches corresponding to tasks
                                       # not to task completions.
        for bar, task in zip(task_patches, sorted_tasks):
            ax.text(bar.get_x()+bar.get_width()/2.0, bar.get_y()+bar.get_height()/2, task.averageNumberOfWorkers, color = 'white', ha = 'center', va = 'center')
        plt.title(title, fontsize=12)
        plt.gca().invert_yaxis()
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels[::timeIncrement])
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

    def getCumulatedExpenses(self):
        ''' Return the values of the cumulated expenses versus the 
            number of days elapsed from the start of the project.'''
        sorted_task_list= self.getSortedTasksByEndDate()
        projectStartDate= self.getStartDate()
        days= [0]
        costs= [0.0]
        totalCost= 0.0
        for task in sorted_task_list:
            totalCost+= task.getTotalCost()
            costs.append(totalCost)
            taskEndDate= task.getEndDate()
            daysFromProjectStart= (taskEndDate-projectStartDate).days
            days.append(daysFromProjectStart)
        return days, costs
    
    def getExpensesIncrements(self, sampleTimes):
        ''' Return the values of the expenses between two consecutive ends of 
            taks.
 
        :param sampleTimes: time values expressed in days elapsed from the 
                            start of the project.
        '''
        cumulatedExpensesFunction= self.getCumulatedExpensesFunction()
        cost_values= list(cumulatedExpensesFunction(sampleTimes))
        inc_costs= [0]
        cost0= 0.0
        for cost1 in cost_values[1:]:
            inc_costs.append(cost1-cost0)
            cost0= cost1
        return sampleTimes, inc_costs
            
    def getCumulatedExpensesFunction(self):
        ''' Return a function that gives the cumulated expenses versus the 
            number of days elapsed from the start of the project.'''
        days, costs= self.getCumulatedExpenses()
        return interpolate.interp1d(days, costs)

    def getExpensesIncrementsFunction(self, sampleTimes):
        ''' Return a function that gives the cumulated expenses versus the 
            number of days elapsed from the start of the project.
 
        :param sampleTimes: time values expressed in days elapsed from the 
                            start of the project.
        '''
        days, inc_costs= self.getExpensesIncrements(sampleTimes= sampleTimes)
        return interpolate.interp1d(days, inc_costs)

    def getSampleTimes(self, timeIncrement):
        ''' Return the time values to sample the cumulate expenses function
            expressed in days elapsed from the start of the project.

        :param timeIncrement: time increment between two samples (in days).
        '''
        projectDurationDays= self.getDuration().days
        retval= list()
        time= 0
        while(time<projectDurationDays):
            retval.append(time)
            time+= timeIncrement
        if(retval[-1]<projectDurationDays):
            retval.append(projectDurationDays)
        return retval

    def getSampleDates(self, sampleTimes):
        '''Return the dates corresponding to the given times.
 
        :param sampleTimes: time values expressed in days elapsed from the 
                            start of the project.
        '''
        projectStartDate= self.getStartDate()
        retval= list()
        for daysElapsed in sampleTimes:
            date= projectStartDate+datetime.timedelta(days= daysElapsed)
            retval.append(date)
        return retval

    def drawMatplotLibExpensesDiagram(self, title, outputFileName= None, timeIncrement= 30, currencyFactor= 1e-3):
        ''' Draws a Matplotlib diagram showing the expenses of the project
            versus time.

        :param title: title of the chart. 
        :param outputFileName: name of the output file (if None display the 
                               chart in a window).
        :param timeIncrement: time increment between two samples (in days).
        :param currencyFactor: 1e-3 to express thousands of currency units.
        '''
        sample_times= self.getSampleTimes(timeIncrement= timeIncrement)
        cumulatedExpensesFunction= self.getCumulatedExpensesFunction()
        cost= cumulatedExpensesFunction(sample_times)/1e3
        cost_inc_function= self.getExpensesIncrementsFunction(sample_times)
        cost_inc= cost_inc_function(sample_times)/1e3
        xTickDates= self.getSampleDates(sample_times)
        xTickLabels= list()
        for xtd in xTickDates:
            xTickLabels.append(xtd.strftime("%d/%m"))

        fig, ax = plt.subplots()
        ax.set_xticks(sample_times)
        ax.set_xticklabels(xTickLabels)
        ax.plot(sample_times, cost_inc, label= 'expenses.')
        ax.plot(sample_times, cost, label= 'cumulated expenses')
        plt.legend()
        ax.grid()
        plt.title(title, fontsize=15)
        if(outputFileName):
            plt.savefig(outputFileName, dpi=200)
        else:
            plt.show()

    def getAvgNumberOfWorkersAlongProject(self):
        ''' Return the number of workers along the project.

        '''        
        # Compute time intervals.
        days_from_start= list()
        projectStartDate= self.getStartDate()
        for task in self.task_dict.values():
            days_from_start.append((task.getStartDate()-projectStartDate).days)
            days_from_start.append((task.getEndDate()-projectStartDate).days)
        days_from_start= sorted(set(days_from_start))
        ## Convert to dates.
        dates= list()
        for d in days_from_start:
            dates.append(projectStartDate+datetime.timedelta(days= d))
        # Compute average number of workers.
        days= list()
        workers= list()
        day0= days_from_start[0]
        for day1 in days_from_start[1:]:
            date0= projectStartDate+datetime.timedelta(days= day0)
            delta= datetime.timedelta(days= (day1-day0))
            calculationDate= date0+0.5*delta
            avgNumberOfWorkers= 0
            for task in self.task_dict.values():
                avgNumberOfWorkers+= task.getAverageNumberOfWorkers(date= calculationDate)
            days.append(day0)
            workers.append(avgNumberOfWorkers)
            day0= day1
        days.append(day1)
        workers.append(avgNumberOfWorkers)

        xTickLabels= list()
        previousDate= None
        for date in dates:
            stringToAppend= date.strftime("%d/%m")
            if(previousDate):
                delta= (date-previousDate).days
                if(delta<2):
                    stringToAppend= ''
            xTickLabels.append(stringToAppend)
            previousDate= date

        return days, workers, xTickLabels

    def drawAvgNumberOfWorkersAlongProjectDiagram(self, title, outputFileName= None, xlabel= 't', ylabel= 'workers'):
        ''' Draws a diagram of the the average number of workers along the 
            project.

        :param title: title of the chart. 
        :param outputFileName: name of the output file (if None display the 
                               chart in a window).
        '''
        days, workers, xTickLabels= self.getAvgNumberOfWorkersAlongProject()

        fig, ax = plt.subplots()
        ax.step(days, workers, where= 'post')
        ax.set_xticks(days)
        ax.set_yticks(workers)
        ax.set_xticklabels(xTickLabels, rotation='vertical')
        ax.grid()
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        if(outputFileName):
            plt.savefig(outputFileName, dpi=200)
        else:
            plt.show()
