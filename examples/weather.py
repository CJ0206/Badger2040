import badger2040
from badger2040 import WIDTH
import urequests
import pngdec
import time

# Set your latitude and longitude here
LAT = 53.38609085276884
LNG = -1.4239983439328177
TIMEZONE = "auto"  # Determine timezone from latitude/longitude

URL = f"http://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LNG}&current_weather=true&timezone={TIMEZONE}"

# Display Setup
display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(2)

png = pngdec.PNG(display.display)

# Connect to the wireless network
display.connect()

def get_data():
    global weathercode, temperature, windspeed, winddirection, formatted_date, api_time
    try:
        print("Connecting to API...")
        r = urequests.get(URL, timeout=10)  # Add timeout for robustness
        print(f"HTTP Status Code: {r.status_code}")
        if r.status_code != 200:
            print("Error: Failed to fetch data.")
            return
        j = r.json()
        print("Data obtained:", j)  # Debugging output

        # Parse relevant data
        current = j["current_weather"]
        temperature = current["temperature"]
        windspeed = current["windspeed"]
        winddirection = calculate_bearing(current["winddirection"])
        weathercode = current["weathercode"]
        date, api_time = current["time"].split("T")  # Use a different variable name here
        year, month, day = date.split("-")
        formatted_date = f"{day}-{month}-{year}"
        print("Weather data parsed successfully.")
        r.close()
    except Exception as e:
        print(f"Error during API request or data parsing: {e}")

def calculate_bearing(d):
    # Calculates compass direction from wind direction in degrees
    dirs = ['N', 'NNE', 'NE', 'ENE', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    ix = round(d / (360. / len(dirs)))
    return dirs[ix % len(dirs)]

def draw_page():
    # Clear the display
    display.set_pen(15)  # Set pen color to white
    display.clear()  # Clear the entire display
    display.set_pen(0)  # Set pen color to black for drawing

    # Draw page header
    display.set_font("bitmap6")
    display.rectangle(0, 0, WIDTH, 20)  # Title bar
    display.set_pen(15)  # Text color for title bar
    display.text("Weather", 3, 4)  # Title text
    display.set_pen(0)  # Reset pen to black

    # Ensure font is correctly set for subsequent text
    display.set_font("bitmap8")

    if temperature is not None:
        # Render the weather icon based on the weather code
        try:
            if weathercode in [71, 73, 75, 77, 85, 86]:  # Codes for snow
                png.open_file("/icons/icon-snow.png")
            elif weathercode in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82]:  # Codes for rain
                png.open_file("/icons/icon-rain.png")
            elif weathercode in [1, 2, 3, 45, 48]:  # Codes for cloud
                png.open_file("/icons/icon-cloud.png")
            elif weathercode in [0]:  # Codes for sun
                png.open_file("/icons/icon-sun.png")
            elif weathercode in [95, 96, 99]:  # Codes for storm
                png.open_file("/icons/icon-storm.png")
            png.decode(10, 30)  # Adjust position for better placement
        except Exception as e:
            print(f"Error displaying weather icon: {e}")

        # Render weather details text
        display.set_pen(0)
        display.text(f"Temperature: {temperature}°C", 80, 30, WIDTH - 90, 2)
        display.text(f"Wind Speed: {windspeed} km/h", 80, 50, WIDTH - 90, 2)
        display.text(f"Wind Direction: {winddirection}", 80, 70, WIDTH - 90, 2)
        display.text(f"", 80, 90, WIDTH - 90, 2)
        display.text(f"Last update: {formatted_date} {api_time}", 10, 110, WIDTH - 20, 2)
    else:
        # Error message if weather data is not available
        display.set_pen(0)
        display.text("Unable to fetch weather data.", 10, 40, WIDTH - 20, 2)

    # Push all updates to the display
    display.update()

# Fetch initial data and draw the first screen
print("Fetching initial data and updating display...")
get_data()
draw_page()

# Main loop with a timer for periodic updates
last_update_time = time.time()

def format_time(t):
    return "{:02}:{:02}:{:02}".format(t[3], t[4], t[5])

while True:
    current_time = time.time()  # Numeric time
    time_now = format_time(time.localtime())  # Formatted string for display

    if current_time - last_update_time >= 900:
        print(f"{time_now} - Refreshing weather data...")
        get_data()
        draw_page()
        last_update_time = current_time

    if display.pressed(badger2040.BUTTON_B):
        print(f"{time_now} - Manual refresh triggered by button B.")
        get_data()
        draw_page()
        last_update_time = time.time()
