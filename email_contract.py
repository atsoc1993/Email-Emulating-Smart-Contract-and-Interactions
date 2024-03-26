from pyteal import *

def set_globals():
    default_owner = Global.zero_address()
    return Seq([
        App.globalPut(Bytes("owner"), default_owner)
        ])

router = Router(
    "MessageReceiver",
    
    BareCallActions(
        no_op=OnCompleteAction.create_only(Seq([
            set_globals(),
            Approve()
        ])),        opt_in=OnCompleteAction.call_only(Approve()),
        close_out=OnCompleteAction.call_only(Approve()),
    ),
    clear_state=Approve(),
)

@router.method
def set_owner():
    default_owner = App.globalGet(Bytes("owner"))
    owner = Txn.sender()
    return Seq([
        Assert(default_owner == Global.zero_address()),
        App.globalPut(Bytes("owner"), owner)
    ])
    
@router.method() 
def message():
    full_message = Txn.application_args[1]
    message_index = Substring(full_message, Int(0), Int(1))
    message_index_int = Btoi(message_index)
    receiver = App.globalGet(Bytes("owner"))
    receiver_inbox = Extract(receiver, Int(0), Int(1))
    receiver_marker = Substring(full_message, Int(1), Int(2))
    message_length = Len(full_message)
    message_content = Substring(full_message, Int(2), message_length)

    return Seq([
        Assert(And(message_index_int >= Int(0), message_index_int <= Int(16))),
        Assert(receiver_marker == receiver_inbox),
        Log(message_index),
        Log(message_content)
    ])

if __name__ == "__main__":
    import os
    import json

    path = os.path.dirname(os.path.abspath(__file__))
    approval, clear, contract = router.compile_program(version=8)
    
    os.makedirs(os.path.join(path, "artifacts"), exist_ok=True)

    with open(os.path.join(path, "artifacts/contract.json"), "w") as f:
        f.write(json.dumps(contract.dictify(), indent=2))

    with open(os.path.join(path, "artifacts/approval.teal"), "w") as f:
        f.write(approval)

    with open(os.path.join(path, "artifacts/clear.teal"), "w") as f:
        f.write(clear)