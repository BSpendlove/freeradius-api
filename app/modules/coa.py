from typing import List, Union

from pyrad.client import Client
from pyrad import dictionary

from app.config.app import settings
from app import schemas

RETURN_CODES = {
    1: "AccessRequest",
    2: "AccessAccept",
    3: "AccessReject",
    4: "AccountRequest",
    5: "AccountingResponse",
    11: "AccessChallenge",
    12: "StatusServer",
    13: "StatusClient",
    40: "DisconnectRequest",
    41: "DisconnectACK",
    42: "DisconnectNAK",
    43: "COARequest",
    44: "COAACK",
    45: "COANAK",
}


class COA:
    """Setup a basic COA client and send RADIUS COA packets to a specific destination

    Arguments:
        address:        IPv4 address of COA Client
        secret:         RADIUS Secret
        port:           UDP Port
        dictionary:     FreeRADIUS dictionary file or pyrad Dictionary attributes dict
        timeout:        Timeout in seconds
    """

    def __init__(
        self,
        *,
        address,
        secret,
        port: int = 3799,
        dictionary: Union[str, dict] = settings.AVPAIRS_DICT,
        timeout: int = 5
    ) -> None:
        self.address = address
        self.secret = str.encode(secret)
        self.port = port
        self.dictionary = dictionary
        self.timeout = timeout
        self.client = self.setup_client()

    def setup_client(self):
        """Setup the client"""
        client = Client(
            server=self.address,
            coaport=self.port,
            secret=self.secret,
            dict=self.dictionary,
            timeout=self.timeout,
        )
        return client

    def send_coa_packet(self, avpairs: List[schemas.COAAVPair]) -> schemas.COAResponse:
        """Send COA Attributes to the client

        Arguments:
            avpairs:        List of AVPairs (Attribute + Value)
        """
        attributes = {}
        for avpair in avpairs:
            avpair.normalize_attribute()
            attributes[avpair.attribute] = avpair.value

        request = self.client.CreateCoAPacket(**attributes)
        response = schemas.COAResponse(
            code=request.code, message=RETURN_CODES[request.code]
        )
        return response
