import logging
import os
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import requests

# Configure logging
logging.basicConfig(
    filename='D:/Medic/MediGo/ProgramLog.log',
    level=logging.INFO,
    format='1MG DRUGINFO %(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

def fetch_page_content(url):
    """
    Fetches the content of a webpage using Playwright.

    Args:
        url (str): The URL of the webpage to fetch.

    Returns:
        BeautifulSoup: Parsed HTML content of the webpage.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            content = page.content()
            browser.close()
            logging.info('Request sent to %s', url)
            return BeautifulSoup(content, 'html.parser')
    except Exception as e:
        logging.error('Failed to fetch page content from %s: %s', url, e)
        return None

def extract_image_links(page_soup):
    """
    Extracts image links from the parsed HTML content.

    Args:
        page_soup (BeautifulSoup): Parsed HTML content of a webpage.

    Returns:
        list: A list of image URLs.
    """
    if not page_soup:
        logging.warning('No content to parse for image links')
        return []

    image_elements = page_soup.find_all(class_='card-slide')
    if not image_elements:
        logging.warning('No image links found on the page')
        return []

    image_links = []
    for image_group in image_elements:
        for image in image_group.find_all('img'):
            if image.has_attr('src'):
                image_links.append(image['src'])
                logging.info('Found image source: %s', image['src'])

    return image_links

def download_image(url, save_path="MediGo/MedicDB/Crawlers/MedicImages", file_name=None):
    """
    Downloads an image from the given URL and saves it to the specified directory.

    Args:
        url (str): URL of the image to download.
        save_path (str): Directory where the image will be saved. Default is 'downloads'.
        file_name (str): Optional. Name of the file to save. If not provided, it uses the name from the URL.

    Returns:
        str: Full path to the saved image, or None if download fails.
    """
    try:
        os.makedirs(save_path, exist_ok=True)
        file_name = file_name or url.split('/')[-1]
        full_path = os.path.join(save_path, file_name)

        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(full_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        logging.info('Image successfully downloaded: %s', full_path)
        return full_path
    except requests.exceptions.RequestException as e:
        logging.error('Failed to download image from %s: %s', url, e)
        return None

def get_drug_data(drug_link, drug_name, drug_code_name):
    """
    Fetches drug data from the given link, extracts image links, and downloads them.

    Args:
        drug_link (str): URL of the drug page.
        drug_name (str): Name of the drug.
        drug_code_name (str): Code name of the drug.
    """
    page_soup = fetch_page_content(drug_link)
    image_links = extract_image_links(page_soup)

    if image_links:
        logging.info('Found %d image link(s) for drug: %s', len(image_links), drug_name)
        for i, image_link in enumerate(image_links):
            download_image(image_link, save_path="MediGo/MedicDB/Crawlers/MedicImages", file_name=f"{drug_code_name}_{i}.jpg")
    else:
        logging.warning('No images to download for drug: %s', drug_name)

# Example usage

get_drug_data('https://www.1mg.com/drugs/vasograin-tablet-116573', 'Vasograin', 'vasograin')
