# Deploying Django to Azure

This guide covers how to deploy your Django application to Azure App Service, using Azure Database for PostgreSQL and Azure Blob Storage.

## Prerequisites
- An active Azure subscription.
- Azure CLI installed locally (optional, but recommended) or access to the Azure Portal.

## Step 1: Create Resource Group
Create a resource group to hold all your resources.
1. Go to "Resource groups" in Azure Portal.
2. Click "Create".
3. Name it (e.g., `socialapp-rg`) and select a region.

## Step 2: Create Azure Database for PostgreSQL
1. Search for "Azure Database for PostgreSQL servers" (Flexible Server is recommended).
2. Click "Create".
3. **Resource Group**: Select `socialapp-rg`.
4. **Server name**: Give it a unique name (e.g., `socialapp-db`).
5. **Authentication**: Choose "PostgreSQL authentication only" (or both). set an Admin username and password. **Write these down.**
6. **Networking**: 
    - Allow public access from valid IP addresses.
    - **Important**: Check "Allow public access from any Azure service within Azure to this server" so the App Service can connect.
7. Review and Create.

## Step 3: Create Azure Blob Storage (for Images)
1. Search for "Storage accounts".
2. Click "Create".
3. **Resource Group**: `socialapp-rg`.
4. **Storage account name**: Unique name (e.g., `socialappstorage`).
5. **Redundancy**: LRS (Locally-redundant storage) is cheapest and sufficient for dev/test.
6. Review and Create.
7. Once created, go to the resource.
8. Under "Data storage" > "Containers", create a new container named `media`.
    - **Public access level**: "Blob (anonymous read access for blobs only)" so images can be served publically.
9. Go to "Security + networking" > "Access keys".
10. Copy "Key 1" -> This is your `AZURE_ACCOUNT_KEY`.

## Step 4: Create Azure App Service (Web App)
1. Search for "App Services".
2. Click "Create" > "Web App".
3. **Resource Group**: `socialapp-rg`.
4. **Name**: Unique name (e.g., `socialapp-web`).
5. **Publish**: Code.
6. **Runtime stack**: Python 3.10 (or matching your local version).
7. **Region**: Same as your other resources.
8. **Pricing Plan**: Basic (B1) or Standard is good for production. Free (F1) works for testing but has limits.
9. Review and Create.

## Step 5: Configure Environment Variables
Go to your new Web App resource.
1. Navigate to **"Settings"** > **"Environment variables"**.
2. Add the following "App settings":
    - `SCM_DO_BUILD_DURING_DEPLOYMENT`: `true`
    - `DJANGO_SETTINGS_MODULE`: `socialapp.settings`
    - `SECRET_KEY`: (Your random secret key)
    - `DEBUG`: `False`
    - `ALLOWED_HOSTS`: `*` (or your specific specific app url)
    - `DATABASE_URL`: `postgres://<admin_user>:<password>@<server_name>.postgres.database.azure.com:5432/postgres` (Construct this from your DB credentials)
    - `AZURE_ACCOUNT_NAME`: `socialappstorage` (your storage account name)
    - `AZURE_ACCOUNT_KEY`: (The key you copied in Step 3)
    - `AZURE_CONTAINER`: `media`
3. Click "Apply".

## Step 6: Configure Startup Command
1. Navigate to **"Settings"** > **"Configuration"** > **"General settings"**.
2. In "Startup Command", enter:
   ```bash
   sh startup.sh
   ```
   (This runs the script we created to migrate DB and start the server).

## Step 7: Deploy Code
You have a few options. Since you are set up locally:

**Option A: Local Git (Simplest)**
1. In Web App > **"Deployment Center"**.
2. Source: **"Local Git"**.
3. Save.
4. Copy the "Git Clone Uri".
5. In your local terminal (`d:\Social_app\socialapp`):
   ```bash
   git init # if not already
   git remote add azure <paste_git_clone_uri>
   git add .
   git commit -m "Deploy to Azure"
   git push azure master
   ```
   (You will be prompted for "Deployment credentials". You can set these in Deployment Center > "Local Git/FTPS credentials").

**Option B: GitHub Actions**
1. In Deployment Center, select "GitHub".
2. Connect your account and select your repo.
3. Azure will automatically create a workflow file to deploy on push.

## Verification
1. Visit your App Service URL (`https://socialapp-web.azurewebsites.net`).
2. It might take a minute to start. If you see the login page, it works!
3. Try uploading a profile picture. It should get saved to your Azure Blob Storage container.
