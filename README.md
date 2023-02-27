# group8-EEG-study
An EEG experiment study by group 8 cognitive science 4th semester AU. 
The experiment is meant to investigate if faces subjected to the thatcher effect activates the N170.

Both thatcher_exp have setParrallelData active, so they can only run on parralel systems.

The trigger codes are defined as following:
    
Conditional trigger choice logic:

    1XX = Unfamilliar,  2XX = Familliar
    X1X = Unchanged,    X2X = Changed
    XX1 = 0 degrees, XX2 = 90 degrees, XX3 = 180 degrees of rotation

The response variable trigger is deciced depending on participant answer, either:
        001 for asnwering 'change' (the face is subjected to the thatcher-warp-effect)
        or
        002 for answering 'no_change' (the face is not subjected to the thatcher-warp-effect)


