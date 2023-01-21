def external_data_from_prices(symbol, open, high, low, close1, close2):
    return {
        "Meta Data": {
            "1. Information": "Daily Time Series with Splits and Dividend Events",
            "2. Symbol": symbol,
            "3. Last Refreshed": "2022-11-25",
            "4. Output Size": "Compact",
            "5. Time Zone": "US/Eastern",
        },
        "Time Series (Daily)": {
            "2022-11-25": {
                "1. open": open,
                "2. high": high,
                "3. low": low,
                "4. close": close1,
                "5. adjusted close": "111.41",
                "6. volume": "12007566",
                "7. dividend amount": "0.0000",
                "8. split coefficient": "1.0",
            },
            "2022-11-23": {
                "1. open": "12.4",
                "2. high": "13.0",
                "3. low": "12.1",
                "4. close": close2,
                "5. adjusted close": "112.24",
                "6. volume": "21343083",
                "7. dividend amount": "0.0000",
                "8. split coefficient": "1.0",
            },
        },
    }


def external_data_unknown_symbol(symbol):
    return {"Error Message": "Invalid API call."}
