
#These are internal functions used by the main OSARI.py code
from psychopy import event, core
from psychopy.visual.shape import ShapeStim


class FillingBar(ShapeStim):
    """
    Extend the class ShapeStim to make a bar that fills
    """
    def __init__(self, win, vert):
        ''' Initialize FillingBar object'''
        ShapeStim.__init__(self,
                                  win = win,
                                  fillColor='skyblue',
                                  lineWidth=0,
                                  opacity=1,
                                  units='cm',
                                  vertices=vert)

    def fill(self, vert, height):
        ''' Reset the height of the FillingBar object
        input:
        vert: set of vertices
        height: new height of upper vertices'''
        vert[1] = (vert[1][0], vert[1][1] + height)  # left corner
        vert[2] = (vert[2][0], vert[2][1] + height)  # right corner
        self.vertices = vert

    def resetVert(self, vert, height):
        ''' Reset vertices of the filling bar to their starting height'''
        vert[1] = (vert[1][0], vert[1][1] - height)  # left corner
        vert[2] = (vert[2][0], vert[2][1] - height)  # right corner
        return vert

def keyWatch(thisExp, keyList=None):
    """
    Wait for key presses and escape if escape pressed
    """
    if keyList:
        keyList.append('escape')
    keys = event.waitKeys(keyList = keyList)
    if keys[0] =='escape':
        print('User pressed escape, quiting now')
        thisExp.close()
        core.quit()

def countdown():
    """ Count down the start of the trial and warn if key is lifted too soon"""
    countdownTime = core.CountdownTimer(3)
    while countdownTime.getTime() > 0:
        remainingKeys = kb.getKeys(keyList=[more_task_info[1]['Response key'], 'escape'], waitRelease=False, clear=False)
        number_text.text = f'{int(countdownTime.getTime())}'
        if remainingKeys:
            for key in remainingKeys:
                if key.duration:
                    kb.clearEvents()  # clear the key events
                    kb.clock.reset()  # reset the keyboard clock
                    instructionsText['tooSoon'].draw()  # early lift warning
                    win.flip()
                    k = event.waitKeys()  # wait for keypress
                    if k[0] == 'escape':  # allow escape during countdown
                        print('User pressed escape, quiting now')
                        win.close()
                        core.quit()
                    countdownTime.reset()  # reset the countdown clock
        Bar.draw()
        fillBar.draw()
        targetArrowRight.draw()
        targetArrowLeft.draw()
        if countdownTime.getTime() > 0:
            number_text.draw()
        win.flip()

def calculateStopTime(correct, stoptime, lower_ssd, upper_ssd, stepsize):
    """
    Calculate stoptime for next trial based on:
        correct (int):
            0 = incorrect stop OR
            2 = correct stop
        stoptime (float):
            stoptime on previous trial
        lower_ssd (float):
            lowest possible ssd selected by the user in the Additional Parameters Dialog 
        upper_ssd (float)
            highest possible ssd selected by the user in the Additional Parameters Dialog 
    """
    if  correct == 2 and stoptime < upper_ssd:
        stoptime = stoptime + stepsize
    elif correct == 2 and stoptime == upper_ssd:
        stoptime = upper_ssd
    elif correct == 0 and stoptime > lower_ssd: 
        stoptime = stoptime - stepsize
    elif correct == 0 and stoptime == lower_ssd:
        stoptime = lower_ssd
    return stoptime

def setHeight(time_elapsed, this_stoptime, bar_height, trial_length):
    """
    Calculate "height" - the current height of the bar in cm
    this will be added to the vertices position to adjust the size of
    the filling (blue) bar.
    """
    if time_elapsed < this_stoptime:
        height = (time_elapsed * bar_height) / trial_length
    elif time_elapsed >= this_stoptime:
        height = (this_stoptime * bar_height) / trial_length  # max_height
    return height

def setTargetCol(kd_start_synced, Target_time, palette):
    """
    set color of the target triangles based on distance
    """
    if abs(kd_start_synced - Target_time) < .02:
        fillCol = palette[0]
    elif .04 > abs(kd_start_synced - Target_time) >= .02:
        fillCol= palette[1]
    elif .06 > abs(kd_start_synced - Target_time) >= .04:
        fillCol = palette[2]
    else:
        fillCol = palette[3]
    return fillCol
