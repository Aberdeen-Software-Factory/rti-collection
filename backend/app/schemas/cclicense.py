from enum import Enum


class CCLicenseType(str, Enum):
    """Creative Commons License options as described at:
    https://creativecommons.org/share-your-work/cclicenses/
    """

    CC_BY = "CC BY"
    CC_BY_SA = "CC BY-SA"
    CC_BY_NC = "CC BY-NC"
    CC_BY_NC_SA = "CC BY-NC-SA"
    CC_BY_ND = "CC BY-ND"
    CC_BY_NC_ND = "CC BY-NC_ND"
