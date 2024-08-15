# Omdena Kutch, India | Cultivate: Enhancing Urban Gardening with Geospatial Intelligence

## Project Overview

This project, in collaboration with Omdena Kutch, India chapter, aims to enhance urban gardening practices using geospatial intelligence. We're developing a system that recommends suitable plants for urban gardens based on location-specific data and user preferences.

## Features

- **Location-based Plant Recommendations**: Suggests plants suitable for specific urban locations.
- **User Preference Integration**: Considers user inputs like sunlight availability and garden type.
- **Geospatial Data Utilization**: Leverages climate and soil data for accurate recommendations.
- **Interactive Web Interface**: Easy-to-use Streamlit frontend for user interaction.
- **Robust Backend**: FastAPI backend for efficient data processing and API endpoints.

## Technology Stack

- Frontend: Streamlit
- Backend: FastAPI
- Data Processing: Python (Pandas, NumPy)
- Geospatial Analysis: Rasterio, GeoPy
- Machine Learning: Scikit-learn
- Data Storage: CSV files, Raster data (WorldClim)

## Project Structure


```
├── ./
│   ├── .DS_Store
│   ├── requirements.txt
│   ├── .dagshub.yaml
│   ├── README.md
│   ├── create_readme.py
│   ├── data/
│   │   ├── .DS_Store
│   │   ├── Complete_Plant_Data_preprocess V2.csv
│   │   ├── cleaned_soil_data.csv
│   │   ├── worldclim/
│   │   │   ├── wc2.1_10m_tmin_01.tif
│   │   │   ├── wc2.1_10m_tmin_02.tif
│   │   │   ├── ..
│   │   │   ├── wc2.1_10m_tmin_11.tif
│   │   │   ├── wc2.1_10m_tmin_12.tif
│   ├── src/
│   │   ├── run.py
│   │   ├── .DS_Store
│   │   ├── __init__.py
│   │   ├── app/
│   │   │   ├── .DS_Store
│   │   │   ├── main.py
│   │   │   ├── utils/
│   │   │   │   ├── helpers.py
│   │   │   ├── pages/
│   │   │   │   ├── home.py
│   │   │   │   ├── about.py
│   │   ├── api/
│   │   │   ├── models.py
│   │   │   ├── main.py
```

## Setup and Installation

1. Clone the repository:
   ```
   git clone [repository URL]
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python run.py
   ```

## Usage

1. Navigate to the provided local URL after running the application.
2. Enter your location and garden preferences.
3. Receive personalized plant recommendations suitable for your urban garden.

## Contributing

We welcome contributions to this project. Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

[Insert chosen license here]

## Contact

Project Link: [Insert project repository URL]

## Acknowledgements

- Omdena Kutch, India Chapter
- [Any other acknowledgements]
