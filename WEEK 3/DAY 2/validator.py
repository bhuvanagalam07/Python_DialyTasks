def validate_weather(data):
    """Validate the structure and values of a weather record."""
    if not isinstance(data, dict):
        raise ValueError("Weather data must be a JSON object.")

    required_fields = ["city", "temperature", "humidity"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    if not isinstance(data["city"], str) or not data["city"].strip():
        raise ValueError("City must be a non-empty string.")

    temperature = data["temperature"]
    if isinstance(temperature, bool) or not isinstance(temperature, (int, float)):
        raise ValueError("Temperature must be numeric.")

    humidity = data["humidity"]
    if isinstance(humidity, bool) or not isinstance(humidity, (int, float)):
        raise ValueError("Humidity must be numeric.")
    if not 0 <= humidity <= 100:
        raise ValueError("Humidity must be between 0 and 100.")

    return data
