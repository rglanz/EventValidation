# Event Validation Program

Behavioral research requires observation. This GUI is designed to accelerate the pre-processing of behavioral data
by playing a video in an epoch-based framework. If you've generated time-stamps for the onset of behaviors-of-interest,
this GUI will play them back one at a time and allow you to adjust the time-stamps or discard events entirely.

*Warning: This GUI is a work-in-progress and will be frequently updated.*

###### (Last updated 5.24.20)

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
        
        Select a csv file with event times in seconds. (If you adjust the event times within the GUI, this file will
        be overwritten, so save a backup!)
        
3. Time Series (Optional)

        Load a csv file with the time-series data. Each
        entry should represent the value of the time-series at that
        particular frame.
        
        The time series will not be loaded if its length does not match
        the number of video frames.
        
4. Control video playback with the next, prev, and replay buttons.

5. Adjust the event time.
        
        Drag the dashed line at time-lag 0 to adjust the event time. Hold down Alt and drag the dashed line
        to add an event before or after the current event.
        
        Warning: These actions overwrite the selected 'Event Times.csv' file.

6. Use the discard button to update the discard log file. 

        Upon loading an Event Times file, a new file called [video_file_name]_discard_log.csv
        is created (or loaded, if it exists already). Each event is stored as a 1 (accepted event)
        or 0 (discarded event). This saves automatically.

## Hotkeys
Open video file (1)

Open event times file (2)

Open time series file (3)

Next event (right arrow)

Previous event (left arrow)

Replay event (r)

Discard event (d)

Add event (hold Alt + drag center line)

1.0x Speed (,)

0.50x Speed (.)

0.25x Speed (/)

## Bugs

Almost certainly full of them. Let me know.