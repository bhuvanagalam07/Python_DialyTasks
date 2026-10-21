def process_weather(data):
    """Apply simple domain logic to validated weather data."""
    temperature = data["temperature"]
    if temperature >= 35:
        condition_note = "It is hot."
    elif temperature <= 15:
        condition_note = "It is cool."
    else:
        condition_note = "Temperature is moderate."

    return (
        f"City: {data['city'].strip()}\n"
        f"Temperature: {temperature}°C\n"
        f"Humidity: {data['humidity']}%\n"
        f"Summary: {condition_note}"
    )
