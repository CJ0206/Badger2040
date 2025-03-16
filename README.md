# Badger2040(W) <a href='https://ko-fi.com/christianjameswatkins' target='_blank'><img height='35' align='right' style='border:0px;height:46px;' src='https://storage.ko-fi.com/cdn/kofi1.png?v1' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>
Below is a collection of random Badger2040/Badger2040 W projects.

## [O's n X's (Tic-Tac-Toe)](/examples/os_n_xs.py)
A simple game of tic-tac-toe, the Badger will need to be passed between players to play a simple three-by-three grid.

You will have to wait for the screen to fully refresh between each move (i.e. it will refresh several times between each move or placement of your mark). Press `a` and `c` to move left and right, press `up` and `down` to move up and down, press `b` to make your mark.

When the game ends it will display the winner along the left side of the screen with the winners’ symbol or declaring a draw. You can press `b` to start a new game.

## [Weather](/examples/weather.py)
Amended the [default weather example](https://github.com/pimoroni/badger2040/blob/main/badger_os/examples/weather.py) to refresh the weather data every 15 minutes, or when the `b` button is pressed.

Just update your latitude and longitude to get going: 

```
LAT = 53.38609085276884
LNG = -1.4239983439328177
```

## [Battery](/examples/battery.py)
A simple social battery, you can increase your social battery by pressing `up` for when you are happy to socialise, or decrease it by pressing `down` when you feel less sociable. There are 5 different charge levels to choose from.

## [WiFi](/examples/wifi.py)
A simple app which creates w WiFi access point on your Badger2040W so you can input the SSID and PSK of a new network by [dawidrylko](https://github.com/dawidrylko/badger2040). The WiFi code carries the [MIT Licence](https://github.com/makew0rld/wordle-badger2040).

Just make sure to set your region in the python script:
```
f.write('COUNTRY = "GB"\n')
```

You will also need to download the contents of [pages](/examples/pages) to your Badger2040W and amend the urls as appropriate:
```
with open("/examples/pages/wifi-setup.html", "r") as file:
```
```
with open("/examples/pages/wifi-setup-successful.html", "r") as file:
```

## [Profiles](/examples/profiles.py)
A simple app which extends the [default badge example](https://github.com/pimoroni/badger2040/blob/main/badger_os/examples/badge.py) by adding the ability to have multiple badge profiles.

Simply upload your multiple `.txt` profiles and matching `.png` or `.jpg` to the existing `/badges` directory. Please note the text and image file names must match.

## [Wordle](/examples/wordle.py)
A fork from [makew0rld](https://github.com/makew0rld/wordle-badger2040) and lightly updated to run on the latest version of the picographics library. The Wordle code carries the [MIT Licence](https://github.com/makew0rld/wordle-badger2040).

You will need to download [winners.txt](/examples/winners.txt), and [all_words.txt](/examples/all_words.txt) to your examples folder along with the python script in order to play.

How to play:
1. Use the *B* and *C* buttons to cycle through the alphabet.
2. Use the arrow buttons to move between squares.
3. Press the *A* button to submit a word.

## [Stats](/examples/stats.py)
A simple app which can show your SoC temperature, memory usage, and disk usage of a Raspberry Pi wirelessly.

This app requires you to run a [server](/etc/server.py) on your Raspberry Pi, to get this code to work you may need to install `flask` (to run the server) and `psutil` (to retrieve the stats):
```
sudo apt update
sudo apt install python3-flask python3-psutil
```

Simply start the server with:
```
python3 server.py
```

In the Badger2040W's code youwill need to update the IP addreeess of your Raspberry Pi:
```
STATS_URL = "http://192.168.1.61:5000/stats"  # Update with your computer's IP
```

The badge will show something similar to the below, the stats will update every 15 seconds (this can be updated on line 76 `time.sleep(15)`):
```
SoC Temp: 47.7C

Memory: 2667.0MB /8048.3MB
███▒▒▒▒▒▒▒ 33.1%

Disk: 5.9GB /28.5GB
██▒▒▒▒▒▒▒▒ 20.7%
```
