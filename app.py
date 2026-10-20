import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Big Box Strategy & OCR Utility", layout="wide"
)

st.title("💱 Big Box Strategy & OCR Utility")

tab1, tab2 = st.tabs(["📈 Big Box Strategy", "📷 Photo to OCR"])

# --- टॅब १: बिग बॉक्स स्ट्रॅटर्जी (Big Box Strategy) ---
with tab1:
  st.subheader("Big Box Strategy (Bollinger Bands + RSI)")

  # डमी डेटा किंवा युजर इनपुटसाठी ऑप्शन
  if st.button("स्ट्रॅटर्जी सिग्नल टेस्ट रन करा"):
    # नमुना डेटा (Sample Data)
    data = {
        "Close": [
            22010,
            21990,
            21950,
            21900,
            21850,
            21840,
            21850,
            21830,
            21810,
            21790,
        ],
        "High": [
            22020,
            22015,
            22000,
            21960,
            21910,
            21865,
            21860,
            21880,
            21850,
            21820,
        ],
        "Low": [
            21995,
            21985,
            21940,
            21890,
            21840,
            21830,
            21820,
            21840,
            21800,
            21780,
        ],
    }
    df = pd.DataFrame(data)

    # Bollinger Bands कॅल्क्युलेशन
    window = 5
    df["SMA"] = df["Close"].rolling(window=window).mean()
    df["STD"] = df["Close"].rolling(window=window).std()
    df["Upper_Band"] = df["SMA"] + (2 * df["STD"])
    df["Lower_Band"] = df["SMA"] - (2 * df["STD"])

    # RSI कॅल्क्युलेशन
    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=5).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=5).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    st.success("स्ट्रॅटर्जी यशस्वीरित्या रन झाली!")
    st.dataframe(df[["Close", "Upper_Band", "Lower_Band", "RSI"]])

# --- टॅब २: फोटो ते एक्सेल (OCR) ---
with tab2:
  st.subheader("Photo to Excel (OCR Text Extraction)")

  try:
    from PIL import Image
    import openpyxl
    import pytesseract

    uploaded_file = st.file_uploader(
        "फोटो अपलोड करा (मराठी/इंग्रजी)", type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
      image = Image.open(uploaded_file)
      st.image(image, caption="अपलोड केलेली इमेज", use_column_width=True)

      lang_choice = st.selectbox("भाषा निवडा", ["eng", "mar", "mar+eng"])

      if st.button("टेक्स्ट एक्स्ट्रॅक्ट करा"):
        with st.spinner("प्रोसेसिंग सुरू आहे..."):
          extracted_text = pytesseract.image_to_string(image, lang=lang_choice)
          st.text_area("वाचलेला मजकूर (Extracted Text):", extracted_text, height=200)

          # एक्सेल फाईल तयार करणे
          lines = [
              line.strip()
              for line in extracted_text.split("\n")
              if line.strip()
          ]
          df_ocr = pd.DataFrame(lines, columns=["Extracted_Lines"])

          output_file = "extracted_data.xlsx"
          df_ocr.to_excel(output_file, index=False)

          with open(output_file, "rb") as f:
            st.download_button(
                label="📁 एक्सेल फाईल डाउनलोड करा",
                data=f,
                file_name="extracted_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
  except Exception as e:
    st.warning(
        "OCR मोड चालू करण्यासाठी packages.txt मध्ये tesseract-ocr असल्याची खात्री"
        f" करा. (एरर: {e})"
    )
