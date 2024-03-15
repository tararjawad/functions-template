# Cloud functions for callstrike project

This repo contains all the cloud functions for the serverless callstrike project.


## Deploy
1. create a function named as the directory name using google cloud console
2. setup appropriate firestore trigger type with filter
3. then deploy the cloud function using cloud code extension in VSCode.

---
## setup-campaign
### summary: 
setup a campaign when a tenant creates one
### trigger:
#### summary: 
    firestore trigger document created in collection campaigns
#### type:
    google.cloud.firestore.document.v1.created (default)
#### path:
    tenants/{tenant_id}/campaigns/{campaign_id}
### what it does:
- Copy *employees* belonging to the set *groups* of the campaign to *pending_calls* sub-collection
- Set status to *running* or *no_license*
- Set *users_targeted* count
- add *created_at* timestamp


## retell-callback
### summary:
### trigger:
### what it does: