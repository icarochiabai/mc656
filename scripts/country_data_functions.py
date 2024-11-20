import pandas as pd

data_path = 'static/countries.csv'
country_data = pd.read_csv(data_path)

def get_country_code(country, data):
    """
    Returns the country code related to a given country. 
    
    Args:
        country (str): Name of the country.
        data (pd.DataFrame): Dataframe containing country data.

    Returns:
        country_code (str)
    """
    country = data[data['name'].str.contains(country, case=False, na=False)]   
    
    if country.empty:
        return "Country not found in the dataset."
    
    country_code = country.iloc[0]['country']
    return country_code

def get_country_coordinates(country, data):
    """
    Returns the coordinates of the capital of a given country. 
    
    Args:
        country (str): Name of the country.
        data (pd.DataFrame): Dataframe containing country data.

    Returns:
        tuple: (latitude, longitude)
    """
    country = data[data['name'].str.contains(country, case=False, na=False)]   
    
    if country.empty:
        return "Country not found in the dataset."
    
    lat, lon = country.iloc[0]['latitude'],country.iloc[0]['longitude']
    return lat, lon

def get_country_flag(country, data):
    """
    Returns the path to a given country's flag image. 
    
    Args:
        country (str): Name of the country.
        data (pd.DataFrame): Dataframe containing country data.

    Returns:
        flag_path (str): Path containing the image of the country's flag
    """
    country_code = get_country_code(country, data).lower()
    
    country = data[data['name'].str.contains(country, case=False, na=False)]   
    
    if country.empty:
        return "Country not found in the dataset."
    
    
    flag_path = f"static/images/{country_code}.png"
    return flag_path
