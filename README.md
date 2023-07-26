# FI-MINT
## File Metadata Intelligence

FI-MINT is a Python-based application that allows you to extract, visualise and analyse metadata from your files. It 
provides an intuitive and user-friendly interface to perform deep and nuanced analyses of your metadata. With unique 
features such as custom weighting, comparison tables, similarity plots, geolocation and hash value comparison, MetaSense 
provides a powerful tool to make sense of your data.

[![License](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)
![GitHub Repo stars](https://img.shields.io/github/stars/tmwProjects/FI-MINT?style=social) 
![GitHub followers](https://img.shields.io/github/followers/tmwProjects?style=social) 
<a href="https://datasci.social/@tmwProjects">
  <img src="https://img.shields.io/mastodon/follow/110580864516294518?domain=https://datasci.social&style=social" alt="Mastodon follow">
</a>
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/tmwProjects/FI-MINT) 
[![Visit my site](https://img.shields.io/badge/Visit%20my%20site-Online-important)](https://tmwprojects.github.io/)
[![Donate on Liberapay](https://img.shields.io/badge/Donate-Liberapay-yellow)](https://liberapay.com/tmwProjects/donate)
<a href="https://www.buymeacoffee.com/tmwcontactQ"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" height="20.4px"></a>

***

### Current features

**File upload**: <br> Upload a ZIP file containing the files whose metadata you want to analyse.

**Custom weighting settings**: <br> Specify specific metadata categories (keys) and their respective weightings. This means how important they should be in the comparison calculation. Example: Author:3, Title:2. Weightings help to refine the similarity calculations.

**Individual file metadata**: <br> Here you can view the metadata of a selected file. You can view detailed information such as file type, creation date, modification date, size and other specific metadata.

**Tabular comparison data**: <br> Here, the comparison data is presented in a user-defined table. Users can easily identify differences and similarities and sort the data as desired.

**Metadata comparison plot**: <br> This intuitive tool helps you quickly capture the similarities between different pairs of files. It displays the similarity values derived from the content or properties of the files.

**Geolocation**: <br> If your files contain longitude and latitude information in their metadata, this information is extracted and the files are placed on a map accordingly.

**Download CSV**: <br> You can download the metadata and comparison data as CSV files.

**Hash value comparison**: <br> MetaSense calculates the SHA-256 hash values for each uploaded file. If two files have the same hash value even though they have different names, a notification is issued. This helps to identify duplicate or identical files.

***

> #### Hint:
> Please note that FI-MINT can currently only be run on local systems. The reason for this is that the programme requires the ExifTool to be installed on your computer. This tool is essential for running MetaSense as it is responsible for reading the metadata from the files.

***

## Installation guide

The following steps will guide you through the installation and setup of MetaSense:

**Clone the repository**:

```bash
git clone https://github.com/tmwProjects/FI-MINT.git
```

**Change to the cloned directory**:

```bash
cd FI-MINT
```

**Install the necessary Python packages**:

If you are using pip:

```bash
pip install -r requirements.txt
```

If you use conda:

```bash
conda create --name fi_mint --file requirements.txt
```


**Install the ExifTool**:

FI-MINT uses ExifTool to read the metadata. Here are the installation instructions for different operating systems:

For Windows: download ExifTool from the official website and add it to your system path.

For MacOS: You can install ExifTool with Homebrew: 

```bash
brew install exiftool
```

For Linux: use the appropriate package manager of your system, for example on Ubuntu: 

```bash
sudo apt-get install libimage-exiftool-perl
```

Start the application:

After you have installed all the necessary packages and tools, you can start FI-MINT:

```bash
streamlit run fi_mint.py
```

Now you can open and use FI-MINT in your favourite browser.

## Usage

![How to use FI-MINT](https://raw.githubusercontent.com/tmwProjects/FI-MINT/master/grafics/fi_mint_example.gif)

***

## Future features

- **Appropriate standard weighting for the metadata (comparison plot)**
- **Comparison of changes in metadata and content of specific files by category**
- **Advanced filter mechanisms for tabular data**
- **Use MetaSense online on Streamlit or other platforms**

***

## Note

Please note that certain known problems may occur when using metadata from different file formats. These problems are 
often related to the specific peculiarities of the respective file formats and may result in metadata not being extracted 
or interpreted correctly.

[ExifTool](https://exiftool.org/), a comprehensive metadata handling tool developed by Phil Harvey, is an excellent resource for navigating these 
challenges. Harvey has extensively documented many of these potential problems. It is advisable to familiarise yourself 
with these resources and use ExifTool to achieve the best possible results. However, unexpected situations can still arise, 
so it is important to do your own testing and validation.

***

## References

[1] **hashlib** - Secure hashes and message digests. Python Software Foundation. Python Language Reference, version 3.x. [Online]. Available: https://docs.python.org/3/library/hashlib.html

[2] **os** - Miscellaneous operating system interfaces. Python Software Foundation. Python Language Reference, version 3.x. [Online]. Available: https://docs.python.org/3/library/os.html

[3] **pandas** - Wes McKinney. Data Structures for Statistical Computing in Python, Proceedings of the 9th Python in Science Conference, 51-56 (2010) [Online]. Available: https://pandas.pydata.org

[4] **exiftool** - Phil Harvey's ExifTool. Perl library plus a command-line application for reading, writing and editing meta information in a wide variety of files. [Online]. Available: https://exiftool.org/

[5] **streamlit** - Streamlit. The fastest way to build custom ML tools. [Online]. Available: https://streamlit.io/

[6] **tempfile** - Generate temporary files and directories. Python Software Foundation. Python Language Reference, version 3.x. [Online]. Available: https://docs.python.org/3/library/tempfile.html

[7] **zipfile** - Work with ZIP archives. Python Software Foundation. Python Language Reference, version 3.x. [Online]. Available: https://docs.python.org/3/library/zipfile.html

[8] **plotly.express** - Plotly Express. A terse, consistent, high-level API for creating figures. [Online]. Available: https://plotly.com/python/plotly-express/

[9] **base64** - Base16, Base32, Base64, Base85 Data Encodings. Python Software Foundation. Python Language Reference, version 3.x. [Online]. Available: https://docs.python.org/3/library/base64.html

[10] **folium** - Python Data, Leaflet.js Maps. [Online]. Available: https://python-visualization.github.io/folium/

[11] **streamlit_folium** - folium functionality for streamlit. [Online]. Available: https://pypi.org/project/streamlit-folium/

***

### Acknowledgement

Hey there! It's really great that you appreciate my work on GitHub! Everything you see here is a product of my voluntary 
efforts, and I'm all about sharing useful content. If you find value in what I do and would like to support me, you might 
consider buying me a coffee. Thank you so much for your generosity and support!

###### Hint: If you would like to buy me a "Coffee", please give a name/pseudonym and the project,I would like to have the possibility to thank you by name. - Thanks :)

***

### License

**MIT License**

The MIT licence is a very permissive licence created by the Massachusetts Institute of Technology. It basically allows 
you to do almost anything you want with the licensed code - you can modify it, incorporate it into your own software 
and sell your software if you want. The only condition is that you always retain the MIT licence in your copies of the 
original or modified code. In other words, you must always recognise that the original code is under the MIT licence.