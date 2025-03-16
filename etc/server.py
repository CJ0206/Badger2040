import psutil
import subprocess
from flask import Flask, jsonify

app = Flask(__name__)

def get_pi_temperature():
    try:
        # Use vcgencmd for Raspberry Pi temperature
        result = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
        temp_output = result.stdout.strip()
        return float(temp_output.split('=')[1].replace("'C", ""))
    except Exception as e:
        print(f"Error getting temperature: {e}")
        return None

@app.route('/stats')
def get_stats():
    try:
        # Get SoC temperature
        cpu_temp = None
        # First attempt to use vcgencmd (for Raspberry Pi)
        cpu_temp = get_pi_temperature()
        # If vcgencmd isn't available, try psutil as a fallback
        if cpu_temp is None and hasattr(psutil, "sensors_temperatures"):
            sensors = psutil.sensors_temperatures()
            if 'coretemp' in sensors:  # For Linux systems
                cpu_temp = sensors['coretemp'][0].current

        # Get memory usage
        memory = psutil.virtual_memory()
        memory_used = memory.used / (1024 ** 2)  # Convert to MB
        memory_total = memory.total / (1024 ** 2)  # Convert to MB

        # Get disk usage
        disk = psutil.disk_usage('/')
        disk_used = disk.used / (1024 ** 3)  # Convert to GB
        disk_total = disk.total / (1024 ** 3)  # Convert to GB

        # Return stats as JSON
        return jsonify({
            'soc_temp': cpu_temp if cpu_temp is not None else "Unavailable",
            'memory_used': memory_used,
            'memory_total': memory_total,
            'disk_used': disk_used,
            'disk_total': disk_total
        })

    except Exception as e:
        # Return error message if something goes wrong
        print(f"Error in get_stats: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
