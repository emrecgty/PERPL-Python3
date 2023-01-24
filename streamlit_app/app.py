# Streamlit app for PERPL

# Import third-party libraries
import streamlit as st
import numpy as np

# Import local libraries
from read_file import read_file
from get_relative_positions import get_relative_positions
from get_vectors import get_vectors
from plotting import plot_histograms, draw_2d_scatter_plots

# Set up the app
st.set_page_config(
    page_title="PERPL",
    page_icon=":microscope:",
    layout="centered",
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
    
    # Divider
    st.write("---")
    
    # Dimensions
    dimensions = st.radio(
        "Choose the dimensions of the data",
        ("2D", "3D")
    )
    
    dimensions = 2 if dimensions == "2D" else 3
    
    # Divider
    st.write("---")
    
    # Filter distance
    filter_dist = st.number_input('Select a filter distance (nm)', 1, 1000, 50, 1)
    
    if filter_dist >= 500:
        st.warning("Filter distance is very large! This may take a long time.")
        
    # Divider
    st.write("---")
    
    # Zoom level for 2D scatter plots
    zoom = st.number_input('Select a zoom level for the magnified scatter plot', 1, 10)
    
    
    
    # Divider
    st.write("---")
    
    colour_information = st.radio(
        "Does the data have colour information?",
        ("Yes", "No")
    )
    
    # Divider
    st.write("---")
    
    # Factors of the filter distance for bin size
    factors = [i for i in range(1, filter_dist+1) if filter_dist % i == 0]
    # Bin size
    bin_size = st.select_slider('Select a bin size for the histogram', factors)
    
    # Read file
    if uploaded_file is not None:
        errors = []
        
        data = read_file(uploaded_file, errors)
        
        scatter_container = st.container()
        
        with scatter_container:
            sct, sct_zoom = st.columns(2)
            
            with sct:
                draw_2d_scatter_plots(data, dimensions, 0)
            
            with sct_zoom:
                draw_2d_scatter_plots(data, dimensions, zoom)
        
        if errors:
            for error in errors:
                st.error(error, icon="🚨")
        
        distance_values = get_relative_positions(
            xyzcolour_values=data,
            filter_dist= filter_dist,
            dims = dimensions,
            start_channel=0,
            end_channel=1,
        )
        
        d_values = get_vectors(distance_values, dims=dimensions)
        
        
        
        plot_histograms(
        d_values, dimensions, filter_dist, binsize=bin_size
        )
        
        

# Tab 2 - About
with tab2:
    st.header("About")