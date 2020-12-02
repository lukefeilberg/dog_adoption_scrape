import os
import platform
from typing import Union
import re
import sys


def __select_geckodriver() -> Union[str, None]:
    sys_arch = platform.architecture()[0]

    if sys_arch == "32bit":
        return os.path.join(os.path.dirname(__file__), "bin", "geckodriver-win32.exe")
    elif sys_arch == "64bit":
        return os.path.join(os.path.dirname(__file__), "bin", "geckodriver-win64.exe")
    else:
        return None


def __reset_configuration(filepath: str) -> None:

    print(
        "Your configuration file appears to be corrupted or non-existent. Script configuration has been reset."
    )
    print(
        f'Please edit {os.path.join(os.path.dirname(__file__), "config.env")} file and provide necessary parameters.'
    )

    if os.path.exists(filepath):
        os.remove(filepath)

    new_conf_file = open(os.path.join(os.path.dirname(__file__), "config.env"), "x")
    new_conf_file.write("# Configuration file for `labs_scrape_and_text.py` script\n")
    new_conf_file.write(
        "sender_email = <sender_email_here> # Sender email for script to work with (must be Gmail and allow less secure apps).\n"
    )
    new_conf_file.write("sender_pwd = <sender_pwd_here> # Password for sender email.\n")
    new_conf_file.write(
        "recipient_email = <recipient_email_here> # Recipient email (where emails will be sent to).\n"
    )
    new_conf_file.write("\n\n# Script configuration parameters. (Edit at your own risk)\n")
    new_conf_file.write(f"geckodriver_path = {__select_geckodriver()}")
    new_conf_file.close()
    sys.exit(-1)


def load_configuration(filepath: str) -> dict:
    unedited_parameters_ptrn = re.compile(
        "^<(sender_email_here|sender_pwd_here|recipient_email_here)>$"
    )

    if type(filepath) != str:
        raise ValueError(
            f"`filepath` parameter needs to be str; got {type(filepath).__name__} instead."
        )

    if not filepath:
        raise ValueError("`filepath` parameter is empty")

    if os.path.exists(filepath):

        if not os.path.isfile(filepath):
            __reset_configuration()

        env_file = open(filepath, "r")
        config = {}
        config_arr = [
            line.replace(" ", "").replace("\n", "").split("#")[0]
            for line in env_file.readlines()
            if not line.startswith("#") and line not in ["", "\n"] and not re.match("^ +$", line)
        ]
        env_file.close()

        for conf_line in enumerate(config_arr):
            conf_pair = conf_line[1].split("=")
            if unedited_parameters_ptrn.match(conf_pair[1]):
                raise Exception(
                    f"Some configuration parameters have not been provided.\nPlease specify those parameters in '{os.path.abspath(filepath)}' file"
                )
            if not conf_pair[0] or not conf_pair[1]:
                __reset_configuration(filepath)
            config[conf_pair[0]] = conf_pair[1]

        return config
    else:
        __reset_configuration("config.env")
