import json

from parser import parse_json
from validator import validate_weather
from processor import process_weather


def main():
    raw_text = input("Enter weather JSON: ")

    try:
        data = parse_json(raw_text)
        validated_data = validate_weather(data)
        result = process_weather(validated_data)
        print("Weather data validated successfully.")
        print(result)
    except ValueError as error:
        print(f"Input error: {error}")


if __name__ == "__main__":
    main()
