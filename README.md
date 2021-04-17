# Open-Source Aniticipated Response Inhibition task (OSARI)

Created in PsychoPy v3.1.2

Last edited: 31/03/2021

If using this task please cite:

He, J. L , Hirst, R. J , Pedapati, E., Byblow, W., Chowdhury, N., Coxon, J., Gilbert, Donald., Heathcote, A., Hinder, M., Hyde, C., Silk. T., Leunissen, I., McDonald, H., Nikitenko, T., Puri, R., Zandbelt, B., Puts, N. (In prep) Open-Source Anticipated Response Inhibition task (OSARI): a cross-platform installation and analysis guide. 

## About OSARI
Anticipated response inhibition (ARI) tasks are a version of the stop-signal paradigm that have seen increasing use in cognitivie neuroscience. This project provides a free-to-use Open-Source Anticipated Response Inhibition (OSARI) developed in PsychoPy and openly available for ongoing contributions and development.

## Getting Started
Running OSARI will require you to have PsychoPy installed (see: https://www.psychopy.org/download.html). Once PsychoPy is installed, you can run OSARI like you would any other task. OSARI was originally developed within coder view, but the code components used here can be easily translated into builder view for more intuitive use and adaptations. Here we provide a quick introduction to the task. For a more in-depth explanation of the task, see the manuscript above. 

## The Task 
OSARI presents participants with a white 'background bar', with two gray arrows on the left and right side of the top end of the bar. The gray arrows are 'target arrows'.

![alt text](https://i.imgur.com/64VQeiZ.png)

OSARI has two types of trials:
  * Go trials
  * Stop trials

*Go* trials require participants to stop a filling bar as close as possible to the target arrows. The filling bar will begin 'filling' when participants have depressed a computer key, and will stop filling when they release the key. Participants will be given feedback on each trial.

Example of the filling bar on a go trial:

![alt text](https://i.imgur.com/ZI9R9Zh.png)

Example of feedback on a go trial where the participant managed to stop the bar close enough to the target arrows for the arrows to turn green:

![alt text](https://i.imgur.com/WfyeFvX.png)

Example of when the filling bar was stopped on a go trial, but too far from the target line, resulting in the arrows turning amber:

![alt text](https://i.imgur.com/bfsAI3j.png)

The arrows will turn red if the participant stops the bar very far from the target line:

![alt text](https://i.imgur.com/HFYrFlC.png)

Or if the participant does not make a response at all:

![alt text](https://i.imgur.com/t4enmYo.png)

For go trials, emphasise to the participant that they should try and keep the arrows green.

*Stop* trials require participants to keep the computer key depressed rather than releasing the computer key (as they would in a go trial) when the filling bar ceases to fill automatically (i.e., the bar stops on its own, acting as a stop-signal). If participants are able to keep the key depressed until the end of the trial, they will be provided with feedback as so:

![alt text](https://i.imgur.com/W0YgoHY.png)

If participants are not able to keep the key depressed, then they will be given the feedback:

![alt text](https://i.imgur.com/2hPiMoN.png)

## Default settings and customisation
Go and Stop trials are presented with a set proportion, but in a random order. The stop-signal delays (SSDs) is adapted based on participant performance (i.e. staircased). By default, participants complete:
  * 1 x practice block of go trials
  * 1 x test block of go trials
  * 1 x practice block of go and stop trials
  * 3 x test blocks of go and stop trials

Researchers can change most task parameters directly from the dialogue box presented at the beginning of the task, without needing to interact with the python code itself. We therefore hope that most task features can be adapted to the researchers needs with minimal coding required.

If you come by any issues, or if you need help with getting started with the task, feel free to email us at: opensourceTAP@gmail.com or report the issue on the github page). 

### Input files:
    
3 csv files:
  * practiceGoTrials.csv
  * practiceMixedTrials.csv
  * testBlocks.csv
  * instructions.xlsx
    
In the .csv files, each row is a trial. The Signal column determines the trial type (0 = go trial and 1 = stop trial). The fixedStopTime column is used for putting in a SSD when you are using fixed rather than staircased SSDs. The value of fixedStopTime cells need to between 0 and 1 (for eg., a fixedStopTime of 0.5 means a SSD of 500 ms - the bar will stop 500 ms into the trial). For more information about how to setup the .csv files, please refer to the instructions.xlsx file.

### Output files:
    
4 output files in format (see format details below):
  * s_123_OSARI_2020_Jul_19_1307.log
  * s_123_OSARI_2020_Jul_19_1307.csv
  * s_123_OSARI_2020_Jul_19_1307.psydat
  * s_123_OSARI_2020_Jul_19_1307.txt

naming format: s_[participant ID]_OSARI_[year]_[month]_[date]_[timestamp].csv

Data is contained in the .txt and .csv files. The .txt file saves the main details of interest but csv stores further details.
    
### Basic information 
    
**Block**: block number

**TrialType**: Practice or real trial

**Trial**: Trial number_text

**Signal**: 0 = Go
            1 = Stop

**Response**: What the participants response was ( 0 = no lift, 1 = lift)

**RT**: Lift time of participants relative to the starting line (to 2 decimal places)

**SSD**: Stop Signal Distance (relative to starting line) if the trial was a stop trial.
    
For details on psydat and log files see 
        https://www.psychopy.org/general/dataOutputs.html#:~:text=PsychoPy%20data%20file%20(.-,psydat),python%20and%2C%20probably%2C%20matplotlib.
        
## Analysing the data
There are currently two ways to analyse the data you collect using OSARI. First, OSTAP provides the batch analysis of stop-signal task data (BASTD), which exists as a separate repository in our GitHub. Second, users may also analyse task performance using the Dynamic Models of Choice (DMC) R system, which can be accessed at: osf.io/tw46u/. Please see the manuscript for further information. 

# Thanks for using OSARI!! 

## About the OSTAP team

The OSTAP team are a group of psychologists/cognitive scientists that like making open source tasks for fun.


