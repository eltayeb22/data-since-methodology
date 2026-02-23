import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.title("Cryptocurrency Profitability Predictor")
st.write("Enter cryptocurrency data below to predict if it will be profitable in 24 hours")

try:
    model = joblib.load("Model.joblib")
except:
    st.error("Model file not found! Make sure Model.joblib is in the same directory.")
    st.stop()


col1, col2 = st.columns(2)

with col1:
    current_price = st.number_input("Current Price (USD)", min_value=0.0, value=50000.0)
    market_cap = st.number_input("Market Cap (USD)", min_value=0.0, value=1000000000.0)
    total_volume = st.number_input("Total Volume (24h)", min_value=0.0, value=50000000.0)
    market_cap_rank = st.number_input("Market Cap Rank", min_value=1, value=1)

with col2:
    high_24h = st.number_input("High Price (24h)", min_value=0.0, value=51000.0)
    low_24h = st.number_input("Low Price (24h)", min_value=0.0, value=49000.0)
    ath_change_percentage = st.number_input("Distance from ATH (%)", value=-20.0)
    atl_change_percentage = st.number_input("Distance from ATL (%)", value=50.0)

def calculate_features(price, volume, mcap, rank, high, low, ath_pct, atl_pct):
    log_price = np.log1p(price)
    log_volume = np.log1p(volume)
    log_mcap = np.log1p(mcap)
    price_range_pct = (high - low) / price if price > 0 else 0
    volume_to_mcap = volume / mcap if mcap > 0 else 0
    mcap_rank_inv = 1 / (rank + 1)
    
    return {
        'Log Price': log_price,
        'Log Volume': log_volume,
        'Log Market Cap': log_mcap,
        'Price Range Pct (24h)': price_range_pct,
        'Volume To Market Cap': volume_to_mcap,
        'Distance From Ath Pct': ath_pct,
        'Distance From Atl Pct': atl_pct,
        'Mc Rank Inv': mcap_rank_inv
    }

if st.button("Predict", type="primary"):
    features = calculate_features(
        current_price, total_volume, market_cap, market_cap_rank,
        high_24h, low_24h, ath_change_percentage, atl_change_percentage
    )
    
    feature_df = pd.DataFrame([features])
    feature_order = ['Log Price', 'Log Volume', 'Log Market Cap',
                   'Price Range Pct (24h)', 'Volume To Market Cap',
                   'Distance From Ath Pct', 'Distance From Atl Pct',
                   'Mc Rank Inv']
    feature_df = feature_df[feature_order]
    
    prediction = model.predict(feature_df)[0]
    probability = model.predict_proba(feature_df)[0]
    
    st.header("Prediction Result")
    
    if prediction == 1:
        st.success("Profitable!")
    else:
        st.error("Not Profitable")
    
    st.write(f"Confidence: {probability[1]*100:.1f}%")
