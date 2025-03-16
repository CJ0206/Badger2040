import badger2040
import network
import urequests
import time

# Wi-Fi Configuration
STATS_URL = "http://192.168.1.61:5000/stats"  # Update with your computer's IP

# Initialize Badger2040
badger = badger2040.Badger2040()
badger.set_update_speed(badger2040.UPDATE_NORMAL)

# Helper function for memory progress bar
def draw_progress_bar(x, y, width, height, percentage, fill_color=0, empty_color=10):
    total_blocks = 10
    block_width = width // total_blocks  # Divide the width into equal parts
    filled_blocks = int((percentage / 100) * total_blocks)

    for i in range(total_blocks):
        if i < filled_blocks:
            badger.set_pen(fill_color)  # Filled part
        else:
            badger.set_pen(empty_color)  # Empty part
        badger.rectangle(x + i * block_width, y, block_width - 2, height)  # Spacing between blocks

    # Add percentage at the end of the bar
    badger.set_pen(0)  # Black pen for text
    badger.text(f"{percentage:.1f}%", x + width + 5, y)

while True:
    try:
        print("Fetching stats...")
        response = urequests.get(STATS_URL)
        if response.status_code == 200:
            stats = response.json()
            print("Stats received:", stats)

            # Clear the display
            badger.set_pen(15)  # White background
            badger.clear()

            # Display SoC temperature
            badger.set_pen(0)  # Black text
            badger.text(f"SoC Temp: {stats['soc_temp']}C", 10, 10)

            # Display memory usage (RAM)
            memory_percentage = (stats['memory_used'] / stats['memory_total']) * 100
            badger.text(
                f"Memory: {stats['memory_used']:.1f}MB / {stats['memory_total']:.1f}MB",
                10,
                40,
            )
            draw_progress_bar(10, 60, 150, 10, memory_percentage)

            # Display hard disk (system memory) usage
            disk_percentage = (stats['disk_used'] / stats['disk_total']) * 100
            badger.text(
                f"Disk: {stats['disk_used']:.1f}GB / {stats['disk_total']:.1f}GB",
                10,
                90,
            )
            draw_progress_bar(10, 110, 150, 10, disk_percentage)

            # Update display
            badger.update()

        else:
            print(f"Error: HTTP {response.status_code}")

        # Wait before refreshing
        time.sleep(15)

    except Exception as e:
        print("Error encountered:", e)
        badger.set_pen(15)  # White background
        badger.clear()
        badger.set_pen(0)  # Black text
        badger.text("Error fetching data", 10, 10)
        badger.text(str(e), 10, 30)
        badger.update()
        time.sleep(5)
