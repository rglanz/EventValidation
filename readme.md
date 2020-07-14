# Event Validation Program

Behavioral research requires observation. This GUI is designed to efficiently validate blindly-generated
events of interest in an epoch-based framework. If you've generated time stamps for the onset of behaviors-of-interest,
this GUI will play them back one at a time and allow you to make adjustments to time stamps, or discard them entirely.

![GUI](https://github.com/rglanz/EventValidation/blob/assets/GUI_screen.png?raw=true)

###### (Last updated 7.14.20)

## Installation

Open a conda prompt.

Change the directory to this folder.

Create the virtual environment by typing ```conda env create -f environment.yaml```

## Launch program

Activate the environment in a conda prompt by typing ```conda activate EventValidation```

Change the directory to this folder.

Type ```python startup.py```

## Typical use case

1. Load Video

2. Event Times
        
        Select a csv file with event times in seconds.
        
3. Time Series (Optional)

        Load a csv file with the time-series data. Each
        entry should represent the value of the time-series at that
        particular frame.
        
        The time-series will not be loaded if its length does not match
        the number of video frames.
        
        To adjust the timing of events and add new events, a time-series must be loaded.
        
4. Control video playback with the next, prev, and replay buttons.

5. Adjust the events.
        
        To adjust the event onset time, drag the dashed line at time-lag 0 to the desired position. To add a new event,
        hold down Alt and drag the dashed line to a new position.

6. Use the discard/flag button to update the output file.

        Upon loading an Event Times file, two new files named [video_file_name]_output.pkl and 
        [video_file_name]_output.csv are created (or loaded, if they exist already).
        
        The output file contains the original and adjusted (if applicable) event times, whether the event has been
        discarded (1) or not (0), whether the event has been flagged (1) or not (0), and the last event viewed
        (for picking up where you left off).
        
        If you added an event, it will have an original time entry of 'nan'.

## Hotkeys
Open video file (1)

Open event times file (2)

Open time series file (3)

Next event (right arrow)

Previous event (left arrow)

Replay event (r)

Discard event (d)

Flag event (f)

Add event (hold Alt + drag center line)

1.0x Speed (,)

0.50x Speed (.)

0.25x Speed (/)

## Bugs

Almost certainly full of them. Let me know.