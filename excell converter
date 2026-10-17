import glob
import os
from PIL import Image
import pandas as pd
import pytesseract

# (टीप: Windows साठी आवश्यक असल्यास Tesseract चा पाथ येथे द्या)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def photos_to_excel(folder_path, output_excel='photos_text_output.xlsx'):
  """फोल्डरमधील सर्व फोटोंमधील मजकूर काढून Excel फाइलमध्ये सेव्ह करते."""

  # सपोर्टेड फोटो फॉरमॅट्स शोधणे
  extensions = ('.png', '.jpg', '.jpeg', '.bmp', '*.tiff')
  all_files = []
  for ext in extensions:
    all_files.extend(glob.glob(os.path.join(folder_path, ext)))

  if not all_files:
    print('या फोल्डरमध्ये कोणत्याच फोटो फाइल्स सापडल्या नाहीत.')
    return

  print(f'एकूण {len(all_files)} फोटो फाइल्स सापडल्या आहेत. प्रक्रिया सुरू आहे...\n')

  data_list = []

  for file in all_files:
    file_name = os.path.basename(file)
    print(f'प्रक्रिया सुरू आहे: {file_name}')

    try:
      # फोटो उघडणे
      img = Image.open(file)

      # फोटोमधील मजकूर वाचणे (मराठी आणि इंग्रजी दोन्हीसाठी 'mar+eng')
      extracted_text = pytesseract.image_to_string(img, lang='eng+mar')

      # ओळींमधील जादा स्पेस आणि नवीन ओळी व्यवस्थित करणे (पर्यायी)
      cleaned_text = extracted_text.strip()

      # डेटा लिस्टमध्ये साठवणे
      data_list.append({
          'Photo_Name': file_name,
          'Extracted_Text': cleaned_text,
      })

    except Exception as e:
      print(f'त्रुटी ({file_name}): {e}')
      data_list.append({
          'Photo_Name': file_name,
          'Extracted_Text': f'Error: {e}',
      })

  # डेटा Pandas DataFrame मध्ये रूपांतरित करणे
  df = pd.DataFrame(data_list)

  # Excel फाईलमध्ये सेव्ह करणे
  df.to_excel(output_excel, index=False)
  print(
      f'\nसर्व फोटोंमधील मजकूर यशस्वीरीत्या "{output_excel}" या एक्सेल फाईलमध्ये'
      ' सेव्ह केला आहे!'
  )


# --- कोड कसा वापरावा ---
# तुमच्या फोटोंचा फोल्डर पाथ खाली द्या:
# folder_path = r"C:\Users\YourName\Pictures\MyPhotos"
# photos_to_excel(folder_path, output_excel="Photos_Data.xlsx")
