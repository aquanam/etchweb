import copy
import re
from typing import Any
from . import available


def _about_settings_file_print(path: str) -> None:
    if len(path) > 0:
            print(f"[pre-start] About setting file '{path}':")
    else:
        print(f"[pre-start] About a setting file:")


def get_keys(dict_list: list[dict[Any, Any]]) -> list[Any]:
    """Get all the keys in a dictionary list."""

    keys = [list(d.keys())[0] for d in dict_list]
    return keys


def get_dict_by_dict_list(dict_list: list[dict[Any, Any]], key: str) -> dict:
    """Get a dictionary by a dictionary list using a key."""
    
    for dictionary in dict_list:
        if key == list(dictionary.keys())[0]:
            return list(dictionary.values())[0]
    
    return {}


def match_settings(content: str, path: str = "") -> list[Any]:
    """Match settings from content."""

    content = re.sub(r"#.*$", "", content, flags=re.MULTILINE)
    content = re.sub(r";.*$", "", content, flags=re.MULTILINE)
    
    content = re.sub(r"^\s*$", "", content, flags=re.MULTILINE)

    compiler = re.compile(r'(\w+)="([^"]+)"')

    key_and_value = {}

    for line in content.strip().split('\n'):
        matched = compiler.search(line)
        if matched:
            key_and_value.update({matched.group(1): matched.group(2)})

    tables = []

    if len(key_and_value) > 0:
        for key, value in key_and_value.items():
            setvar_attr = key.lower().capitalize()

            if not hasattr(available, setvar_attr):
                _about_settings_file_print(path)
                print(f"[pre-start]    Ignoring setvar '{key}' since it is invalid")
                continue

            setvar_class: available.SetVar = getattr(available, setvar_attr)()
            tables.append({setvar_class.name: copy.deepcopy(setvar_class.table)})

            for item in value.split(" "):
                equals_count = item.count("=")

                if equals_count == 0:
                    if item[0] != "-":
                        setvar_class.set_value(item, True)
                    else:
                        setvar_class.set_value(item[1:], False)
                elif equals_count == 1:
                    subvar, val = item.split("=")
                    setvar_class.set_value(subvar, val)
                elif equals_count > 1:
                    _about_settings_file_print(path)
                    print(f"[pre-start]    [{item}]")
                    print("[pre-start]    Invalid subvar|val syntax: More than one equal")
                    print("[pre-start]                               signs.")

            tables[-1][setvar_class.name] = copy.deepcopy(setvar_class.table)

    all_keys = get_keys(tables)
    for default in available.DEFAULT_SETVARS:
        if default not in all_keys:
            _class: available.SetVar = getattr(available, default.lower().capitalize())()
            tables.append({default: copy.deepcopy(_class.table)})

    warn_dict = get_dict_by_dict_list(tables, "WARN")
    if "SETTINGS" not in key_and_value.keys() and \
        warn_dict.get("no-settings-setvar"):
        _about_settings_file_print(path)
        print("[pre-start]    Warn: There is no 'SETTINGS' setvar!")
        print("[pre-start]          This will create a default settings table, which could")
        print("[pre-start]          cause problems. To remove this warning, put in the file:")
        print("[pre-start]              WARN=\"-no-settings-setvar\"")

    return tables


def setting_file_content(path: str = "settings.conf") -> str:
    """Return the content of a setting file."""
    with open(path) as setting_file:
        return setting_file.read()


def read_setting_file(path: str = "settings.conf") -> list[Any]:
    content = setting_file_content(path)
    matched = match_settings(content, path)
    return matched
