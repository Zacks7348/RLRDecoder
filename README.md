# RLRDecoder - Rocket League Replay Decoder
This library is meant to be used to decode [Rocket League](https://www.rocketleague.com/) replay files.

The goal is to develop a python replay decoder library capable of decoding all replay attributes and perform CRC checks

# Installation

## Requirements
* [bitstring](https://pypi.python.org/pypi/bitstring)

## Setup
TODO

# Usage

## Getting Started
```python
from rlrdecoder import decode_replay

replay = decode_replay('REPLAY FILEPATH')
```

As of now RLRDecoder does not support decoding network data or performing CRC checks. These are planned features that will be released in the future.

## Working with decoded replays
```python

# To output the decoded data to JSON
# All keyword arguments are sent to json.dump()
replay.to_json('FILEPATH', indent=4)

# Create Replay object from JSON file
from rlrdecoder import replay_from_json
replay = replay_from_json('FILEPATH')

# Get all player stats
stats = replay.properties.player_stats

# Get stats of a specific player
stats = replay.properties.get_player_stats('PLAYER NAME')
```

----

# License
This project is published under the MIT License. I would appreciate it if you
credit/contact me if you released a project using this library

# References
I leaned heavily on https://github.com/nickbabcock/boxcars and https://github.com/Bakkes/CPPRP for understanding the replay encoding structure. 
Shoutout to [nickbabcock](https://github.com/nickbabcock) for explicitly documenting the replay encoding structure [here](https://github.com/nickbabcock/boxcars/blob/master/src/parser.rs)

