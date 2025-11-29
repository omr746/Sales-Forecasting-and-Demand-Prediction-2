import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import socket
import threading
import time
from pyngrok import ngrok, conf
import uvicorn
from fastapi import FastAPI

# -------------------------------
# CONFIG
# -------------------------------
NGROK_AUTH_TOKEN = "35XQhumf8PVgLvNrxiPJJOwfiRT_2CpjLK3prEMjLYquQr216"  # replace with your token

# -------------------------------
# START NGROK
# -------------------------------
def free_port():
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

port = free_port()
conf.get_default().auth_token = NGROK_AUTH_TOKEN

# If you want FastAPI server (optional)
app = FastAPI()

def run_api():
    uvicorn.run(app, host="0.0.0.0", port=port)

threading.Thread(target=run_api, daemon=True).start()
time.sleep(1)

public_url = ngrok.connect(port).public_url
print("Your public URL:", public_url)

# -------------------------------
# STREAMLIT DASHBOARD
# -------------------------------
st.title("📊 Future Sales Forecast Dashboard")

# Sample Data
data = {
    "year": [2018, 2018, 2018, 2018, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2020, 2020, 2020, 2020, 2020, 2020, 2020, 2020, 2020],
    "month": [9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "is_holiday": [1,1,1,1,1,0,1,1,1,0,0,0,1,1,1,1,1,0,1,1,1,0,0,0,1],
    "predicted_sales": [
        940100.9375, 926625.6875, 937185.3125, 923155.6875, 873438.6875,
        852133.4375, 880764.3125, 881573.1875, 888721.5625, 874418.4375,
        876659.9375, 894834.3125, 925460.9375, 925129.9375, 935802.6875, 923155.6875,
        873438.6875, 852133.4375, 880764.3125, 881573.1875, 888721.5625,
        874418.4375, 876659.9375, 894834.3125, 925460.9375
    ]
}

df = pd.DataFrame(data)
df['date'] = df['year'].astype(str) + '-' + df['month'].astype(str)
df_display = df[['date', 'predicted_sales']]

# Display Table
st.subheader("Forecasted Sales Data")
st.dataframe(df_display)

# Plot
st.subheader("Predicted Sales Over Time")
plt.figure(figsize=(12,6))
plt.plot(df_display['date'], df_display['predicted_sales'], marker='o', linestyle='-', color='blue')
plt.title('Predicted Sales Over Time')
plt.xlabel('Date (YYYY-M)')
plt.ylabel('Predicted Sales')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)


