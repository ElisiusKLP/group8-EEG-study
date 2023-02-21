####
# File for writing classes and functions that can be imported into the psychopy script
# Laurits Lyngbæk
####

def dialogbox():
    dialog = gui.Dlg(title="Face EEG experiment")
    dialog.addField("Participant ID:")
    dialog.addField("Age:")
    dialog.addField("Gender:", choices=["female", "male", "other"])  # making a drop down menu
    dialog.addField("Handedness:", choices=["right-handed", "left-handed"])
    dialog.show()


class ExpRunner:
    def __init__(self):
        dialogbox

