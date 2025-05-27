import PyPDF2
from PIL import Image
import io
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from pdf2image import convert_from_path

def find_content_bounds(image, threshold=250):
    # Конвертируем изображение в черно-белое
    if image.mode != 'L':
        image = image.convert('L')
    
    # Преобразуем в numpy массив для быстрой обработки
    img_array = np.array(image)
    
    # Находим все непустые пиксели (не белые)
    rows = np.any(img_array < threshold, axis=1)
    cols = np.any(img_array < threshold, axis=0)
    
    # Проверяем, есть ли вообще черные пиксели
    if not np.any(rows) or not np.any(cols):
        # Если черных пикселей нет, возвращаем границы всего изображения
        height, width = img_array.shape
        return (0, 0, width - 1, height - 1)
    
    # Получаем границы контента
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    
    # Добавляем отступ в 15 пикселей
    padding = 15
    height, width = img_array.shape
    
    rmin = max(0, rmin - padding)
    rmax = min(height - 1, rmax + padding)
    cmin = max(0, cmin - padding)
    cmax = min(width - 1, cmax + padding)
    
    return (cmin, rmin, cmax, rmax)

def process_pdf(input_path, output_path):
    # Конвертируем PDF в изображения с высоким разрешением
    images = convert_from_path(
        input_path,
        dpi=600,  # Увеличиваем DPI для лучшего качества
        fmt='png'  # Используем PNG для избежания артефактов сжатия
    )
    
    # Создаем PDF writer для нового документа
    pdf_writer = PyPDF2.PdfWriter()
    
    # Создаем временную директорию для хранения промежуточных файлов
    temp_dir = os.path.join(os.path.dirname(output_path), 'temp_pdf_files')
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        for i, img in enumerate(images):
            try:
                # Находим границы содержимого
                bbox = find_content_bounds(img)
                
                # Обрезаем изображение
                cropped_image = img.crop(bbox)
                
                # Создаем временный файл для каждой страницы
                temp_file = os.path.join(temp_dir, f'temp_page_{i}.pdf')
                
                # Сохраняем страницу как PDF
                cropped_image.save(
                    temp_file,
                    format='PDF',
                    resolution=600.0,
                    quality=100
                )
                
                # Открываем сохраненный PDF и добавляем его страницу
                with open(temp_file, 'rb') as f:
                    pdf = PyPDF2.PdfReader(f)
                    page = pdf.pages[0]
                    
                    # Устанавливаем размер страницы
                    width_pt = cropped_image.width * 72 / 600
                    height_pt = cropped_image.height * 72 / 600
                    
                    # Устанавливаем размеры страницы
                    page.mediabox.lower_left = (0, 0)
                    page.mediabox.upper_right = (width_pt, height_pt)
                    
                    # Копируем размеры для всех боксов
                    for box in [page.cropbox, page.trimbox, page.artbox, page.bleedbox]:
                        box.lower_left = (0, 0)
                        box.upper_right = (width_pt, height_pt)
                    
                    pdf_writer.add_page(page)
                
            except Exception as e:
                print(f"Ошибка при обработке страницы {i}: {str(e)}")
                continue
        
        # Сохраняем результат
        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)
    
    finally:
        # Удаляем временные файлы
        for file in os.listdir(temp_dir):
            try:
                os.remove(os.path.join(temp_dir, file))
            except:
                pass
        try:
            os.rmdir(temp_dir)
        except:
            pass

class PDFCropGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Crop Tool")
        self.root.geometry("400x200")
        
        # Переменные для хранения путей к файлам
        self.input_file = ""
        self.output_file = ""
        
        # Создаем элементы интерфейса
        self.create_widgets()
    
    def create_widgets(self):
        # Метка для отображения выбранного файла
        self.file_label = tk.Label(self.root, text="Файл не выбран", wraplength=350)
        self.file_label.pack(pady=10)
        
        # Кнопка выбора файла
        self.select_button = tk.Button(self.root, text="Открыть PDF", command=self.select_file)
        self.select_button.pack(pady=10)
        
        # Кнопка запуска конвертации
        self.start_button = tk.Button(self.root, text="Начать обработку", command=self.start_processing)
        self.start_button.pack(pady=10)
    
    def select_file(self):
        self.input_file = filedialog.askopenfilename(
            title="Выберите PDF файл",
            filetypes=[("PDF files", "*.pdf")]
        )
        if self.input_file:
            self.file_label.config(text=f"Выбран файл: {self.input_file}")
    
    def start_processing(self):
        if not self.input_file:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите PDF файл")
            return
        
        # Получаем путь для сохранения результата
        self.output_file = filedialog.asksaveasfilename(
            title="Сохранить обработанный файл",
            filetypes=[("PDF files", "*.pdf")],
            defaultextension=".pdf"
        )
        
        if self.output_file:
            try:
                process_pdf(self.input_file, self.output_file)
                messagebox.showinfo("Успех", "Обработка завершена успешно!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

def main():
    root = tk.Tk()
    app = PDFCropGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()