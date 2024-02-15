import re

from pathlib import Path
import json


def find_variables(template_str):

    matches = re.findall(r"Variable\s*{\s*(.*?)\s*}", template_str, re.DOTALL)

    # Brute force, you motherfucker!
    extracted_data = []
    for match in matches:
        name_match = re.search(r'name\s*=\s*"(.*?)"', match)
        class_match = re.search(r'class\s*=\s*"(.*?)"', match)
        type_match = re.search(r'type\s*=\s*"(.*?)"', match)
        value_match = re.search(r'value\s*=\s*"(.*?)"', match)
        default_value_match = re.search(r'defaultValue\s*=\s*"(.*?)"', match)
        if name_match and type_match and value_match and default_value_match:
            extracted_data.append(
                {
                    "name": name_match.group(1),
                    "class": class_match.group(1),
                    "type": type_match.group(1),
                    "value": value_match.group(1),
                    "default_value": default_value_match.group(1),
                }
            )

    for item in extracted_data:
        # ! We only need real since that's the only item we can multiply anyway.
        if item.get("type") in ["real"]:
            print(item)

    return extracted_data


def main():

    script_parent_dir = Path.cwd()
    params_templates_dir = script_parent_dir / "__scripts/__templates/__params"
    params_templates = list(params_templates_dir.glob("**/*.tpl"))

    consolidated_params = []

    for params_template in params_templates:
        template_str = params_template.read_text()
        extracted_params = find_variables(template_str)
        for extracted_param in extracted_params:
            consolidated_params.append(extracted_param)
            # consolidated_params[extracted_param["name"]] = {
            #     "class": extracted_param["class"],
            #     "type": extracted_param["type"],
            #     "value": extracted_param["value"],
            #     "default_value": extracted_param["default_value"],
            # }

    print(consolidated_params)
    j = json.dumps(consolidated_params, indent=4)
    Path(params_templates_dir / "consolidated.json").write_text(j)


if __name__ == "__main__":
    main()
