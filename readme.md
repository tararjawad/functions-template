<img src="https://avatars2.githubusercontent.com/u/2810941?v=3&s=96" alt="Google Cloud Platform logo" title="Google Cloud Platform" align="right" height="96" width="96"/>

# Cloud functions for {project_name} project

This repo contains all the cloud functions for the serverless {project} project.


## Deploy
### Using build script(recommended):
1. Open function directory in Vscode. (This readme is in the parent directory, not the directory of the specific function you want to deploy)
2. Configure project params in .vscode/config.properties.
3. Run build script:
    ### Linux: ```.vscode/deploy.sh``` OR Run Build task in Vscode (ctrl + shift + B)
    ### Windows: `.vscode/deploy.ps1` OR Run Build task in Vscode (ctrl + shift + B)
 

### Using cloud code:
    1. create a function named as the directory name using google cloud console
    2. setup appropriate firestore trigger type with filter with reference to the documentation of the function
    3. then deploy the cloud function using cloud code extension in VSCode.


---
## setup-campaign
### summary: 
setup a campaign when a tenant creates one

## retell-callback
### summary:
### trigger:
### what it does:


## GCP Cloud shell tips:
1. 
    use git credentials helper so you don't have to login everytime session resets:
    `git config --global credential.helper store`

2. set gcp project in .bashrc
    ```
    nano ~/.bashrc
    ```
    ADD:
    ```
    gcloud config set project phonecall-bot-v1
    ```
