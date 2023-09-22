import requests
from config import Config
import os
import json
from vector_store_manager import ingest_docs
import re

def get_token(code):
    token_data = {
        "grant_type": "authorization_code",
        "client_id": Config.CLIENT_ID,
        "client_secret": Config.CLIENT_SECRET,
        "code": code,
        "redirect_uri": Config.REDIRECT_URI,
    }
    response = requests.post(Config.TOKEN_URL, data=token_data)
    return response.json().get("access_token")

def get_all_pages(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    all_data = {}

    cloud_response = requests.get(
        Config.CONFLUENCE_ACCESSIBLE_RESOURCES_URL,
        headers=headers,
    )

    sites = cloud_response.json()
    for site in sites:
        cloudid = site["id"]
        site_name = site["name"]
        all_data[site_name] = {}

        # Get all spaces in the site
        spaces_url = f"https://api.atlassian.com/ex/confluence/{cloudid}/wiki/rest/api/space"
        spaces_response = requests.get(spaces_url, headers=headers)
        if spaces_response.status_code == 200:
            spaces = spaces_response.json()["results"]

            # Iterate over all spaces
            for space in spaces:
                space_key = space["key"]
                all_data[site_name][space_key] = []

                # Get all pages in the space
                pages_url = f"https://api.atlassian.com/ex/confluence/{cloudid}/wiki/rest/api/content?spaceKey={space_key}&expand=body.view"
                pages_response = requests.get(pages_url, headers=headers)
                if pages_response.status_code == 200:
                    pages = pages_response.json()["results"]
                    all_data[site_name][space_key].extend(pages)
    
    root_path = save_to_local_files(all_data)
    ingest_docs(root_path)
    return all_data

def save_to_local_files(all_data):
    base_dir = "confluence_data"
    
    # Create the base directory if it doesn't exist
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        
    for site, spaces in all_data.items():
        site_dir = os.path.join(base_dir, site)
        
        # Create directory for each site
        if not os.path.exists(site_dir):
            os.makedirs(site_dir)
        
        for space, pages in spaces.items():
            space_dir = os.path.join(site_dir, space)
            
            # Create directory for each space in each site
            if not os.path.exists(space_dir):
                os.makedirs(space_dir)
                
            for page in pages:
                sanitized_title = sanitize_filename(page['title'])
                page_file = os.path.join(space_dir, f"{page['id']}_{sanitized_title}.html")
                
                # Save each page as a JSON file in its respective directory
                with open(page_file, 'w') as f:
                    f.write(page["body"]["view"]["value"])
    
    print("All data has been saved to local files.")
    return base_dir

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', '', filename).strip()