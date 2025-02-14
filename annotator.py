import pandas as pd
import requests
import concurrent.futures

# Api 
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

# Define categories
CATEGORIES = ["Deep Learning", "Computer Vision", "Reinforcement Learning", "NLP", "Optimization"]

def classify_paper(title, abstract):
    """Send a request to the Gemini API to classify a research paper."""
    prompt = f"""
    Classify the following research paper into one of the categories: {', '.join(CATEGORIES)}.
    Return only the category name.

    Title: {title}
    Abstract: {abstract}
    """

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(GEMINI_URL, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
        response_json = response.json()

        # Extract category from response
        if "candidates" in response_json:
            return response_json["candidates"][0]["content"]["parts"][0]["text"].strip()
        else:
            return "Unknown"
    
    except requests.exceptions.RequestException:
        return "API Error"

def process_row(row):
    """Process a single row and classify the paper."""
    return classify_paper(row["Title"], row["Abstract"])

# Load the scraped dataset
df = pd.read_csv("neurips_papers.csv")

# Use parallel processing to annotate papers
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    df["Category"] = list(executor.map(process_row, df.to_dict(orient="records")))

df.to_csv("neurips_papers_annotated.csv", index=False)
print(f"✅ Annotation completed! {len(df)} papers classified and saved to neurips_papers_annotated.csv")
