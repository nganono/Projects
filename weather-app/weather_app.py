#import libraries
import datetime
import requests
from requests.exceptions import RequestException
import csv
import time
from statistics import mean, median, mode

#Funtion for users to enter the name of the city
def city_name():
    while True:
        city = input("Enter the name of the city: ").strip()
        if city:
            return city
        else:
            print("City name cannot be empty. Please try again.")


# Function to fetch current weather data from API
def current_weather(api_key, city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching current weather data: {e}")
        return None

#Function to display current weather data
def display_weather_data(today_weather):
    try:
        city = today_weather['name']
        lat= today_weather["coord"]["lat"]
        lon= today_weather["coord"]["lon"]
        weather_description = today_weather['weather'][0]['description']
        current_temperature = today_weather['main']['temp']
        current_pressure = today_weather['main']['pressure']
        current_humidity = today_weather['main']['humidity']
        return city, lat, lon, weather_description,current_temperature, current_pressure, current_humidity
    except Exception as e:
        print(f"Error displaying weather data: {e}")


#Function to fetch historical weather data for the last seven days from API
def fetch_historical_weather(lat, lon, api_key):
    try:
        # Store Historical data in dictionary
        historical_data = []
        # Get current Unix timestamp
        current_timestamp=time.time()
        for i in range(1,8):
        # Get past seven days Unix timestamp
            unix_timestamp = int(current_timestamp - (24*60*60*i))
            url = f'http://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={unix_timestamp}&appid={api_key}&units=metric'
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            historical_data.append(data)
        return historical_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching historical weather data: {e}")
        return []

# Function to dispay historical weather data for the last seven days
def fetch_7_days_temperatures(historical_data):
    try:
        temp_dates = {}
        for temperature in historical_data:
            for i in temperature['data']:
                timestamp = i['dt']
                date = datetime.datetime.fromtimestamp(timestamp, datetime.UTC).strftime('%Y-%m-%d')
                temp_dates[date] = i['temp']
        return temp_dates
    except Exception as e:
        print(f"Error fecthing temperature: {e}")

# Function to calculate statistics for the last seven days
def calculate_statictics(temperatures):
    try:
        average_temp= round((sum(temperatures) / len(temperatures)), 2)
        median_temp=median(temperatures)
        mode_temp=mode(temperatures)
        return average_temp, median_temp, mode_temp
    except:
        average_temp=None
        mode_temp=None
        median_temp=None

# Function to save data and statistical analysis results to a CSV file
def save_to_csv(city, lat, lon, weather_description,current_temperature, current_pressure, current_humidity,
                temp_dates, average_temp, median_temp, mode_temp ):
    try:
        filename = f"{city}_weather_data.csv"
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([city, "Values"])
            writer.writerow(["Temperature", str(current_temperature)+"C"])
            writer.writerow(["Pressure", str(current_pressure)+"hPa"])
            writer.writerow(["Humidity", str(current_humidity)+"%"])
            writer.writerow(["Weather Description", weather_description])
            writer.writerow([])

            writer.writerow(["Historical weather data (last 7 days):"])
            writer.writerow(["Date", "Temperature(C)"])
            for date, temperature in temp_dates.items():
              writer.writerow([date, temperature])

            writer.writerow([])

            writer.writerow(["Statistics", "Temperature(C)"])
            writer.writerow(["Average Temperature", average_temp])
            writer.writerow(["Median Temperature", median_temp])
            writer.writerow([f"Mode Temperature", mode_temp])
        print("Data saved to CSV file successfully.")
    except Exception as e:
        print(f"Error saving data to CSV file: {e}")

# Main function to run the application
def main():
    try:
        api_key= 'f785af6ca494bcbd7a1417fa690d7d58'
        city=city_name()
        today_weather=current_weather(api_key, city)
    
        # Display current weather data
        city, lat, lon, weather_description,current_temperature, current_pressure, current_humidity=display_weather_data(today_weather)
        print(f"Current Weather in {city} Coordinates({lat},{lon}):")
        print(f"Weather Description: {weather_description}.")
        print(f"Temperature: {current_temperature}°C")
        print(f"Pressure: {current_pressure}hPa")
        print(f"Humidity: {current_humidity}%")

        # Dispay historical weather data for the last seven days
        historical_data=fetch_historical_weather(lat, lon, api_key)
        print("\nHistorical weather data (last 7 days):")
        temp_dates=fetch_7_days_temperatures(historical_data)
        for date, temperature in temp_dates.items():
            print(f"{date}: {temperature}°C")
    
        #cDisplay statistics for the last seven days
        temperatures=list(temp_dates.values())
        average_temp, median_temp, mode_temp= calculate_statictics(temperatures)
        print("\nStatistics for the last seven days:")
        print(f"Average Temperature: {average_temp}°C")
        print(f"Median Temperature: {median_temp}°C")
        print(f"Mode Temperature: {mode_temp}°C")
        print()

        # Save data and statistics to a CSV file
        save_to_csv(city, lat, lon, weather_description,current_temperature, current_pressure, current_humidity,
                temp_dates, average_temp, median_temp, mode_temp )
    
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
