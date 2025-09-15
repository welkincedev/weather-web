import requests
import json
import os
import argparse
from colorama import Fore, Style, init

init(autoreset=True)  # Auto-reset color after each print

# -------------------- CONFIG --------------------
API_KEY = "3597b64f37581e5dabd6fc08902ae36e"  # Replace with your OpenWeatherMap API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
HISTORY_FILE = "history.json"
MAX_HISTORY = 5

# ------------------ WEATHER ICONS ------------------
weather_icons = {
    "clear": "☀️",
    "clouds": "☁️",
    "rain": "🌧️",
    "drizzle": "🌦️",
    "thunderstorm": "⛈️",
    "snow": "❄️",
    "mist": "🌫️",
    "fog": "🌫️"
}

# ------------------ FUNCTIONS ------------------
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(city):
    history = load_history()
    if city not in history:
        history.insert(0, city)
        history = history[:MAX_HISTORY]
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f)

def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()

        if data.get("cod") != 200:
            print(Fore.RED + f"Error: {data.get('message', 'City not found!')}" + Style.RESET_ALL)
            return

        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        desc = data["weather"][0]["description"]
        main_weather = data["weather"][0]["main"].lower()
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        icon = weather_icons.get(main_weather, "")
        print(Fore.CYAN + f"\nWeather in {city}: {icon}" + Style.RESET_ALL)
        print(Fore.YELLOW + f"Description : {desc}" + Style.RESET_ALL)
        print(Fore.GREEN + f"Temperature : {temp}°C (Feels like {feels_like}°C)" + Style.RESET_ALL)
        print(Fore.MAGENTA + f"Humidity    : {humidity}%" + Style.RESET_ALL)
        print(Fore.BLUE + f"Wind Speed  : {wind_speed} m/s\n" + Style.RESET_ALL)

        save_history(city)

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Network error: {e}" + Style.RESET_ALL)

def show_history():
    history = load_history()
    if history:
        print(Fore.CYAN + "Recent Searches:" + Style.RESET_ALL)
        for i, city in enumerate(history, 1):
            print(f"{i}. {city}")
        print()
    else:
        print(Fore.YELLOW + "No search history found.\n" + Style.RESET_ALL)

# ------------------ MAIN ------------------
def main():
    parser = argparse.ArgumentParser(description="Weather CLI - Get current weather info")
    parser.add_argument("city", nargs="?", help="City name (optional)")
    parser.add_argument("--history", action="store_true", help="Show recent search history")
    args = parser.parse_args()

    if args.history:
        show_history()
    elif args.city:
        get_weather(args.city.strip())
    else:
        city = input("Enter city name: ").strip()
        get_weather(city)

if __name__ == "__main__":
    main()
