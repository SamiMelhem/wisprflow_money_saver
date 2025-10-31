from window_capture import test_window_capture
from ocr_extractor import OCRExtractor
from calculator import test_calculator
from json import load

if __name__ == "__main__":
    # Capture the window with the metrics
    file_name = test_window_capture()
    # Extract the words and WPM from the image using OCR
    words, wpm = OCRExtractor().extract_metrics(file_name)
    print(f"Words: {words}, WPM: {wpm}")

    # Load inputs from JSON file, or prompt user if file doesn't exist
    try:
        with open('computer_inputs.json', 'r') as f:
            inputs = load(f)
        
        typing_wpm = inputs['typing_wpm']
        subscription_type = inputs['subscription_type']
        hourly_rate = inputs['hourly_rate']
        daily_words = inputs['daily_words']
        print("Using inputs from computer_inputs.json")

    except FileNotFoundError:
        print("inputs.json not found. Please enter your data manually.")
        typing_wpm = int(input("Enter your typing speed in WPM: "))
        subscription_type = input("Enter your subscription type (student, pro_monthly, pro_annually): ")
        hourly_rate = float(input("Enter your hourly rate: "))
        daily_words = int(input("Enter your daily words spoken per day that you would like to speak for: "))

    test_calculator(
        words_spoken = words,
        speaking_wpm = wpm,
        typing_wpm = typing_wpm,
        subscription_type = subscription_type,
        hourly_rate = hourly_rate,
        daily_words = daily_words
    )

    # Mobile inputs
    with open('mobile_inputs.json', 'r') as f:
        inputs = load(f)
    
    typing_wpm = inputs['typing_wpm']
    subscription_type = inputs['subscription_type']
    hourly_rate = inputs['hourly_rate']
    daily_words = inputs['daily_words']
    print("Using inputs from mobile_inputs.json")

    test_calculator(
        words_spoken = 810,
        speaking_wpm = 116,
        typing_wpm = typing_wpm,
        subscription_type = subscription_type,
        hourly_rate = hourly_rate,
        daily_words = daily_words
    )
        