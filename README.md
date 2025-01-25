# 🤖 Crypto Market Analysis Bot

An intelligent cryptocurrency trading bot that combines real-time market data with AI-powered analysis to deliver insights via WhatsApp.

## 🌟 Overview

This bot continuously monitors cryptocurrency markets (BTC, ETH, DOGE), analyzes trends using DeepSeek AI, and sends automated WhatsApp updates to keep you informed about market movements and opportunities.

## 🚀 Key Features

- **Real-time Monitoring**: Track live cryptocurrency prices and market movements
- **AI Analysis**: Leverage DeepSeek AI for intelligent market insights
- **Automated Alerts**: Receive WhatsApp notifications with market updates
- **Multi-Currency Support**: Track BTC, ETH, DOGE, and more
- **Scheduled Updates**: Hourly market analysis and notifications
- **Comprehensive Reports**: Get detailed price, volume, and trend information

## 🛠️ Tech Stack

- **Python 3.x**: Core programming language
- **yfinance**: Real-time cryptocurrency data fetching
- **DeepSeek AI**: Advanced market analysis
- **Twilio**: WhatsApp integration
- **Schedule**: Automated task management
- **python-dotenv**: Environment variable management

## ⚙️ Setup & Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/VinaySingh561/crypto-market-bot.git
   cd crypto-market-bot
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   Create a `.env` file with:
   ```env
   DEEPSEEK_API_KEY=your_api_key
   TWILIO_ACCOUNT_SID=your_sid
   TWILIO_AUTH_TOKEN=your_token
   WHATSAPP_FROM=your_twilio_number
   WHATSAPP_TO=your_whatsapp_number
   ```

4. **Run the Bot**
   ```bash
   python traindgapp.py
   ```

## 📊 Sample Output
