
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

## Deploy
### Using build script(recommended):
1. Open this function's directory in Vscode. 
2. Configure project params in .vscode/config.properties.
3. Run build script:
    ### Linux: ```.vscode/deploy.sh``` OR Run Build task in Vscode (ctrl + shift + B)
    ### Windows: `.vscode/deploy.ps1` OR Run Build task in Vscode (ctrl + shift + B)
 