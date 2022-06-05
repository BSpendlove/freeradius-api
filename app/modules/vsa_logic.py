from pymongo.mongo_client import MongoClient
from loguru import logger
from pathlib import Path
from ttp import ttp
import re

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


def vsa_loader(paths: list):
    vendors = {}
    dictionary_paths = []

    for directory in paths:
        _path = Path(directory)
        if not _path.exists():
            logger.debug(f"Path {_path} does not exist... Skipping...")
            continue

        dictionary_path = {"root_path": directory, "dictionary_files": []}

        for file in _path.iterdir():
            if not file.is_file:
                continue

            # Skip .local files
            if file.suffix and file.suffix.lower() in [".local", ".illegal"]:
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

        dictionary_paths.append(dictionary_path)

    if not dictionary_paths:
        logger.info("No dictionary paths found")
        return

    for dictionary_path in dictionary_paths:
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
                    if dictionary_file_name in dictionary_path["dictionary_files"]:
                        valid_files_for_search.append(dictionary_file_name)
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
