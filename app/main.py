import streamlit as st
from streamlit_option_menu import option_menu
import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.pages import home, about

st.set_page_config(layout="wide", page_title="Urban Garden Plant Finder - Omdena (Kutch, India)")


# Custom CSS to improve the look and feel
st.markdown("""
<style>
.big-font {
    font-size: 30px !important;
    font-weight: bold;
    color: #1E8449;
}
.medium-font {
    font-size: 24px !important;
    font-weight: bold;
    color: #2E86C1;
}
.small-font {
    font-size: 18px !important;
    color: #1E8449;
}
.highlight {
    background-color: #F0F3F4;
    padding: 10px;
    border-radius: 5px;
}
.stProgress > div > div > div > div {
    background-color: #2ECC71;
}
</style>
""", unsafe_allow_html=True)

# Get the backend URL from environment variable
BACKEND_URL = os.environ.get("BACKEND_URL")

if not BACKEND_URL:
    st.error("BACKEND_URL environment variable is not set. Please set it and restart the application.")
    st.stop()

def main():
    st.markdown('<p class="big-font">Urban Garden Plant Finder - Omdena (Kutch, India)</p>', unsafe_allow_html=True)

    # Pass the BACKEND_URL to the pages that need it
    page = st.sidebar.selectbox("Pages", ["Home", "About"])

    if page == "Home":
        home.show(BACKEND_URL)
    elif page == "About":
        about.show()

if __name__ == "__main__":
    main()