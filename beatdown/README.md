# Beatdown 
A simple script that will create a MIDI tempo track from an audio file

## Introduction

Often times when producing a song the drummer will speed up (or slow down) a little during the recording. The "usual" way to handle this is to either:

- fix the drum tack to the grid - which can be tedious and often hurts the feel or swing.

- manually create tempo markers so that the grid lines up to the downbeats. This can be done manually (which is time consuming) or by using a tool like Beat Detective which is not very accurate.

Because the commercially available solutions for this problem don't do a very good job I decided to use a machine learning library (madmom) to solve this problem.

__Beatdown__ is a simple python script that will use a modern ML system to recognize the downdeats of a track (or complete/mixed song) and use them to create a tempo track that you can import into your DAW. 

This is useful if you want to create a tempo map from the session you are recording (by feeding a drum stem to the script) or if you want to remix a final song. Just add the generated MIDI file to a blank MIDI track in your project and most DAWs should be able to follow along.

## Installation ##

For now, you'll have to install all the requirements by hand.

    pip install madmom, midiutil, numpy

I'm working on compiled version to distribute, but the state of Python packagers is pretty awful!

## Usage

Usage is easy.

    python3 beatdown.py _audio file_

For example, the following command:

    python3 beatdown.py ~/music/mysong.mp3

will create a midi file named: _~/music/mysong.mp3.midi_