import base64
import os

import requests
from requests.exceptions import HTTPError


class ConfluenceClient:
    """A client for interacting with the Confluence API."""

    def __init__(self):
        domain = os.getenv("CONFLUENCE_DOMAIN")
        if not domain:
            raise ValueError("CONFLUENCE_DOMAIN environment variable not set.")
        self.base_url = f"https://{domain}/wiki/rest/api"
        self.username = os.getenv("CONFLUENCE_USERNAME")
        self.api_token = os.getenv("CONFLUENCE_API_TOKEN")
        self.space_key = os.getenv("CONFLUENCE_SPACE_KEY")
        if not self.username:
            raise ValueError("CONFLUENCE_USERNAME environment variable not set.")
        if not self.api_token:
            raise ValueError("CONFLUENCE_API_TOKEN environment variable not set.")
        if not self.space_key:
            raise ValueError("CONFLUENCE_SPACE_KEY environment variable not set.")

        credentials = f"{self.username}:{self.api_token}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        self.headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json",
        }

        # For local development behind corporate proxies, allow disabling SSL verification.
        # This is insecure and should not be used in production.
        self.verify = os.getenv("REQUESTS_VERIFY", "true").lower() != "false"
        if not self.verify:
            print(
                "\n"
                "!!! WARNING: SSL verification is DISABLED for ConfluenceClient. !!!\n"
                "This is insecure and should only be used for local development.\n"
                "Do not use this setting in production.\n"
            )

    def get_page_by_title(self, title: str) -> dict | None:
        """Gets a page by title."""
        url = f"{self.base_url}/content"
        params = {"spaceKey": self.space_key, "title": title}
        response = requests.get(url, headers=self.headers, params=params, verify=self.verify)
        try:
            response.raise_for_status()
        except HTTPError as e:
            print(f"Error getting page by title: {e.response.text}")
            raise
        results = response.json().get("results")
        if results:
            return results[0]
        return None

    def get_child_pages(self, page_id: str) -> list:
        """Gets the child pages of a given page."""
        url = f"{self.base_url}/content/{page_id}/child/page"
        response = requests.get(url, headers=self.headers, verify=self.verify)
        try:
            response.raise_for_status()
        except HTTPError as e:
            print(f"Error getting child pages: {e.response.text}")
            raise
        return response.json().get("results", [])

    def update_page(self, page_id: str, title: str, version: int) -> dict:
        """Updates the title of a page."""
        url = f"{self.base_url}/content/{page_id}"
        data = {
            "version": {"number": version},
            "title": title,
            "type": "page",
        }
        response = requests.put(url, headers=self.headers, json=data, verify=self.verify)
        try:
            response.raise_for_status()
        except HTTPError as e:
            print(f"Error updating page: {e.response.text}")
            raise
        return response.json()

    def get_page_content(self, page_id: str) -> dict:
        """Gets the content of a Confluence page."""
        url = f"{self.base_url}/content/{page_id}?expand=body.storage"
        response = requests.get(url, headers=self.headers, verify=self.verify)
        try:
            response.raise_for_status()
        except HTTPError as e:
            print(f"Error getting page content: {e.response.text}")
            raise
        return response.json()

    def create_page(
        self, space_key: str, parent_id: str, title: str, content: str
    ) -> dict:
        """Creates a new Confluence page."""
        url = f"{self.base_url}/content/"
        data = {
            "type": "page",
            "title": title,
            "space": {"key": space_key},
            "ancestors": [{"id": parent_id}],
            "body": {"storage": {"value": content, "representation": "storage"}},
        }
        response = requests.post(url, headers=self.headers, json=data, verify=self.verify)
        try:
            response.raise_for_status()
        except HTTPError as e:
            print(f"Error creating page: {e.response.text}")
            raise
        return response.json()

    def copy_page(self, page_id: str, destination: dict) -> dict:
        """Copies a Confluence page."""
        url = f"{self.base_url}/content/{page_id}/copy"
        print(f"DEBUG: copy_page request body (destination): {destination}") # Added print statement
        response = requests.post(url, headers=self.headers, json=destination, verify=self.verify)
        try:
            response.raise_for_status()
        except HTTPError as e:
            print(f"Error copying page: {e.response.text}")
            raise
        return response.json()
