# Mario is Missing! Randomizer

## Introduction

This is a randomizer that will change elements of gameplay in Mario is Missing! for the Super Nintendo/Super Famicom. It makes a couple of changes to the game based on your preferences and you can share your seed values with others if you want to race or compare.

## Features

* Automatic or manual setting of initial seed values, which changes the location of items within the game
* The ability to enable a mode that flashes a Koopa carrying an item

### Upcoming features

* Automatic removal of content that is problematic

## Supported versions

* NTSC release (MD5: `2a2152976e503eaacd9815f44c262d73`)
* PAL release (MD5: `d5217f2137a4f4df63d83264a9a92bcc`)

To the best of my knowledge there are no other releases of this game. The above MD5 values are based on the hash value generated with the ROM headers themselves, so if you have a copy that doesn't match the above, do let me know or just find something that matches. The PAL and NTSC releases do not appear to have any real differences with respect to memory locations but I am treating them separate just in case.

## Requirements

* Python 3.7+

## Installation

Some technical knowledge is required to run this application as it is written as a command line tool.

### macOS / Linux

You should be able to use this right out of the box with your existing Python 3 installation provided you have kept your OS install up to date.

### Windows

There are two options to run this in Windows 10:

* Installing a WSL package via the Microsoft Store application. These [steps](https://docs.microsoft.com/en-us/windows/wsl/install-win10) will help you along in installing Debian or Ubuntu atop of your Windows installation.
* Installing [ActivePython](https://www.activestate.com/products/python/downloads/). This method is not recommended or supported as it has not been tested, but it is unlikely to fail based on how the tool has been written.

Once this is addressed, you can use the instructions below.

## Use

You can get help by running the following command:

`python3 main.py -h`

To quickly produce a new randomized ROM, you can use this example:

`python3 main.py -i MarioIsMissing.smc -o MarioIsMissing_New.smc`

If `MarioIsMissing_New.smc` already exists, it will be overwritten. The tool will not unpatch any changes you have made so don't make the output the same as your source ROM if you intend to reuse the tool or need to regenerate due to a bug.

If you have a seed value provided by someone else, you can use this example:

`python3 main.py -i MarioIsMissing.smc -o MarioIsMissing_New.smc --seed 08d2,31ab`

Seed values must be in the format similar to `af01,01af` and are not case sensitive. There are two values contained within and they're 16-bits each, meaning you can use `0001-ffff` for each. Some seeds could include `081d,3fff` or `11f7,981b`, but they must meet that format. You cannot use `0000` for either of the pair as the game will crash and the tool will reject it.

Any other options you wish to enable can be found by using the initial command.

## Bugs

Please report any bugs via the issue tracker in GitHub.

## Final remarks

Other than from the aforementioned PRNG project, some code is borrowed from [PySNES](https://github.com/JonnyWalker/PySNES). Many people have helped out with this project through providing technical assistance or just encouragement. This is my first time disassembling a Super Nintendo game so enjoy my weird hacks in order to achieve the outcome I wanted.

If you want to watch me speedrun or work on other things, check me out on Twitch:

[https://twitch.tv/KateLibC](https://twitch.tv/KateLibC)

You can also chat on Discord if you'd like too:

[https://discord.vulpine.dev](https://discord.vulpine.dev)