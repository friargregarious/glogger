# Changelog: GSLogger
## [ ISSUES & FUTURE CHANGES ]
* 1 - Future updates will be included under doc header, before versions details.
* 2 - Need to package a new release as soon as output changelog is working
## Version: 0.2.58 | 2024-09-24 | Build: 111

CONTRIBUTORS: Gregory Denyes <Greg.Denyes@gmail.com>
### [ ADDED ]
* Now including future updates to standard artifact types. will not include these in details.
### [ CHANGED ]
* Artifacts now use .txt extension as they don't contain any markup formatting.
### [ FIXED ]
* New sort was throwing error because of invalid key in dict. my bad. manually replaced keys in json.
## Version: 0.2.43 | 2024-09-24 | Build: 96

CONTRIBUTORS: Gregory Denyes <Greg.Denyes@gmail.com>
### [ CHANGED ]
* Split collect_changelogs into collect & output. collect will now update the templates.json file and output will use templates.json to create changelod.md.
### [ FIXED ]
* Config save was blanking toml file instead of saving.
* Collect was appending new details to bottom of details, now it sorts details prior to saving.
* Previous sort was on date, new sort now on version.
## Version: 0.2.3 | 2024-09-20 | Build: 56

CONTRIBUTORS: ['Gregory Denyes <Greg.Denyes@gmail.com>']
### [ ADDED ]
* included flags in commit msg request to educate user on semantic versioning. new feature version
* added template check, the .md files don't get installed using pip for some reason. now it creates the files before jinja2 asks for them.
### [ CHANGED ]
* moved __name__==__main__ lines into main() function for packaging purposes.
## Version: 0.2.15 | 2024-09-20 | Build: 68

CONTRIBUTORS: Gregory Denyes <Greg.Denyes@gmail.com>
### [ CHANGED ]
* 2024-09-24-12-53
changed
split collect_changelogs into collect & output. collect will now update the templates.json file and output will use templates.json to create changelod.md.
gregory denyes <greg.denyes@gmail.com>
### [ FIXED ]
* 2024-09-24-12-54
fixed
config save was blanking toml file instead of saving.
gregory denyes <greg.denyes@gmail.com>
* 2024-09-24-13-01
fixed
collect was appending new details to bottom of details, now it sorts details prior to saving.
gregory denyes <greg.denyes@gmail.com>
## Version: 0.2.12 | 2024-09-20 | Build: 65

CONTRIBUTORS: Gregory Denyes <Greg.Denyes@gmail.com>
### [ CHANGED ]
* 2024-09-24-12-53
changed
split collect_changelogs into collect & output. collect will now update the templates.json file and output will use templates.json to create changelod.md.
gregory denyes <greg.denyes@gmail.com>
### [ FIXED ]
* 2024-09-24-12-54
fixed
config save was blanking toml file instead of saving.
gregory denyes <greg.denyes@gmail.com>
## Version: 0.1.2 | 2024-09-20 | Build: 36

CONTRIBUTORS: ['Gregory Denyes <Greg.Denyes@gmail.com>']
### [ ADDED ]
* now using pathlib, still need to replace some old os.path references.
## Version: 0.1.0 | 2024-09-19 | Build: 25

CONTRIBUTORS: ['Gregory Denyes <Greg.Denyes@gmail.com>']
### [ ADDED ]
* Artifact collection confirmed.
### [ FIXED ]
* Templates finalized.
* Template rendering fixed. new feature version initiated.
## Version: 0.0.12 | 2024-09-19 | Build: 12

CONTRIBUTORS: ['Gregory Denyes <Greg.Denyes@gmail.com>']
### [ ADDED ]
* Added changelog template generator
### [ CHANGED ]
* Updated template for changeloger artifacts
* New app name gslogger
### [ FIXED ]
* Config wasn't saving to file between runs.
* Added some input validation to create_artifact inputs
--- This Changelog Maintained by (Greg's Simple Changelogger)['https://github.com/friargregarious/glogger'] ---