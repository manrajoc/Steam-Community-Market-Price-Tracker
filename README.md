# Dependencies
python-daemon (2.2.3)
requests (2.22.0)
plyer (1.4.0)

# Syntax
```
python3 tracker.py market_url critical price
```

# Example
To track item https://steamcommunity.com/market/listings/578080/PLAYERUNKNOWN%27S%20Trenchcoat
and notify when price reaches below or equal to a critical value 1000(let's say)

the command would be:
```
python3 tracker.py https://steamcommunity.com/market/listings/578080/PLAYERUNKNOWN%27S%20Trenchcoat 1000
```

# Working
It queries steam servers every 3 seconds for price update and creates a notification if the current price is equal to or lower than critical price.

Daemon process stops at only 3 conditions,
* Current price drops to or below critical price
* Steam API requests get timed-out or fail for some reason consecutively 5 times
* Daemon process is terminated externally

To terminate Daemon externally, look for process with PID equal to first line of std_out.log and kill that process with any process/resource manager or command