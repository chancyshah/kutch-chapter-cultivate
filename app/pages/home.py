import streamlit as st
from app.utils.helpers import get_coordinates, create_map, search_plants, clean_plant_name
import wikipedia
import requests
import json
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

def get_wiki_image(search_term):
    cleaned_term = clean_plant_name(search_term)
    try:
        result = wikipedia.search(cleaned_term, results=1)
        if not result:
            logger.info(f"No Wikipedia search results for {cleaned_term}")
            return None
        wikipedia.set_lang('en')
        wkpage = wikipedia.WikipediaPage(title=result[0])
        title = wkpage.title
        response = requests.get(WIKI_REQUEST + title)
        json_data = json.loads(response.text)
        img_link = list(json_data['query']['pages'].values())[0]['original']['source']
        return img_link
    except Exception as e:
        logger.error(f"Error fetching image for {cleaned_term}: {str(e)}")
        return None

def show(backend_url):
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown('<p class="medium-font">Find Your Location</p>', unsafe_allow_html=True)
        location_input = st.text_input("Enter location (e.g., city, address):")
        search_location = st.button("Search Location")

        if search_location and location_input:
            with st.spinner('Searching for location...'):
                lat, lon = get_coordinates(location_input)
            if lat and lon:
                st.success(f"Location found: {lat}, {lon}")
                st.session_state['lat'] = lat
                st.session_state['lon'] = lon
                m = create_map(lat, lon)
                st.components.v1.html(m._repr_html_(), height=300)
            else:
                st.error("Unable to find location. Please check your internet connection and try again, or enter a different address.")

    with col2:
        st.markdown('<p class="medium-font">Plant Preferences</p>', unsafe_allow_html=True)
        
        sunlight = st.selectbox("Select sunlight:", ["", "Full Sunlight", "Partial Shade", "Full Shade"])
        garden_type = st.selectbox("Select garden type:", ["", "City Courtyard", "Cottage/Informal", "Wildlife Garden"])
        spread = st.selectbox("Select spread:", ["", "0.1-0.5 meters", "0.5-1.0 meters", "1.0-1.5 meters"])

    if st.button("Search Plants"):
        if 'lat' not in st.session_state or 'lon' not in st.session_state:
            st.error("Please select a location first.")
        elif not all([sunlight, garden_type, spread]):
            st.error("Please select all plant preferences.")
        else:
            with st.spinner('Searching for plants...'):
                plants = search_plants(backend_url, location_input, sunlight, garden_type, spread)
            if plants is not None:
                if len(plants) > 0:
                    st.success(f"Found {len(plants)} matching plants!")
                    display_plants(plants)
                else:
                    st.warning("No plants found matching your criteria. Try adjusting your preferences.")
            else:
                st.error("An error occurred while searching for plants. Please try again later.")

    st.markdown("""
    <p class='small-font'>
    This plant finder uses your location and preferences to recommend suitable plants for your urban garden. 
    The suitability score indicates how well each plant matches your criteria. 
    Images are sourced from Wikipedia and may not always be available or accurate.
    </p>
    """, unsafe_allow_html=True)

    
def display_plants(plants):
    st.markdown('<p class="medium-font">Recommended Plants</p>', unsafe_allow_html=True)
    
    for i, plant in enumerate(plants, 1):
        with st.container():
            st.markdown(f"<p class='small-font highlight'>Plant Recommendation #{i}</p>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 2])
            
            with col1:
                common_name = plant['common_name'] or 'N/A'
                botanical_name = plant['botanical_name']
                st.markdown(f"**Common Name:** {common_name}")
                st.markdown(f"**Botanical Name:** *{botanical_name}*")
                st.write(f"**Plant Type:** {plant['plant_type']}")
                st.write(f"**Min Temperature:** {plant['temperature']:.1f}°C")
                
                st.markdown("**Suitability Score**")
                st.progress(min(plant['similarity_score'], 1.0))
                st.write(f"{plant['similarity_score']:.2f}")
            
            with col2:
                with st.spinner('Loading image...'):
                    image_url = get_wiki_image(botanical_name)
                if image_url:
                    try:
                        st.image(image_url, caption=common_name, use_column_width=True)
                    except Exception as e:
                        logger.error(f"Error displaying image: {str(e)}")
                        st.error("Image preview not available")
                else:
                    cleaned_name = clean_plant_name(botanical_name)
                    st.write(f"No image available for {cleaned_name}")
                    logger.info(f"Failed to find image for {cleaned_name}")
            
            st.markdown("---")

    st.markdown("""
    <p class='small-font'>
    The suitability score indicates how well the plant matches your specified criteria. 
    A higher score means the plant is more suitable for your garden conditions.
    Images are sourced from Wikipedia and may not always be available or accurate.
    </p>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show()


    