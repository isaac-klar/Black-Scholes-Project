import streamlit as st
from calculation import black_scholes
from visualizations import generate_heatmap

st.title('Black-Scholes Option Pricer')
S = st.number_input('Asset Price (USD)', value=100.0)
K = st.number_input('Strike Price (USD)', value=100.0)
T = st.number_input('Time to Expiration (Years)', value=1.0)
r = st.number_input('Risk-Free Interest Rate (USD)', value=0.05)
sigma = st.number_input('Volatility', value=0.2)
option_type = st.selectbox('Option Type', ('call', 'put'))

if st.button('Calculate'):
    price = black_scholes(S, K, T, r, sigma, option_type)
    st.write(f'The {option_type} option price is: ${round(price,2)}')

st.write('### Option Price Heatmap')
sigma_range = (0.1, 0.5)
S_range = (S/2, S*1.5)
if st.button('Generate Heatmap'):
    generate_heatmap(S, K, T, r, sigma_range, S_range, option_type)
