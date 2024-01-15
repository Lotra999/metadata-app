import json
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



cell_line_file_path = 'cell_line_data.json' 
#options_path = 'options.json'
options_path = './Desktop/options.json'

# Set page config
st.set_page_config(
    page_title="Experiment Metadata App",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

def get_options(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            options_mapping = json.load(file)
        return options_mapping
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Function to collect QCM-D metadata
def collect_qcmd_metadata():
    st.header("QCM-D Metadata Collection")



    # Collect metadata form for QCM-D
    experiment_date = st.date_input("Experiment Date")
    experiment_name = st.text_input("Experiment name")
    researcher_name = st.text_input("Researcher name")

    options = get_options(options_path)
    cell_line_type_options = options['cell_line_type_options']
    
    cell_line_type = st.selectbox("Cell line type", cell_line_type_options, key='cell_line_type')
    if 'selected_cell_line_type' not in st.session_state or st.session_state.selected_cell_line_type != cell_line_type:
        st.session_state.selected_cell_line_type = cell_line_type
        st.experimental_rerun()

    cell_line_options = options['cell_line_options'][cell_line_type]
    cell_line = st.selectbox("Cell line", cell_line_options)

    ligand = st.text_input("Ligand")
    ligand_concentration = st.text_input("Ligand concentration")

    sensor_options = options['sensor_options']
    sensor = st.selectbox("Sensor", sensor_options)

    buffer_options = options['buffer_options']
    buffer = st.selectbox("Buffer", buffer_options)

    temperature_options = options['temperature_options']
    temperature = st.selectbox("Temperature", temperature_options)

    temperature_fluctuation_options = options['temperature_fluctuation_options']
    temperature_fluctuation = st.selectbox("Temperature fluctuation", temperature_fluctuation_options)

    flow_options = options['flow_options']
    flow = st.selectbox("Flow", flow_options)

    unit_of_time_options = options['unit_of_time_options']
    unit_of_time = st.selectbox("Unit of time", unit_of_time_options)

    additional_description = st.text_input("Additional description")
    upload_results = st.file_uploader("Upload results", type=["csv", "txt"])
   

    if st.button("Submit"):
        # Process and save QCM-D metadata
        save_qcmd_metadata("qcmd_metadata.csv", experiment_date, experiment_name, researcher_name, cell_line_type, cell_line, ligand,
                            ligand_concentration, sensor, buffer, temperature, temperature_fluctuation, flow, unit_of_time, additional_description, upload_results)
        

    # Function to display and download uploaded results
def browse_metadata():
    st.header("Browse Metadata")

    # Load the metadata
    metadata_path = f"{experiment_type.lower()}_metadata.csv"
    try:
        metadata = pd.read_csv(metadata_path)
    except FileNotFoundError:
        st.warning("No metadata available.")
        return
  
    # Function to save QCM-D metadata to CSV file
def save_qcmd_metadata(metadata_path, experiment_date, experiment_name, researcher_name, cell_line_type, cell_line, ligand,
                        ligand_concentration, sensor, buffer, temperature, temperature_fluctuation, flow, unit_of_time, additional_description, 
                        upload_results):
    # Load existing metadata or create an empty DataFrame
    metadata_path = f"{experiment_type.lower()}_metadata.csv"
    try:
        existing_metadata = pd.read_csv(metadata_path)
    except FileNotFoundError:
        existing_metadata = pd.DataFrame()

    # Save new QCM-D metadata to DataFrame
    new_metadata = pd.DataFrame({
        "Experiment Date": [str(experiment_date)],
        "Experiment Name": [experiment_name],
        "Researcher Name": [researcher_name],
        "Cell line type": [cell_line_type],
        "Cell line": [cell_line],
        "Ligand": [ligand],
        "Ligand concentration": [ligand_concentration],
        "Sensor": [sensor],
        "Buffer": [buffer],
        "Temperature": [temperature],
        "Temperature fluctuation": [temperature_fluctuation],
        "Flow": [flow],
        "Unit of time": [unit_of_time],
        "Additional description": [additional_description],
        "Upload results": [upload_results.name if upload_results else None]
    })

    # Concatenate new QCM-D metadata with existing metadata
    metadata = pd.concat([existing_metadata, new_metadata], ignore_index=True)

    # Save QCM-D metadata to a CSV file
    metadata.to_csv(metadata_path, index=False)




    st.success("QCM-D Metadata submitted successfully!")
    

def metadata_visualization():
    st.header("Visualization of Results")

    # Load QCM-D data from Streamlit file uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        try:
            qcm_data = pd.read_csv(uploaded_file)
        except pd.errors.ParserError as e:
            print(f"Error reading CSV: {e}")


        # Generate and display plot
        st.subheader("QCM-D Experiment Results")
        plt.figure(figsize=(8, 6))
        plt.plot(qcm_data['Time'], qcm_data['Frequency'])
        plt.title('QCM-D Experiment Results')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.grid(True)
        st.pyplot()

if __name__ == "__main__":
    metadata_visualization()

    



# Function to collect SPR metadata
def collect_spr_metadata():
    st.header("SPR Metadata Collection")

    # Collect metadata form for SPR
    experiment_date = st.date_input("Experiment Date")
    experiment_name = st.text_input("Experiment name")
    researcher_name = st.text_input("Researcher name")
    sample_type = st.text_input("Sample type")
    ligand = st.text_input("Ligand")
    ligand_concentration = st.text_input("Ligand concentration")
    analyte = st.text_input("Analyte")
    analyte_concentration = st.text_input("Analyte concentration")
    flow_rate = st.text_input("Flow rate")
    additional_description = st.text_input("Additional description")
    upload_results = st.file_uploader("Upload results", type=["csv", "txt"])

    if st.button("Submit"):
        # Process and save SPR metadata
        save_spr_metadata("spr_metadata.csv", experiment_date, experiment_name, researcher_name, sample_type, ligand,
                            ligand_concentration, analyte, analyte_concentration, flow_rate,
                            additional_description, upload_results)

# Function to save SPR metadata to CSV file
def save_spr_metadata(metadata_path, experiment_date, experiment_name, researcher_name, sample_type, ligand,
                        ligand_concentration, analyte, analyte_concentration, flow_rate,
                        additional_description, upload_results):
    # Load existing metadata or create an empty DataFrame
    metadata_path = f"{experiment_type.lower()}_metadata.csv"

    try:
        existing_metadata = pd.read_csv(metadata_path)
    except FileNotFoundError:
        existing_metadata = pd.DataFrame()

    # Save new SPR metadata to DataFrame
    new_metadata = pd.DataFrame({
        "Experiment Date": [str(experiment_date)],
        "Experiment Name": [experiment_name],
        "Researcher Name": [researcher_name],
        "Sample type": [sample_type],
        "Ligand": [ligand],
        "Ligand concentration": [ligand_concentration],
        "Analyte": [analyte],
        "Analyte concentration": [analyte_concentration],
        "Flow rate": [flow_rate],
        "Additional description": [additional_description],
        "Upload results": [upload_results.name if upload_results else None]
    })

    # Concatenate new SPR metadata with existing metadata
    metadata = pd.concat([existing_metadata, new_metadata], ignore_index=True)

# Function to save SPR metadata to CSV file
def save_spr_metadata(metadata_path, experiment_date, experiment_name, researcher_name, sample_type, ligand,
                        ligand_concentration, analyte, analyte_concentration, flow_rate,
                        _, additional_description, upload_results):
    # Load existing metadata or create an empty DataFrame
    try:
        existing_metadata = pd.read_csv(metadata_path)
    except FileNotFoundError:
        existing_metadata = pd.DataFrame()

    # Save new SPR metadata to DataFrame
    new_metadata = pd.DataFrame({
        "Experiment Date": [str(experiment_date)],
        "Experiment Name": [experiment_name],
        "Researcher Name": [researcher_name],
        "Sample type": [sample_type],
        "Ligand": [ligand],
        "Ligand concentration": [ligand_concentration],
        "Analyte": [analyte],
        "Analyte concentration": [analyte_concentration],
        "Flow rate": [flow_rate],
        "Additional description": [additional_description],
        "Upload results": [upload_results.name if upload_results else None]
    })

    # Concatenate new SPR metadata with existing metadata
    metadata = pd.concat([existing_metadata, new_metadata], ignore_index=True)

    # Save SPR metadata to a CSV file
    metadata.to_csv(metadata_path, index=False)

    st.success("SPR Metadata submitted successfully!")

# Function to browse and visualize metadata
def browse_and_visualize_metadata(experiment_type):
    st.header(f"Browse and Visualize {experiment_type} Metadata")

    # Load metadata from the CSV file
    try:
        metadata = pd.read_csv(f"{experiment_type.lower()}_metadata.csv")
    except FileNotFoundError:
        metadata = pd.DataFrame()

    if not metadata.empty:
        # Display an interactive table with selected columns
        st.write(f"### All {experiment_type} Metadata")

        # Ensure necessary columns are present in the DataFrame
        necessary_columns = ["Experiment Date", "Experiment Name", "Researcher Name"]
        for column in necessary_columns:
            if column not in metadata.columns:
                metadata[column] = ""

        st.table(metadata[necessary_columns])

        # Add a multiselect for row selection
        all_rows_option = "Select All Rows"
        selected_rows = st.multiselect("Select Rows for Detailed View", [all_rows_option] + metadata.index.tolist())

        if all_rows_option in selected_rows:
            # Display additional details for all rows
            st.write(f"### All {experiment_type} Rows Details:")
            st.table(metadata)
        elif selected_rows:
            
            # Display additional details for the selected rows
            selected_data = metadata.loc[selected_rows]
            st.write(f"### Selected {experiment_type} Rows Details:")
            st.table(selected_data)
            
            # Add delete button for selected rows
            delete_button = st.button(f"Delete Selected {experiment_type} Rows")

            if delete_button:
                # Delete selected rows from the DataFrame
                metadata = metadata.drop(selected_rows)

                # Save the updated metadata to the CSV file
                metadata.to_csv(f"{experiment_type.lower()}_metadata.csv", index=False)
                st.success("Selected rows deleted successfully.")

            # Add download button for selected rows
            download_format = st.selectbox("Select Download Format", ["CSV", "TXT"])
            download_button = st.button(f"Download Selected {experiment_type} Rows")

            if download_button:
                # Prepare data for download
                if download_format == "CSV":
                    csv_data = selected_data.to_csv(index=False)
                    b64 = base64.b64encode(csv_data.encode()).decode()
                    href = f'<a href="data:file/csv;base64,{b64}" download="selected_rows.csv" style="color: white; background-color: #4CAF50; padding: 8px 16px; text-decoration: none; display: inline-block; border-radius: 5px;">Download CSV</a>'
                    st.markdown(href, unsafe_allow_html=True)
                elif download_format == "TXT":
                    txt_data = selected_data.to_csv(index=False, sep="\t")
                    b64 = base64.b64encode(txt_data.encode()).decode()
                    href = f'<a href="data:file/txt;base64,{b64}" download="selected_rows.txt" style="color: white; background-color: #4CAF50; padding: 8px 16px; text-decoration: none; display: inline-block; border-radius: 5px;">Download TXT</a>'
                    st.markdown(href, unsafe_allow_html=True)
                
    else:
        st.info(f"No {experiment_type} metadata available.")


# Sidebar navigation with buttons
st.sidebar.title("🔬 Navigation")
st.sidebar.markdown(
    """
    Welcome to the Experiment Metadata App
    \n
    ---\n
    """)

# Select the type of experiment
experiment_type = st.sidebar.selectbox("Select Experiment Type", ["QCM-D", "SPR"])

# Function to create the "New Parameters" page
def new_parameters_page():
    st.header("New Parameters")

    experiment_type_options = ["QCM-D", "SPR"]  # Add other experiment types if needed
    selected_experiment_type = st.selectbox("Select Experiment Type", experiment_type_options)

    if selected_experiment_type == "QCM-D":
        collect_qcmd_metadata()
    elif selected_experiment_type == "SPR":
        collect_spr_metadata()

# Select the page
selected_page = st.sidebar.radio("Select Page", ["Collect Metadata", "Browse Metadata", "Visualization of Results", "New parameters"])

# Based on the selected experiment and page, perform the corresponding action
if selected_page == "Collect Metadata":
    if experiment_type == "QCM-D":
        collect_qcmd_metadata()
    elif experiment_type == "SPR":
        collect_spr_metadata()
elif selected_page == "Browse Metadata":
    if experiment_type == "QCM-D":
        browse_and_visualize_metadata("QCM-D")
    elif experiment_type == "SPR":
        browse_and_visualize_metadata("SPR")
elif selected_page == "Visualization of Results":
    # Add the code for visualization of results here
    st.header("Visualization of Results Page")
else:  # Corrected the page label here
    new_parameters_page()


# Check if there is uploaded data in session_state
    if st.session_state.uploaded_data is not None:
        uploaded_data = st.session_state.uploaded_data

        # Display the raw data
        st.subheader("Raw Data:")
        st.write(uploaded_data)

        # Check if the data has columns suitable for visualization (e.g., numeric columns)
        numeric_columns = uploaded_data.select_dtypes(include=['float64', 'int64']).columns

        if len(numeric_columns) > 0:
            # Allow users to select columns for visualization
            selected_columns = st.multiselect("Select columns for visualization", numeric_columns)

            if len(selected_columns) > 0:
                # Allow users to choose the type of plot (e.g., line plot, scatter plot)
                plot_type = st.selectbox("Select plot type", ["line", "scatter"])

                # Create the selected plot
                st.subheader("Visualization:")
                if plot_type == "line":
                    st.line_chart(uploaded_data[selected_columns])
                elif plot_type == "scatter":
                    st.scatter_chart(uploaded_data[selected_columns])

            else:
                st.warning("Please select at least one numeric column for visualization.")

        else:
            st.warning("No numeric columns found for visualization in the uploaded data.")
    else:
        st.info("No data available for visualization. Please submit metadata with results first.")




