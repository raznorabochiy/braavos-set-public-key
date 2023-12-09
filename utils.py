from starknet_py.hash.address import compute_address
from starknet_py.hash.selector import get_selector_from_name

from config import BRAAVOS_IMPLEMENTATION_CLASS_HASH, BRAAVOS_PROXY_CLASS_HASH


def get_braavos_address(public_key: int) -> str:
    selector = get_selector_from_name("initializer")

    calldata = [public_key]

    address = compute_address(
        class_hash=BRAAVOS_PROXY_CLASS_HASH,
        constructor_calldata=[BRAAVOS_IMPLEMENTATION_CLASS_HASH, selector, len(calldata), *calldata],
        salt=public_key,
    )

    return hex(address)
