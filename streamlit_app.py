import streamlit as st

# #streamlit run streamlit_app.py

def app():
    st.set_page_config(
        page_title="Home",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.write("""
# Production planer demo

""")


if __name__ == "__main__":
    app()
