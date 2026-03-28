import streamlit as st
import numpy as np
import joblib
import re
from urllib.parse import urlparse

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Phishing URL Detector",
    page_icon="🔍",
    layout="centered"
)

# ---------------- LOAD MODEL ----------------
rf_model = joblib.load('models/final_rf.joblib')

# ---------------- FEATURE FUNCTIONS ----------------
def extract_features(url):
    try:
        parsed = urlparse(url)

        url_length = len(url)
        hostname_length = len(parsed.netloc)
        path_length = len(parsed.path)

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

        count_dir = len(path_parts)

        ip_pattern = r'^\d{1,3}(\.\d{1,3}){3}$'
        use_of_ip = -1 if re.match(ip_pattern, parsed.netloc) else 1

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


# ---------------- UI ----------------
st.markdown("<h1 style='text-align: center;'>🔍 Phishing URL Detector</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Enter a URL to check if it is <b>Phishing</b> or <b>Legitimate</b></p>", unsafe_allow_html=True)

st.divider()

# Example URLs
st.subheader("📌 Try Example URLs")

col1, col2 = st.columns(2)

with col1:
    if st.button("Phishing Example"):
        st.session_state.url = "http://secure-login-paypal.com.verify-user-account.ru/login"

with col2:
    if st.button("Legitimate Example"):
        st.session_state.url = "https://www.google.com"

# Input box
url = st.text_input("🌐 Enter URL", value=st.session_state.get("url", ""))

# ---------------- PREDICTION ----------------
if st.button("🚀 Check URL"):
    if url:
        features = extract_features(url)

        if features is not None:
            prediction = rf_model.predict(features)

            # Probability (if available)
            if hasattr(rf_model, "predict_proba"):
                prob = rf_model.predict_proba(features)[0][1]
            else:
                prob = None

            st.divider()

            if prediction[0] == 1:
                st.error("🚨 Phishing URL Detected!")
            else:
                st.success("✅ Legitimate URL")

            if prob is not None:
                st.info(f"Confidence Score: {prob:.2f}")

        else:
            st.warning("⚠️ Invalid URL")
    else:
        st.warning("⚠️ Please enter a URL")

# ---------------- FOOTER ----------------
st.divider()
st.markdown(
    "<p style='text-align: center; color: grey;'>© 2026 Saim Qazi | Phishing Detection System</p>",
    unsafe_allow_html=True
)
