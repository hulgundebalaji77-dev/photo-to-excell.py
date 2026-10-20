import numpy as np
import pandas as pd


def big_box_strategy(df: pd.DataFrame) -> pd.DataFrame:
  """'बिग बॉक्स स्ट्रॅटर्जी' नुसार ट्रेडिंग सिग्नल जनरेट करणारी फंक्शन.

  df मध्ये किमान 'Open', 'High', 'Low', 'Close' हे कॉलम असणे आवश्यक आहे.
  """

  # १. Bollinger Bands कॅल्क्युलेट करणे (उदा. २२ कालावधी, मानक विचलन २)
  window = 20
  df["SMA"] = df["Close"].rolling(window=window).mean()
  df["STD"] = df["Close"].rolling(window=window).std()
  df["Upper_Band"] = df["SMA"] + (2 * df["STD"])
  df["Lower_Band"] = df["SMA"] - (2 * df["STD"])

  # Bollinger Band Squeeze ची अट (बँड्समधील अंतर कमी होणे)
  df["Band_Width"] = df["Upper_Band"] - df["Lower_Band"]
  df["Avg_Band_Width"] = df["Band_Width"].rolling(window=50).mean()
  df["Is_Squeeze"] = df["Band_Width"] < df["Avg_Band_Width"]

  # २. RSI (Relative Strength Index - १४ अवधी) कॅल्क्युलेट करणे
  delta = df["Close"].diff()
  gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
  loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
  rs = gain / loss
  df["RSI"] = 100 - (100 / (1 + rs))

  # ३. एन्ट्रीचे नियम (Entry Rules)
  # - बाय साईड (Buy Side): कॅण्डल लोअर बँडच्या खाली क्लोज झाली पाहिजे आणि RSI ४० च्या वर असला पाहिजे.
  # - सेल साईड (Sell Side): कॅण्डल अपर बँडच्या वर क्लोज झाली पाहिजे आणि RSI ६० च्या खाली असला पाहिजे.

  df["Buy_Signal"] = (
    (df["Close"] < df["Lower_Band"])
    & (df["RSI"] > 40)
    & (df["Is_Squeeze"].shift(1))
  )

  df["Sell_Signal"] = (
    (df["Close"] > df["Upper_Band"])
    & (df["RSI"] < 60)
    & (df["Is_Squeeze"].shift(1))
  )

  # ४. स्टॉप लॉस (Stop Loss): ज्या कॅण्डलवर एन्ट्री घेतली, तिचा High किंवा Low
  df["Stop_Loss"] = np.where(
      df["Buy_Signal"],
      df["Low"],
      np.where(df["Sell_Signal"], df["High"], np.nan),
  )

  # सिग्नल कॉलम तयार करणे
  df["Signal"] = 0
  df.loc[df["Buy_Signal"], "Signal"] = 1  # Buy
  df.loc[df["Sell_Signal"], "Signal"] = -1  # Sell

  return df


# --- डमी डेटा वापरून टेस्ट करण्यासाठी उदाहरण ---
if __name__ == "__main__":
  # ५ मिनिटांच्या निफ्टीच्या डेटाचे उदाहरण (डेटा तुमच्या प्रत्यक्ष ऐतिहासिक डेटाने बदलावा)
  data = {
      "Open": [
          22000,
          22010,
          21990,
          21950,
          21900,
          21850,
          21840,
          21860,
          21830,
          21800,
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
  }

  df = pd.DataFrame(data)

  # स्ट्रॅटर्जी रन करणे
  result_df = big_box_strategy(df)

  # निकाल पाहणे
  print(result_df[["Close", "Upper_Band", "Lower_Band", "RSI", "Signal", "Stop_Loss"]])
