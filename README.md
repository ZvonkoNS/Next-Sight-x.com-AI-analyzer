
# **Next Sight - X.com AI Analyzer**

## **Overview**
The Next Sight X.com AI Analyzer is a powerful tool designed to monitor harmful online behavior on X.com (formerly Twitter). It fetches tweets from a user-specified account, analyzes their content using advanced Natural Language Processing (NLP) techniques and keyword matching, and generates a professional PDF report.

---

## **Features**
- Fetch tweets from any public X.com profile.
- Analyze tweets for:
  - **Toxicity**
  - **Hate Speech**
  - **Cyberbullying**
  - **Grooming**
  - **Aggressive Behavior**
  - **Terrorism**
  - **Drugs**
- Generate a professionally formatted PDF report:
  - The first page contains a centered logo and report title.
  - The second page onwards includes detailed findings.
- Graceful exit on `Ctrl+C` or `Ctrl+X`.

---

## **Prerequisites**
### **System Requirements**
- Python 3.8 or higher.
- A stable internet connection.

### **Python Dependencies**
Install the required libraries:
```bash
pip install fpdf requests transformers textblob
```

### **Assets**
Ensure the following are in the project directory:
- `keywords.json`: Contains categories and associated keywords.
- `assets/logo.jpg`: A logo file to include in the report.

---

## **Setup**
1. Clone the repository or download the script files.
2. Create a `keywords.json` file with the structure (NOTE: The provided keywords.json file already has an extensive list, that you can extend even further):
   ```json
   {
       "cyberbullying": ["idiot", "stupid", "worthless"],
       "hate_speech": ["racist", "bigot", "hate"],
       "grooming": ["DM me", "let's meet", "secret"],
       "drugs": ["cocaine", "meth", "weed", "deal"],
       "terrorism": ["bomb", "ISIS", "attack", "jihad"],
       "aggressive_behavior": ["kill", "hurt", "destroy"]
   }
   ```
3. Add the logo to the `assets/` folder as `logo.jpg`.

---

## **Getting an X.com Bearer Token**
To fetch tweets from X.com, you need a **Bearer Token** from the X.com Developer platform. Follow these steps:

### **Step 1: Sign Up for a Developer Account**
1. Go to the [Twitter Developer Portal](https://developer.twitter.com/).
2. Log in with your X.com account credentials.
3. If you don’t already have a developer account, follow the prompts to apply. Provide the required details.

### **Step 2: Create a New App**
1. Navigate to the **Dashboard**.
2. Click **Create App** or **Create Project**.
3. Provide an app name and complete the setup process.

### **Step 3: Generate Bearer Token**
1. Once the app is created, go to the **Keys and Tokens** section.
2. Under **Authentication Tokens**, generate a Bearer Token.
3. Copy the token and keep it secure.

---

## **Usage**
### **Step 1: Run the Script**
Run the script from the command line:
```bash
python next_sight_analyzer.py
```

### **Step 2: Provide Your Bearer Token**
When prompted, enter your X.com Bearer Token:
```
🔑 Enter your X.com (Twitter) Bearer Token:
```

### **Step 3: Enter a Profile URL**
Enter the X.com profile URL you want to analyze:
```
🌐 Enter the X.com profile URL to analyze: https://twitter.com/exampleuser
```

### **Step 4: Wait for Analysis**
The script will:
1. Fetch tweets from the specified profile.
2. Analyze the tweets for harmful behavior.
3. Generate a PDF report in the `reports/` folder.

### **Step 5: View the Report**
Locate the generated report in the `reports/` folder. The filename will follow this format:
```
report_YYYYMMDD-HHMMSS.pdf
```

---

## **File Structure**
```
Next_Sight_AI_Analyzer/
│
├── next_sight_analyzer.py        # Main script
├── README.md                     # Instructions and documentation
├── requirements.txt              # Python dependencies
├── keywords.json                 # Keywords for analysis
├── assets/
│   └── logo.jpg                  # Logo for the report
└── reports/                      # Generated PDF reports
```

---

## **Report Layout**
1. **Page 1: Cover Page**
   - **Centered logo** at the top.
   - **Report title**: "Next Sight AI generated report for x.com account [username]" centered on the page.

2. **Page 2 Onwards: Detailed Report**
   - Total tweets analyzed.
   - Flagged tweets with:
     - **Category**
     - **Content**
     - **Toxicity Score**

---

## **Graceful Exit**
- Press `Ctrl+C` or `Ctrl+X` anytime to exit the script cleanly.

---

## **Troubleshooting**
### **Common Issues**
1. **Error: "TTF Font file not found"**
   - Ensure the `assets/logo.jpg` exists in the correct directory.

2. **Error: "Failed to fetch tweets"**
   - Verify the profile URL is correct and public.
   - Ensure your Bearer Token is valid.

3. **KeyboardInterrupt**
   - If you accidentally exit with `Ctrl+C`, simply rerun the script.

---

## **Contact**
**Next Sight**  
Website: [www.next-sight.com](https://www.next-sight.com)  
Email: [info@next-sight.com](mailto:info@next-sight.com)  

**For more advanced investigation**:  
We specialize in OSINT, HUMINT, and comprehensive background checks. Contact us for worldwide investigations tailored to your specific needs.

**Training Opportunities**:  
Want to learn how to conduct professional investigations using the latest tools and techniques? Ask about our customized training programs for individuals, organizations, and law enforcement.

---

