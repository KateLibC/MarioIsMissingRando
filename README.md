# Mario is Missing! Randomizer

## Introduction

This is a randomizer that will change elements of gameplay in Mario is Missing! for the Super Nintendo/Super Famicom.

Currently, this only changes the initial PRNG seed values and alters them so they change item locations. If you're curious about how the PRNG works, you should check out the [Mario is Missing PRNG Project](https://github.com/KateLibC/pyMarioIsMissing) which should give you an idea of how items are distributed. We only have to change two values in order to affect the PRNG throughout the game.

Next major change anticipated is changing the level order for each dungeon over in the game overall. The reverse engineering of the game is an ongoing project of mine so this is forthcoming.

## Supported versions

* NTSC release (MD5: `2a2152976e503eaacd9815f44c262d73`)
* PAL release (MD5: `d5217f2137a4f4df63d83264a9a92bcc`)

These should be the only releases for Mario is Missing in existence. If there are any copies out there, please provide me with details about them. We need to know the location of where the instructions `A9 9A 11` and `A9 84 0E` are in ROM in order to change the initial seed.

## Requirements

* Python 3.7+

## Use

From a command line, you can just issue the following command:

`python3 main.py MarioIsMissing.Original.sfc MarioIsMissing.New.sfc`

Adjust to your liking of course. Make sure to not use the same file name as the original otherwise it will overwrite it.

## Remarks

Other than from the aforementioned PRNG project, some code is borrowed from [PySNES](https://github.com/JonnyWalker/PySNES).