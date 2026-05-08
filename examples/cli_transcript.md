# CLI transcript (simulated)

```text
$ python -m mcp_delegation_lab.server
# server started (stdio)

# get_delegation_scope
{"delegation_id":"del_001"}
{"ok":true,"audit_id":"b3f8d96b-0bcf-4c2d-bd7f-03f8f3cf6ab0","data":{"delegation_id":"del_001","delegatee":"agent_abc","allowed_tokens":["INR_STABLE"],"max_amount":"1000","expires_at":"2026-05-16T12:00:00+00:00","policy_tags":["demo"]}}

# check_transfer_eligibility
{"delegation_id":"del_001","from_account":"acct_001","to_account":"acct_002","token_class":"INR_STABLE","amount":"1500"}
{"ok":true,"audit_id":"0dbd9c0f-2a6c-4e4a-8e76-9fe6e2e5b4a4","data":{"eligible":false,"code":"SCOPE_EXCEEDED","message":"Requested transfer exceeds delegation scope.","detail":{"token_class":"INR_STABLE","requested_amount":"1500","delegated_limit":"1000","checks_failed":["amount_limit"],"checks_passed":["delegation_active","token_class","from_account_scope","sufficient_balance"]}}}

# initiate_transfer
{"delegation_id":"del_001","from_account":"acct_001","to_account":"acct_002","token_class":"INR_STABLE","amount":"500"}
{"ok":true,"audit_id":"f2bcb54d-4f4c-4cd1-9e27-4d0e76c3e61b","data":{"transfer_id":"tr_a1b2c3d4e5f6","status":"committed","executed_at":"2026-05-09T12:10:00+00:00","from_account":"acct_001","to_account":"acct_002","token_class":"INR_STABLE","amount":"500","audit_id":"f2bcb54d-4f4c-4cd1-9e27-4d0e76c3e61b","policy_result":{"eligible":true,"code":null,"message":null,"detail":{"token_class":"INR_STABLE","requested_amount":"500","delegated_limit":"1000","checks_failed":[],"checks_passed":["delegation_active","token_class","from_account_scope","amount_limit","sufficient_balance"]}}}}
```
