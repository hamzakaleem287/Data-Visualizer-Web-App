# Importing the Required Libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Setting the Page Configuration
st.set_page_config(page_title="Data Visualizer", page_icon="📊", layout='centered')

# Title of the Web App
st.markdown( 
    """
    <style>
    .st-emotion-cache-10trblm.e1nzilvr1{
            text-align:center;
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style=color:#ff4c5b;><img width='64px',height='64', src='https://cdn-icons-png.freepik.com/512/12191/12191411.png?uid=R140683934&ga=GA1.1.2115474961.1709795892&'> <span style=color:#f77600;> Data Visual</span><span style=color:#1fb4ff;>izer Web App</span></h1>", unsafe_allow_html=True)
st.markdown("<h5 style=color:#384949; ><span style=color:#1fb4ff;>Explore, Analyze, and Visualize</span> <span style=color:#f77600;>data like never before...</span></h5>",unsafe_allow_html=True) 
try:
    # Getting the Working Directory
    working_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = f"{working_dir}/data"

    # Listing the files present in 'data' folder
    files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

    # Dropdown for all the Files
    selected_files = st.selectbox("Select a File",[None]+files)

    if selected_files:
        # Get the Complete Path of the Selected Files
        file_path = os.path.join(folder_path, selected_files)
        
        # Case 3: Handle FileNotFoundError if the selected CSV file does not exist
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The selected file '{selected_files}' does not exist.")

        # Reading the CSV Files as Pandas Dataframe
        df = pd.read_csv(file_path)
        # Dividing the Layout into Two Columns
        col1, col2 = st.columns(2)
        columns = df.columns.tolist()
        with col1:
            st.write("")
            st.write(df.head())
        with col2:
            # User Selection of the Columns
            x_axis = st.selectbox("Select the X-Axis", options=[None] + columns)
            y_axis = st.selectbox("Select the Y-Axis", options=[None] + columns)
            plot_list = [None, "Line Plot", "Bar Chart", "Scatter Plot", "Distribution Plot", "Count Plot"]
            selected_plot = st.selectbox("Select a Plot", options=plot_list)
        # Generate the plot based on user selection
        if st.button('Generate Plot'):
            fig, ax = plt.subplots(figsize=(6,4))
            if selected_plot == 'Line Plot':
                sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax, marker='o')
            elif selected_plot == 'Bar Chart':
                sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif selected_plot == 'Scatter Plot':
                sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax, marker='o')
            elif selected_plot == 'Distribution Plot':
                sns.histplot(df[x_axis], kde=True, ax=ax)
                y_axis = 'Density'
            elif selected_plot == 'Count Plot':
                sns.countplot(x=df[x_axis], ax=ax)
                y_axis = 'Count'

            # Adjust label sizes
            ax.tick_params(axis='x', labelsize=6)  # Adjust x-axis label size
            ax.tick_params(axis='y', labelsize=6)  # Adjust y-axis label size

            # Adjust title and axis labels with a smaller font size
            plt.title(f'{selected_plot} of {y_axis} vs {x_axis}', fontsize=8)
            plt.xlabel(x_axis, fontsize=7)
            plt.ylabel(y_axis, fontsize=7)
            #plt.xticks(rotation=10)

            # Show the results
            st.pyplot(fig)

except FileNotFoundError as e:
    st.error(f"An error occurred: {str(e)}")
except pd.errors.EmptyDataError:
    st.error("The selected CSV file is empty. Please choose another file.")
except KeyError:
    st.error("Please select valid X and Y axes.")
except Exception as e:
    st.error(f"An unexpected error occurred: {str(e)}")
