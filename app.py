import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Title
st.title("📧 Email Spam Detector")

# Load dataset
try:
    df = pd.read_csv("spam.csv", encoding="latin-1")
except FileNotFoundError:
    st.error("❌ spam.csv not found in the current folder!")
    st.stop()

df = df[['v1', 'v2']]
df.dropna(inplace=True)

# Preprocessing
texts = df['v2'].str.lower().str.replace(r'[^\w\s]', '', regex=True).str.strip()
labels = df['v1'].apply(lambda x: 1 if x.strip().lower() == 'spam' else 0)

# Train-test split
x_train, x_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42, stratify=labels
)

# Vectorization
vectorizer = TfidfVectorizer(stop_words='english')
x_train_vec = vectorizer.fit_transform(x_train)
x_test_vec = vectorizer.transform(x_test)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(x_train_vec, y_train)

# Accuracy
accuracy = model.score(x_test_vec, y_test)
st.write(f"✅ Model Accuracy: **{accuracy * 100:.2f}%**")

# User input
st.subheader("✉️ Enter an email to check:")
user_email = st.text_area("Email Content")

if st.button("Check Spam"):
    if not user_email.strip():
        st.warning("⚠️ Please enter some email content first!")
    else:
        email_clean = pd.Series(user_email.lower()).str.replace(r'[^\w\s]', '', regex=True).iloc[0]
        email_vec = vectorizer.transform([email_clean])
        prediction = model.predict(email_vec)[0]

        if prediction == 1:
            st.error("🚨 This email is SPAM")
        else:
            st.success("✅ This email is NOT SPAM")
