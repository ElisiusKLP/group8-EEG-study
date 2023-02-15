# Thatcher EEG Experiment

#importing modules
from psychopy import visual, core, event, sound, gui, data #gui making the gui, data making the data of the logfile with the results
import glob
import random #need to figure out what this does??
import pandas as pd

dialog = gui.Dlg (title = "Face EEG experiment")
dialog.addField("Participant ID:")
dialog.addField("Age:")
dialog.addField("Gender:", choices = ["female", "male", "other"]) #making a drop down menu
dialog.addField("Handedness:", choices = ["right-handed", "left-handed"]) 
dialog.show()
if dialog.OK: 
    ID = dialog.data[0]
    Age = dialog.data[1]
    Gender = dialog.data[2]
    Handedness = dialog.data[3]
elif dialog.Cancel:
    core.quit
print(ID,Age,Gender,Handedness)

# Defintions
## Defining window
win = visual.Window(color = "black", fullscr = True)

## Defining columns for dataframe
cols = ["Timestamp","ID", "Age","Gender", "Handedness","Response", "ReactionTime", "Stimulus", "Rotation", "Familiarity", "Changed","Accuracy"]

## Define stopwatch
stopwatch = core.Clock()

# define timestamp/date
date = data.getDateStr()

## Defing logfile dataframe for appending
logfile = pd.DataFrame(columns = cols)


## Defining stimulus images from folder
stimuli = glob.glob("stimuli/*")

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

blank = ''' '''

# Experiment intiated

## designing functions
### msg function show text and wait for key press
def msg(txt):
    message = visual.TextStim(win, text = txt, alignText = "left", height = 0.05)
    message.draw()
    win.flip()
    event.waitKeys(keyList = ["space"])

def blanker(txt):
    message = visual.TextStim(win, text = txt, alignText = "left", height = 0.05)
    message.draw()
    win.flip()

# Experiment intiation

## Msg Instructions
msg(instruction)

## Experiment loop

for i in stimuli:
    #prepare stimulus
    stimulus = visual.ImageStim(win, image = i)
    #draw to canvas
    stimulus.draw()
    #flip the window
    win.flip()
    # wait 
    core.wait(1)
    # draw visual noise for 0.2 sec
    noise.draw()
    win.flip()
    core.wait(0.5)
    #show a blank screen
    blanker(blank)
    #reseting the stop watch
    stopwatch.reset() #asking it to start the timer here
    #wait until key press
    key = event.waitKeys(keyList = ["left","right"])
    # "ask" how much time it took for the participants to answer?
    reaction_time = stopwatch.getTime()
    print(reaction_time)
    
    #define variables based on stimuli at hand for appending to dataframe
    if (key == ["left"]):
        Response = "change"
    else:
        Response = "no_change"
    
    
    if ("_0rotation" in i):
        Rotation = "0"
    if ("_90rotation" in i):
        Rotation = "90"
    if ("_180rotation" in i):
        Rotation = "180"
        
    if ("_familiar" in i):
        Familiarity = "1"
    if ("_unfamiliar" in i):
        Familiarity = "0"
        
    if ("_changed" in i):
        Changed = "1"
    if ("_unchanged" in i):
        Changed = "0"
        
    if ( ("_changed" in i and key == ["left"]) or ("_unchanged" in i and key == ["right"]) ):
        Accuracy = 1
    else:
        Accuracy = 0

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
    "Accuracy":Accuracy
    }, ignore_index = True)

## message goodbye 
msg(goodbye)
win

# saving the logfile
##Creating a unique file name
logfile_name= "logfiles/Logfile_{}_{}.csv".format(ID, date) 

## saving the data frame
logfile.to_csv(logfile_name)

