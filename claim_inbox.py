from algosdk.transaction import ApplicationCallTxn, OnComplete, wait_for_confirmation
from algosdk.v2client.algod import AlgodClient
from dotenv import load_dotenv
import os

load_dotenv()
algod_token = os.getenv('NODE_TOKEN')
algod_port = os.getenv('NODE_PORT')
algod_client = AlgodClient(algod_token, algod_port)
account_private_key = os.getenv('PRIVATE_KEY')
account_address = os.getenv('ADDRESS')
params = algod_client.suggested_params()


'''
Previous Output from launch_contract.py

Tx ID: 6FDEB4M362KD6KR5CB2KX4Q73ZYNLMNQYMN45UXZTYUKTY6TNSAQ
App ID: 628544102
Application Address: D4GQ32AOJNYST4YJWCICG4OKEEOXFU6AY25GLAUBN5YVOMBHMJTQJVLIMU

'''

app_id = 628544102

#"set_owner()void" #2867b803

set_owner_txn = ApplicationCallTxn(
    sender=account_address,
    sp=params,
    index = app_id,
    app_args = [0x2867b803.to_bytes(4, 'big'), account_address],
    on_complete= OnComplete.NoOpOC,
    )

signed_txn = set_owner_txn.sign(account_private_key)
txid = algod_client.send_transaction(signed_txn)
print(f'Tx ID: {txid}')

wait_for_confirmation(algod_client, txid)
tx_info = algod_client.pending_transaction_info(txid)
print(f'Tx Info: {tx_info}')
