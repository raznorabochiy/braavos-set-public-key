import asyncio

from starknet_py.contract import Contract
from starknet_py.net.account.account import Account
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair

from config import BRAAVOS_ABI, BRAAVOS_ORIGINAL_IMPLEMENTATION, RPC_URL
from utils import get_braavos_address

with open("old_private_key.txt", "r") as file:
    old_private_key, *_ = [row.strip() for row in file]

with open("new_private_key.txt", "r") as file:
    new_private_key, *_ = [row.strip() for row in file]

client = FullNodeClient(RPC_URL)


async def main():
    # Старый приватник нужно только для того, чтобы получить старый адрес
    old_key_pair = KeyPair.from_private_key(old_private_key)
    address = get_braavos_address(old_key_pair.public_key)
    print(f'Address: {address}')

    # Новый приватник используется для подписи транзакций
    new_key_pair = KeyPair.from_private_key(new_private_key)

    account = Account(
        address=address,
        client=client,
        key_pair=new_key_pair,
        chain=StarknetChainId.MAINNET,
    )

    contract = Contract(address=address, abi=BRAAVOS_ABI, provider=account, cairo_version=0)

    call = contract.functions["upgrade"].prepare(BRAAVOS_ORIGINAL_IMPLEMENTATION)
    tx = await account.execute(calls=call, auto_estimate=True)

    print(f'https://voyager.online/tx/{hex(tx.transaction_hash)}')


asyncio.run(main())
