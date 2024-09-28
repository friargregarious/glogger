import os
import pathlib
import argparse
# import jin
from jin import fmt_det_lst, build_report
from extras import load_json, save_json, date

def create_artifact(data:dict) -> None:
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

    # get the changelog type
    for i, a in enumerate(data['CHTYPES']):
        print(f"{i}. {a}")

    selection = int(input(f"Enter the log type: \n> ").strip())
    if selection > len(data['CHTYPES']) or selection < 0:
        print("Invalid selection, exiting without changes.")
        exit(1)
    artifact_type = data['CHTYPES'][selection]

    # Get the commit message from the user
    a_msg = "Enter the commit message"
    a_msg += " (include --r or --f to initiate semantic versioning):"
    a_msg += f" \n{artifact_type}> "
    artifact_message = input(a_msg.strip())

    # Check commit message for minimum length
    if len(artifact_message) < 10:
        raise ValueError("Entry must be at least 10 characters long")

    # Create the changelog file name
    artifact_file = (
        f"{data['paths']['DIR_OUTPUT']}/{date()}-{artifact_type}{data["app"]["atf_pattern"]}"
    )
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


def collect_changelogs(data):

    # Get the current build and version numbers
    build_number: int = data["app"]["build_number"]  # int
    version_number: list = data["app"]["version_number"]  # [0, 0, 0]

    # Get the list of changelog files
    changelog_files = [
        f for f in os.listdir(data["paths"]["DIR_OUTPUT"]) if f.endswith(data["app"]["atf_pattern"])
    ]

    if len(changelog_files) == 0:
        print("No changelog files found. Exiting without changes.")
        exit(0)

    # Sort the changelog files by date
    changelog_files.sort()

    # # Create the new changelog content
    context = {}
    changes = {x.upper(): [] for x in data["CHTYPES"][1:]}
    future_changes = []
    contributors = set()

    # Iterate over the sorted changelog files
    for file in changelog_files:
        # Read the file content
        with open(pathlib.Path( data["paths"]["DIR_OUTPUT"] ) / file, "r") as f:
            _, a_type, a_msg, a_dev = f.read().splitlines()

        build_number, version_number = semantic_versioning(
            build_number, version_number, a_msg
        )

        replaced_content = a_msg.replace("--f", "new FEATURE version")
        replaced_content = a_msg.replace("--r", "new RELEASE version")

        if a_type == "FUTURE UPDATES":
            future_changes.append(replaced_content.strip().capitalize())
        else:
            changes[a_type.upper()].append(replaced_content.strip().capitalize())

        contributors.add(a_dev.strip())  # add this dev to the set of contributors

    # updatate the changelog config
    data["app"]["build_number"] = build_number
    data["app"]["version_number"] = version_number

    # refresh_config data
    save_json(data, data["paths"]["FILE_CONFIG"] )

    # gather the header and metadata for the changelog
    try:
        context = {
            "version_number": version_number,
            "date": date(reporting=True),
            "build_number": build_number,
            "contributors": ", ".join(sorted(contributors)),
            "logs": {x: y for x, y in changes.items() if y},
        }

        # with open(data["paths"]["FILE_LOG"], "r", encoding="utf-8") as fs:
        #     log_store = dict(json.loads(fs.read()))
        log_store = load_json(data["paths"]["FILE_LOG"])

        # collect future updates and store in log store
        if len(future_changes) > 0:
            f_count = data["app"]["f_count"] + 1
            future_changes = [
                f"{f} - {x}" for f, x in enumerate(future_changes, start=f_count)
            ]
            data["app"]["f_count"] = f_count + len(future_changes)

            # refresh_config data
            save_json(data, data["paths"]["FILE_CONFIG"])

            if (
                "futures" not in log_store["doc_parts"]
                or log_store["doc_parts"]["futures"] is None
            ):
                log_store["doc_parts"]["futures"] = sorted(future_changes)
            else:
                future_changes.extend(log_store["doc_parts"]["futures"])
                log_store["doc_parts"]["futures"] = sorted(future_changes)

        old_logs = log_store["details"]
        old_logs.append(context)

        sorted_logs = sorted(old_logs, key=lambda x: x["version_number"], reverse=True)

        log_store["details"] = sorted_logs

        # with open(data["paths"]["FILE_LOG"], "w", encoding="utf-8") as fs:
        #     json.dump(log_store, fs, indent=4)
        save_json(log_store, data["paths"]["FILE_LOG"])

        print(f"{data['paths']['FILE_LOG']} successfully updated.")

        # remove old changelogs
        for file in changelog_files:
            # TODO: replace os.path with pathlib
            os.remove(pathlib.Path(data["paths"]["DIR_OUTPUT"]) / file)
            print(f"Archived artifact {file} successfully removed.")

    except Exception as e:
        print(f"Error updating {data['paths']['FILE_LOG']}:", e)


def build_initial(config:dict)->dict:

    ##########################################################################
    # PATH WORK ##############################################################
    # get the current working directory
    if "CWD" not in config["paths"]:
        # todo: search for the config file within the current path tree
        # then set the CWD to that path and move there.
        config["paths"]["CWD"] = str(pathlib.Path.cwd())
    
    else:
        # we should be working from the same directory as the config file
        os.chdir(config["paths"]["CWD"])

    # get the config path
    if "FILE_CONFIG" not in config["paths"]:
        config["paths"]["FILE_CONFIG"] = str(pathlib.Path(config["paths"]["CWD"]) / "glog.json")

    # initialize the config if it doesn't exist
    if not os.path.exists(config['paths']['FILE_CONFIG']):        
        save_json(data=config, target=config['paths']['FILE_CONFIG'])

    # load the config to memory
    config.update ( load_json(config['paths']['FILE_CONFIG']) )
                
    # initialize local data folder for GLogger if not present
    if "DIR_OUTPUT" not in config["paths"]:
        config["paths"]["DIR_OUTPUT"] = str(pathlib.Path(config["paths"]["CWD"]) / "ch-logs")

    # Create the output folder if it doesn't exist
    if not os.path.exists(config["DIR_OUTPUT"]):
        os.makedirs(config["DIR_OUTPUT"])

    # initialize changes log file if not present
    if "FILE_LOG" not in config["paths"]:
        config["paths"]["FILE_LOG"] = str(pathlib.Path(config["paths"]["DIR_OUTPUT"]) / "log_store.json")
    
    if not os.path.exists(config['paths']['FILE_LOG']):
        save_json({}, config['paths']['FILE_LOG'])
    
    if 'FILE_OUTPUT' not in config['paths']:
        config['paths']['FILE_OUTPUT'] =str(pathlib.Path(config['paths']['DIR_OUTPUT']) / 'changelog.md')
    
    # not os.path.exists(config['paths']['FILE_LOG']): / "changelog.md"

    ##########################################################################
    # REPORTING CONSTANTS ####################################################
    if "CHTYPES" not in config:
        config["CHTYPES"] = [
            "FUTURE UPDATES",
            "ADDED",
            "CHANGED",
            "REMOVED",
            "FIXED",
            "SECURITY",
        ]

    # make sure the artifact extension pattern is present
    if "atf_pattern" not in config["app"]:
        config["app"]["atf_pattern"] = ".txt"

    ##########################################################################
    # initialize app config ##################################################
    # get app_title from config, initialize if not present
    if "app_title" not in config["app"]:
        config["app"]["version_number"] = [0,0,0]
        config["app"]["build_number"] = 0
        config["app"]["app_title"] = input("What is the name for this application?\n> ")


    # initialize user config ##################################################
    # get developer from config, initialize if not present
    if "dev_name" not in config["dev"]:
        if "Y" == input("Would you like to use your git config as the developer?\n (Y/N) > ").upper():
            config["dev"]["dev_name"] = os.popen("git config user.name").read().strip()
            config["dev"]["dev_email"] = os.popen("git config user.email").read().strip()
            config["dev"]["dev_link"] = os.popen("git config remote.origin.url").read().strip()

        else:
            config["dev"]["dev_name"] = input("Who is the developer?\n> ")

            # get developer's email from config, initialize if not present
            if "dev_email" not in config["dev"]:
                config["dev"]["dev_email"] = input("What is the developer's email address?\n> ")

            # get developer's link from config, initialize if not present
            if "dev_link" not in config["dev"]:
                config["dev"]["dev_link"] = input("What is the developer's link?\n> ")

    return config

def start_up():
    # load the running configuration
    try:
        data = load_json( pathlib.Path.cwd() / "glog.json" )

    except Exception as e:        
        print(f"Error loading glog.json: {e}")
        data = build_initial(  {
               "paths":{
                   "CWD": pathlib.Path.cwd(),
                   },
               })
            
        # refresh or backup the config
        save_json(data, data["paths"]["FILE_CONFIG"])

    return data
    

def main():
    parser = argparse.ArgumentParser(description="Changelog generator")
    parser.add_argument(
        "-c",
        "--collect",
        action="store_true",
        help="Collect existing changelogs and update the main changelog file",
    )

    parser.add_argument(
        "-g",
        "--generate",
        action="store_true",
        help="Generate Changelog file from collected data.",
    )
    
    args = parser.parse_args()

    data = start_up()

    if args.collect:
        collect_changelogs(data)

    elif args.generate:
        try:
            with open(data['paths']['FILE_OUTPUT'], "w", encoding="utf-8") as f:
                f.write(build_report(data))
        except Exception as e:
            print(f"Error generating changelog: {e}")
    else:
        create_artifact(data)


if __name__ == "__main__":
    main()
