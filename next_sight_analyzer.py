import os
import json
import requests
import getpass
import time
from fpdf import FPDF
from transformers import pipeline
from textblob import TextBlob
import signal
import sys
from cryptography.fernet import Fernet

# ==========================================
# Initialization & Configuration
# ==========================================

# Constants
REPORTS_FOLDER = "reports"
LOGO_PATH = "assets/logo.jpg"
KEYWORDS_FILE = "keywords.json"  # File containing keyword categories
ENC_FILE = "api_key.enc"         # Encrypted file for Bearer Token
KEY_FILE = "encryption_key.key"  # Encryption key file

# NLP Classifier Initialization
try:
    classifier = pipeline("text-classification", model="unitary/toxic-bert")
except Exception as e:
    print(f"❌ Error initializing NLP model: {e}")
    sys.exit(1)

# Create reports folder if not exists
if not os.path.exists(REPORTS_FOLDER):
    os.makedirs(REPORTS_FOLDER)

# ==========================================
# Graceful Exit Setup (Ctrl+C or Ctrl+X)
# ==========================================
def graceful_exit(signal_received, frame):
    print("\n🛑 Exiting script. Goodbye!")
    sys.exit(0)

# Capture Ctrl+C (SIGINT) or Ctrl+X (SIGTERM) for graceful exit
signal.signal(signal.SIGINT, graceful_exit)
signal.signal(signal.SIGTERM, graceful_exit)

# ==========================================
# UX Setup
# ==========================================
def print_logo():
    print("""
    ===============================================
           🌐 Next Sight - X.com AI Analyzer
    ===============================================
       Cutting-edge analysis tool for monitoring 
    harmful online behavior on x.com (ex Tweeter).
    ===============================================
       www.next-sight.com | info@next-sight.com
    ===============================================
        Contact us for worldwide investigations
    =============================================== 
    """)

# ==========================================
# Encryption Key Management
# ==========================================
def load_or_create_encryption_key():
    """Load the encryption key, or create one if it doesn't exist."""
    if not os.path.exists(KEY_FILE):
        print("🔑 No encryption key found. Generating a new one...")
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        print("✅ Encryption key generated and saved.")
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    return key

# ==========================================
# Bearer Token Management
# ==========================================
def get_bearer_token():
    """Retrieve or prompt for a Bearer Token and store it securely."""
    key = load_or_create_encryption_key()
    cipher = Fernet(key)

    if os.path.exists(ENC_FILE):
        # Decrypt and return the Bearer Token
        with open(ENC_FILE, "rb") as enc_file:
            encrypted_token = enc_file.read()
        token = cipher.decrypt(encrypted_token).decode("utf-8")
        return token
    else:
        # Prompt the user for a new Bearer Token
        print("🛑 Bearer Token not found!")
        token = getpass.getpass("🔑 Enter your X.com (Twitter) Bearer Token: ").strip()

        # Encrypt and save the token
        encrypted_token = cipher.encrypt(token.encode("utf-8"))
        with open(ENC_FILE, "wb") as enc_file:
            enc_file.write(encrypted_token)
        print("✅ Bearer Token encrypted and saved as api_key.enc.")
        return token

# ==========================================
# Fetch Tweets
# ==========================================
def fetch_tweets(bearer_token, profile_url):
    try:
        username = profile_url.split("/")[-1]
        url = f"https://api.twitter.com/2/users/by/username/{username}"
        headers = {"Authorization": f"Bearer {bearer_token}"}
        
        # Get user ID from username
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTP errors
        user_id = response.json().get("data", {}).get("id")
        if not user_id:
            print("❌ Could not retrieve user ID. Please check the profile URL.")
            return None, None

        # Fetch tweets
        tweets_url = f"https://api.twitter.com/2/users/{user_id}/tweets"
        params = {"tweet.fields": "created_at"}
        response = requests.get(tweets_url, headers=headers, params=params)
        response.raise_for_status()
        print("✅ Tweets fetched successfully!")
        return response.json().get("data", []), username
    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error occurred: {http_err}")
    except Exception as e:
        print(f"❌ An error occurred while fetching tweets: {e}")
    return None, None

# ==========================================
# Load Keywords
# ==========================================
def load_keywords():
    try:
        if not os.path.exists(KEYWORDS_FILE):
            print(f"❌ Keywords file not found: {KEYWORDS_FILE}")
            return {}
        with open(KEYWORDS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error decoding keywords file: {e}")
    except Exception as e:
        print(f"❌ Error loading keywords file: {e}")
    return {}

# ==========================================
# AI Analysis for Behavior Categorization
# ==========================================
def analyze_tweet_with_nlp_and_keywords(tweet, keywords):
    flagged = []
    try:
        # NLP Sentiment Analysis
        nlp_result = classifier(tweet)[0]
        toxicity_score = nlp_result["score"] if nlp_result["label"] == "toxic" else 0

        # Flag if NLP score is high
        if toxicity_score > 0.85:  # Adjust threshold as needed
            flagged.append({"content": tweet, "category": "General Toxicity", "score": toxicity_score})

        # Keyword Matching
        for category, words in keywords.items():
            if any(word.lower() in tweet.lower() for word in words):
                flagged.append({"content": tweet, "category": category, "score": toxicity_score})
    except Exception as e:
        print(f"❌ Error analyzing tweet: {e}")
    return flagged

def analyze_tweets(tweets, keywords):
    flagged_tweets = []
    try:
        for tweet in tweets:
            content = tweet["text"]
            flagged = analyze_tweet_with_nlp_and_keywords(content, keywords)
            flagged_tweets.extend(flagged)
    except Exception as e:
        print(f"❌ Error analyzing tweets: {e}")
    return flagged_tweets

# ==========================================
# Generate PDF Report
# ==========================================
def generate_pdf_report(flagged_tweets, profile_url, username, total_tweets):
    try:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        # First Page - Cover Page
        pdf.add_page()
        if os.path.exists(LOGO_PATH):
            pdf.image(LOGO_PATH, x=75, y=20, w=60)  # Center the logo

        pdf.ln(90)  # Space after logo
        pdf.set_font("Arial", size=16, style="B")
        pdf.multi_cell(0, 10, txt=f"Next Sight AI generated report for x.com account\n{username}", align="C")

        # Second Page - Detailed Report
        pdf.add_page()
        pdf.set_font("Arial", size=14)
        pdf.cell(200, 10, txt=f"Number of Tweets Analyzed: {total_tweets}", ln=True)
        pdf.ln(10)

        if not flagged_tweets:
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="No suspicious activity detected.", ln=True)
        else:
            pdf.cell(200, 10, txt="Detailed Flagged Tweets:", ln=True)
            pdf.ln(10)

            for idx, tweet in enumerate(flagged_tweets, 1):
                pdf.set_font("Arial", size=13, style="B")
                pdf.cell(200, 10, txt=f"Flagged Tweet {idx}:", ln=True)
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, txt=f"Category: {tweet['category']}\nContent: {tweet['content']}\nToxicity Score: {tweet['score']:.2f}")
                pdf.ln(5)

        # Save Report
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        report_path = os.path.join(REPORTS_FOLDER, f"report_{timestamp}.pdf")
        pdf.output(report_path)
        print(f"📄 Report generated: {report_path}")
    except Exception as e:
        print(f"❌ Error generating PDF report: {e}")

# ==========================================
# Main Functionality
# ==========================================
def main():
    print_logo()
    try:
        bearer_token = get_bearer_token()
        keywords = load_keywords()

        if not keywords:
            print("⚠️ No keywords loaded. Exiting.")
            return

        # Prompt user for profile URL
        profile_url = input("🌐 Enter the X.com profile URL to analyze: ").strip()
        tweets, username = fetch_tweets(bearer_token, profile_url)

        if tweets is not None:
            flagged_tweets = analyze_tweets(tweets, keywords)
            generate_pdf_report(flagged_tweets, profile_url, username, len(tweets))
        else:
            print("No tweets were fetched or analyzed.")
    except KeyboardInterrupt:
        print("\n🛑 Script interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
