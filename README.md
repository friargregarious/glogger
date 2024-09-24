# GSLogger: Greg's Simple Changelog Generator

A Python-based tool for generating changelogs in Markdown format.
created by: [Friar Greg Denyes](https://github.com/friargregarious)
Licensed under: Apache License Version 2.0
Can be found at
PyPi: https://pypi.org/project/GSLogger/0.1.0/ 
and 
Github: https://github.com/friargregarious/glogger

## Features

* Automatically generates changelogs based on user input
* Supports multiple changelog entries
* Uses Markdown formatting for easy readability

## Usage & initialization

### create logs

To use the changelog generator run it from the command line and follow the prompts.

```cmd
c:\myproject>glog
```

If this is the first run, here is where you will be asked details about the app and the developer/contributor. Newly created changelog artifacts will be stored in ```c:\myproject\ch-logs\``` directory as ```c:\myproject\ch-logs\<date>.txt``` files. These can be opened and edited any time before being collected.

*example:*

```txt
2024-09-24-18-09
ADDED
this is an example of a changelog artifact message for the updated README.md
Gregory Denyes <Greg.Denyes@gmail.com>
```

### Collecting logs & Versioning

For collecting artifacts and incrementing the current version, use the ```-c``` flag like so:

```cmd
c:\myproject>glog -c
```

Any artifacts containing ```--r``` or ```--f``` will force increment **Major Release** or **Feature** versioning psuedo-Semantically. All existing artifacts will be processed and stored in ```c:\myproject\ch-logs\log_store.json```.

### Generating Changelog.md

Generate the changelog.md from the ```c:\myproject\ch-logs\log_store.json``` file by using the ```-g``` flag like so:

```cmd
c:\myproject>glog -g
```

Version details will be sorted by version, and all parts of the final Changelog will be output to ```c:\myproject\changelog.md```

## Configuration

The tool uses a ```glog.toml``` file to store configuration data, including the application title, developer name, and developer link.

On first run, if this file and the configuration are not present, app will automatically begin asking for these details and save them to a newly created file.

*example:*

```toml
[app]
app_title = "GSLogger"
version_number = [ 0, 2, 58,]
build_number = 111
f_count = 3
atf_pattern = ".txt"

[dev]
developer = "Gregory Denyes"
dev_email = "Greg.Denyes@gmail.com"
dev_link = "https://github.com/friargregarious"
```

*Note: future features includes a re-calibrate command to update and change these settings if user wants to.*

## Output

The generated changelog is stored in a file called ```changelog.md``` in the app's root directory.

## Contributing

If you'd like to contribute to the development of this tool, please fork the repository and submit a pull request with your changes.
