# GSLogger: Greg's Simple Changelog Generator

- A Python-based tool for generating changelogs in Markdown format.
- created by: [Friar Greg Denyes](https://github.com/friargregarious)
- Licensed under: Apache License Version 2.0

- app can be found at
    - PyPi: https://pypi.org/project/GSLogger/0.1.0/ 
    - Github: https://github.com/friargregarious/glogger

## Urls

- [Bug Reports / Issues](https://github.com/friargregarious/glogger/issues) : https://github.com/friargregarious/glogger/issues
- [Funding / Buy me a coffee!](https://paypal.me/friargreg?country.x=CA&locale.x=en_US) : https://paypal.me/friargreg
- [Say Hi or Thanks!](https://mastodon.social/@gregarious) : https://mastodon.social/@gregarious
- [Source Code](https://github.com/friargregarious/glogger) : https://github.com/friargregarious/glogger

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

Any artifacts containing ```--r``` or ```--f``` will force increment **Major Release** or **Feature** versioning psuedo-Semantically. All existing artifacts will be processed and stored in ```~myproject\ch-logs\log_store.json```.

### Generating Changelog.md

Generate the changelog.md from the ```~myproject\ch-logs\log_store.json``` file by using the ```-g``` flag like so:

```cmd
c:\myproject>glog -g
```

Version details will be sorted by version, and all parts of the final Changelog will be output to ```~myproject\changelog.md```

## Configuration

On first run, if this file and the configuration are not present, app will automatically begin asking for these details and save them to a newly created file. The tool uses a ```glog.json``` file to store the configuration:

```json
{
    "CHTYPES": [
        "FUTURE UPDATES",
        "ADDED",
        "CHANGED",
        "REMOVED",
        "FIXED",
        "SECURITY"
    ],
    "app": {
        "app_title": "GSLogger",
        "atf_pattern": ".txt",
        "build_number": 123,
        "f_count": 3,
        "version_number": [
            0,
            2,
            70
        ]
    },

```

This section contains your name and email for proper labelling of contributors to the changelog.
when first initiating the app, you will be asked to either allow the app to pull from your git profile,
or enter it manually.

```json
"dev": {
        "dev_email": "Greg.Denyes@gmail.com",
        "dev_link": "https://github.com/friargregarious",
        "developer": "Gregory Denyes"
    },
```

This section contains full paths to the files & folders that will be used by this tool.

```json
    "paths": {
        "CWD": "",
        "DIR_OUTPUT": "",
        "FILE_CONFIG": "",
        "FILE_LOG": "",
        "FILE_OUTPUT": ""
    }
}
```

*Note: future features includes a re-calibrate command to update and change these settings if user wants to.*

## Output

The generated changelog is stored in a file called ```changelog.md``` in the app's root directory.

## Contributing

If you'd like to contribute to the development of this tool, please fork the repository and submit a pull request with your changes.
