from datetime import date
from unittest.mock import MagicMock, patch

import pytest
from backend.src.models.config import ConfluenceConfig
from backend.src.services.confluence_service import ConfluenceService


# Fixture for a mock ConfluenceConfig
@pytest.fixture
def mock_confluence_config():
    return ConfluenceConfig(
        enabled=True,
        schedule="0 10 * * 1",
        confluence_url="https://your-domain.atlassian.net/wiki/spaces/SPACE/pages/12345",
        slack_channel="C12345678"
    )

# Mocking the requests library for API calls
@pytest.fixture
def mock_requests():
    with patch('requests.get') as mock_get, \
         patch('requests.post') as mock_post:
        yield mock_get, mock_post

def test_generate_report_title():
    test_date = date(2025, 1, 6) # Monday of W2 2025
    expected_title = "2025 W02 RD4 Team Weekly Report (0106-0110)"
    title = ConfluenceService._generate_report_title("RD4 Team", "Weekly Report", test_date)
    assert title == expected_title

    test_date_yearend = date(2025, 12, 29) # Monday of W1 2026
    expected_title_yearend = "2026 W01 RD4 Team Weekly Report (1229-0102)"
    title_yearend = ConfluenceService._generate_report_title("RD4 Team", "Weekly Report", test_date_yearend)
    assert title_yearend == expected_title_yearend

def test_get_page_content_success(mock_confluence_config, mock_requests):
    mock_get, _ = mock_requests
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "body": {"storage": {"value": "Original content"}}
    }

    service = ConfluenceService()
    content = service._get_page_content(mock_confluence_config.confluence_url)
    assert content == "Original content"

def test_get_page_content_failure(mock_confluence_config, mock_requests):
    mock_get, _ = mock_requests
    mock_get.return_value.status_code = 404

    service = ConfluenceService()
    with pytest.raises(Exception, match="Failed to retrieve Confluence page content"):
        service._get_page_content(mock_confluence_config.confluence_url)

@patch('backend.src.services.confluence_service.ConfluenceService._get_page_content')
@patch('backend.src.services.confluence_service.ConfluenceService._generate_report_title')
def test_create_weekly_report_success(
    mock_generate_title, mock_get_content,
    mock_confluence_config, mock_requests
):
    mock_get, mock_post = mock_requests
    mock_get_content.return_value = "Original content"
    mock_generate_title.return_value = "New Report Title"

    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"_links": {"webui": "http://new-page-url"}}

    service = ConfluenceService()
    result_url = service.create_weekly_report(mock_confluence_config)

    assert result_url == "http://new-page-url"
    mock_get_content.assert_called_once()
    mock_generate_title.assert_called_once()
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert "New Report Title" in kwargs['json']['title']
    assert "Original content" in kwargs['json']['body']['storage']['value']

def test_create_weekly_report_failure(
    mock_confluence_config, mock_requests,
    mock_get_page_content=None, mock_generate_report_title=None
):
    mock_get, mock_post = mock_requests
    mock_get_page_content = MagicMock(return_value="Original content")
    mock_generate_report_title = MagicMock(return_value="New Report Title")
    mock_post.return_value.status_code = 500

    service = ConfluenceService()
    with pytest.raises(Exception, match="Failed to create Confluence page"):
        service.create_weekly_report(mock_confluence_config)
    mock_post.assert_called_once()
