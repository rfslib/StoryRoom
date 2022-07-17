# StoryRoom

This repository contains the code for the Story Room at the Riverton FamilySearch Library.

Note: the file simpleobsws.py needs to be manually added, since a pip install gets a newer version that uses different class names. It can be found at: https://github.com/IRLToolkit/simpleobsws/tree/simpleobsws-4.x

## Purpose

The Story Room is a sound-proofed room where people can record a one-hour video. The format usually involved an interviewee who is asked various questions about his or her life by an interviewer.

## Technical Componenets

* PTZ camera
* ceiling-mounted microphones feeding into a automixer (Rane)
* computer
* Two monitors (one for the projector/monitor, one for control)
* Windows 10 as the OS
* OBS Studio to do the recording
* OBS websockets
* Python as the controlling program

Note that OBS Studio allows internal scripting with Python, but that it was substantially more complex to do the controlling and on-screen display.
