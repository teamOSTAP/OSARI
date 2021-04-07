from psychopy import data, visual, event, core
from os import path

taskInfo_brief_a={}
taskInfo_brief_a['All Go block'] = 1
taskInfo_brief_a['Practice trials'] = 1
taskInfo_brief_a['Trial order'] = 'random'

thisExp = data.ExperimentHandler(
    name = 'OSARI', version = '1.8',
    extraInfo = taskInfo_brief_a, #this will save all of the user input for task info brief - might want also the full task info
        savePickle=True, saveWideText=True, autoLog = True)

''' make a list of conditions that is dependant on if we have prac trials and 
a go block. Note: this is created in a fixed order, assuming that if a Go block
is requested, it will be presented first'''
condFileList=[]
if taskInfo_brief_a['All Go block']:
    if taskInfo_brief_a['Practice trials']:
        condFileList.append('practiceGoTrials.csv')
    condFileList.append('testGoBlocks.csv')
if taskInfo_brief_a['Practice trials']:
    condFileList.append('practiceMixedTrials.csv')
condFileList.append('testBlocks.csv')

condFileList=[]
if taskInfo_brief_a['All Go block']:
    if taskInfo_brief_a['Practice trials']:
        condFileList.append(['practiceGoTrials.csv', 1])
    condFileList.append(['testGoBlocks.csv', 1])
if taskInfo_brief_a['Practice trials']:
    condFileList.append(['practiceMixedTrials.csv', 1])
condFileList.append(['testBlocks.csv', 3])

'''previously all of our trialHandler objects had the same parameters, 
so we can make this slicker using a loop. This does require that we name our 
conditions files with what we want the loop to be called ('practiceGoTrials',
'testGoBlocks''practiceMixedTrials'-'testBlocks') but I think this is 
good as it reduces the number of similar variable names'''
for cond in condFileList: 
    thisConditions = data.importConditions(cond[0])#import the .csv file
    thisTrials = data.TrialHandler(trialList = thisConditions, nReps = cond[1], 
        method = taskInfo_brief_a['Trial order'], 
        name = path.splitext(cond[0])[0],autoLog = True)#name of loop is .csv filename
    thisExp.addLoop(thisTrials)

print(dir(thisExp))
print(len(thisExp.loops))#tells us how many loops we have in our task - should be as long as blocks for us

for loop in thisExp.loops:
    print(loop.name)
    print(loop.nReps)
    

'''
so we now create our loops in experiment handler more simply. what about the start
of our block loop'''
win = visual.Window(
    fullscr=False,
    monitor='testMonitor',
    color=[-1,-1,-1],
    colorSpace='rgb',
    blendMode='avg',
    mouseVisible = False,
    allowGUI=False,
    size=(1440, 900))

understand=visual.TextStim(win, pos=[0, 0], height=1, color= [1,1,1],
    text="Do you understand the task? (Y/N)", units='cm' )
practice_go_inst=visual.TextStim(win, pos=[0, 0], height=1, color= [1,1,1],
    text="Lets start with some Go trials.\n Press any button to begin!", units='cm' )
real_go_inst=visual.TextStim(win, pos=[0, 0], height=1, color= [1,1,1],
    text="OK now we will try some real Go trials.\n Press any button to begin!", units='cm' )
real_mixed_inst=visual.TextStim(win, pos=[0, 0], height=1, color= [1,1,1],
    text="Great! Next, lets do some Go and Stop trials!\n Press any button to begin!", units='cm' )

for i, block in enumerate(thisExp.loops):
    for trials in block:
        print(dir(block))
        print(block.thisN)
        if block.name=='practiceGoTrials':
            understand.draw()
            win.flip()
            #wait for key press
            UnderstandKey = event.waitKeys(keyList=['y','n'])
            if UnderstandKey[0] == 'n':
                core.quit()
        elif block.name=='testGoBlocks':
            real_go_inst.draw()
            win.flip()
            event.waitKeys()
            #check if the user understood the task, if not ('n') quit the task
        elif block.name=='testBlocks' and i>0:
            #set message
            Blocks_completed = visual.TextStim(win, pos=[0, 0], height=1, color=[1,1,1],
                text="Block %s of %s complete!!\n\nPress space when ready to continue!"%(block.thisRepN, block.nReps), units='cm')#the "-1" here is for the go block 
            Blocks_completed.draw()
            win.flip()
            core.wait(1)
            #wait for keypress
            event.waitKeys()
        elif block.name=='testBlocks' and i==0:
            real_mixed_inst.draw()
            win.flip()
            event.waitKeys()