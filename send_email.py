from algosdk.transaction import ApplicationCallTxn, OnComplete, wait_for_confirmation, assign_group_id
from algosdk.v2client.algod import AlgodClient
from algosdk.encoding import decode_address
from dotenv import load_dotenv
import os


load_dotenv()
algod_token = os.getenv('NODE_TOKEN')
algod_port = os.getenv('NODE_PORT')
algod_client = AlgodClient(algod_token, algod_port)
account_private_key = os.getenv('PRIVATE_KEY')
account_address = os.getenv('ADDRESS')
params = algod_client.suggested_params()


#3000 character message encoded as bytes
message = """Dear Team,

I hope this message finds you well and thriving in your respective roles. As we navigate through the ever-evolving landscape of our industry, it is imperative to reflect on our journey, acknowledge our current standing, and envision the path that lies ahead.

The past few months have been a testament to our resilience and commitment. We've tackled challenges head-on, adapted to new market dynamics, and continued to deliver exceptional value to our clients. Your hard work and dedication have not gone unnoticed, and I want to express my heartfelt gratitude for your relentless pursuit of excellence.

As we look towards the future, it's clear that change is not just inevitable but necessary. The world around us is transforming at an unprecedented pace, and to stay ahead, we must embrace change with open arms. This means being willing to re-evaluate our strategies, innovate continuously, and sometimes, take calculated risks to propel us forward.

In the coming weeks, we will embark on a series of strategic initiatives aimed at enhancing our operational efficiency, fostering innovation, and expanding our market presence. These initiatives will require collaboration across all departments, a shared commitment to our goals, and a willingness to venture into uncharted territories.

To facilitate this transformation, we will provide resources for skill development and create opportunities for cross-functional collaboration. It’s crucial that we all contribute to a culture of learning and adaptability, as these elements are the bedrock of sustained success in a rapidly changing environment.

I understand that change can be daunting and may bring about uncertainty. However, I assure you that these steps are taken with the long-term vision of securing our position as industry leaders and ensuring the continued growth and stability of our company. Your support and active participation in this process are invaluable and will be the key to our collective success.

Let’s approach this next chapter with optimism and a shared resolve to achieve new heights. I am confident that together, we can navigate the complexities of our industry, overcome any obstacles, and emerge stronger and more capable than ever before.

In closing, I invite each of you to share your ideas, aspirations, and concerns as we move forward. Your insights are critical to our ongoing evolution and success. Please feel free to reach out to me directly or through your respective managers. Let's make this journey a collaborative, inclusive, and transformative one.

Thank you once again for your hard work, dedication, and commitment to excellence. Here’s to a future filled with growth, opportunities, and success!
"""



'''
Previous Output from launch_contract.py

Tx ID: 6FDEB4M362KD6KR5CB2KX4Q73ZYNLMNQYMN45UXZTYUKTY6TNSAQ
App ID: 628544102
Application Address: D4GQ32AOJNYST4YJWCICG4OKEEOXFU6AY25GLAUBN5YVOMBHMJTQJVLIMU

'''

app_id = 628544102

message_bytes = message.encode()
chunk_size = 1022
message_chunks = [message_bytes[i:i + chunk_size] for i in range(0, len(message_bytes), chunk_size)]

address_corresponding_to_inbox = account_address
receiver_marker = decode_address(address_corresponding_to_inbox)[0]

txns = []
for index, message_fragment in enumerate(message_chunks):
    formatted_message_fragment = bytes([index]) + bytes([receiver_marker]) + message_fragment
    length_of_fragment = len(formatted_message_fragment)
    email_fragment = ApplicationCallTxn(
        sender=account_address,
        sp=params,
        index = app_id,
        app_args = [0xf00ec344.to_bytes(4, 'big'), formatted_message_fragment, length_of_fragment],
        on_complete= OnComplete.NoOpOC,
        )

    txns.append(email_fragment)
    

assign_group_id(txns)
signed_txns = [txn.sign(account_private_key) for txn in txns]
txid = algod_client.send_transactions(signed_txns)
print(f'Tx ID: {txid}')

wait_for_confirmation(algod_client, txid)
tx_info = algod_client.pending_transaction_info(txid)
print(f'Tx Info: {tx_info}')
