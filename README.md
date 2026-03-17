# Weather CLI
### Your Gateway to Real-Time Weather Information

---

Welcome to the **Weather App** – your ultimate companion for staying updated with the latest weather conditions! 
With features like real-time updates, personalized city management, and insightful weather-based tips, we ensure you're 
always prepared for whatever the skies bring.

---

## Table of content


1. [Introduction](#introduction)  

2. [Features](#features)  

3. [Installation](#installation)   

4. [Usage](#usage)  
  
5. [File Structure](#file-structure)  

6. [API Information](#api-information)  

7. [Dependencies](#dependencies)  

8. [Contribution](#contribution)  

9. [License](#license)
    
10. [Acknowledgements](#acknowledgements)  

---

## Introduction

The Weather App is a simple and user-friendly application designed to provide real-time weather updates. 
You can check the weather for any city or country, save your favorite locations, and view your search history. 
The app also offers helpful weather tips and motivational quotes to enhance your experience.

---


## Features

1. **Real-Time Weather Information**:
   - Fetch weather data for any city or country.
   - Displays temperature, humidity, wind speed, and weather conditions.

2. **Predefined Cities**:
   - Quickly fetch weather for predefined cities in countries like the USA, India, Canada, Australia, and more.

3. **Favorites Management**:
   - Add cities to your favorites list.
   - View and fetch weather for your favorite cities.

4. **Search History**:
   - Keeps track of your weather searches.
   - View your search history in a tabular format.

5. **Weather Tips and Quotes**:
   - Provides helpful tips and motivational quotes based on the current weather conditions.

6. **Advanced TUI Interface**:
   - Modern Terminal User Interface with sidebar navigation.
   - Real-time dashboard with world weather hub.
   - 24-hour forecasts with 3-hour interval details.
   - Immediate Unit conversion (Metric/Imperial).
   - Theme switching (Mocha Dark/Light).

7. **Developer Information**:
   - Learn about the developers behind the app.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- `pip` (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/ovishkh/WeatherApp.git
   cd WeatherApp
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

---

## Usage

1. **Start the Application**:
   - Run `python app.py` to start the app.

2. **Commands**:
   - `exit`: Quit the application.
   - `history`: View your search history.
   - `favorites`: Manage your favorite cities.
   - `about`: Learn more about the app and its developers.

3. **Search Weather**:
   - Enter a country name to fetch weather for predefined cities in that country.
   - Enter a city name to fetch weather for that specific city.

4. **Favorites Menu**:
   - Option 1: View your favorite cities.
   - Option 2: Add a city to your favorites.
   - Option 3: Fetch weather for all your favorite cities.

---

## File Structure

```
Weather-App/
├── api/
│   ├── __init__.py
│   ├── weather_api.py
├── info/
│   ├── __init__.py
│   ├── info.py
│   ├── requirment.txt
│   ├── concept.txt
├── services/
│   ├── __init__.py
│   ├── history_service.py
├── models/
│   ├── __init__.py
│   ├── weather_model.py
├── favorites/
│   ├── __init__.py
│   ├── favorites_service.py
├── resources/
│   ├── __init__.py
│   ├── goods.py
├── app.py

```

---

## API Information

This app uses the [OpenWeatherMap API](https://openweathermap.org/api) to fetch weather data. You need an API key to use this service.

- **API Key**: The app includes a default API key (`adb293c2eba52c05f58f2a3148b5bdcb`). Replace it with your own key if needed.
- **Base URL**: `http://api.openweathermap.org/data/2.5/weather`

---

## Dependencies

The following Python libraries are required:
- `requests`: For making HTTP requests to the weather API.
- `pandas`: For managing and displaying tabular data.

Install all dependencies using:
```bash
pip install -r info/requirements.txt
```

---

## Contribution
I welcome contributions to improve the Weather App! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---


---

## **Team Responsibilities**

Our weather application project is a collaborative effort, with each team member handling specific components of the project. Below is the breakdown of responsibilities for each member:

---

### **Ovi Shekh **
1. **Main Functionality**:  
   - Handles the overall program execution (`main` function) and flow of the application.  
   - Ensures smooth integration of different modules.
   
2. **API Module**:  
   - Manages API interactions to fetch weather data.  
   - Implements functions to connect with OpenWeatherMap and handle responses.

3. **Weather Model (District-wise)**:  
   - Builds models to represent weather data for specific districts.  
   - Focuses on localized weather insights.

4. **History Module**:  
   - Implements the feature to store and retrieve weather search history.  
   - Supports viewing past searches in a tabular format.

5. **Weather Movements**:  
   - Handles features related to weather phenomena like **rain** and **heatwaves**.

---

### **Apra Aditi**
1. **Weather Model (Country-wide)**:  
   - Develops models to represent weather data on a national scale.  
   - Focuses on larger geographic regions and trends.

2. **Favorites Module**:  
   - Implements the functionality for users to save and view favorite cities or locations for weather updates.

3. **Resources Module**:  
   - Manages additional resources, such as user guides, FAQs, or external links for weather-related data.

4. **Weather Movements**:  
   - Covers **snowfall** and **storms**, including predictions and reports.

---

### **Khalid Anwar**
1. **Info Module**:  
   - Handles the `Info` class for app and developer details.  
   - Manages the abstract class `AppInfo` and its implementation.  
   - Displays app information and developer credits.

2. **Project Report**:  
   - Prepares and compiles the final project documentation.  
   - Summarizes application functionality, team contributions, and technical details.

---

## **Project Summary**

This weather application provides real-time weather updates, historical data, and insights into various weather movements. It offers localized and country-wide reports and supports favorite locations for quick access. Developed collaboratively by **Team Tengen**, the project showcases robust modular design and innovative features.

---

## **Acknowledgements**

Special thanks to our team members for their dedicated contributions:
- **Ovi** for spearheading the core application functionality and district-wise insights.
- **Apra** for national-scale weather models and resource management.
- **Khalid** for enriching the app with detailed information and professional documentation.

Version: **3.0**  
Developed by **Team Tengen**  


--- 

Enjoy using the Weather App! Stay informed and prepared for any weather conditions. 🌤️
