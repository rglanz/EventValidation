# Event Validation Program

This GUI plays through 1-s epochs of a video, allowing the user to
discard unwanted events.

*Warning: This GUI is a work-in-progress and will be frequently updated.*

###### (Last updated 5.13.20)

## Installation

Open a conda prompt.

Change the directory to this folder.

Create the virtual environment by typing ```conda env create -f environment.yaml```

## Launch program

Activate the environment in a conda prompt by typing ```conda activate EventValidation```

Change the directory to this folder.

Type ```python startup.py```

## Typical use case

1. Open Video

2. Event Times
        
        Select a csv file with event times in seconds.
        
3. Time Series (Optional)

        If desired, load a csv file with the time-series data. Each
        entry should represent the value of the time-series at that
        particular frame.
        
        The time series will not be loaded if its length does not match
        the number of video frames.
        
4. Control video playback with the next, prev, and replay buttons.

5. Use the discard, undo, and save buttons to update the discard log file. 

        Upon loading an Event Times file, a new file called [video_file_name]_discard_log.csv
        is created (or loaded, if it exists already). Each event is stored as a 1 (accepted event)
        or 0 (discarded event).

## Hotkeys
Open video file (1)

Open event times file (2)

Open time series file (3)

Next event (right arrow)

Previous event (left arrow)

Replay event (r)

Discard event (d)

Undo discarded event (u)

Save discard log (s)

## Bugs

Almost certainly full of them. Let me know.
