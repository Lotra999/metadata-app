import json
import os
import streamlit as st
import pandas as pd
import base64
import yaml


cell_line_file_path = 'cell_line_data.json'  # Adjust this path as necessary
options_path = 'options.json'


def read_yaml_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

# Set page config
st.set_page_config(
    page_title="Experiment Metadata App",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)


def create_download_link(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/octet-stream;base64,{b64}" download="{os.path.basename(file_path)}">Download</a>'
    return href



def plot_dual_line_chart(file_path):
    
    import pandas as pd
    import matplotlib.pyplot as plt

    # Load the dataset
    data = pd.read_csv(file_path, sep=';')

    # Converting Time_1, F_1:13, and D_1:13 to numeric values and handling comma as decimal separator
    data['Time_1'] = pd.to_numeric(data['Time_1'].str.replace(',', '.'), errors='coerce')
    data['F_1:13'] = pd.to_numeric(data['F_1:13'].str.replace(',', '.'), errors='coerce')
    data['D_1:13'] = pd.to_numeric(data['D_1:13'].str.replace(',', '.'), errors='coerce')

    # Create a plot with two y-axes
    fig, ax1 = plt.subplots()

    # First line plot for F_1:13
    color = 'tab:blue'
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Frequency', color=color)
    ax1.plot(data['Time_1'], data['F_1:13'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Second y-axis for D_1:13
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Dissipation', color=color)
    ax2.plot(data['Time_1'], data['D_1:13'], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    # Show the plot
    plt.title('Line Plot of frequency and dissipation vs time')
    return plt



def get_options(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            options_mapping = json.load(file)
        return options_mapping
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def collect_qcmd_metadata(yaml_config_path, options_path):
    st.header("QCM-D Metadata Collection")
    config = read_yaml_config(yaml_config_path)
    options = get_options(options_path)

    collected_data = {}

    for field in config['fields']:
        if field['type'] == 'text':
            collected_data[field['name']] = st.text_input(field['label'])
        elif field['type'] == 'date':
            collected_data[field['name']] = st.date_input(field['label'])
        elif field['type'] == 'select':
            options_key = field['options_key']
            selected_option = st.selectbox(field['label'], options[options_key], key=field['name'])
            collected_data[field['name']] = selected_option
        elif field['type'] == 'select_dynamic':
            depends_on = field['depends_on']
            dependent_value = collected_data[depends_on]
            dynamic_options = options[field['options_key']][dependent_value]
            selected_dynamic_option = st.selectbox(field['label'], dynamic_options, key=field['name'])
            collected_data[field['name']] = selected_dynamic_option
        elif field['type'] == 'file':
            uploaded_file = st.file_uploader(field['label'], type=field.get('file_types', ["csv", "txt"]))
            if uploaded_file is not None:
                st.session_state['uploaded_file'] = uploaded_file
                collected_data[field['name']] = uploaded_file.name
    # Add other field types as needed
    if st.button("Submit"):
        save_metadata("qcmd_metadata.csv", collected_data)
   

def save_metadata(metadata_path, collected_data):
    metadata_path = f"{experiment_type.lower()}_metadata.csv"
    try:
        existing_metadata = pd.read_csv(metadata_path)
    except FileNotFoundError:
        existing_metadata = pd.DataFrame()
    
    uploaded_file_path = None
    print(collected_data.keys())
    if collected_data["upload_results1"] is not None:
        file_path = f"{collected_data['experiment_name']}-{collected_data['upload_results1']}"  # Adjust the path
        with open(file_path, 'wb') as f:
            f.write(st.session_state['uploaded_file'].getbuffer())

        uploaded_file_path = file_path
    else:
        uploaded_file_path = None

    collected_data['Uploaded File Path'] = uploaded_file_path
    
    print(collected_data)
    new_metadata = pd.DataFrame([collected_data])
    # Concatenate new QCM-D metadata with existing metadata
    metadata = pd.concat([existing_metadata, new_metadata], ignore_index=True)

    # Save QCM-D metadata to a CSV file
    metadata.to_csv(metadata_path, index=False)

    st.success("QCM-D Metadata submitted successfully!")
    
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


    uploaded_file_path = None
    if upload_results is not None:
        file_path = f"{experiment_name}-{upload_results.name}"  # Adjust the path
        with open(file_path, 'wb') as f:
            f.write(upload_results.getbuffer())

        uploaded_file_path = file_path
    else:
        uploaded_file_path = None

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
        "Uploaded File Path": [uploaded_file_path]
    })

    # Concatenate new QCM-D metadata with existing metadata
    metadata = pd.concat([existing_metadata, new_metadata], ignore_index=True)

    # Save QCM-D metadata to a CSV file
    metadata.to_csv(metadata_path, index=False)

    st.success("QCM-D Metadata submitted successfully!")
    

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

    if upload_results is not None:
        st.session_state['uploaded_file'] = upload_results

    if st.button("Submit"):
        # Process and save SPR metadata
        save_spr_metadata("spr_metadata.csv", experiment_date, experiment_name, researcher_name, sample_type, ligand,
                            ligand_concentration, analyte, analyte_concentration, flow_rate,
                            additional_description, upload_results)


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
        necessary_columns = ["experiment_date", "experiment_name", "researcher_name"]

        
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
            # Add download links to the selected data
            st.write(f"### Selected {experiment_type} Rows Details:")
            st.table(selected_data)
            
            for index, row in selected_data.iterrows():
                download_link = create_download_link(row['Uploaded File Path'])
                st.markdown(f"Download file for record {index}: {download_link}", unsafe_allow_html=True)
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
                

        st.write(f"### Dual Line Chart Visualization for {experiment_type} Metadata")
        selected_index = st.selectbox("Select Record for Visualization", metadata.index)
        record = metadata.iloc[selected_index]
        file_path = record.get("Uploaded File Path")

        if file_path and os.path.exists(file_path):
            # No need for a second upload, use the file from session state
            plt = plot_dual_line_chart(file_path)
            st.pyplot(plt)
        else:
            st.info("Please upload a file in the 'Collect Metadata' section for visualization.")


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
        collect_qcmd_metadata("qcmd_metadata_config.yaml",options_path)
    elif selected_experiment_type == "SPR":
        collect_spr_metadata()

# Select the page
selected_page = st.sidebar.radio("Select Page", ["Collect Metadata", "Browse Metadata"])

# Based on the selected experiment and page, perform the corresponding action
if selected_page == "Collect Metadata":
    if experiment_type == "QCM-D":
        collect_qcmd_metadata("qcmd_metadata_config.yaml",options_path)
    elif experiment_type == "SPR":
        collect_spr_metadata()
elif selected_page == "Browse Metadata":
    if experiment_type == "QCM-D":
        browse_and_visualize_metadata("QCM-D")
    elif experiment_type == "SPR":
        browse_and_visualize_metadata("SPR")



else:
    st.warning("Invalid page selected.")


