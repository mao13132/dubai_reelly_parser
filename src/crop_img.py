from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import base64
from PIL import Image, ImageOps
from io import BytesIO
from PIL import Image


def get_image_maps(driver):
    try:
        _frame = driver.find_element(by=By.XPATH, value=f"//div[contains(@wized, 'locationBlockProject')]"
                                                        f"//iframe")
    except:
        return False

    filename = "map.png"

    _frame.save_screenshot(filename)

    # send_image(filename, msg)


# img = Image.open("screenshot1.png")
# border = (250, 150, 30, 420)  # left, top, right, bottom
# cropped_img = ImageOps.crop(img, border)
# cropped_img.save(f'screenshot1.png')
# cropped_img.show()
# with open("image.jpg", "rb") as image_file:
#     data = base64.b64encode(image_file.read())
# im = Image.open(BytesIO(base64.b64decode(img)))
# im.save('image1.png', 'PNG')
