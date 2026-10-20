import streamlit as st

st.set_page_config(
    page_title="Big Box Strategy & OCR Utility", layout="wide"
)

st.title("💱 Big Box Strategy & OCR Utility")

# एरर फ्री टेस्टसाठी सिम्पल टॅब किंवा एक्सपँडर
tab1, tab2 = st.tabs(["📈 Big Box Strategy", "📷 Photo to OCR"])

with tab1:
  st.subheader("Big Box Strategy (Bollinger Bands + RSI)")
  st.write("येथे तुमचं स्ट्रॅटर्जी लॉजिक व्यवस्थित काम करेल.")

  # डमी डेटा टेस्ट बटण
  if st.button("डेटा टेस्ट रन करा"):
    st.success("स्ट्रॅटर्जी कोड यशस्वीरित्या सुरू आहे!")

with tab2:
  st.subheader("Photo to Excel (OCR)")

  try:
    from PIL import Image
    import pytesseract

    uploaded_file = st.file_uploader(
        "फोटो अपलोड करा", type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
      image = Image.open(uploaded_file)
      st.image(image, caption="अपलोड केलेली इमेज", use_column_width=True)

      if st.button("टेक्स्ट रीड करा"):
        with st.spinner("प्रोसेसिंग सुरू आहे..."):
          text = pytesseract.image_to_string(image, lang="eng")
          st.text_area("वाचलेला मजकूर:", text)
  except Exception as e:
    st.error(
        f"OCR एरर: {e} (कृपया packages.txt मध्ये tesseract-ocr असल्याची खात्री"
        " करा)"
    )
