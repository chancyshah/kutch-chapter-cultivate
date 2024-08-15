import streamlit as st

def show():
    st.title('About Us')

    st.subheader("Goals of Cultivate")
    st.write("Cultivate is a project aimed at helping urban gardeners choose the right plants for their specific environment. By leveraging machine learning and local climate data, we provide personalized plant recommendations to ensure successful and sustainable urban gardening.")

    st.subheader("The Omdena Kutch Chapter")
    url = "https://www.omdena.com/chapter-challenges/cultivate-enhancing-urban-gardening-with-geospatial-intelligence"
    st.write(f"This project is part of the Omdena Kutch Chapter. Learn more about our challenge [here]({url}).")

    st.subheader("Contributors")
    st.markdown('''Names and Roles:
    ''')

if __name__ == "__main__":
    show()