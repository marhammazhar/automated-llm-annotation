import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://papers.nips.cc"

def get_paper_links(year="2023"):
    """Extracts paper links for a given NeurIPS year."""
    url = f"{BASE_URL}/paper_files/paper/{year}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"❌ Failed to retrieve paper list for {year}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    paper_links = []

    # Find all links to individual papers
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith(f"/paper_files/paper/{year}/hash/"):
            full_url = BASE_URL + href
            paper_links.append(full_url)

    print(f"✅ Found {len(paper_links)} papers for {year}")
    return paper_links

def scrape_papers(year="2023"):
    """Scrapes titles and abstracts from NeurIPS papers."""
    paper_links = get_paper_links(year)
    papers = []

    if not paper_links:
        print("❌ No papers found.")
        return []

    for paper_url in paper_links:
        paper_page = requests.get(paper_url)
        paper_soup = BeautifulSoup(paper_page.text, "html.parser")

        # Extract title and abstract
        title = paper_soup.find("h4")
        abstract = paper_soup.find("p")

        if title:
            title_text = title.text.strip()
            abstract_text = abstract.text.strip() if abstract else "No abstract available"
            papers.append({"Title": title_text, "Abstract": abstract_text})
            print(f"✅ Scraped: {title_text}")

    return papers

# Run the scraper
papers_data = scrape_papers("2023")


if papers_data:
    df = pd.DataFrame(papers_data)
    df.to_csv("neurips_papers.csv", index=False)
    print(f"✅ Scraping completed! {len(df)} papers saved to neurips_papers.csv")
else:
    print("❌ No papers found. Check the website structure.")
