import os
import datetime
import argparse
import json

# Get the current date and time
def date():
    """
    Returns the current date and time as a string in the format "YYYY-MM-DD-HH-MM"

    :return: A string representing the current date and time
    """
    return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")

def save_config(data):
    """
    Saves the configuration to a file named "glog.json".

    :param data: The configuration data to be saved
    :return: True if the save is successful, False otherwise
    """
    try:
        with open("glog.json", "w") as f:
            json.dump(data, f, indent=3)
        return True
    
    except Exception as e:
        print(f"Error saving glog.json: {e}")
        return False
    
    
# Constants and templates
# initialize local data for GLogger if not present

output_folder = "ch-logs"  # Set the output folder

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

try:
    # Load the JSON data
    with open("glog.json", "r") as f:
        data = json.load(f)    
except:
    # or Initialize the JSON data
    data = {"build_number": 0, "version_number": [0, 0, 0]}  

if "app_title" not in data:
    app_title = input("What is the name for this application?\n> ")
    data["app_title"] = app_title
    
else:
    app_title = data["app_title"]

if "developer" not in data:
    developer = input("Who is the developer?\n> ")
    data["developer"] = developer
else:
    developer = data["developer"]

if "dev_link" not in data:
    dev_link = input("What is the developer's link?\n> ")
    data["dev_link"] = dev_link
else:
    dev_link = data["dev_link"]
    
# refresh or backup the glog.json configuration
save_config(data)

chlog_title = f"# Changelog for {app_title}\n\n"
chlog_footer = f"# **GLogger created & maintained by:** [{data['developer']}]({data['dev_link']})"
anchor = "\n\n<!--  NEW CHANGES   /-->\n\n"

changelog_file = "changelog.md" # Set the changelog file
if not os.path.exists(changelog_file):
    with open(changelog_file, "w") as f:
        f.write(chlog_title)
        f.write(anchor)
        f.write(chlog_footer)


def create_artifact():
    os.system("cls")

    # get the changelog type
    chtypes = ["ADDED", "CHANGED", "DELETED", "REMOVED", "FIXED", "SECURITY"]
    for i, a in enumerate(chtypes):
        print(f"{i+1}. {a}")
        
    selection = int(input(f"Enter the log type: \n> "))
    artifact_type = chtypes[selection - 1]

    # Get the commit message from the user
    artifact_message = input(f"Enter the commit message: \n{artifact_type}> ")

    # Create the changelog file name
    artifact_file = f"{output_folder}/{date()}-{artifact_type}.md"

    # Create the changelog file
    try:
        with open(artifact_file, "w") as f:
            f.write(f"# {date()}\n")
            f.write(f"{artifact_type}\n")
            f.write(f"{artifact_message}\n")

        print(f"Changelog Artifact created: {artifact_file}")
        
    except Exception as e:
        print(f"Error creating Artifact: [{artifact_file}]\n{e}")

def collect_changelogs():

    # Get the current build and version numbers
    build_number:int = data["build_number"] # int
    version_number:list = data["version_number"] # [0, 0, 0]

    # Get the list of changelog files
    changelog_files = [f for f in os.listdir(output_folder) if f.endswith(".md")]

    # Sort the changelog files by date
    # changelog_files.sort(key=lambda f: datetime.datetime.strptime(f.split("-")[1].split(".")[0], "%Y-%m-%d-%H-%M"))
    changelog_files.sort()

    # Create the new changelog content
    with open(changelog_file, "r") as f:
        old_changelog_content = "\n" + f.read()

    new_changelog_content = ""

    # Iterate over the sorted changelog files
    for file in changelog_files:
        # Read the file content
        with open(os.path.join(output_folder, file), "r") as f:
            content = f.read()

        # Extract the changelog type and date
        # TODO: Add support for multiple changelog types
        # TODO: fix the date format
        
        lines = content.splitlines()
        changelog_type = lines[1].strip().split(" ")[1]
        date = lines[1].strip().split(" ")[0]

        # Append the content to the new changelog
        new_changelog_content += f"## {changelog_type} - {date}\n"
        new_changelog_content += content.splitlines()[2] + "\n\n"
        
        build_number += 1
        if "major version" in new_changelog_content:
            version_number[0] += 1
            version_number[1] = 0
            version_number[2] = 0
        elif "medium version" in new_changelog_content:
            version_number[1] += 1
            version_number[2] = 0
        else:
            version_number[2] += 1

    # Append the new build and version numbers to the changelog
    new_changelog_content = f"## Version [{version_number}] - Build [{build_number}]\n" + new_changelog_content
    final_changelog_content = new_changelog_content + old_changelog_content

    # updatate the changelog json
    data["build_number"] = build_number
    data["version_number"] = version_number

    save_config(data)

    # Write the new changelog content to the file
    with open(changelog_file, "w") as f:
        f.write(new_changelog_content)

    print(f"Changelog updated: {changelog_file}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Changelog generator")
    parser.add_argument("-c", "--collect", action="store_true", help="Collect existing changelogs and update the main changelog file")
    args = parser.parse_args()

    if args.collect:
        collect_changelogs()
    else:
        create_artifact()