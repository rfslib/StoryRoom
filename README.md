# StoryRoom

This repository contains the code for an FSC Story Room.

Note: the file simpleobsws.py needs to be manually added, since a pip install gets a newer version that uses different class names. It can be found at: https://github.com/IRLToolkit/simpleobsws/tree/simpleobsws-4.x

## Purpose

The Story Room is a sound-proofed room where people can record a one-hour video. The format usually involves an interviewee who is asked various questions about his or her life by an interviewer (who is off-camera).

## Technical Componenets

* main recording computer with:
    * PTZ camera
    * ceiling-mounted microphones feeding into a automixer (Rane)
    * a small touchscreen monitor for control
    * a larger (current 22") monitor for viewing by the interviewee
    * Windows 10 as the OS
    * OBS Studio to do the recording
    * OBS websockets as the interface
    * Python for the control program
* backup recording camera with:
    * fixed camera (webcam) with embedded microphone
    * Windows 10
    * OBS Studio
    * OBS websockets

Note that OBS Studio allows internal scripting with Python, but that it was substantially more complex to do the controlling and on-screen display, so the control program was changed to be stand-alone (and also use a supported, current version of Python).
