# Open-Source Aniticipated Response Inhibition task (OSARI)

Originally created in PsychoPy v3.1.2 updated in v2020.2.10

Last edited: 31/03/2021

**If using this task please cite**:

He, J. L , Hirst, R. J , Puri, R.,Coxon, J., Byblow, W., Hinder, M., Skippen, P., Matzke, D., Heathcote, A., Wadsley, C.G., Hyde, C., Parmar., D., Pedapati, E., Gilbert, D.L., Huddleston, D.A., Motofsky, S., Leunissen, I., McDonald, H., Chowdhury, N., Gretton, M., Nikitenko, T., Zandbelt, B., Luke., Strickland., Puts, N. (In prep) *OSARI, an Open-Source Anticipated Response Inhibition task*

## About OSARI
Anticipated response inhibition (ARI) tasks are a version of the stop-signal paradigm that have seen increasing use in cognitivie neuroscience. This project provides a free-to-use Open-Source Anticipated Response Inhibition (OSARI) developed in PsychoPy and openly available for ongoing contributions and development.

## Getting Started
Running OSARI will require you to have [PsychoPy installed](https://www.psychopy.org/download.html). Once PsychoPy is installed, you can run OSARI from within coder view or your chosed development environment. OSARI was originally developed in pure python code, but the code components used here can be easily translated into builder view for more intuitive use and adaptations (we have started this transition to create [a version of OSARI that runs in browser](https://run.pavlovia.org/lpxrh6/osari_online) you can find the files associated with this [here](https://pavlovia.org/lpxrh6/osari_online). Here we provide a quick introduction to the task. For a more in-depth explanation, see the cited manuscript. 

## The Task 
OSARI presents participants with a white 'background bar', with two gray arrows on the left and right side of the top end of the bar. The gray arrows are 'target arrows'.


OSARI has two types of trials:
  * Go trials
  * Stop trials

*Go* trials require participants to stop a filling bar as close as possible to the target arrows. The filling bar will begin 'filling' when participants have depressed a computer key, and will stop filling when they release the key. Participants will be given feedback on each trial.

Example of the filling bar on a go trial. The arrows will turn red if the participant stops the bar very far from the target line:

<img src="/media/example-go.gif" width="60%"/>

For go trials, emphasise to the participant that they should try and keep the arrows green.

*Stop* trials require participants to keep the computer key depressed rather than releasing the computer key (as they would in a go trial) when the filling bar ceases to fill automatically (i.e., the bar stops on its own, acting as a stop-signal). If participants are able to keep the key depressed until the end of the trial, they will be provided with feedback as so:

<img src="/media/example-stop.gif" width="60%"/>

If participants are not able to keep the key depressed, then they will be given the feedback:

<img src="/media/static-incorrect-stop.png" width="60%"/>

## Default settings and customisation
Go and Stop trials are presented with a set proportion, but in a random order. The stop-signal delays (SSDs) is adapted based on participant performance (i.e. staircased). By default, participants complete:
  * 1 x practice block of go trials
  * 1 x test block of go trials
  * 1 x practice block of go and stop trials
  * 3 x test blocks of go and stop trials

Researchers can change most task parameters directly from the dialogue box presented at the beginning of the task, without needing to interact with the python code itself. We therefore hope that most task features can be adapted to the researchers needs with minimal coding required.

If you come by any issues, or if you need help with getting started with the task, feel free to email us at: opensourceTAP@gmail.com or report the issue on the github page). 

### Input files:
    
Four xlsx files in `connditionsFiles`:
  * `instructions.xlsx` : text instructions and feedback presented during the task
  * `practiceGoTrials.xlsx` : trial info of the practice go block
  * `testGoBlocks.xlsx` : trial info of the main ("test") go block
  * `practiceMixedTrials.xlsx`: trial info of the practice mixed (Go and Stop) block
  * `testBlocks.xlsx` : : trial info of each main ("test") mixed block

In the `.xlsx` files, each row is a trial. The *Signal* column determines the trial type (0 = go trial and 1 = stop trial). The *fixedStopTime* column is used for putting in a SSD when you are using fixed rather than staircased SSDs. The value of *fixedStopTime* cells need to between 0 and 1 (eg., a fixedStopTime of 0.5 means a SSD of 500 ms - the bar will stop 500 ms into the trial). 

### Output files:
    
Four output files are generated with the format `ID_OSARI_yyyy_mm_d_hhmm` where ID = participant ID, yyyy = year, mo = month in string format, d = day in numeric format, h = hour and m = minute. The primary data output file used by our analysis script are the `.txt` files stored in the `dataTxt/` subfolder. All other files are stored in `data/` `.csv` files include all additional data [Log files](https://www.psychopy.org/general/dataOutputs.html) provide a timestamped log of events that can be used for checking stimulus and event timings.
    
### Basic information 

**id**: Participant identification number or string
    
**block**: Block number

**trialType**: Practice or real trial

**trial**: Trial number within a block

**signal**: 0 = Go
            1 = Stop

**response**: What the participants response was ( 0 = no lift, 1 = lift)

**correct**: 0 = incorrect stop
             -1 = incorrect go (omission error)
             1 = correct go
             2 = correct stop

**rt**: Lift time of participants relative to the starting line

**ssd**: Stop Signal Distance (relative to starting line) if the trial was a stop trial (NaN for go trials).
        
## Analysing the data
There are currently two ways to analyse the data you collect using OSARI. First, OSTAP provides the [Batch Analysis of Stop-signal Task Data (BASTD)](https://github.com/teamOSTAP/BASTD), which exists as a separate repository in our GitHub. Second, users may also analyse task performance using the [Dynamic Models of Choice (DMC) R system](osf.io/tw46u/). Please see the manuscript for further information. 

# Thanks for using OSARI!! 



