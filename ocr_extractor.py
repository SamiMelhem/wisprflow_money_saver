from pytesseract import image_to_string, pytesseract
from PIL.Image import open
from re import search, IGNORECASE

class OCRExtractor:
    def __init__(self):
        # Specify the path to the Tesseract executable
        pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def extract_text_from_image(self, image_path):
        """
        Extract all text from the image using OCR.
        """
        image = open(image_path)
        text = image_to_string(image, config='--oem 3 --psm 6')
        return text.strip()

    def parse_metrics(self, text):
        words = search(r'(\d+)\s*words?', text, IGNORECASE)
        if words:
            words = int(words.group(1))
        
        wpm = search(r'(\d+)\s*WPM?', text, IGNORECASE)
        if wpm:
            wpm = int(wpm.group(1))

        return words, wpm

    def extract_metrics(self, image_path):
        """
        Extract the words and WPM from the image using OCR.
        Return: tuple (words, wpm)
        """
        
        text = self.extract_text_from_image(image_path)
        words, wpm = self.parse_metrics(text)
        return words, wpm

if __name__ == "__main__":
    words, wpm = OCRExtractor().extract_metrics("stats.png")
    print(f"Words: {words}, WPM: {wpm}")
