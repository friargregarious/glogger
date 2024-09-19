# GSLogger: Greg's Simple Changelog Generator

A Python-based tool for generating changelogs in Markdown format.
created by: [Friar Greg Denyes](https://github.com/friargregarious)

## Features

* Automatically generates changelogs based on user input
* Supports multiple changelog entries
* Uses Markdown formatting for easy readability

## Usage & initialization

To use the changelog generator, simply run the ```chlog.py``` script or run it from the command prompt and follow the prompts.

```cmd
c:\myproject>glog
```

For collecting artifacts and building the changelog.md file, use the ```-c``` flag like so:

```cmd
c:\myproject>glog -c
```

*Note: runing from command prompt will be a future feature once the app packaging/building functionality is complete.*

Newly created changelog artifacts will be stored in ```ch-logs/``` directory as ```ch-logs/<date>.md``` files.

## Configuration

The tool uses a ```chlog.json``` file to store configuration data, including the application title, developer name, and developer link.

On first run, if this file and the configuration are not present, app will automatically begin asking for these details and save them to a newly created file.

*Note: future features includes a re-calibrate command to update and change these settings if user wants to.*

## Output

The generated changelog is stored in a file called ```changelog.md``` in the app's root directory.

## Contributing

If you'd like to contribute to the development of this tool, please fork the repository and submit a pull request with your changes.
