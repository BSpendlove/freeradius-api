import re
from pathlib import Path

from pyrad import dictionary
from pymongo.mongo_client import MongoClient
from loguru import logger
from ttp import ttp

VSA_TEMPLATE = """
<group name="vendor">
VENDOR		{{ vendor_name }}		{{ vendor_id | to_int }}

BEGIN-VENDOR	{{ vendor_name }}

<group name="attributes">
ATTRIBUTE		{{ attribute_name }}	{{ attribute_id | to_int }}	{{ attribute_type }}
</group>
<group name="values">
VALUE		{{ attribute_name }}	{{ attribute_value }}	{{ attribute_id | to_int }}
</group>

END-VENDOR		{{ vendor_name }}
</group>
"""


def check_pyrad_dict(directory: str):
    logger.info("Validiating RADIUS dictionaries")
    validate = dictionary.Dictionary(dict=directory)
    attributes = validate.attributes
    logger.success("Successfully validated RADIUS dictionaries")
    logger.debug(f"Total RADIUS AVPairs loaded = {len(attributes)}")
    return attributes


def vsa_loader(directory: str = "/freeradius_dictionaries"):
    vendors = {}

    _path = Path(directory).parent
    dictionary_path = {"root_path": _path, "dictionary_files": []}
    skip_files = []

    for file in _path.iterdir():
        if not file.is_file:
            continue

        # Skip .local files
        if file.suffix and file.suffix.lower() in [".local", ".illegal", ".compat"]:
            skip_files.append(file.name)
            logger.debug(f"Skipping file {file} due to .local/.illegal suffix")
            continue

        if (
            file.name == "dictionary"
        ):  # Typical format name of a file which we can use to prevent unwanted AVPairs that don't have $INCLUDE
            dictionary_path["master_file"] = file.name
            logger.debug(
                f"Found 'master' dictionary file {file.name} for directory {directory}"
            )
            continue

        logger.debug(f"Found dictionary file {file.name} in {directory}")
        dictionary_path["dictionary_files"].append(file.name)

    valid_files_for_search = []
    if dictionary_path.get("master_file"):
        with Path(
            dictionary_path["root_path"], dictionary_path["master_file"]
        ).open() as master_file:
            lines = master_file.readlines()
            for line in lines:
                match = re.match(f"\$INCLUDE\s+(\S+)", line)
                if not match:
                    continue
                dictionary_file_name = match.group(1)
                if dictionary_file_name in skip_files:
                    logger.info(f"Skipping file {dictionary_file_name}")
                    continue

                if dictionary_file_name in dictionary_path["dictionary_files"]:
                    valid_files_for_search.append(dictionary_file_name)
                else:
                    error_message = f"Unable to find {dictionary_file_name}. Please comment it out in the root freeradius dictionary file or ensure this file exist..."
                    logger.error(error_message)
                    raise ValueError(error_message)
    else:
        valid_files_for_search.extend(dictionary_path["dictionary_files"])

        logger.debug(f"Valid files for search: {valid_files_for_search}")

    for valid_file in valid_files_for_search:
        valid_file = Path(dictionary_path["root_path"], valid_file)
        if not valid_file.exists():
            logger.error(
                f"Dictionary file in valid_files_for_search does not exist {valid_file}"
            )

        logger.debug(f"Attempting to parse {valid_file}")
        with valid_file.open() as _file:
            parser = ttp(data=_file.read(), template=VSA_TEMPLATE)
            parser.parse()

            results = parser.result()[0]
            if not results:
                logger.error(f"Unable to parse {valid_file}")
                continue

            for vendor in results:
                if not vendor.get("vendor"):
                    # Probably a native attribute (eg. User-Name)
                    vendor["vendor"] = {"vendor_id": 0, "vendor_name": "reserved"}

                vendor = vendor["vendor"]

                # Check for duplicated vendors and skip them...
                vendor_name = vendor["vendor_name"]
                vendor_id = vendor["vendor_id"]
                if vendor_id in vendors:
                    logger.error(
                        f"""Found repeated vendor in another parsed file {vendor_name} ({vendor_id}), there is not reason to separate attributes from the same vendor into multiple files. This is not supported and the file will be skipped."""
                    )
                    continue

                vendors[vendor_id] = vendor

    return vendors
