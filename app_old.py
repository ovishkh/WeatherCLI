import requests
from api.weather_api import display_weather_table, fetch_weather_for_country
from info.info import DevInfo
from services.history_service import HistoryService
from models.weather_model import Weather
from favorites.favorites_service import FavoritesService
from resources.goods import PREDEFINED_CITIES,WEATHER_TIPS, WEATHER_QUOTES
from api.weather_api import API_KEY, WEATHER_URL 



def main():
    app_info = DevInfo()
    history_service = HistoryService()
    favorites_service = FavoritesService()
    

    app_info.show_app_info()
    print("\nCommands:")
    print(" - Type 'exit' to quit the application.")
    print(" - Type 'history' to view your search history.")
    print(" - Type 'favorites' to manage your favorite cities.")
    print(" - Type 'about' to know more about the app.")

    while True:
        choice = input("\nEnter a country name, city name, or command: ").strip()

        if choice.lower() == "exit":
            print("Goodbye! Thank you for using this app.")
            break
        elif choice.lower() == "history":
            history_service.show_history()
        elif choice.lower() == "favorites":
            print("\nFavorite Cities Menu:")
            print("1. View Favorites")
            print("2. Add a City to Favorites")
            print("3. Fetch Weather for Favorites")
            action = input("Choose an option (1/2/3): ").strip()

            if action == "1":
                favorites_service.show_favorites()
            elif action == "2":
                city_to_add = input("Enter the city name to add to favorites: ").strip()
                favorites_service.add_to_favorites(city_to_add)
            elif action == "3":
                fav_weather = favorites_service.fetch_favorites_weather()
                if fav_weather:
                    display_weather_table(fav_weather)
                    for weather in fav_weather:
                        history_service.add_to_history(weather)
            else:
                print("Invalid option. Please try again.")
                
        elif choice.lower() == "about":
            app_info.show_developer_info()        
        else:
            # Handle weather search by country or city
            if choice.lower() in PREDEFINED_CITIES:
                weather_data = fetch_weather_for_country(choice)
                if weather_data:
                    display_weather_table(weather_data)
                    for weather in weather_data:
                        history_service.add_to_history(weather)
            else:
                # Treat input as a city name
                weather_data = []
                params = {
                    "q": choice,
                    "appid": API_KEY,
                    "units": "metric",
                }
                try:
                    response = requests.get(WEATHER_URL, params=params)
                    if response.status_code == 200:
                        data = response.json()
                        weather = Weather(data)
                        weather.display_single_city_weather()
                        weather_data.append(weather.to_dict())
                        history_service.add_to_history(weather.to_dict())
                    else:
                        print(f"Error fetching weather for {choice}: {response.status_code}")
                except requests.RequestException as e:
                    print(f"Error fetching weather for {choice}: {e}")

            # if weather_data:
            #     display_weather_table(weather_data)
            #     for weather in weather_data:
            #         history_service.add_to_history(weather)

if __name__ == "__main__":
    main()