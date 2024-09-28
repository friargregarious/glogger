# for the sake of my dumb ass not able to build my packages if they have
# external dependencies. i am replaceing jinja2 as my templating engine
# with this personalized hack of a package.

from extras import load_json, save_json, date
from version import __version__


HEADER_DOC = "# CHANGELOG: {app_title}\n"
HEADER_FUTURES = "\n## [ ISSUES & FUTURE CHANGES ]\n"
HEADER_VERSION = "\n## VERSION: {version_number} | {date} | BUILD: {build_number}\n"
CONTRIBUTORS = "\nCONTRIBUTORS: {contributors}\n"
HEADER_SECTION = "\n### [ {artifact_type} ]\n"
FOOTER = "\n\n***This Changelog Maintained by [Greg's Simple Changelogger](https://github.com/friargregarious/glogger)***"


def fmt_det_lst(det_list:list)->str:
    """
    Formats a list of strings into a markdown formatted list.

    The list elements are stripped of whitespace and capitalized before being
    added to the formatted string.

    :param det_list: The list of strings to format
    :return: A markdown formatted string containing the list elements
    """
    det_txt = "\n"
    for txt in det_list:
        det_txt += f"- {txt.strip().capitalize()}\n"
    
    return det_txt


def build_report(data:dict)->str:
    """
    Builds a changelog report based on the provided data and configuration.

    :param data: the changelog data previously collected from artifacts
    :param cfg: the configuration for the application
    :return: a string containing the MD formatted changelog report
    """
    output = ""
    
    log_store = load_json(data["paths"]["FILE_LOG"])
    
    print(f"Generating Changelog Text.")

    # build the header and metadata portion of the changelog
    try:
        output += HEADER_DOC.format(app_title=data["app"]["app_title"]).upper()
        print(f"Changelog formatting HEADER: Success!")
    except Exception as e:
        print(f"Changelog formatting HEADER: Error: {e} app_title: {data['app']['app_title']}")

    # FUTURES are details only found under the main heading
    try:
        output += HEADER_FUTURES
        output += fmt_det_lst(log_store["doc_parts"]["futures"])
        print(f"Changelog formatting FUTURES: Success!")

    except Exception as e:
        print(f"Changelog formatting FUTURES: Error: {e}")

    # assemble the versions data & template of the changelog
    # append the version header to the changelog
    for ver in log_store["details"]:
        ver_headers = {
            "version_number": "v" + ".".join(map(str, ver["version_number"])), 
            "date": ver["date"],
            "build_number": ver["build_number"],
            "contributors": ver["contributors"],
        }
        version_logs = ver["logs"]
               
        try:
            output += HEADER_VERSION.format(**ver_headers)
            print(
                f"Changelog version header {ver['version_number']}: Successfully appended."
            )

            for a_type, a_list in version_logs.items():
                output += HEADER_SECTION.format(artifact_type=a_type)
                output += fmt_det_lst(a_list)

        except Exception as e:
            print(f"Changelog formatting Versions: Error: {e}")

        print(f"Changelog formatting Versions {ver['version_number']} Success!")

    try:
        # last line of the changelog
        output += FOOTER

        print(f"Changelog Text: Successfully Completed!")

    except Exception as e:
        print(f"Error adding footer: {e}")


    return output
