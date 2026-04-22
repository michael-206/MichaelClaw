tools = [
    {
        "type": "function",
        "name": "get_current_weather",
        "description": "Get current weather for a given city",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name, e.g. Toronto"
                }
            },
            "required": ["location"]
        }
    },
    {
        "type": "function",
        "name": "get_weather_forecast",
        "description": "Get the current weather and weather forcast for a given city",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name, e.g. Toronto"
                },
                "days":{
                    "type": "integer",
                    "description": "for how many days ahead to get the forecast, includes today. default is three"
                }
            },
            "required": ["location"]
        }
    },
    {
        "type": "function",
        "name": "get_nearby_departures",
        "description": "Gets the next 3 departures from all the transit stops within a certain radius of a address or lat,long",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "location from which to run the query. either a street address, or a set of coordinates: lat, long. keep responses shortish"
                },
                "radius":{
                    "type": "integer",
                    "description": "the radius around the location for which to search for transit stops, default is 400"
                }
            },
            "required": ["location"]
        }
    }
]
