import mss
import pygetwindow as gw
from PIL import Image
import time

class WindowCapture:
    def __init__(self):
        self.wisprflow_window = None
    
    def find_wisprflow_window(self):
        """
        Find the WisprFlow window by searchign for windows
        that contain 'Wispr Flow' in the title.
        """
        # Get all of the windows on the screen
        windows = gw.getAllWindows()

        for window in windows:
            if window.title == "Hub": # This is WisprFlow's window title
                self.wisprflow_window = window
                return True
    
        return False
    
    def capture_window(self):
        """
        Capture a screenshot of the WisprFlow window.
        Return: PIL Image object
        """
        was_minimized = self.wisprflow_window.isMinimized
        orig_active = gw.getActiveWindow()

        if was_minimized:
            self.wisprflow_window.restore()
            time.sleep(0.012)

        self.wisprflow_window.maximize()

        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        
        if was_minimized:
            self.wisprflow_window.minimize()
        
        if orig_active:
            try:
                orig_active.activate()
            except:
                pass

        return img
    
    def capture_top_right_region(self, img):
        """
        Extract the top-right region where the metrics are displayed.
        """
        width, height = img.size

        # Rough estimates of the top-right region
        right_start = int(width * 0.6825)
        top_start = int(height * 0.13)
        right_end = int(width * 0.83)
        region_height = int(height * 0.03)

        # Crop the image
        region = img.crop((
            right_start,
            top_start,
            right_end,
            top_start + region_height
        ))

        return region
    
def test_window_capture():
    """Test the window capture functionality."""
    capture = WindowCapture()

    if capture.find_wisprflow_window():
        print("WisprFlow window found.")
        # Capture the screenshot
        screenshot = capture.capture_window()

        # # Save for debugging
        # screenshot.save("debug_screenshot.png")
        # print("Debug screenshot saved to debug_screenshot.png")

        # Extract top-right region
        region = capture.capture_top_right_region(screenshot)

        # Save for debugging
        region.save("stats.png")
        print("Stats region saved to stats.png")
        
        return region

    print("WisprFlow window not found.")
    return None

if __name__ == "__main__":
    test_window_capture()
    