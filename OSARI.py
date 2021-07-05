"""
Open-Source Anticipated Response Inhibition (OSARI)
Created in PsychoPy v3.1.2
Authors: Rebecca J Hirst [1] Rohan Puri [2] Jason L He [3]
[1] Trinity College Institute of Neuroscience, Trinity College Dublin
[2] University of Tasmania
[3] King's College London
Mail to Authors:  opensourceTAP@gmail.com

Input:
    5 xlsx files:
        practiceGoTrials.xlsx
        testGoBlocks.xlsx
        practiceMixedTrials.xlsx
        testBlocks.xlsx
        instructions.xlsx

    See header comments for details on each parameter.

Output:

    4 output files in format:
        data/ID_OSARI_yyyy_mo_d_hhmm.log
        data/ID_OSARI_yyyy_mo_d_hhmm.csv
        data/ID_OSARI_yyyy_mo_d_hhmm.psydat
        data_txt/ID_OSARI_yyyy_mo_d_hhmm.txt

    ID = Participant ID ; yyyy = Year; mo = month
    d = day; h = hour; m = minute
    Data stored in "data_txt" is compatible with BASTD analysis script (https://github.com/HeJasonL/BASTD)
    Block: current repetition of this block type
    TrialType: block label (practice/real all go/mixed)
    Trial: trial number
    Signal: 0 = Go
                1 = Stop
    Response: 0 = no lift, 1 = lift
    SSD: Stop Signal Distance (relative to start time) if the trial was a stop trial.
    RT: key lift time of participants relative to start time

    Note:
        Make sure the resolution of "testMonitor" in monitor centre matches actual screen resolution
        Please limit the number of background programmes running
        We recommend running the demo view>input>timeByFrames.py to assess reliability of frame duration
"""


#======================================
# Import Modules and set defaults
#======================================
from __future__ import absolute_import, division
import os
from os import path
import numpy as np
from psychopy import gui, visual, core, data, event, logging
from psychopy.hardware import keyboard
from psychopy.tools.filetools import fromFile, toFile
import pickle
from OSARI_functions import *

# fetch keyboard using Keyboard class (better timing)
kb = keyboard.Keyboard(bufferSize=10, waitForStart=True)

# set the directory to be the current directory to save files
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Set the experiment name (expName)
expName = 'OSARI'

#======================================
# Setup the Dialog Boxes
#======================================
    #OSARI presents users with three Dialog Box:
        # 1. The Participant Information Dialog Box
        # 2. The Trial Structure Dialog Box
        # 3. The Additional Parameters Dialog Box

#---------------------------------------------------
# The participant information GUI (expInfo)
#---------------------------------------------------
demographic_file = data.importConditions('demographics.xlsx')
expInfo = {}
expInfo['Participant ID'] = '0000'

tips = {}

for field in demographic_file:
    if type(field['Default']) == str:
        if ',' in field['Default']:
            # check if the value provided is a list and if so convert string to list
            expInfo[field['Name']] = field['Default'].split(',')
    else:
        expInfo[field['Name']] = field['Default']
    tips[field['Name']] = field['Tip']

expInfo['Default Parameters?'] = True
tips['Default parameters?'] = 'This will run the task with no additional options'

# Dictionary for the participant information GUI (expInfo)
dlg = gui.DlgFromDict(
    dictionary=expInfo,
    sortKeys = False, title= 'Participant Information',
    tip=tips,
    order= expInfo.keys())

if not dlg.OK: core.quit()
expInfo['date'] = data.getDateStr()

#---------------------------------------------------
# The Trial Structure GUI (more_task_info[0])
#---------------------------------------------------
try:  # try to find pickle files if they exist
    more_task_info1 = open("more_task_info1.pickle", "rb")
    more_task_info1 = pickle.load(more_task_info1)
    more_task_info2 = open("more_task_info2.pickle", "rb")
    more_task_info2 = pickle.load(more_task_info2)
    more_task_info = [more_task_info1, more_task_info2]
except:
    more_task_info = [{'Practice Trials': True,
                        'Test Go Block': True,
                        'Method': ['staircase', 'fixed'],
                        'Trial Order': ['random', 'sequential']},
                      {'Count Down': False,
                        'Trial-by-trial Feedback': True,
                        'Step size (s)': 0.025,
                        'Lowest SSD (s)': 0.05,
                        'Highest SSD (s)': 0.775,
                        'Total Bar Height (in cm)': 15,
                        'Number of Test Mixed Blocks': 3,
                        'Full Screen': True,
                        'Color Blind Palette?': False,
                        'Response Key': ['space', 'left', 'right', 'up', 'down'],
                       'Remember Parameters': False
                       }]

# If user selected 'no' to Default Parameters, present Additional Parameter options.
if not expInfo['Default Parameters?']:
    dlg = gui.DlgFromDict(
    dictionary=more_task_info[0], 
    sortKeys = False,
    title='Trial Structure',
                          tip={
                              'Test Go Block': 'Do you want to present a full block of go trials in advance of the '
                                              'mixed go/stop blocks?',
                              'Method': 'What SSD method do you want?',
                              'Trial Order': 'Do you want trials to be in a random order or in the order you have set '
                                             'in the conditions .xlsx file [sequential]'
                                             })
    if not dlg.OK: core.quit()
else:
    # parameters with multiple options need their default selecting
    more_task_info[0]['Trial Order'] = 'random'
    more_task_info[0]['Method'] = 'staircase'

#---------------------------------------------------
# The Additional Parameters GUI (more_task_info[1])
#---------------------------------------------------
if not expInfo['Default Parameters?']:
    dlg = gui.DlgFromDict(
    dictionary=more_task_info[1], 
    sortKeys = False,
    title='Additional parameters',
                          tip={
                              'Count Down': 'Do you want a countdown before the bar starts filling?',
                              'Trial-by-trial Feedback': 'Do you want participants to receive trial to trial feedback',
                              'Step size (s)': 'What do you want the step size to be in ms - e.g., 0.025 is 25ms',
                              'Lowest SSD (s)': 'The lowest the SSD can go in ms - e.g., 0.05 is 50ms',
                              'Highest SSD (s)': 'The highest the SSD can go in ms - e.g., 0.775 is 775ms',
                              'Total Bar Height (in cm)': 'The total height of the bar',
                              'Number of Test Mixed Blocks': 'Number of test mixed blocks [i.e. number of times trials in .xlsx '
                                                       'file will be repeated. To set trial number and proportion of '
                                                       'stop vs. go edit the .xlsx file]',
                              'Full Screen': 'Do you want to run the task with Full Screen - recommended'
                              })
    if not dlg.OK: core.quit()
else:
    # Parameters with multiple options need their default selecting
    more_task_info[1]['Response Key'] = 'space'

if more_task_info[1]['Remember Parameters']: #if participant selects 'remember parameters'
    # print and save that information into the working directory
    print('storing parameters for later')
    toFile("more_task_info1.pickle", more_task_info[0])
    toFile("more_task_info2.pickle", more_task_info[1])

#---------------------------------------------------
# Further Additional Parameters Outside of the GUIs
#---------------------------------------------------
# This section is to adjust parameters that are not available in the GUIs
# These parameters are more technical and affect the task quite dramatically
# Do not change these parameters without fully considering their implications

# Bar_top: how many cm above the centre of the screen (x = 0 y = 0) the top of the bar will be drawn.
Bar_top = more_task_info[1]['Total Bar Height (in cm)'] / 2

# Target_pos: position of target line relative to total bar height (default is 80% of bar height)
Target_pos = (.8 * more_task_info[1]['Total Bar Height (in cm)']) - Bar_top

taskInfo = {
            'Bar base below fixation (cm)': Bar_top,
            'Bar width (cm)': 3,
            'Bar top above fixation (cm)': Bar_top,
            'Target line width (cm)': 5,
            'Target line above fixation (cm)': Target_pos,
            'rise velocity (cm/sec)': 15, # RP - Equal this to bar height?
            'trial length (max trial duration in seconds)': 1,
            'StopS start pos. (seconds)': .5
            }

# trial_length: max duration of a trial in seconds (time for bar to fill completely)
trial_length = taskInfo['trial length (max trial duration in seconds)']
bar_height = more_task_info[1]['Total Bar Height (in cm)']

# Target_time: time taken to reach target line (default: 80% of the total trial time)
Target_time = (.8 * taskInfo['trial length (max trial duration in seconds)'])

# Initial stop signal position
stoptime = taskInfo['StopS start pos. (seconds)']

#======================================
# Hardware parameters
#======================================
# Presents users with options for hardware parameters

# Set up the window in which we will present stimuli
win = visual.Window(
                fullscr=more_task_info[1]['Full Screen'],
                winType='pyglet',
                monitor='testMonitor',
                color=[-1, -1, -1],
                colorSpace='rgb',
                blendMode='avg',
                allowGUI=False,
                size=(1440, 900)
                )
mouse = event.Mouse(visible=False, newPos=None, win=win)
#======================================
# Data output
#======================================
# Create output directories if they do not already exist
outDirs = ['data_txt', 'data']
outFiles = []
for outDir in outDirs:
    if not os.path.exists(_thisDir + os.sep + outDir + os.sep):
        print(f'{outDir}folder did not exist, making one in current directory')
        os.makedirs(f'{_thisDir}{os.sep}{outDir}{os.sep}')
    outFiles.append(f'{_thisDir}{os.sep}{outDir}{os.sep}{expInfo["Participant ID"]}_{expName}_{expInfo["date"]}')

# Write header for txt file (i.e., column names)
Output = outFiles[0]
with open(Output + '.txt', 'a') as b:
    b.write('id	block	trialType	trial	signal	response	correct	ssd	rt\n')

#======================================
# Experiment Handler
#======================================
# Merge all info dictionaries so that we can save all the information to our output files
allInfo = {**expInfo, **more_task_info[0], **more_task_info[1]}

# Create experiment handler
thisExp = data.ExperimentHandler(
                name=expName, version='beta',
                extraInfo=allInfo,
                savePickle=True, saveWideText=True,
                dataFileName=outFiles[1], autoLog=True
                )
thisExp.nextEntry()

# save a log file for detailed verbose information
logFile = logging.LogFile(outFiles[1] + '.log', level=logging.DEBUG)
logging.console.setLevel(logging.WARNING)

# Create a list of all the conditions the user selected for
    # OSARI has two conditions:
        # Go and Mixed
            # Go conditions are just blocks with only go trials
            # Mixed conditions are blocks with both go and stop trials

    # The conditions are then further divided into those that are:
            # Practice - block of 'practice' trials completed before the 'test' blocks
            # Test - block of test trials that are used to assess participant performance

# Note that the only compulsory blocks are the test mixed blocks (see below)

condFileList = [] # Create a list to store the block conditions

# The condition files are excel or .xlsx files that contain two columns and X number of rows
    # with 'X' being the number of rows the user wants the participant's to complete
    # The columns are 'Signal' and 'fixedStopTime'

# Signal denotes the trial type, with 0's being a go trial and 1 being a stop trial
# Fixed stop time is only relevant for stop trials and
    # only if participants are NOT using staircased stop-signal delays (SSD)

#---------------------------------------------------
# Practice Go Block
#---------------------------------------------------
if more_task_info[0]['Practice Trials']: # if practice was selected
    condFileList.append(
                    ['conditionFiles/practiceGoTrials.xlsx', 1]
                    )

#---------------------------------------------------
# Test Go Block
#---------------------------------------------------
if more_task_info[0]['Test Go Block']: # if test go block was selected
    condFileList.append(
                    ['conditionFiles/testGoBlocks.xlsx', 1]
                    )

#---------------------------------------------------
# Practice Mixed Block
#---------------------------------------------------
if more_task_info[0]['Practice Trials']:  # if practice was selected
    condFileList.append(
                    ['conditionFiles/practiceMixedTrials.xlsx', 1]
                    )

#---------------------------------------------------
# Test Mixed Block
#---------------------------------------------------
condFileList.append(
                ['conditionFiles/testBlocks.xlsx',
                more_task_info[1]['Number of Test Mixed Blocks']
                ]
                )

#---------------------------------------------------
# Create trial handler object based on selected blocks
#---------------------------------------------------
for cond in condFileList:
    thisConditions = data.importConditions(cond[0])  # import the .xlsx file
    thisfilename = path.split(cond[0])[1]
    thisTrials = data.TrialHandler(
                    trialList=thisConditions,
                        nReps=cond[1],
                    method=more_task_info[0]['Trial Order'],
                    name=path.splitext(thisfilename)[0],
                        autoLog=True
                    )  # name of loop is .xlsx filename
    thisExp.addLoop(thisTrials)

#======================================
# Task instructions
#======================================

#---------------------------------------------------
# String text feedback
#---------------------------------------------------
instructions = data.importConditions(
                'conditionFiles/instructions.xlsx'
                )# import the excel file

instructionsText={}

for thisInstruction in instructions:
    if thisInstruction['respKey']:
        thisTxt = thisInstruction['instruction'].format(
                        variable = more_task_info[1]['Response Key']
                        )
    else:
        thisTxt = thisInstruction['instruction']
    thisInst = visual.TextStim(
                    win,
                    pos=[thisInstruction['thisX'],
                    thisInstruction['thisY']],
                    height=1,
                    wrapWidth = 30,
                    color=[1, 1, 1],
                    text=thisTxt,
                    units='cm'
                    )
    instructionsText[f"{thisInstruction['label']}"] = thisInst

#---------------------------------------------------
# Visual image feedback
#---------------------------------------------------
go_instr_image = visual.ImageStim(
                win, image='Stimuli' + os.sep + 'go_instr_image.jpeg',
                units='norm',
                size=(2, 2),
                interpolate = True
                )

stop_instr_image = visual.ImageStim(
                win, image='Stimuli' + os.sep + 'stop_instr_image.jpeg',
                units='norm',
                size=(2, 2),
                interpolate = True
                )

#---------------------------------------------------
# Numerical text feedback
#---------------------------------------------------
number_text = visual.TextStim(win,
                pos=[0, Target_pos],
                height=1,
                color=[-1, -1, -1],
                text="1",
                units='cm'
                )

#======================================
# Stimulus Parameters
#======================================
# OSARI presents participants with a (by default) white background bar
# When participants depress the response key, the background bar appears to be filled from the bottom up
# This is achieved by having a blue filling bar superimposed on the background bar

#---------------------------------------------------
# The Filling Bar (fillBar)
#---------------------------------------------------
bar_width_vert = [0 - (taskInfo['Bar width (cm)'] / 2), (taskInfo['Bar width (cm)'] / 2)]

# "vert" = vertices (corners) of filling bar in x y coordinates ([0, 0] = center)
vert = [(bar_width_vert[0], 0 - taskInfo['Bar base below fixation (cm)']),
        (bar_width_vert[0], 0 - taskInfo['Bar base below fixation (cm)'] + .01),
        (bar_width_vert[1], 0 - taskInfo['Bar base below fixation (cm)'] + .01),
        (bar_width_vert[1], 0 - taskInfo['Bar base below fixation (cm)'])
        ]

original_vert = vert

fillBar = FillingBar(
                win = win,
                vert = vert
                )

#---------------------------------------------------
# The Background Bar (Bar)
#---------------------------------------------------
# "fullvert" = vertices of the static background bar
fullvert = [(bar_width_vert[0], 0 - taskInfo['Bar base below fixation (cm)']),
            (bar_width_vert[0], taskInfo['Bar top above fixation (cm)']),
            (bar_width_vert[1], taskInfo['Bar top above fixation (cm)']),
            (bar_width_vert[1], 0 - taskInfo['Bar base below fixation (cm)'])
            ]

Bar = visual.ShapeStim(
                win, vertices=fullvert,
                fillColor='white',
                lineWidth=0,
                opacity=1,
                units='cm'
                )

#---------------------------------------------------
# The Target Arrows
#---------------------------------------------------
# OSARI denotes the 'target' through two equilateral triangles
# The inner most point of the triangles (pointing towards eachother) act as the target line
# Triangles were used so that a line was not superimposed onto the background bar

# The target width
target_width = 0.5

# Right Target Arrow
targetArrowRightvert = [(1.5, Target_pos),
                        (1.5 + target_width, Target_pos + (target_width / np.sqrt(3))),
                        (1.5 + target_width, Target_pos - (target_width / np.sqrt(3)))
                        ]

targetArrowRight = visual.ShapeStim(
                win,
                vertices=targetArrowRightvert,
                fillColor='gray',
                lineWidth=0,
                opacity=1,
                units='cm'
                )

# Left Target Arrow
targetArrowLeftvert = [
                (-1.5 - target_width, Target_pos + (target_width / np.sqrt(3))),
                (-1.5 - target_width, Target_pos - (target_width / np.sqrt(3))),
                (-1.5, Target_pos)
                ]

targetArrowLeft = visual.ShapeStim(
                win,
                vertices=targetArrowLeftvert,
                fillColor='gray',
                lineWidth=0,
                opacity=1,
                units='cm'
                )

#======================================
# Set the stimulus colors
#======================================
if more_task_info[1]['Color Blind Palette?']:
    palette = ['#009E73', '#F0E442', '#E69F00', '#D55E00']
else:
    palette = ['Green', 'Yellow', 'Orange', 'Red']

#======================================
# Begin task
#======================================
# At the beginning of the task, participants will be presented with the welcome image followed by the go instructions

#---------------------------------------------------
# Welcome Image
#---------------------------------------------------
welcome_image = visual.ImageStim(
                win,
                image='Stimuli' + os.sep + 'welcome_image.jpeg',
                units='norm',
                size=(2, 2),
                interpolate = True
                )

welcome_image.draw()
win.flip()
keyWatch(thisExp=thisExp)

#---------------------------------------------------
# Go Instructions
#---------------------------------------------------
go_instr_image.draw()
win.flip()
keyWatch(thisExp=thisExp)

#======================================
# Initialise Trials
#======================================
# Trial loop
height = 0
correct = []
correctThisTrial = []
ITI = 2 # the inter-trial interval or wait period

#======================================
# Start the task
#======================================
for i, block in enumerate(thisExp.loops):
    # iterate through the set of trials we have been given for this block
    for thisTrial in block:
        #---------------------------------------------------
        # Warning of upcoming trials and further instructions
        #---------------------------------------------------
        # if this is a practice go block
        if block.name == 'practiceGoTrials':
            # and if this is the first repetition of this block,
            if block.thisRepN == 0 and block.thisTrialN ==0:
                # warn of upcoming practice block of go trials
                instructionsText['practiceGoWarning'].draw()
                win.flip()
                keyWatch(thisExp=thisExp)
        # if this is a test go block
        if block.name == 'testGoBlocks':
            if block.thisRepN == 0 and block.thisTrialN ==0:
                # ask participant if they understand the task
                instructionsText['doYouUnderstand'].draw()
                win.flip()
                understand = event.waitKeys(keyList=['y', 'n'])
                if understand[0] == 'n':
                    thisExp.close()
                    core.quit()
                # warn of upcoming test block of go trials
                instructionsText['testGoWarning'].draw()
                win.flip()
                keyWatch(thisExp=thisExp)
        # if this is a practice block of go and stop trials
        if block.name == 'practiceMixedTrials':
            if block.thisRepN == 0 and block.thisTrialN ==0:
                stop_instr_image.draw()
                win.flip()
                keyWatch(thisExp=thisExp)
               # warn of upcoming practice mixed block of trials
                instructionsText['practiceMixedWarning'].draw()
                win.flip()
                keyWatch(thisExp=thisExp)
        # if this is a test block of go and stop trials
        if block.name == 'testBlocks':
            # If practice trials were not selected
            if block.thisRepN == 0 and block.thisTrialN == 0 and more_task_info[0]['Practice Trials']==False:
                # give the stop instruction image
                stop_instr_image.draw()
                win.flip()
                keyWatch(thisExp=thisExp)
            if block.thisRepN == 0 and block.thisTrialN ==0:
                # ask participant if they understand the task
                instructionsText['doYouUnderstand'].draw()
                win.flip()
                understand = event.waitKeys(keyList=['y','n'])
                if understand[0] == 'n':
                    thisExp.close()
                    core.quit()
                # warn of upcoming test block of mixed trials
                instructionsText['testMixedWarning'].draw()
                win.flip()
                keyWatch(thisExp=thisExp)
                #Store whether the response was correct = 2 or incorrect (correct = 0)
                correctThisTrial = correct
                # Set the stopTime to the starting stop-signal delay (SSD) requested
                stoptime = taskInfo['StopS start pos. (seconds)']
                correct = []  # Reset correct
                trial_label = 'main'
            #---------------------------------------------------
            # Give feedback after each test block is completed
            #---------------------------------------------------
            elif block.thisRepN > 0 and block.thisTrialN == 0:
                # set message
                Blocks_completed = visual.TextStim(
                                win, pos=[0, 0],
                                height=1,
                                color=[1, 1, 1],
                                text=f"Block {block.thisRepN} of {block.nReps} complete!\n\nPress space when ready to continue",
                                units='cm'
                                )
                # draw the message
                Blocks_completed.draw()
                win.flip()
                core.wait(3)# Wait at least 3 seconds untill a key press is registered
                keyWatch(thisExp=thisExp)
        #---------------------------------------------------
        # Set or Reset variables at the beginning of the trial
        #---------------------------------------------------
        # Set or reset the target arrows to be gray
        targetArrowRight.fillColor = 'gray'
        targetArrowLeft.fillColor = 'gray'
        trial_label = block.name
        # Set or reset the SSD (only relevant if it is a stop trial)
        if not more_task_info[0]['Method'] == 'fixed':
            stoptime = calculateStopTime(
                            correct, 
                            stoptime, 
                            more_task_info[1]['Lowest SSD (s)'],
                            more_task_info[1]['Highest SSD (s)'],
                            more_task_info[1]['Step size (s)']
                            )
        elif more_task_info[0]['Method'] == 'fixed':
            stoptime = int(thisTrial['fixedStopTime'])
        # Reset correct
        correct = []
        # Set the SSD
        Signal = thisTrial['Signal']
        if Signal == 1:
            # If stop trial, this_stoptime (SSD) = stoptime
            this_stoptime = stoptime
        else:
            # If go trial, SSD is just trial length
            this_stoptime = trial_length
        #---------------------------------------------------
        # Begin trial
        #---------------------------------------------------
        # Tell participant to hold response key down
        instructionsText['pressHold'].draw()
        win.flip()
        kb.start()  # Watch for the response key to be depressed
        kb.clearEvents()
        k = keyWatch(thisExp = thisExp, keyList=[more_task_info[1]['Response Key']])
        # Reset the vertices to their begining position
        fillBar.vertices = original_vert  # vert
        # Count down before trial starts
        if more_task_info[1]['Count Down']:
            countdown()
        stimList = [targetArrowLeft, targetArrowRight, Bar, fillBar]
        for stim in stimList:
            stim.setAutoDraw(True)
        # Set autoDraw for the stimulus elements before trial starts
        #   (Note: draw order is defined by the order in which setAutoDraw is called)
        # Record the frame intervals for the interested user
        win.frameIntervals = []
        win.recordFrameIntervals = True
        # "waiting" are we waiting for the key to be lifted
        waiting = 1
        win.flip()
        jitter = np.random.choice(np.arange(.5, 1, .05), 1)
        core.wait(jitter)
        # We want bar height and time elapsed to be 0 at this point
        height = 0
        time_elapsed = 0
        win.callOnFlip(kb.clock.reset)
        win.flip()
        # Whilst we are waiting for the button to be lifted
        while time_elapsed < trial_length and waiting == 1:
            # Watch the keyboard for a response
            remainingKeys = kb.getKeys(
                            keyList=[more_task_info[1]['Response Key'],
                            'escape'],
                            waitRelease=False,
                            clear=False
                            )
            # Record how much time has elapsed since the start of the trial
            time_elapsed = kb.clock.getTime()
            height = setHeight(
                            time_elapsed,
                            this_stoptime,
                            bar_height,
                            trial_length
                            )
            # If the key has been depressed (i.e. there is something in the keyboard events) ...
            # ... draw the filling bar. This will stop if key lift detected.
            if remainingKeys:
                for key in remainingKeys:
                    if key.duration:
                        lift_time = kb.clock.getTime()
                        kd_start_synced = key.duration - np.abs(
                                        (key.tDown - kb.clock.getLastResetTime())
                                        )
                        kb.clearEvents()  # clear the key events
                        waiting = 0
                    # Set the vertices of the filling bar
                    fillBar.fill(vert, height)
                    # Reset vertices to original position
                    vert = fillBar.resetVert(vert, height)
                    win.flip()
        # Stop recording frame intervals
        win.recordFrameIntervals = False
        # If this was a stop trial then the above while loop will have broken when the stoplimit was
        # reached. but, we still want to wait until the end of the trial to make sure they
        # actually hold and don't lift as soon as the stop limit is reached
        #---------------------------------------------------
        # End of Trial:
        #---------------------------------------------------
        kb.stop()  # Stop watching the keyboard
        # if the bar has filled but we are still waiting for the key to lift
        if waiting == 1:
            kd_start_synced = 'NaN'
            lifted = 0
            RT = 'NaN'
            #'''''''''''''''''''''''''''''''''''''''''''''''''''
            # Omission Error
            #'''''''''''''''''''''''''''''''''''''''''''''''''''
            if Signal == 0:
                feedback = instructionsText['Omission']
                # Change the colour of the target arrows based on feedback
                targetArrowRight.fillColor = palette[3]
                targetArrowLeft.fillColor = palette[3]
                correct = -1 
            #'''''''''''''''''''''''''''''''''''''''''''''''''''
            # Correct Stop
            #'''''''''''''''''''''''''''''''''''''''''''''''''''
            elif Signal == 1:
                correct = 2
                # Change the colour of the target Arrows
                targetArrowRight.fillColor = palette[0]
                targetArrowLeft.fillColor = palette[0]
                feedback = instructionsText['correctStop']
        # If the key was lifted before the bar filled
        else:
            # If this was a stop trial give feedback that the participant incorrectly stopped
            lifted = 1
            RT = lift_time
            if Signal == 0:
                #'''''''''''''''''''''''''''''''''''''''''''''''''''
                # Correct Go 
                #'''''''''''''''''''''''''''''''''''''''''''''''''''
                correct = 1
                targetArrowRight.fillColor = setTargetCol(kd_start_synced, Target_time, palette)
                targetArrowLeft.fillColor = setTargetCol(kd_start_synced, Target_time, palette)
                if RT > .100:
                    feedback = instructionsText['correctGo']
                else:
                    feedback = instructionsText['almostGo']
            elif Signal == 1:
                #'''''''''''''''''''''''''''''''''''''''''''''''''''
                # Correct Stop
                #'''''''''''''''''''''''''''''''''''''''''''''''''''
                feedback = instructionsText['incorrectGo']
                targetArrowRight.fillColor = palette[3]
                targetArrowLeft.fillColor = palette[3]
                correct = 0
        if more_task_info[1]['Trial-by-trial Feedback']:
            feedback.setAutoDraw(True)
        win.flip()
        if Signal == 0:
            this_stoptime = 'NaN'
        #---------------------------------------------------
        # Write data to .txt file
        #---------------------------------------------------
        with open(Output + '.txt', 'a') as b:
            b.write(f'{expInfo["Participant ID"]}	{block.thisRepN}	{trial_label}	{block.thisTrialN}	{Signal}	{lifted}	{correct}	{this_stoptime}	{kd_start_synced}\n')
        #---------------------------------------------------
        # Write data to .csv file
        #---------------------------------------------------
        # Column headers
        colHeaders=[
            'block',
            'trialType',
            'trial',
            'signal',
            'response',
            'correct',
            'ssd',
            'rt'
            ]
        # Column values for given trial
        values =[
            i,
            trial_label,
            block.thisTrialN,
            Signal,
            lifted,
            correctThisTrial,
            this_stoptime,
            kd_start_synced
            ]
        for idx, header in enumerate(colHeaders):
            thisExp.addData(header, values[idx])
        thisExp.nextEntry()
        core.wait(ITI)
        # Reset visual stimuli for next trial
        stimList = [
            feedback,
            targetArrowLeft,
            targetArrowRight,
            Bar,
            fillBar]
        for stim in stimList:
            stim.setAutoDraw(False)
#======================================
# End Task
#======================================
EndMessage = visual.TextStim(
                win, pos=[0, 0.4],
                height=1, units='cm',
                color=[1, 1, 1],
                text="The End!\nThanks for taking part!\n[press a key to end]"
                )
EndMessage.draw()
win.flip()
event.waitKeys()
thisExp.close()
core.quit()
