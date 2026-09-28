import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# 1. Fetch the clean dataset directly from the internet (no local file needed!)
data_url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
df = pd.read_csv(data_url, sep='\t', header=None, names=['label', 'text'])

# 2. Data Cleaning
df = df.dropna()
df['text'] = df['text'].astype(str)

# 3. Split the data
X_train, X_test, y_train, y_test = train_test_split(
    df['text'],   
    df['label'],  
    test_size=0.2, 
    random_state=42
)

# 4. Vectorize the Text
vectorizer = TfidfVectorizer(stop_words='english')
X_train_vectorized = vectorizer.fit_transform(X_train)

# 5. Train the Brain
classifier = MultinomialNB()
classifier.fit(X_train_vectorized, y_train)

# 6. Test with a New Threat
new_email = ["URGENT: Your network account has been compromised. Click here to reset your password and claim a $50 reward."]
new_email_vectorized = vectorizer.transform(new_email)
prediction = classifier.predict(new_email_vectorized)

if prediction[0] == 1 or prediction[0] == 'spam':
    print("Result: Threat Detected: SPAM")
else:
    print("Result: Clear: SAFE EMAIL")
  # 6. Scan a batch of new emails from a CSV

# --- NEW: Create a sample file automatically so you don't get an error ---
sample_data = {
    'text': [
        "Hey, let's grab coffee tomorrow.",
        "WINNER! Claim your free vacation now by clicking here.",
        "Don't forget the team meeting at 3 PM.",
        "URGENT: Your account will be locked. Update your billing info.",
        None # A blank row to test our data cleaner!
    ]
}
pd.DataFrame(sample_data).to_csv('unscanned_emails.csv', index=False)
# -------------------------------------------------------------------------

# Read the file we just created
new_emails_df = pd.read_csv('unscanned_emails.csv')

# Clean the data: Drop blank rows and force the 'text' column to be strings
new_emails_df = new_emails_df.dropna(subset=['text'])
new_emails_df['text'] = new_emails_df['text'].astype(str)

# Convert the text into numbers using your trained vectorizer
vectorized_batch = vectorizer.transform(new_emails_df['text'])

# Predict the threat level for every single row instantly
predictions = classifier.predict(vectorized_batch)

# Add a new column to the spreadsheet with the AI's verdict
new_emails_df['Threat_Status'] = predictions

# Print the final scanned table to the terminal
print(new_emails_df)

# Save the fully scanned results to a brand new file
new_emails_df.to_csv('scanned_results.csv', index=False)