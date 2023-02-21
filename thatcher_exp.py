# Thatcher EEG Experiment
#importing modules
from psychopy import visual, core, event, sound, gui, data #gui making the gui, data making the data of the logfile with the results
import glob
import random #need to figure out what this does??
import pandas as pd
from psychopy import parallel
import platform
import csv
import os # package to fix file directions onto every os
#from triggers import setParallelData #for the EEG trigger

# Experimental parameters
RETINA = True #set to true if using mac with retina screen, set to false if using other OS

# Monitor parameters
MON_DISTANCE = 60 # Distance between subject's eyes and monitor
MON_WIDTH = 20 # Width of your monitoir in cm
MON_SIZE = [1440, 900] # Pixel dimension of your monitor
FRAME_RATE = 60 # Hz

# Defining and running dialog_boxes
def dialog_box(): #Gui of dialogbox
    global dialog
    dialog = gui.Dlg(title="Face EEG experiment")
    dialog.addField("Participant ID:")
    dialog.addField("Age:")
    dialog.addField("Gender:", choices=["female", "male", "other"])  # making a drop down menu
    dialog.addField("Handedness:", choices=["right-handed", "left-handed"])
    dialog.show()

def save_values(): #Saving values of dialogbox in global variables
    global ID, Age, Gender, Handedness
    if dialog.OK:
        ID = dialog.data[0]
        Age = dialog.data[1]
        Gender = dialog.data[2]
        Handedness = dialog.data[3]
    elif dialog.Cancel:
        core.quit

dialog_box()
save_values()

# Defintions
## Defining window
win = visual.Window(color = "black", fullscr = True)

## Defining columns for dataframe
cols = ["Timestamp","ID", "Age","Gender", "Handedness","Response", "ReactionTime", "Stimulus", "Rotation", "Familiarity", "Changed","Accuracy", "StimulusTrigger", "ResponseTrigger"]

## Define stopwatch
stopwatch = core.Clock()

# define timestamp/date
date = data.getDateStr()

## Defing logfile dataframe for appending
logfile = pd.DataFrame(columns = cols)

## Defining stimulus images from folder
stimuli = glob.glob(os.path.join("stimuli", "*") )

random.shuffle(stimuli) # putting the list of all movie paths in random order

### define noise stimulus

noise = visual.ImageStim(win, image = "noise/noise.png")

## Defining messages
### Define instruction message
instruction = '''Welcome to our EEG experiment

Your task is to look at a series of images and determine whether there have been made changes to the local facial features
or if the face image remains in its original form.

Use your right hand to press 
left arrow for a changed image and
right arrow for no changes.


Press space when you're ready to start
'''

### Defining goodbye message
goodbye = ''' 
Eksperimentet er nu færdigt. Tak for din deltagelse. '''


## designing functions
### msg function show text and wait for key press
def msg(txt):
    message = visual.TextStim(win, text = txt, alignText = "left", height = 0.05)
    message.draw()
    win.flip()
    event.waitKeys(keyList = ["space"])


def save_stimuli_variables(i):  
    if ("_0rotation" in i): #check rotation
        Rotation = "0"
    if ("_90rotation" in i):
        Rotation = "90"
    if ("_180rotation" in i):
        Rotation = "180"
        
    if ("_familiar" in i): #check familiraity
        Familiarity = "1"
    if ("_unfamiliar" in i):
        Familiarity = "0"
        
    if ("_changed" in i): #check if picture is changed
        Changed = "1"
    if ("_unchanged" in i):
        Changed = "0"
        
    return Rotation, Familiarity, Changed

def get_stimuli_trigger(Rotation, Familiarity, Changed):
    """ 
    conditional trigger decision
    1XX = Unfamilliar,  2XX = Familliar
    X1X = Unchanged,    X2X = Changed
    XX1 = 0 degrees, XX2 = 90 degrees, XX3 = 180 degrees of rotation
    
    
    takes three conditions and return a stim trigger in logic with flow chart above.
    """
    Rotation = int(Rotation)
    Familiarity = int(Familiarity)
    Changed = int(Changed)
    
    Stim_trigger = 0
    Stim_trigger += int((Rotation+90)/90)
    Stim_trigger += (Changed+1)*10
    Stim_trigger += (Familiarity+1)*100
    return Stim_trigger

def check_accuracy(key, i):
    #Check response
    if (key == ["q"]): 
        core.quit
    elif (key == ["left"]):
        Response = "change"
    else:
        Response = "no_change"
    #check accuracy
    if ( ("_changed" in i and key == ["left"]) or ("_unchanged" in i and key == ["right"]) ): 
        Accuracy = 1
    else:
        Accuracy = 0
    return Response, Accuracy
    
def get_response_trigger(Response):
    """
    Returnes the response variable as a trigger, either:
        001 for asnwering 'change'
        or
        002 for answering 'no_change'
    """
    if Response == "change":
        Response_trigger = 1
    else:
        Response_trigger = 2
    return Response_trigger


# Experiment intiation

## Msg Instructions
msg(instruction)

## Experiment loop

for i in stimuli:
    #### setParallelData(0) should this be reset after flip?
    #prepare stimulus
    stimulus = visual.ImageStim(win, image = i)
    Rotation, Familiarity, Changed = save_stimuli_variables(i)
    StimTrig = get_stimuli_trigger(Rotation, Familiarity, Changed)
    print(f"Stim = {StimTrig}")
    #### win.callOnFlip(setParallelData, StimTrig)
    #draw to canvas
    stimulus.draw()
    #flip the window
    win.flip()
    #### setParallelData(0) should this be reset after flip?
    
    
    #reseting the stop watch
    stopwatch.reset() #asking it to start the timer here
    #wait until key press
    key = event.waitKeys(keyList = ["left","right", "q"])
    Response, Accuracy = check_accuracy(key, i)
    RespTrig = get_response_trigger(Response)
    #### win.callOnFlip(setParallelData, RespTrig)
    print(f"Resp = {RespTrig}")
    
    # "ask" how much time it took for the participants to answer?
    reaction_time = stopwatch.getTime()
        
    noise.draw() #draw noise stimuli
    win.flip() #show noise
    #### setParallelData(0) should this be reset after flip?
    core.wait(1) #wait a second

    #append data to logfile
    logfile = logfile.append({
    "Timestamp": date, 
    "ID":ID,
    "Age":Age,
    "Gender":Gender,
    "Handedness":Handedness,
    "Response":Response,
    "ReactionTime":reaction_time,
    "Stimulus": i,
    "Rotation":Rotation,
    "Familiarity":Familiarity,
    "Changed":Changed,
    "Accuracy":Accuracy,
    "StimulusTrigger":StimTrig,
    "ResponseTrigger":RespTrig  
    }, ignore_index = True)





## message goodbye 
msg(goodbye)
win

# saving the logfile
##Creating a unique file name
logfile_name= "logfiles/Logfile_{}_{}.csv".format(ID, date) 

## saving the data frame
logfile.to_csv(logfile_name)

