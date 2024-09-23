# Changelog for Application: GSLogger

Version: 0.2.3 | 2024-09-20 | Build: 20

CONTRIBUTORS: Gregory Denyes,me

## [ ADDED ]

   * included flags in commit msg request to educate user on semantic versioning. new feature version
   * added template check, the .md files don't get installed using pip for some reason. now it creates the files before jinja2 asks for them.

## [ CHANGED ]
   * moved __name__==__main__ lines into main() function for packaging purposes.

# Changelog for Application: GSLogger

Version: 0.1.2 | 2024-09-20 | Build: 16

CONTRIBUTORS: Gregory Denyes

## [ ADDED ]

   * now using pathlib, still need to replace some old os.path references

# Changelog for Application: Glogger

Version: 0.1.0 | 2024-09-19 | Build: 15

CONTRIBUTORS: Gregory Denyes

## [ ADDED ]

   * Artifact collection confirmed

## [ FIXED ]

   * Templates finalized
   * Template rendering fixed. new feature version initiated.

# Changelog for Application: Glogger

Version: 0.0.12 | 2024-09-19 | Build: 12

CONTRIBUTORS: Gregory Denyes

## [ ADDED ]

   * Added changelog template generator

## [ CHANGED ]

   * Updated template for changeloger artifacts
   * New app name glogger

## [ FIXED ]

   * Config wasn't saving to file between runs.
   * Added some input validation to create_artifact inputs
