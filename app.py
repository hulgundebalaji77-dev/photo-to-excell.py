import pandas as pd
from PIL import Image
import pytesseract
import streamlit as st

st.set_page_config(
    page_title="Photo to Excel Text Extractor", page_icon="📸", layout="centered"
)

st.title("📸 फोटोमधून मजकूर काढून Excel बनवा")
st.write(
    "येथे तुमचे फोटो अपलोड करा, ॲप त्यातील मराठी आणि इंग्रजी मजकूर वाचून Excel"
    " फाईल तयार करेल!"
)

# एकापेक्षा जास्त फोटो अपलोड करण्यासाठी युजर इंटरफेस
uploaded_files = st.file_uploader(
    "फोटो निवडा (Select Photos)",
    type=["png", "jpg", "jpeg", "bmp", "tiff"],
    accept_multiple_files=True,
)

if uploaded_files:
  st.info(f"एकूण {len(uploaded_files)} फोटो निवडले आहेत.")

  if st.button("मजकूर बाहेर काढा (Extract Text & Create Excel)"):
    data_list = []

    with st.spinner("प्रक्रिया सुरू आहे, कृपया थोडा वेळ वाट पाहा..."):
      for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        try:
          # फोटो उघडणे
          img = Image.open(uploaded_file)

          # मराठी आणि इंग्रजी मजकूर वाचणे
          extracted_text = pytesseract.image_to_string(img, lang="eng+mar")
          cleaned_text = extracted_text.strip()

          data_list.append({
              "Photo_Name": file_name,
              "Extracted_Text": cleaned_text,
          })
        except Exception as e:
          data_list.append(
              {"Photo_Name": file_name, "Extracted_Text": f"Error: {e}"}
          )

      # DataFrame तयार करणे
      df = pd.DataFrame(data_list)
      output_file = "Photos_Data.xlsx"
      df.to_excel(output_file, index=False)

    st.success("काम पूर्ण झाले! खालील बटणावरून एक्सेल फाईल डाऊनलोड करा:")

    # डाऊनलोड बटण देणे
    with open(output_file, "rb") as f:
      st.download_button(
          label="📥 Excel फाईल डाऊनलोड करा (Download Excel)",
          data=f,
          file_name=output_file,
          mime=(
              "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
          ),
      )
