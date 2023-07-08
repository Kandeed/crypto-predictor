import pandas as pd
import yfinance as yf
import datetime
import plotly.express as px

# Get historical data for Bitcoin
btc_data = yf.download("BTC-USD", start="2022-01-01", end=datetime.datetime.today())

# Calculate Fibonacci retracements
fib_levels = [0.236, 0.5, 0.764]
for level in fib_levels:
    btc_data["fib_" + str(level)] = btc_data["Close"].rolling(window=20).apply(lambda x: x[-1] - x[0]) * level

# Calculate demand and supply zones
demand_zones = []
supply_zones = []
for i in range(len(btc_data)):
    if btc_data["Close"][i] > btc_data["Close"][i - 1]:
        demand_zones.append(btc_data["Close"][i])
    elif btc_data["Close"][i] < btc_data["Close"][i - 1]:
        supply_zones.append(btc_data["Close"][i])

# Calculate impulse MACD by lazy bear
btc_data["macd"] = btc_data["Close"].diff(12) - btc_data["Close"].diff(26)
btc_data["macd_signal"] = btc_data["macd"].ewm(span=9, adjust=False).mean()
btc_data["macd_hist"] = btc_data["macd"] - btc_data["macd_signal"]

# Create a candlestick chart
fig = px.candlestick(btc_data, x="Date", y=["Open", "High", "Low", "Close"])

# Add Fibonacci retracements to the chart
for level in fib_levels:
    fig.add_line(x=btc_data["Date"], y=btc_data["fib_" + str(level)], line_color="blue")

# Add demand and supply zones to the chart
for zone in demand_zones:
    fig.add_rect(x0=zone, x1=zone, ymin=0, ymax=1, fill_color="green", alpha=0.3)
for zone in supply_zones:
    fig.add_rect(x0=zone, x1=zone, ymin=0, ymax=1, fill_color="red", alpha=0.3)

# Add impulse MACD to the chart
fig.add_line(x=btc_data["Date"], y=btc_data["macd_hist"], line_color="yellow")

# Update the chart data every minute
while True:
    btc_data = yf.download("BTC-USD", start=datetime.datetime.today(), end=datetime.datetime.today())
    fig.update_data(btc_data)
    fig.show()
