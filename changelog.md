# CHANGELOG: GSLOGGER

## [ ISSUES & FUTURE CHANGES ]

- 1 - future updates will be included under doc header, before versions details.
- 2 - need to package a new release as soon as output changelog is working

## VERSION: v0.2.69 | 2024-09-29 | BUILD: 122

### [ FIXED ]

- I thought i fixed serializing paths... guess i was wrong. i hope it takes this time.

## VERSION: v0.2.68 | 2024-09-29 | BUILD: 121

### [ REMOVED ]

- Got rid of find_file. it was only used in one spot anyway.

## VERSION: v0.2.67 | 2024-09-28 | BUILD: 120

### [ FIXED ]

- Find_file function was stuck in loop if it can't find file. bad when trying to initialize.

## VERSION: v0.2.66 | 2024-09-28 | BUILD: 119

### [ FIXED ]

- Fixed the scripts line in pyproject.toml so that it will now build a proper executable and be available from command line

## VERSION: v0.2.65 | 2024-09-28 | BUILD: 118

### [ ADDED ]

- First build to actually let me run from commandline

### [ FIXED ]

- Generate_changelog was pulling the current version number for all version entries. changed this back to reading the stored version numbers.

## VERSION: v0.2.63 | 2024-09-27 | BUILD: 116

### [ FIXED ]

- Collect_changelogs refused to delete old artifacts because i missed the pathlib issue from previous build.

## VERSION: v0.2.62 | 2024-09-27 | BUILD: 115

### [ FIXED ]

- Some errors appeared in new code. cleaned it up.
- Pathlib objects not seralizable with json. had to hunt down all the locations it was used.

## VERSION: v0.2.60 | 2024-09-27 | BUILD: 113

### [ CHANGED ]

- Rearranged code into extras.py, jin.py & version.py

### [ REMOVED ]

- Removed dependancies for jinja2 & toml

## VERSION: v0.2.58 | 2024-09-24 | BUILD: 111

### [ ADDED ]

- Now including future updates to standard artifact types. will not include these in details.

### [ CHANGED ]

- Artifacts now use .txt extension as they don't contain any markup formatting.

### [ FIXED ]

- New sort was throwing error because of invalid key in dict. my bad. manually replaced keys in json.

## VERSION: v0.2.43 | 2024-09-24 | BUILD: 96

### [ CHANGED ]

- Split collect_changelogs into collect & output. collect will now update the templates.json file and output will use templates.json to create changelod.md.

### [ FIXED ]

- Config save was blanking toml file instead of saving.
- Collect was appending new details to bottom of details, now it sorts details prior to saving.
- Previous sort was on date, new sort now on version.

## VERSION: v0.2.15 | 2024-09-20 | BUILD: 68

### [ CHANGED ]

- 2024-09-24-12-53
changed
split collect_changelogs into collect & output. collect will now update the templates.json file and output will use templates.json to create changelod.md.
gregory denyes <greg.denyes@gmail.com>

### [ FIXED ]

- 2024-09-24-12-54
fixed
config save was blanking toml file instead of saving.
gregory denyes <greg.denyes@gmail.com>
- 2024-09-24-13-01
fixed
collect was appending new details to bottom of details, now it sorts details prior to saving.
gregory denyes <greg.denyes@gmail.com>

## VERSION: v0.2.12 | 2024-09-20 | BUILD: 65

### [ CHANGED ]

- 2024-09-24-12-53
changed
split collect_changelogs into collect & output. collect will now update the templates.json file and output will use templates.json to create changelod.md.
gregory denyes <greg.denyes@gmail.com>

### [ FIXED ]

- 2024-09-24-12-54
fixed
config save was blanking toml file instead of saving.
gregory denyes <greg.denyes@gmail.com>

## VERSION: v0.2.3 | 2024-09-20 | BUILD: 56

### [ ADDED ]

- Included flags in commit msg request to educate user on semantic versioning. new feature version
- Added template check, the .md files don't get installed using pip for some reason. now it creates the files before jinja2 asks for them.

### [ CHANGED ]

- Moved __name__==__main__ lines into main() function for packaging purposes.

## VERSION: v0.1.2 | 2024-09-20 | BUILD: 36

### [ ADDED ]

- Now using pathlib, still need to replace some old os.path references.

## VERSION: v0.1.0 | 2024-09-19 | BUILD: 25

### [ ADDED ]

- Artifact collection confirmed.

### [ FIXED ]

- Templates finalized.
- Template rendering fixed. new feature version initiated.

## VERSION: v0.0.12 | 2024-09-19 | BUILD: 12

### [ ADDED ]

- Added changelog template generator

### [ CHANGED ]

- Updated template for changeloger artifacts
- New app name gslogger

### [ FIXED ]

- Config wasn't saving to file between runs.
- Added some input validation to create_artifact inputs


***This Changelog Maintained by [Greg's Simple Changelogger](https://github.com/friargregarious/glogger)***