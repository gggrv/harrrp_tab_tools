# [harrrp] Core

| Item | Description |
| ------------- | ------------- |
| What is this? | Critical part of project `harrrp`, several interfaces and tools for harmonica tabs in `.yaml` format. |
| What does it contain? <sub>not a complete list, please see further sections</sub> | <ul><li>Base python `interfaces` to all historical `harrrp` harmonica tab versions, starting from minimum version `4.1.0`.</li><li>Difficulty estimator.</li><li>`index.csv` creator.</li></ul> |
| What does it NOT contain? | <ul><li>Batch tab editor.</li><li>Tab creator.</li></ul> |
| Why does it NOT contain some items? | Because the items in question are abstract programmatic text-editing tools, which are not unique nor native to project harrrp — they belong to a different project. |

## Installation

1. Clone the repository
2. Run `pip install -r requirements.txt`.

## Usage

Since the tools in this repository are targeted towards batch non-editing operations on already existing harmonica tabs, the first step requires the user to define the paths to any relevant folders.

### Define paths

Paths to existing tab folders are defined using the `tab_folders.txt` file, located at the root of the project. The example contents could be as follows:
```
some/custom/path/tabs
c:\another\custom\path\tabs

d:\third\different\location\tabs
```

### Run some tool

After defining paths to at least one existing folder with harmonica tabs, `some tool launchers` become usable.

Please choose the `autorun_*.py` file according to current goals, open it with IDE of choice and run it.

## Structure

### Overall

The base project structure involves:

1. Some complex `tools` — they are persistent across different format versions.
2. Some complex tool `launchers`, named `autorun_*.py`.
3. Multiple minimalistic version-specific `interfaces`.
4. One automatic version-specific `interface chooser`.

Please see the comparison table below for more information:

|  | Some `tool` | Version-specific `interface` | Some tool `launcher` |
| ------------- | ------------- | ------------- |------------- |
| Welcomes structural changes | ❌ | ✔️<sup>any changes will be available in the form of a new version-specific interface</sup>| ✔️|
| Has to be compatible with | No one | 👈 Some tool | The `interface chooser`, aka `some_TabFormat_Columns.py` <sub>wIll be elaborated on below</sub> |
| Can automatically choose correct version-specific interface | ❌  | ❌ | ✔️|

### Some Tools

*Please note that not all available tools are documented in this readme file — please see the actual code for more documentation and use cases.*

| Tool name | Purpose | How it is used |
| ------------- | ------------- | ------------- |
| `index.csv` creator | <ul><li>Provide quick overview of all harmonica tabs in specific user-defined root folder.</li><li>Allow applications to access critical metadata regarding harmonica tabs without actually parsing them. </li><li>Automatically calculate and save tab difficulty scores for future use.</li></ul> | Please see `autorun_IndexCsv.py` |
| Difficulty estimator | <ul><li>Analyze given harmonica tab and determine its actual real-life performance difficulty using sensible multifactor scoring system.</li><li>Calculate the most optimal sorting order (easiest → hardest).</li></ul> | Please see `src/some_Difficulty_Columns.py` |
| Version-specific `interface chooser` | <ul><li>Parse given harmonica tab and choose the correct python interface for it.</li></ul> | Please see `src/some_TabFormat_Columns.py` |

### Version-specific interfaces

As was noted in the beginning of this document, this repository contains all historical version-specific `interfaces` for harmonica tabs, written in the .yaml format, **starting from tab format version `4.1.0`**.

Each fully-functional version-specific `interface` is represented by the `Columns_Tab.py` file in the appropriately-named folder within the `src` directory.

## License

The actual licenses are available per-flie, please see the source code.  
Any files which contain data, unique to project harrrp, are subject to GPL v3.  
Any general files which contain data, not unique to project harrrp, are subject to BSD0.  
Any unmarked file is implied to be subject to either BSD0 ot GPL v3, according to the statements above.
