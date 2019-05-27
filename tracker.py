# imports
import daemon, requests, sys, re, time, math, os
from urllib.parse import unquote
from plyer import notification


# check for correct parameter syntax -> python tracker.py url critical_price
if len(sys.argv) == 3:

    # split arg vector into market url and critical price
    market_url = unquote(sys.argv[1])
    critical_price = float(sys.argv[2])

    # use regex to extract appid and market_hash_name from market url
    pattern = re.compile(r"listings/")
    match = pattern.search(market_url)
    pos = match.end()

    appid, name = market_url[pos:].split("/")
    name = name.split("?")[0]

    # set payload with the extracted values from url
    payload = {
        "appid": int(appid),
        "currency": 24,
        "market_hash_name": name
    }

    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # use context manager(with) to set "std_out.log" as the stdout file descriptor
    with open("std_out.log", "w+") as std_out:

        # use DaemonContext() to create a well behaved Daemon
        with daemon.DaemonContext(working_directory=base_dir, stdout=std_out, stderr=std_out):
            # Log Daemon PID to sys.stdout
            print("PID : " ,os.getpid(), "\n")
            
            price = math.inf
            timeouts = 0

            # loop as a daemon until a price drop is detected or the API times out
            while price > critical_price and timeouts < 5:
                response = requests.get("https://steamcommunity.com/market/priceoverview/", params=payload)
                response_dict = response.json()

                # log request url, response status code and API success value
                print("URL     : ", response.url)
                print("STATUS  : ", response.status_code)
                print("SUCCESS : ", response_dict["success"])

                # chech response status and current price
                if response_dict["success"] == True:
                    price = float(response_dict["lowest_price"].split()[1])
                    timeouts = 0
                else:
                    timeouts += 1

                # sleep for 3 seconds before next request
                time.sleep(3)
            
            # create a notification when the loop breaks
            if price <= critical_price:
                notification.notify("Price Alert!", "Price dropped below critical value, current minimum = " + str(price))
            else:
                notification.notify("Error!", "Price request timedout, check internet")


# Incorrect syntax error condition
else:
    print("Incorrect input parameters\nSyntax: tracker.py steam_market_url critical_price")