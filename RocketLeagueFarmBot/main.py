import pytesseract
import cv2
import numpy as np
import pyautogui
import keyboard
import time

# Устанавливаем путь к исполняемому файлу Tesseract
pytesseract.pytesseract.tesseract_cmd = r'E:\Programs\Tesseract\tesseract.exe'

# Область для скриншота (left, top, width, height)
screenshot_region = (890, 10, 45, 80)

# Интервал между сменой направлений
move_interval = 1
# Интервал между скриншотами
screenshot_interval = 2
isBut = False

# Загрузка изображения для сравнения
processed_image_true = cv2.imread('processed_image_true.png', cv2.IMREAD_GRAYSCALE)

def preprocess_image(image):
    # Конвертируем изображение в градации серого
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

    # Применяем пороговую фильтрацию
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Увеличиваем изображение для улучшения распознавания
    scale_percent = 150  # увеличение на 150%
    width = int(binary.shape[1] * scale_percent / 100)
    height = int(binary.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(binary, dim, interpolation=cv2.INTER_LINEAR)

    return resized

def images_are_equal(image1, image2):
    # Сравниваем два изображения
    return np.array_equal(image1, image2)

def take_screenshot_and_check_timer():
    global isBut
    # Делаем скриншот области
    screenshot = pyautogui.screenshot(region=screenshot_region)
    print("Скрін")
    # Предобрабатываем изображение
    processed_image = preprocess_image(screenshot)

    # Сохраняем предобработанное изображение (опционально)
    cv2.imwrite("processed_image.png", processed_image)

    # Сравниваем обработанное изображение с эталонным
    if images_are_equal(processed_image, processed_image_true):
        print("Вихід")
        isBut = False
        # Выполняем действие при таймере 3 или меньше
        pyautogui.press('esc')
        time.sleep(0.5)
        for _ in range(5):
            pyautogui.press('down')
            time.sleep(0.1)
        time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.1)
        pyautogui.press('left')
        time.sleep(0.1)
        pyautogui.press('enter')
        isBut = True

def main():
    global isBut
    last_screenshot_time = time.time()

    while True:
        if keyboard.is_pressed('9'):
            isBut = True
        elif keyboard.is_pressed('0'):
            isBut = False

        if isBut:
            pyautogui.click(button='right')
        time.sleep(0.1)
        # Проверяем, прошло ли 10 секунд с последнего скриншота
        if time.time() - last_screenshot_time >= screenshot_interval:
            take_screenshot_and_check_timer()
            last_screenshot_time = time.time()

        time.sleep(1)

if __name__ == "__main__":
    main()
