import aiohttp
import asyncio
import os
import zipfile
from bs4 import BeautifulSoup


BASE_URL = "https://www.scrapethissite.com/pages/forms/?page="


HTML_DIR = "hockey_html"


async def fetch_page(session, page_number):
    """Fetch HTML content of a single page."""
    url = f"{BASE_URL}{page_number}"
    async with session.get(url) as response:
        if response.status == 200:
            html_content = await response.text()
            return html_content
        else:
            print(f"Failed to fetch page {page_number}: HTTP {response.status}")
            return None


async def fetch_all_pages():
    """Fetch all pages and save them as HTML files."""
    os.makedirs(HTML_DIR, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, page) for page in range(1, 25)] 
        html_pages = await asyncio.gather(*tasks)

        for idx, html in enumerate(html_pages, start=1):
            if html:
                with open(f"{HTML_DIR}/{idx}.html", "w", encoding="utf-8") as file:
                    file.write(html)
                print(f"Saved: {HTML_DIR}/{idx}.html")


def create_zip_file():
    """Compress all HTML files into a single ZipFile."""
    zip_filename = "hockey_pages.zip"
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for filename in os.listdir(HTML_DIR):
            zipf.write(os.path.join(HTML_DIR, filename), filename)
    print(f"Created {zip_filename}")


if __name__ == "__main__":
    asyncio.run(fetch_all_pages()) 
    create_zip_file()  
