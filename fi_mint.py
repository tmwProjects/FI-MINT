import hashlib
import os
import pandas as pd
from exiftool import ExifToolHelper
import streamlit as st
import tempfile
import zipfile
import plotly.express as px
import base64
import folium
from streamlit_folium import folium_static

st.title('FI-MINT')
st.subheader('File Metadata Intelligence')
st.write('Welcome to FI-MINT, your smart file metadata app. With this app you can extract, visualise and analyse metadata from your files. MetaSense harnesses the power of Python to perform deep and nuanced analysis of your metadata.')
st.write('Here is a quick guide to the key features:')
st.write('**File upload**: \n Upload a ZIP file containing the files whose metadata you want to analyse.')
st.write('**Custom weighting settings**: \n Specify specific metadata categories (keys) and their respective weightings. This means how important they should be in the comparison calculation. Example: Author:3, Title:2. Weightings help to refine the similarity calculations.')
st.write('**Individual file metadata**: \n Here you can view the metadata of a selected file. You can view detailed information such as file type, creation date, modification date, size and other specific metadata.')
st.write('**Tabular comparison data**: \n Here, the comparison data is presented in a user-defined table. Users can easily identify differences and similarities and sort the data as desired.')
st.write('**Metadata comparison plot**: \n This intuitive tool helps you quickly capture the similarities between different pairs of files. It displays the similarity values derived from the content or properties of the files.')
st.write('**Geolocation**: \n If your files contain longitude and latitude information in their metadata, this information is extracted and the files are placed on a map accordingly.')
st.write('**Download CSV**: \n You can download the metadata and comparison data as CSV files.')
st.write('**Hash value comparison**: \n FI-MINT calculates the SHA-256 hash values for each uploaded file. If two files have the same hash value even though they have different names, a notification is issued. This helps to identify duplicate or identical files.')
st.write('FI-MINT is designed to help you get more out of your files and their metadata. It provides powerful tools to understand, analyse and gain valuable insights from this data. We hope you like it and find it useful!')


# Liste der wichtigen Schlüssel
important_keys = ["Author", "Creator", "Producer"]

# Liste der seltenen Schlüssel
rare_keys = ["Language", "Modify Date", "PDF Version"]

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)


def get_files_from_dir(directory):
    files = []
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            full_path = os.path.abspath(os.path.join(dirpath, f))
            if os.path.isfile(full_path):
                files.append(full_path)
    return files


def calculate_hash(file_path):
    with open(file_path, "rb") as file:
        bytes = file.read()
        readable_hash = hashlib.sha256(bytes).hexdigest()
    return readable_hash


def calculate_weighted_similarity(metadata1, metadata2, weighting_system, custom_weights):
    keys = set(metadata1.keys()).intersection(metadata2.keys())
    similarity = 0
    matching_keys = {}

    for key in keys:
        if metadata1[key] == metadata2[key]:
            matching_keys[key] = metadata1[key]
            if weighting_system == 'equal':
                similarity += 1
            elif weighting_system == 'important_keys':
                if key in important_keys:
                    similarity += 2
                else:
                    similarity += 1
            elif weighting_system == 'rare_keys':
                if key in rare_keys:
                    similarity += 3
                else:
                    similarity += 1
            elif weighting_system == 'custom':
                similarity += custom_weights.get(key, 1)
    return similarity, matching_keys

def normalize_keywords(val):
    if isinstance(val, list):
        return val
    else:
        return [val]

def normalize_subject(val):
    if isinstance(val, list):
        return val
    else:
        return [val] if pd.notnull(val) else []

def normalize_creator(val):
    if isinstance(val, list):
        return val
    else:
        return [val] if pd.notnull(val) else []

def normalize_column(value):
    if isinstance(value, list):
        return [v if v is not None and v==v else "" for v in value]
    else:
        return [value] if value is not None and value==value else []

def get_description(metadata):
    return metadata.get('EXIF:ImageDescription', 'No description')

def get_geolocation_data(metadata):
    if 'EXIF:GPSLatitude' in metadata and 'EXIF:GPSLongitude' in metadata:
        return metadata['EXIF:GPSLatitude'], metadata['EXIF:GPSLongitude'], get_description(metadata)
    return None, None, None

def plot_on_map(df):
    # Create the folium map with an arbitrary center
    map = folium.Map(location=[0, 0], zoom_start=1)

    # Create an empty list to contain the latitude and longitude values
    latitudes = []
    longitudes = []

    # Add points to the map and to the lists
    for index, row in df.iterrows():
        lat, lon = row['Latitude'], row['Longitude']
        # Get the metadata dictionary
        metadata = row['metadata']

        # Prepare the description
        description = ""
        for column in ['File:FileName', 'File:FileType', 'EXIF:Make', 'EXIF:Model', 'EXIF:Artist']:
            value = metadata.get(column)  # Get value from the metadata dictionary
            if value is None:  # Check if the value is None (as get() would return)
                value = 'N/A'
            description += f"{column}: {value}<br>"

        marker = folium.Marker([lat, lon])
        # Add popup to the marker
        folium.Popup(description, max_width=250).add_to(marker)
        marker.add_to(map)
        latitudes.append(lat)
        longitudes.append(lon)

    # Adjust map to fit all markers
    map.fit_bounds([(min(latitudes), min(longitudes)), (max(latitudes), max(longitudes))])

    # Display the map in Streamlit
    folium_static(map)


def main():
    def get_image_base64_str(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')

    logo_path = "grafics/fi_mint.gif"
    logo_base64_str = get_image_base64_str(logo_path)
    logo_sidebar_markdown = f'<img src="data:image/png;base64,{logo_base64_str}" alt="logo" style="display:block; margin:auto; width:330px;height:330px;">'
    st.sidebar.markdown(logo_sidebar_markdown, unsafe_allow_html=True)

    st.sidebar.title("Data Upload")
    st.sidebar.write("Please upload your files as ZIP format. Note that our system only reads files from the root directory of the ZIP archive. Subdirectories are not recognized. All relevant files should therefore be placed in the main directory.")
    uploaded_file = st.sidebar.file_uploader("Upload ZIP file")

    # Benutzerdefinierte Gewichtungseinstellungen
    st.sidebar.title("Custom weight settings")
    custom_weight_input = st.sidebar.text_input("Please enter the keys (i.e. the specific metadata categories you wish to compare) and their respective weights (i.e. the relative value or importance you wish to attach to each key). The input should be separated by commas, with each key and weight pair joined by a colon. For example, your input might look like this: 'Author:3,Title:2'. In this case you have entered the 'Author' key with a weight of 3 and the 'Title' key with a weight of 2. This means that when calculating the similarity between two documents, matches in the 'Author' field are weighted three times as much as matches in the 'Title' field. So if you enter multiple keys and weights, make sure they are correctly separated by commas and colons.")
    custom_weights = {}
    if custom_weight_input:
        for item in custom_weight_input.split(','):
            key, weight = item.split(':')
            custom_weights[key.strip()] = int(weight)

    st.sidebar.markdown("""
        [![Visit my site](https://img.shields.io/badge/Visit%20my%20site-Online-important)](https://tmwprojects.github.io/)
        [![Donate on Liberapay](https://img.shields.io/badge/Donate-Liberapay-yellow)](https://liberapay.com/tmwProjects/donate)
        <a href="https://www.buymeacoffee.com/tmwcontactQ"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" height="20.4px"></a>
        """, unsafe_allow_html=True)

    files = []
    if uploaded_file is not None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(uploaded_file, 'r') as z:
                z.extractall(temp_dir)
            files = get_files_from_dir(temp_dir)

            # Speichert Hash-Werte und Metadaten
            data_dict = {}

            # Sammle alle möglichen Schlüssel
            all_keys = set()

            with ExifToolHelper() as et:
                for file in files:
                    # Berechnung der Hash-Werte
                    hash_value = calculate_hash(file)
                    # Extrahieren der Metadaten
                    metadata = {}
                    for d in et.get_metadata(file):
                        for k, v in d.items():
                            metadata[k] = v
                            all_keys.add(k)
                    # Speichern in data_dict
                    data_dict[file] = {'hash': hash_value, 'metadata': metadata}

            # Erstellen Sie einen DataFrame aus data_dict
            df = pd.DataFrame.from_dict(data_dict, orient='index')

            # Fügen Sie eine neue Spalte für Geolokationsdaten hinzu
            df['Latitude'], df['Longitude'], df['Description'] = zip(*df['metadata'].map(get_geolocation_data))

            # Filtern Sie die Zeilen, die Geolokationsdaten enthalten
            geo_df = df.dropna(subset=['Latitude', 'Longitude', 'Description'])

            if not geo_df.empty:
                st.write('Our application offers you a unique way to display geographical metadata on an interactive map. If your files contain longitude and latitude information in their metadata, this information is extracted and the files are placed on a map accordingly. This feature allows you to gain a better understanding of the geographical distribution of your files. This can be particularly useful if you manage large amounts of data generated in different locations, such as photos, research data or other geolocated information. Visualise the geographical aspects of your data in a simple and intuitive way with our cartographic display feature.')
                plot_on_map(geo_df)

            # Erstellen eines DataFrames für die Metadaten
            metadata_df = pd.DataFrame(columns=["File", "Hash"] + list(all_keys))
            for file, data in data_dict.items():
                row = {"File": file, "Hash": data['hash']}
                row.update(data['metadata'])
                metadata_df = metadata_df._append(row, ignore_index=True)

            if "PDF:Keywords" in metadata_df.columns:
                metadata_df["PDF:Keywords"] = metadata_df["PDF:Keywords"].apply(normalize_keywords)

            if "XMP:Creator" in metadata_df.columns:
                metadata_df['XMP:Creator'] = metadata_df['XMP:Creator'].apply(normalize_creator)

            if "XMP:Subject" in metadata_df.columns:
                metadata_df['XMP:Subject'] = metadata_df['XMP:Subject'].apply(normalize_subject)

            if "XMP:CrossMarkDomains" in metadata_df.columns:
                metadata_df['XMP:CrossMarkDomains'] = metadata_df['XMP:CrossMarkDomains'].apply(normalize_column)

            st.subheader('Single file metadata')
            st.write('This area displays the metadata of a selected individual file. You can view detailed information such as file type, creation date, modification date, size and other specific metadata. This section allows users to gain deeper insight into individual files and to manage and analyse this data efficiently. The display is user-friendly and easy to navigate, with metadata categories clearly defined and easy to understand.')

            # Anzeigen der Metadaten in einer Tabelle
            st.dataframe(metadata_df.fillna(""))

            # Exportieren der Metadaten-Tabelle
            csv = metadata_df.to_csv(index=False)
            st.download_button(
                label="Download CSV File",
                data=csv,
                file_name='metadata.csv',
                mime='text/csv'
            )

            # DataFrames zur Speicherung der Ausgabe
            output_df = pd.DataFrame(columns=['File1', 'File2', 'System', 'Similarity'])
            matching_keys_df = pd.DataFrame(columns=['File1', 'File2', 'System', 'Matching Keys'])

            # Vergleichen Sie die Hash-Werte und Metadaten von jeder Datei mit denen jeder anderen Datei
            for i in range(len(files) - 1):
                file1 = files[i]
                data1 = data_dict[file1]
                for j in range(i + 1, len(files)):  # Startet von i+1, so dass jede Paarung nur einmal vorkommt
                    file2 = files[j]
                    data2 = data_dict[file2]

                    if data1['hash'] == data2['hash']:
                        file1_name = os.path.basename(file1)
                        file2_name = os.path.basename(file2)
                        st.warning(f'Attention: The files {file1_name} and {file2_name} have the same hash value.')

                    # Gewichtete Ähnlichkeitsbewertung
                    for system in ['equal', 'important_keys', 'rare_keys']:
                        similarity, matching_keys = calculate_weighted_similarity(data1['metadata'], data2['metadata'], system, custom_weights)

                        output_df = output_df._append(
                            {'File1': file1, 'File2': file2, 'System': system, 'Similarity': similarity},
                            ignore_index=True)
                        if matching_keys:  # Nur wenn es übereinstimmende Schlüssel gibt
                            matching_keys_df = matching_keys_df._append(
                                {'File1': file1, 'File2': file2, 'System': system, 'Matching Keys': matching_keys},
                                ignore_index=True)

            st.subheader('Tabulated comparative data')
            st.write('This section presents comparison data in a customisable table. Each column represents a metadata category and each row represents a record. Users can easily identify differences and similarities and sort the data as they wish. They can select which metadata categories to display, allowing flexible and intuitive analysis of data.')

            # Anzeigen der Daten in einer Tabelle
            st.markdown('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            st.dataframe(output_df, height=500)
            st.download_button(
                label="Download CSV File",
                data=csv,
                file_name='metadata_compared.csv',
                mime='text/csv'
            )

            # Zusammenführen der DataFrames
            output_df = output_df.merge(matching_keys_df, how='left', on=['File1', 'File2', 'System'])

            # Erstellen einer neuen Spalte "File1_File2" für das Balkendiagramm
            output_df['File1_File2'] = output_df['File1'] + " <-> " + output_df['File2']

            st.subheader('Metadata comparison plot')
            st.write('What you see here is an intuitive tool that helps you quickly capture the similarities between different file pairs. The bars of the diagram represent the similarity values derived from the contents or properties of the files. The higher the bar, the greater the similarity between the file pairs.')
            st.write('The coloured bar chart simplifies data interpretation and makes it easy to directly compare the similarity values of different file pairs. This is especially useful when working with a large number of files, as it eliminates the need for manual comparisons, which can be time-consuming and error-prone. Use this tool to work more efficiently and make informed decisions based on your data.')

            # Erstellen des Balkendiagramms
            fig = px.bar(output_df, x='File1_File2', y='Similarity', color='System', title='Comparison of similarity for files',
                         labels={'File1_File2': 'Dateipaar', 'Similarity': 'Similarity'},
                         category_orders={"File1_File2": output_df['File1_File2'].unique()})

            # Anpassen der Größe der Grafik
            fig.update_layout(height=1000, width=2000)

            # Reduzieren der Anzahl der Zeichen in der x-Achsenbeschriftung
            max_chars_per_label = 30
            ticktext = [f"{file1.split('/')[-1][:max_chars_per_label]} <-> {file2.split('/')[-1][:max_chars_per_label]}"
                        for file1, file2 in zip(output_df['File1'], output_df['File2'])][::2]
            fig.update_layout(xaxis=dict(tickmode='array', tickvals=fig.data[0].x, ticktext=ticktext))

            # Anzeigen des Plots in Streamlit
            st.plotly_chart(fig)

if __name__ == "__main__":
    main()