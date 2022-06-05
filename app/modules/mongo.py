from pymongo.mongo_client import MongoClient
from loguru import logger


class Mongo:
    def __init__(self, uri: str):
        self.uri = uri
        self.client = None
        self.db = None

    def setup_mongodb(self) -> None:
        try:
            if not self.uri:
                raise ValueError(
                    "Unable to setup database, please ensure MongoDB URI is set in the config"
                )

            self.client = MongoClient(self.uri)
            self.db = self.client.freeradius_api
        except:
            raise ValueError(
                "Unable to connect to mongodb, probably not running or wrong uri?"
            )

    def create_vsa_mappings(self, vsas: dict) -> None:
        logger.debug("Creating initial VSA mappings")
        vendors_col = self.db.vendors
        attributes_col = self.db.attributes
        values_col = self.db.values

        for vendor_id, vendor_data in vsas.items():
            vendor_name = vendor_data["vendor_name"]
            logger.debug(f"Attempting to insert/update {vendor_id} ({vendor_name})")
            vendors_col.update_one(
                {"vendor_id": vendor_id},
                {"$set": {"vendor_name": vendor_name}},
                upsert=True,
            )

            vendor_result = vendors_col.find_one({"vendor_id": vendor_id})

            for attribute in vendor_data.get("attributes"):
                attribute_name = attribute["attribute_name"]
                attribute_id = attribute["attribute_id"]
                attribute_type = attribute["attribute_type"]

                result = attributes_col.update_one(
                    {
                        "vendor_id": vendor_result["_id"],
                        "attribute_id": attribute_id,
                    },
                    {
                        "$set": {
                            "attribute_name": attribute_name,
                            "attribute_type": attribute_type,
                        }
                    },
                    upsert=True,
                )

                logger.debug(
                    f"Attempting to insert or update attribute {attribute_name}: {result.modified_count}"
                )

            for value in vendor_data.get("values"):
                attribute_id = value["attribute_id"]
                attribute_value = value["attribute_value"]
                parent_attribute_name = value["attribute_name"]

                parent_attribute = attributes_col.find_one(
                    {"attribute_name": parent_attribute_name}
                )
                if not parent_attribute:
                    logger.error(
                        f"""Unable to find an attribute called {parent_attribute_name} for FreeRADIUS value {attribute_value}"""
                    )
                    continue

                result = values_col.update_one(
                    {"attribute_id": attribute_id},
                    {
                        "$set": {
                            "attribute_name": parent_attribute["_id"],
                            "attribute_value": attribute_value,
                        }
                    },
                    upsert=True,
                )

                logger.debug(
                    f"Attempting to insert or update value {attribute_value}: {result.modified_count}"
                )
