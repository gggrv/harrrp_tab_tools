# [harrrp] Tab Format Specification

| Item | Description |
| ------------- | ------------- |
| What is this? | Critical part of project `harrrp`, the .yaml tab format specification. |
| What does it contain? | <ul><li>Python `interfaces` to all historical format versions, starting from minimum version `4.1.0`.</li><li>Convenient `launchers` for some frequently-used `tools` that rely on these `interfaces`.</li></ul> |
| What does it NOT contain? | <ul><li>Batch tab editor.</li><li>Tab creator.</li></ul> |
| Why does it NOT contain some items? | Because the items in question are abstract programmatic text-editing tools, which are not unique nor native to project harrrp --- they belong to a different project. |

## Installation

1. Clone the repository
2. Run `pip install -r requirements.txt`.

## Usage

Since the tools in this repository are targeted towards batch non-editing operations on already existing harmonica tabs, the first step requires the user to define the actual paths to these folders.

### Define paths

Paths to existing tab folders are defined using the `tab_folders.txt` file, located at the root of the project. The example contents could be as follows:
```
some/custom/path/tabs
c:\another\custom\path\tabs

d:\third\different\location\tabs
```

### Run some interface

After defining paths to at least one existing tab folder, the `launchers` become usable.

Please choose the `autorun_*.py` file according to current goals, open it with IDE of choice and run it.

## Structure

### Overall

The base project structure involves:

1. Some complex tools --- they are persistent across different format versions.
2. Some complex tool `launchers`.
3. Multiple minimalistic *version-specific interfaces*.
4. One automatic version-specific interface *chooser*.

Please see the comparison table below for more information:

|  | Some tool | Version-specific interface | Some tool `launcher` |
| ------------- | ------------- | ------------- |------------- |
| Welcomes changes | ❌ | ✔️| ✔️|
| Has to be compatible with | No one | 👈 Some tool | Version interface chooser `some_TabFormat_Columns.py` <sub>WIll be elaborated on below</sub> |
| Can automatically choose correct version-specific interface | ❌  | ❌ | ✔️|

### Some Tools

*Please note that not all available tools are documented in this readme file --- please see the actual code for more documentation and use cases.*

| Tool name | Purpose | How it is used |
| ------------- | ------------- | ------------- |
| `index.csv` creator | <ul><li>Provide quick overview of all the tabs in the user-defined folder.</li><li>Allow apps to access critical metadata regarding harmonica tabs without actually parsing them. </li><li>Save pre-calculated tab difficulty scores for future use.</li></ul> | Please see `autorun_IndexCsv.py` |
| Difficulty estimator | <ul><li>Analyze the harmonica tabs and determine their actual real-life performance difficulty using sensible multifactor scoring system.</li><li>Calculate the most optimal sorting order (easiest -> hardest).</li></ul> | Please see `autorun_IndexCsv.py` |
| Version interface chooser | <ul><li>Parse the given harmonica tab and choose the correct python interface for it according to the actual parsed tab format version.</li></ul> | Please see `some_TabFormat_Columns.py` |

### Version-specific interfaces

As was noted in the beginning of this document, this repository contains all historical version-specific interfaces for the harmonica tabs, written in the .yaml format, **starting from tab format version 4.1.0**.

Each fully-functional version-specific interface is represented by the `Columns_Tab.py` file in the appropriately-named folder within the `src` directory.
