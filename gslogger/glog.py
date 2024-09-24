import os
import datetime
import argparse
import json
from jinja2 import Template
import pathlib

try:
    # if python version >= 3.11
    import toml as tom
except ModuleNotFoundError:
    import tomli as tom

# PATH = pathlib.Path(__file__).parent.resolve()


# Get the current date and time
def date(reporting=None) -> str:
    """
    Returns the current date and time as a string in the format "YYYY-MM-DD-HH-MM"

    :return: A string representing the current date and time
    """
    if reporting is not None:
        return datetime.datetime.now().strftime("%Y-%m-%d")
    return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")

def save_config(data, target) -> None:
    """
    Saves the configuration to a file named "glog.toml".

    :param data: The configuration data to be saved
    :return: None
    """
    try:
        # with open(PATH / "glog.toml", "wb") as toml_file:
        with open(target, "w") as toml_file:
            tom.dump(data, toml_file)
        print(f"save_config: Success saved {target}.")
        

    except Exception as e:
        print(f"save_config: Error saving glog.json: {e}")


def get_config(src) -> dict:

    try:
        with open(src, "r", encoding="utf-8") as toml_file:
            config_data = tom.loads(toml_file.read())
            print(f"get_config: successfully loaded {src}")
        
            return config_data

    except Exception as e:
        print(f"get_config: Error loading {src}: {e}")
        print(f"get_config: rebuilding default config {src}.")
        
        raw = {
            "app": {
                "version_number": [0, 0, 0],
                "build_number": 0,
                }
            }

        save_config(raw, src)

        with open(CONFIG_FILE,"r", encoding="utf-8") as fs:
            config_data = tom.loads(fs.read())

        return config_data


def get_template_files(template_folder):
    """
    Retrieves the template files, creating them if they do not exist.

    :param template_folder: The folder where the template files are located
    :return: A tuple containing the header and sections template text
    """
    SECTION_FILE = template_folder / "template_section.md"
    HEADER_FILE = template_folder / "template_header.md"

    # find/build template header ############

    # # Changelog for Application: GSLogger
    # Version: 0.2.3 | 2024-09-20 | Build: 20
    # CONTRIBUTORS: Gregory Denyes

    try:
        with open(HEADER_FILE, "r") as fs:
            header = fs.read()
            
    except Exception as e:
        print(f"failed to open header template, building file. Error:", e)
        
        TEMPLATE_INTRO = "\n---\n# {{ title }}\n\nVersion: {{ version_number }} " 
        TEMPLATE_INTRO += "| {{ date }} | Build: {{ build_number }}\n\n"
        TEMPLATE_INTRO += "CONTRIBUTORS: {{ contributors }}\n\n"
        print("Changelog template.md not found. Creating file.")

        with open(HEADER_FILE, "w") as f:
            f.write(TEMPLATE_INTRO)

        with open(HEADER_FILE, "r") as fs:
            header = fs.read()

    # Find/Build template sections ###########

    # ## [ ADDED ]
    # * this is a line of text under the added header.
    # * added template check,...
    
    if not os.path.exists(SECTION_FILE):
        TEMPLATE_SECTIONS = "\n## [ {{ artifact_type }} ]\n\n{% for artifact in artifact_list %}   * {{ artifact }}\n{% endfor %}\n\n"
        print("Changelog template_sections.md not found. Creating file.")

        with open(SECTION_FILE, "w") as fs:
            fs.write(TEMPLATE_SECTIONS)

    with open(SECTION_FILE, "r") as fs:
        sections = f.read()

    return header, sections


# Constants and templates ################################################
CHTYPES = [
    "FUTURE UPDATES",
    "ADDED",
    "CHANGED",
    "DELETED",
    "REMOVED",
    "FIXED",
    "SECURITY",
]

# get the current working directory
PATH = pathlib.Path.cwd()

# initialize local data for GLogger if not present
OUTPUT_FOLDER = PATH / "ch-logs"  # Set the output folder

# Create the output folder if it doesn't exist
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

CONFIG_FILE = PATH / "glog.toml"
data = get_config(CONFIG_FILE)

# make sure the artifact extension pattern is present
if "atf_pattern" not in data["app"]:
    data["app"]["atf_pattern"] = ".txt"

# initialize app data ##################################################
# get app_title from config, initialize if not present
if "app_title" not in data["app"]:
    data["app"]["app_title"] = input("What is the name for this application?\n> ")
else:
    app_title = data["app"]["app_title"]

# initialize user data ##################################################
# get developer from config, initialize if not present
if "developer" not in data["dev"]:
    data["dev"]["developer"] = input("Who is the developer?\n> ")
else:
    developer = data["dev"]["developer"]

# get developer's link from config, initialize if not present
if "dev_link" not in data["dev"]:
    data["dev"]["dev_link"] = input("What is the developer's link?\n> ")
else:
    dev_link = data["dev"]["dev_link"]

# get developer's email from config, initialize if not present
if "dev_email" not in data["dev"]:
    data["dev"]["dev_email"] = input("What is the developer's email address?\n> ")
else:
    dev_link = data["dev"]["dev_email"]

# refresh or backup the config
save_config(data, CONFIG_FILE)
data = get_config(CONFIG_FILE)

def create_artifact()->None:
    """
    Prompts the user to create a new changelog artifact. 

    First, the user is asked to select the type of changelog artifact to create. 
    This is done by providing a list of available types (ADDED, CHANGED, DELETED, REMOVED, FIXED, SECURITY, FUTURE UPDATES).

    Next, the user is asked to provide a commit message that will be used to describe the changes made in the changelog artifact. 
    This message should be at least 10 characters long.

    If the user enters "--r" or "--f" in the commit message, the version number will be incremented accordingly.

    Once the user has entered all required information, the function will create a new changelog artifact in the specified output folder.

    :return: None
    """
    os.system("cls")

    # get the changelog type
    for i, a in enumerate(CHTYPES):
        print(f"{i}. {a}")

    selection = int(input(f"Enter the log type: \n> ").strip())
    if selection > len(CHTYPES) or selection < 0:
        print("Invalid selection, exiting without changes.")
        exit(1)
    artifact_type = CHTYPES[selection]

    # Get the commit message from the user
    a_msg = "Enter the commit message"
    a_msg += " (include --r or --f to initiate semantic versioning):"
    a_msg += f" \n{artifact_type}> "
    artifact_message = input(a_msg.strip())

    # Check commit message for minimum length
    if len(artifact_message) < 10:
        raise ValueError("Entry must be at least 10 characters long")

    # Create the changelog file name
    artifact_file = f"{OUTPUT_FOLDER}/{date()}-{artifact_type}{data["app"]["atf_pattern"]}"
    contrib_line = f"{data["dev"]['developer']} <{data["dev"]['dev_email']}>"
    # Create the changelog file
    try:
        with open(artifact_file, "w") as f:
            f.write(date() + "\n")
            f.write(artifact_type + "\n")
            f.write(artifact_message + "\n")
            f.write(contrib_line + "\n")

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

def v_num_str(version):
    return ".".join([str(x) for x in version])
    
    
    
def collect_changelogs(data):

    # Get the current build and version numbers
    build_number: int = data["app"]["build_number"]  # int
    version_number: list = data["app"]["version_number"]  # [0, 0, 0]

    # Get the list of changelog files
    changelog_files = [f for f in os.listdir(OUTPUT_FOLDER) if f.endswith(data["app"]["atf_pattern"])]

    if len(changelog_files) == 0:
        print("No changelog files found. Exiting without changes.")
        exit(0)

    # Sort the changelog files by date
    changelog_files.sort()

    # # Create the new changelog content
    context = {}
    changes = {x.upper(): [] for x in CHTYPES[1:]}
    future_changes = []
    contributors = set()

    # Iterate over the sorted changelog files
    for file in changelog_files:
        # Read the file content
        with open(OUTPUT_FOLDER / file, "r") as f:
            content = f.read()
        _, a_type, a_msg, a_dev = content.splitlines()

        build_number, version_number = semantic_versioning(
            build_number, version_number, content
        )

        replaced_content = a_msg.replace("--f", "new feature version").replace(
            "--r", "new release version"
        )

        if a_type == "FUTURE UPDATES":
            future_changes.append(replaced_content.strip().capitalize())
        else:
            changes[a_type.upper()].append(replaced_content.strip().capitalize())
    
        contributors.add(a_dev.strip())  # add this dev to the set of contributors

    # updatate the changelog config
    data["app"]["build_number"] = build_number
    data["app"]["version_number"] = version_number

    # refresh_config data
    save_config(data, CONFIG_FILE)
    data = get_config(CONFIG_FILE)

    # gather the header and metadata for the changelog
    try:        
        context = {
            "version_number": v_num_str(version_number),
            "date" : date(True),
            "build_number":build_number,
            "contributors": ",".join(sorted(contributors)),
            "logs": {x: y for x, y in changes.items() if y}
                    }
        
        LOG_FILE = OUTPUT_FOLDER / "templates.json"

        with open(LOG_FILE, "r", encoding="utf-8") as fs:
            log_store = dict(json.loads(fs.read()))

        if len(future_changes) > 0:
            f_count = data["app"]["future_count"] + 1
            future_changes = [f"{f} - {x}" for f, x in enumerate(future_changes, start=f_count)]
            data["app"]["future_count"] = f_count + len(future_changes)

            # refresh_config data
            save_config(data, CONFIG_FILE)
            data = get_config(CONFIG_FILE)
            
            if "futures" not in log_store["doc_parts"] or log_store["doc_parts"]["futures"] is None:
                log_store["doc_parts"]["futures"] = sorted(future_changes)
            else:
                future_changes.extend(log_store["doc_parts"]["futures"])
                
                log_store["doc_parts"]["futures"] = sorted(future_changes)

        old_logs = log_store["details"]
        old_logs.append(context)
        
        sorted_logs = sorted(old_logs, key=lambda x: x["version_number"], reverse=True)
        
        log_store["details"] = sorted_logs

        with open(LOG_FILE, "w", encoding="utf-8") as fs:
            json.dump(log_store, fs, indent=4)

        print(f"{LOG_FILE} successfully updated.")

        # remove old changelogs
        for file in changelog_files:
            # TODO: replace os.path with pathlib
            os.remove(OUTPUT_FOLDER / file)  # commenting until fixed templates.json update
            print(f"Archived artifact {file} successfully removed.")

    except Exception as e:
        print(f"Error updating {LOG_FILE}:", e)


def generate_document():
    """
    Generate the changelog text from the context data and write it to file.

    :param context: The data to populate the changelog template with
    """
    with open(OUTPUT_FOLDER / "templates.json", "r") as fs:
        context = dict(json.loads(fs.read()))

    # context.extend(dict(data))

    OUTPUT_FILE = OUTPUT_FOLDER / "changelog.md"
    print(f"Generating Changelog File: {OUTPUT_FILE}")

    temp_doc_header = context["doc_parts"]["doc_header"]



    doc_footer = context["doc_parts"]["doc_footer"]
    


    # build the header and metadata portion of the changelog
    try:
        output = Template(temp_doc_header).render(**data["app"])
        print(f"Changelog HEADER: Successfully created.")

        temp_futures = context["doc_parts"]["futures_details"]
        futures = context["doc_parts"]["futures"]
        output += Template(temp_futures).render(**futures)
        print(f"Changelog FUTURES: Successfully created.")
    
        # assemble the sections data & template of the changelog
        temp_ver_header = context["doc_parts"]["log_header"]
        details = context["doc_parts"]["ch_type_details"]

        for ver in context["details"]:
            output += Template(temp_ver_header).render(**[ver]) 
            
            for detail in ver["logs"]:
                output += Template(details).render(**detail)
            
            for artifact_type, artifact_list in ver["logs"].items():
                output += sect_temp.render(artifact_type, artifact_list)

            print(f"Changelog version {ver['version_number']} Successfully created.")


        # append the populated sections to the changelog

        # last line of the changelog
        output += doc_footer
        
        print(f"Changelog Text: Successfully created.")

    except Exception as e:
        print(f"Error building changelog text: {e}")

    try:
        # # append the previous changelog content
        # with open(OUTPUT_FILE, "r") as f:
        #     output += f.read()

        # Write the new changelog content back to file
        with open(OUTPUT_FILE, "w") as f:
            f.write(output)

        print(f"Changelog updated: {OUTPUT_FILE}")


    except Exception as e:
        print(f"Error updating changelog: {e}")


def main():
    parser = argparse.ArgumentParser(description="Changelog generator")
    parser.add_argument(
        "-c",
        "--collect",
        action="store_true",
        help="Collect existing changelogs and update the main changelog file",
    )
    args = parser.parse_args()

    if args.collect:
        collect_changelogs(data)
    else:
        create_artifact()


if __name__ == "__main__":
    main()
