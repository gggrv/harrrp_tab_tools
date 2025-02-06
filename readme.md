# [harrrp] Core

| Item | Description |
| ------------- | ------------- |
| What is this? | Critical part of project `harrrp`, several `python` interfaces and tools for `.yaml` harmonica tabs. |
| What does it contain?<br><sub>Not a complete list, please see further sections.</sub> | <ul><li>Python `interfaces` to all historical `harrrp` `harmonica tab schema versions`, starting from minimum version `4.1.0`.</li><li>Tab difficulty estimator.</li><li>`index.csv` creator.</li></ul> |
| What does it NOT contain? | <ul><li>Batch tab editor.</li><li>Tab creator.</li></ul> |
| Why does it NOT contain some items? | Because the items in question are abstract programmatic text-editing tools, which are not unique nor native to project harrrp — they belong to a different project. |

## Installation

1. Clone the repository.
2. Install requirements `pip install -r requirements.txt`.

## Usage

Since the tools in this repository are targeted towards batch non-editing operations on already existing harmonica tabs, the first step requires the user to actually provide the paths to his already existing harmonica tabs.

### Define paths

Paths to existing harmonica tabs are defined using the `tab_folders.txt` file, located at the root of the project. The example contents could be as follows:
```
some/custom/path/tabs
c:\another\custom\path\tabs

d:\third\different\location\tabs
```

### Run some tool

After defining paths to at least one existing folder with harmonica tabs, `tool launchers` become usable.

Please choose the `autorun_*.py` file according to current goals, open it with IDE of choice and run it.

## Structure

### Overall

The project contains several parts that nicely fit together and allow to easily accomodate future changes while preserving past versions and functionality.

### Individual Parts

| Name | Description | How to Locate |
| --- | --- | --- |
| Some `tool` | Rather abstract data analysis tool that can be applied to any compatible user input, regardless of its origin or meaning.<br><sub>There can be many of them, they exist for different purposes.</sub> | Any file named `src/some_*_Columns`. |
| Some `tool launcher` | Wapper code that allows the user to one-click apply the `tool` of choice to any `harrrp` harmonica tabs without headaches or low-level considerations.<br><sub>There can be many of them, they exist for usage convenience.</sub> | Any file named `autorun_*.py`. |
| Some `interface` to specific `harmonica tab schema version` | Actual low-level programmatic `interface` to some specific `harrrp` harmonica tab.<br><sub>There are many of them, they evolve according to user needs.</sub> | Any file named `src/format_*/Columns_Tab.py`. |
| The `interface chooser` | One convenient endpoint that automatically chooses the correct programmatic `interface` for any given harmonica tab, freeing the developer from any worries regarding "how to process this specific tab".<br><sub>There is only one.</sub> | The file named `src/some_TabFormat_Columns.py`. |

### How They Communicate

|  | Some `tool` | Some `interface` to specific `harmonica tab schema version` | The `interface chooser` | Some `tool launcher` |
| --- | --- | --- | --- | --- |
| Welcomes structural changes? | ❌<br><sub>Any functionality-adding changes are appended to the latest version. Any functionality-altering changes are not welcome and should be avoided as much as possible, because they may dramatically affect apps that rely on the output of this tool.</sub> | ✔️<br><sub>Any functionality-adding changes are appended to the latest version. Any functionality-altering changes are placed in the new version.</sub> | ❌<br><sub>Any functionality-adding changes are appended to the latest version. Any functionality-altering changes are not welcome and should be avoided as much as possible, because they may dramatically affect apps that rely on this code.</sub> | ✔️<br><sub>Must be as convenient as possible, usually calls appropriate methods from `interface chooser`, but in more complex cases can combine some `tool` with `interface chooser`.</sub> |
| Has to be compatible with... | No one. | <p>👈 Some `tool`.<br><sub>Efficiently use tool's methods.</sub></p><p>👉 The `interface chooser`.<br><sub>Provide some reserved endpoints to it.</sub></p> | No one. | <p>👈 Some `tool`.<br><sub>Efficiently use tool's methods.</sub></p><p>👈 The `interface chooser`.<br><sub>Efficiently use its methods.</sub></p> |

## Available Functionality

In this section the functionality of all available "some `tools`" and "some `tool launchers`" is listed.

| Tool | Description | How to Locate |
| --- | --- | --- |
| Estimate tab difficulty. | <ul><li>Analyze given input (that usually represents notes within some harmonica tab) and determine its actual real-life performance difficulty using sensible multifactor scoring system.</li><li>Calculate the most optimal default sorting order (easiest → hardest) based on the assumption that the player is capable of consistently producing single notes.</li></ul> | <p>The file named `src/some_Difficulty_Columns.py`.</p><p>The file named `autorun_IndexCsv.py`.</p> |
| Create convenient tab comparison table. | <ul><li>Provide quick overview of all harmonica tabs in specific user-defined root folder.</li><li>Allow applications to access critical metadata regarding harmonica tabs without actually parsing them. </li><li>Automatically calculate and save tab difficulty scores for future use.</li></ul> | <p>The file named `src/some_IndexCsv_Columns.py`.</p><p>The file named `autorun_IndexCsv.py`.</p> |
| Process `.midi` attachments. | <ul><li>Embed externally-created timecodes into the actual harmonica tab so that the apps know which part of `.midi` to playback for any given line.</li><li>Temporarily convert `.midi` data to simplified debug `.csv` with absolute timecodes so that app development becomes easier.</li><li>Force all `.midi` files to comply with the `MIDI Type 1` standard so that any application can reliably calculate correct timecodes.</li></ul> | <p>The file named `src/some_MidiText_Columns.py`.</p><p>The file named `autorun_MidiCsv.py`.</p><p>The file named `autorun_MidiType1Force.py`.</p><p>The file named `autorun_PasteTimecodes.py`.</p> |

## Available Interfaces to Specific Schema Versions

```
versions:
  4.1.0: ok
```

## License

The actual licenses are available per-flie, please see the source code.  
Any files which contain data, unique to project harrrp, are subject to GPL v3.  
Any general files which contain data, not unique to project harrrp, are subject to BSD0.  
Any unmarked file is implied to be subject to either BSD0 or GPL v3, according to the statements above.
