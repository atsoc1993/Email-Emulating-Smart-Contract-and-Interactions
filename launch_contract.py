
from algosdk.transaction import ApplicationCreateTxn, StateSchema, OnComplete, wait_for_confirmation
from algosdk.v2client.algod import AlgodClient
from algosdk import logic
from dotenv import load_dotenv
import base64
import os

load_dotenv()
algod_token = os.getenv('NODE_TOKEN')
algod_port = os.getenv('NODE_PORT')
algod_client = AlgodClient(algod_token, algod_port)
account_private_key = os.getenv('PRIVATE_KEY')
account_address = os.getenv('ADDRESS')
params = algod_client.suggested_params()

with open('artifacts/approval.teal', 'r') as f:
    approval_teal_source = f.read()

with open('artifacts/clear.teal', 'r') as f:
    clear_teal_source = f.read()

approval_result = algod_client.compile(approval_teal_source)
approval_program = base64.b64decode(approval_result['result'])

clear_result = algod_client.compile(clear_teal_source)
clear_program = base64.b64decode(clear_result['result'])

global_schema = StateSchema(num_uints=1, num_byte_slices=1)
local_schema = StateSchema(num_uints=1, num_byte_slices=1)

txn = ApplicationCreateTxn(
    account_address,
    params,
    OnComplete.NoOpOC,
    approval_program=approval_program,
    clear_program=clear_program,
    global_schema=global_schema,
    local_schema=local_schema,
)
signed_txn = txn.sign(account_private_key)
txid = algod_client.send_transaction(signed_txn)
print(f'Tx ID: {txid}')

wait_for_confirmation(algod_client, txid)
tx_info = algod_client.pending_transaction_info(txid)
print(f'App ID: {tx_info['application-index']}')

app_address = logic.get_application_address(tx_info['application-index'])
print(f'Application Address: {app_address}')


'''
Example Output:

Tx ID: 6FDEB4M362KD6KR5CB2KX4Q73ZYNLMNQYMN45UXZTYUKTY6TNSAQ
App ID: 628544102
Application Address: D4GQ32AOJNYST4YJWCICG4OKEEOXFU6AY25GLAUBN5YVOMBHMJTQJVLIMU

'''