import streamlit as st
import yfinance as yf
from calculation import black_scholes
from visualizations import generate_heatmap

st.title('Black-Scholes Option Pricer')

# Checkbox to choose stock symbol or manually enter asset price
S = None

# Checkbox to choose stock symbol or manually enter asset price
use_stock = st.checkbox('Use a stock ticker')
if use_stock:
    stock_ticker = st.text_input("Enter Stock Ticker (e.g., AAPL for Apple)")
    
    if stock_ticker:
        try:
            stock_data = yf.Ticker(stock_ticker)
            S = stock_data.history(period="1d")["Close"][-1]  # Fetch the latest price
            st.write(f"Current price of {stock_ticker.upper()}: ${S:.2f}")
        except Exception as e:
            st.write(f"Failed to retrieve data for {stock_ticker.upper()}. Please check the ticker symbol.")
    else:
        st.write("Please enter a stock ticker.")

# If ticker option not used, allow manual entry
if not use_stock or S is None:
    S = st.number_input('Asset Price (USD)', value=100.0)



# Get other option parameters
K = st.number_input('Strike Price (USD)', value=100.0)
T = st.number_input('Time to Expiration (Years)', value=1.0)
r = st.number_input('Risk-Free Interest Rate (USD)', value=0.05)
sigma = st.number_input('Volatility', value=0.2)
option_type = st.selectbox('Option Type', ('call', 'put'))

if 'price_output' not in st.session_state:
    st.session_state.price_output = None
if 'heatmap_output' not in st.session_state:
    st.session_state.heatmap_output = None

# Inline buttons for price calculation
if st.button('Calculate'):
    st.session_state.price_output = f'The {option_type} option price is: ${round(black_scholes(S, K, T, r, sigma, option_type), 2)}'

# Display price calculation result if available
if st.session_state.price_output:
    st.write(st.session_state.price_output)

# Inline button for heatmap generation
if st.button('Generate Heatmap'):
    # Set the heatmap to generate every time the button is pressed
    sigma_range = (0.1, 0.5)
    S_range = (S / 2, S * 1.5)
    st.session_state.heatmap_output = generate_heatmap(S, K, T, r, sigma_range, S_range, option_type)

# Display heatmap if generated
if st.session_state.heatmap_output:
    st.write('### Option Price Heatmap')
    st.session_state.heatmap_output