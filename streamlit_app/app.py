# Streamlit app for PERPL

# Import third-party libraries
import streamlit as st
import numpy as np

# Import local libraries
from read_file import read_file

# Set up the app
st.set_page_config(
    page_title="PERPL",
    page_icon=":microscope:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": None,
    })

# Page title
st.title("PERPL")
st.subheader("Pattern Extraction from Relative Positions of Localisations")

# Tabs
tab1, tab2 = st.tabs(["Relative Positions", "About"])

# Tab 1 - Relative Positions
with tab1:
    st.header("Relative Positions")
    
    # File uploader
    try:
        uploaded_file = st.file_uploader("Choose a file")
    except (EOFError, IOError, OSError) as exception:
        st.error("Could not read file", icon="🚨")
    
    # Read file
    if uploaded_file is not None:
        errors = []
        data = read_file(uploaded_file, errors)
        if errors:
            for error in errors:
                st.error(error, icon="🚨")

# Tab 2 - About
with tab2:
    st.header("About")