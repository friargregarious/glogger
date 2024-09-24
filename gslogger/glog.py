import os
import datetime
import argparse
import json
from jinja2 import Template
import pathlib

try:
    # if python version >= 3.11
    import tomllib as tom
except ModuleNotFoundError:
    import tomli as tom

PATH = pathlib.Path(__file__).parent.resolve()



# Get the current date and time
def date(reporting=None)->str:
    """
    Returns the current date and time as a string in the format "YYYY-MM-DD-HH-MM"

    :return: A string representing the current date and time
    """
    if reporting is not None:
        return datetime.datetime.now().strftime("%Y-%m-%d")
    return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")

def save_config(data:json)->bool:
    """
    Saves the configuration to a file named "glog.json".

    :param data: The configuration data to be saved
    :return: True if the save is successful, False otherwise
    """
    try:
        with open(PATH / "glog.json", "w") as f:
            json.dump(data, f, indent=3)
        return True
    
    except Exception as e:
        print(f"Error saving glog.json: {e}")
        return False

def get_template_files(template_folder):
    """
    Retrieves the template files, creating them if they do not exist.

    :param template_folder: The folder where the template files are located
    :return: A tuple containing the header and sections template text
    """
    # template header ############
    if not os.path.exists(template_folder / "template.md"):
        TEMPLATE_INTRO = "\n---\n# {{ title }}\n\nVersion: {{ version_number }} | {{ date }} | Build: {{ build_number }}\n\nCONTRIBUTORS: {{ contributors }}\n\n"
        print("Changelog template.md not found. Creating file.")

        with open(template_folder / "template_sections.md", "w") as f:
            f.write(TEMPLATE_INTRO)

    with open(template_folder / "template.md", "r") as f:
        header = f.read()

    # template sections ###########
    if not os.path.exists(template_folder / "template_section.md"):
        TEMPLATE_SECTIONS = "\n## [ {{ artifact_type }} ]\n\n{% for artifact in artifact_list %}   * {{ artifact }}\n{% endfor %}\n\n"
        print("Changelog template_sections.md not found. Creating file.")
        
        with open(template_folder / "template_section.md", "w") as f:
            f.write(TEMPLATE_SECTIONS)

    with open(template_folder / "template_sections.md", "r") as f:
        sections = f.read()
    
    return header, sections


# Constants and templates ################################################
CHTYPES = ["ADDED", "CHANGED", "DELETED", "REMOVED", "FIXED", "SECURITY"]

# get the current working directory
PATH = pathlib.Path.cwd()

# initialize local data for GLogger if not present
OUTPUT_FOLDER = PATH / "ch-logs"  # Set the output folder

# Create the output folder if it doesn't exist
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

try:
    # Load the JSON data
    with open(PATH / "glog.json", "r") as f:
        data = json.load(f)    
except:
    # or Initialize the JSON data
    data = {"build_number": 0, "version_number": [0, 0, 0]}  

# get app_title from config, initialize if not present
if "app_title" not in data:
    app_title = input("What is the name for this application?\n> ")
    data["app_title"] = app_title
    
else:
    app_title = data["app_title"]

# get developer from config, initialize if not present
if "developer" not in data:
    developer = input("Who is the developer?\n> ")
    data["developer"] = developer
else:
    developer = data["developer"]

# get developer's link from config, initialize if not present
if "dev_link" not in data:
    dev_link = input("What is the developer's link?\n> ")
    data["dev_link"] = dev_link
else:
    dev_link = data["dev_link"]
    
# refresh or backup the glog.json configuration
save_config(data)

chlog_title = f"# Changelog for {app_title}\n\n"
chlog_footer = f"# **GLogger created & maintained by:** [{developer}]({dev_link})"
anchor = "\n\n<!--  NEW CHANGES   /-->\n\n"

changelog_file = PATH / "changelog.md" # Set the changelog file

if not os.path.exists(changelog_file):
    with open(changelog_file, "w") as f:
        f.write(chlog_title)
        f.write(anchor)
        f.write(chlog_footer)

def create_artifact():
    os.system("cls")

    # get the changelog type
    for i, a in enumerate(CHTYPES):
        print(f"{i+1}. {a}")
        
    selection = int(input(f"Enter the log type: \n> ").strip())
    if selection > len(CHTYPES) or selection < 1:
        print("Invalid selection, exiting without changes.")
        exit(1)
    artifact_type = CHTYPES[selection - 1]

    # Get the commit message from the user
    artifact_message = input(f"Enter the commit message (include --r or --f to initiate semantic versioning): \n{artifact_type}> ".strip())
    if artifact_message == "":
        print("Empty commit message, exiting without changes.")
        exit(1)

    # Check for minimum length
    if len(artifact_message) < 10:
        raise ValueError("Entry must be at least 10 characters long")

    # Create the changelog file name
    artifact_file = f"{OUTPUT_FOLDER}/{date()}-{artifact_type}.md"

    # Create the changelog file
    try:
        with open(artifact_file, "w") as f:
            f.write(date() + "\n")
            f.write(artifact_type + "\n")
            f.write(artifact_message + "\n")
            f.write(data["developer"] + "\n")

        print(f"Changelog Artifact created: {artifact_file}")
        
    except Exception as e:
        print(f"Error creating Artifact: [{artifact_file}]\n{e}")


def semantic_versioning(build, version, content):
    build += 1

    if "--r" in content.lower():
        version[0] += 1
        version[1] = 0
        version[2] = 0
    
    elif "--f" in content.lower():
        version[1] += 1
        version[2] = 0
    
    else:
        # new fix version
        version[2] += 1
    
    return build, version
    

def collect_changelogs(data):

    # Get the current build and version numbers
    build_number:int = data["build_number"] # int
    version_number:list = data["version_number"] # [0, 0, 0]

    # Get the list of changelog files
    changelog_files = [f for f in os.listdir(OUTPUT_FOLDER) if f.endswith(".md")]

    if len(changelog_files) == 0:
        print("No changelog files found. Exiting without changes.")
        exit(0)

    # Sort the changelog files by date
    # changelog_files.sort(key=lambda f: datetime.datetime.strptime(f.split("-")[1].split(".")[0], "%Y-%m-%d-%H-%M"))
    changelog_files.sort()

    # # Create the new changelog content
    # with open(changelog_file, "r") as f:
    #     old_changelog_content = "\n" + f.read()

    context = {}
    changes = {x.upper(): [] for x in CHTYPES}
    contributors = set()
    
    # Iterate over the sorted changelog files
    for file in changelog_files:
        # Read the file content
        with open(os.path.join(OUTPUT_FOLDER, file), "r") as f:
            content = f.read()
        
        _, a_type, a_msg, a_dev = content.splitlines()

        build_number, version_number = semantic_versioning(build_number, version_number, content)
        replaced_content = content.replace("--f", "new feature version").replace("--r", "new release version")
        
        changes[a_type.upper()].append(replaced_content.strip().capitalize())
        contributors.add(a_dev.strip()) # add this dev to the set of contributors

    # updatate the changelog json
    data["build_number"] = build_number
    data["version_number"] = version_number

    save_config(data)
    
    # Check for template files, they might not get installed for some reason
    part1, part2 = get_template_files(PATH)
            
    try:
        # gather the header and metadata for the changelog
        context = {
            "build_number": build_number,
            "version_number": ".".join(str(x) for x in version_number),
            "date": date("ymd"),
            "title": f"Changelog for Application: {data['app_title']}",
            "contributors": ",".join(sorted(contributors)),
        }

        # build the header and metadata portion of the changelog
        output = Template(part1).render(**context)
        print(f"Changelog Header: Successfully created.")
        
        # assemble the sections data & template of the changelog
        changes = {x:y for x, y in changes.items() if y}
        sect_temp = Template(part2)

        # append the populated sections to the changelog
        for sect, chgs in changes.items():
            this_sect = sect_temp.render(artifact_type=sect, artifact_list=chgs)
            output += this_sect

        print(f"Changelog Sections: Successfully created.")
        print(f"Changelog Text: Successfully created.")
        
    except Exception as e:
        print(f"Error building changelog text: {e}")


    try:
        # append the previous changelog content
        with open(changelog_file, "r") as f:
            output += f.read()

        # Write the new changelog content back to file
        with open(changelog_file, "w") as f:
            f.write(output)

        print(f"Changelog updated: {changelog_file}")

        # remove old changelogs 
        for file in changelog_files:
            # TODO: replace os.path with pathlib
            os.remove(os.path.join(OUTPUT_FOLDER, file))

    except Exception as e:
        print(f"Error updating changelog: {e}")


def main():
    parser = argparse.ArgumentParser(description="Changelog generator")
    parser.add_argument("-c", "--collect", action="store_true", help="Collect existing changelogs and update the main changelog file")
    args = parser.parse_args()

    if args.collect:
        collect_changelogs(data)
    else:
        create_artifact()

if __name__ == "__main__":
    main()