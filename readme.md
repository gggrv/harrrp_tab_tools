# [harrrp] Core

<p style="text-align:right;"><a href="https://gggrv.github.io/something/2022/03/22/devinfo-harrrp/">🏠 Project Homepage</a></p>

## What is this?

This repository contains critical "behind-the-scenes" part of project `harrrp` — convenient tools that allow anyone to easily extract meaningful intelligence from already existing `.yaml` harmonica tabs (for example estimate performance difficulty) and perform other operations.

This repository DOES NOT yet contain tools for creating new `.yaml` harmonica tabs from scratch.

## Installation

1. Clone the repository.
2. Install requirements `pip install -r requirements.txt`.

## Usage

This repository is useful for batch non-composing operations on already existing harmonica tabs. Therefore the first step requires the user to actually provide the paths to these already existing harmonica tabs.

### Define paths

Please create the plaintext file named `tab_folders.txt` at the root of this repository and write desired paths to it (one path per line). Example:
```
some/custom/path/tabs
c:\another\custom\path\tabs

d:\third\different\location\tabs
```

### Run some tool

After defining paths to at least one existing folder with harmonica tabs, `tool launchers` become usable.

Please choose the `autorun_*.py` file according to current goals, open it with any python code editor of choice and run it.

## Structure

### Overall

This project contains several parts that nicely fit together and allow to easily accommodate future changes while preserving past versions and functionality.

### Individual Parts

| Name | Description | How to Locate |
| --- | --- | --- |
| Some `tool` | Rather abstract data analysis tool that can be applied to any compatible user input, regardless of its origin or meaning.<br><sub>There can be many of them, they exist for different purposes.</sub> | Any file named `src/some_*_Columns`. |
| Some `tool launcher` | Wrapper code that allows the user to one-click apply the `tool` of choice to any `harrrp` harmonica tabs without headaches or low-level considerations.<br><sub>There can be many of them, they exist for usage convenience.</sub> | Any file named `autorun_*.py`. |
| Some `interface` to specific `tab version` | Actual low-level programmatic `interface` to some specific `harrrp` harmonica tab.<br><sub>There are many of them, they evolve according to user needs.</sub> | Any file named `src/format_*/Columns_Tab.py`. |
| The `interface chooser` | One convenient endpoint that automatically chooses the correct programmatic `interface` for any given harmonica tab, freeing the developer from any worries regarding "how to process this specific tab".<br><sub>There is only one.</sub> | The file named `src/some_TabFormat_Columns.py`. |

### How They Communicate

|  | Some `tool` | Some `interface` to specific `tab version` | The `interface chooser` | Some `tool launcher` |
| --- | --- | --- | --- | --- |
| Welcomes structural changes? | ❌<br><sub>Any functionality-adding changes are appended to the latest version. Any functionality-altering changes are not welcome and should be avoided as much as possible, because they may dramatically affect apps that rely on the output of this tool.</sub> | ✔️<br><sub>Any functionality-adding changes are appended to the latest version. Any functionality-altering changes are placed in the new version.</sub> | ❌<br><sub>Any functionality-adding changes are appended to the latest version. Any functionality-altering changes are not welcome and should be avoided as much as possible, because they may dramatically affect apps that rely on this code.</sub> | ✔️<br><sub>Must be as convenient as possible, usually calls appropriate methods from `interface chooser`, but in more complex cases can combine some `tool` with `interface chooser`.</sub> |
| Has to be compatible with... | No one. | <p>👈 Some `tool`.<br><sub>Efficiently use tool's methods.</sub></p><p>👉 The `interface chooser`.<br><sub>Provide some reserved endpoints to it.</sub></p> | No one. | <p>👈 Some `tool`.<br><sub>Efficiently use tool's methods.</sub></p><p>👈 The `interface chooser`.<br><sub>Efficiently use its methods.</sub></p> |

## Available Functionality

In this section the functionality of all available "some `tools`" and "some `tool launchers`" is listed.

| Tool | Description | How to Locate |
| --- | --- | --- |
| Estimate tab difficulty. | <ul><li>Analyze given input (that usually represents notes within some harmonica tab) and determine its actual real-life performance difficulty using sensible multifactor scoring system.</li><li>Calculate the most optimal default sorting order (easiest → hardest) based on the assumption that the player is capable of consistently producing single notes.</li></ul> | <p>The file named `src/some_Difficulty_Columns.py`.</p><p>The file named `autorun_IndexCsv.py`.</p> |
| Create convenient tab comparison table. | <ul><li>Provide quick overview of all harmonica tabs in specific user-defined root folder.</li><li>Allow applications to access critical metadata regarding harmonica tabs without actually parsing them. </li><li>Automatically calculate and save tab difficulty scores for future use.</li></ul> | <p>The file named `src/some_IndexCsv_Columns.py`.</p><p>The file named `autorun_IndexCsv.py`.</p> |
| Process `MIDI` attachments. | <ul><li>Embed externally-created timecodes into the actual harmonica tab so that the apps know which part of `.mid` to playback for any given line.</li><li>Temporarily convert `.mid` to simplified debug `.csv` with absolute timecodes so that app development becomes easier.</li><li>Force all `.mid` files to comply with the `MIDI Type 1` standard so that any application can reliably calculate correct timecodes.</li></ul> | <p>The file named `autorun_PasteTimecodes.py`.</p><p>The file named `src/some_MidiText_Columns.py`.</p><p>The file named `autorun_MidiCsv.py`.</p><p>The file named `autorun_MidiType1Force.py`.</p> |

## Supported Tab Versions

```
4.1.0: ok
```

## License

The actual licenses are available per-flie, please see the source code.  
Any files which contain data, unique to project harrrp, are subject to GPL v3.  
Any general files which contain data, not unique to project harrrp, are subject to BSD0.  
Any unmarked file is implied to be subject to either BSD0 or GPL v3, according to the statements above.
