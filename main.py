import streamlit as st
import numpy as np
import joblib
import re
from urllib.parse import urlparse
from sklearn.preprocessing import StandardScaler
import joblib
# Load model
rf_model = joblib.load('models/final_rf.joblib')

# If you used scaler (optional)
# scaler = joblib.load('scaler.pkl')

# ---------------- FEATURE FUNCTIONS ----------------

def extract_features(url):
    try:
        parsed = urlparse(url)

        url_length = len(url)
        hostname_length = len(parsed.netloc)
        path_length = len(parsed.path)

        # First directory length
        path_parts = [p for p in parsed.path.split('/') if p]
        fd_length = len(path_parts[0]) if len(path_parts) > 0 else 0

        count_dash = url.count('-')
        count_at = url.count('@')
        count_q = url.count('?')
        count_per = url.count('%')
        count_dot = url.count('.')
        count_equal = url.count('=')
        count_http = url.count('http')
        count_https = url.count('https')
        count_www = url.count('www')

        count_digits = sum(c.isdigit() for c in url)
        count_letters = sum(c.isalpha() for c in url)

        # Directory count
        count_dir = len(path_parts)

        # IP check
        ip_pattern = r'^\d{1,3}(\.\d{1,3}){3}$'
        use_of_ip = -1 if re.match(ip_pattern, parsed.netloc) else 1

        # Short URL check
        shorteners = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly"}
        short_url = -1 if parsed.netloc in shorteners else 1

        features = [
            url_length, hostname_length, path_length, fd_length,
            count_dash, count_at, count_q, count_per, count_dot,
            count_equal, count_http, count_https, count_www,
            count_digits, count_letters, count_dir,
            use_of_ip, short_url
        ]
        return np.array(features).reshape(1, -1)
        

    except:
        return None

# ---------------- STREAMLIT UI ----------------

st.title("🔍 Phishing URL Detection")

url = st.text_input("Enter URL")

if st.button("Check URL"):
    if url:
        features = extract_features(url)

        if features is not None:
            # If scaler used
            # features = scaler.transform(features)

            prediction = rf_model.predict(features)

            if prediction[0] == 1:
                st.error("🚨 Phishing URL Detected!")
            else:
                st.success("✅ Legitimate URL")
        else:
            st.warning("Invalid URL")
    else:
        st.warning("Please enter a URL")