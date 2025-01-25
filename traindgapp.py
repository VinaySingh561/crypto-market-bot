import yfinance as yf
from openai import OpenAI  # Note: This is a hypothetical import
from datetime import datetime
import pandas as pd
import requests
from twilio.rest import Client  # For WhatsApp messaging
import schedule
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)

# Initialize API keys and credentials
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
WHATSAPP_FROM = os.getenv('WHATSAPP_FROM')
WHATSAPP_TO = os.getenv('WHATSAPP_TO')

# Verify environment variables are loaded
if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, WHATSAPP_FROM, WHATSAPP_TO]):
    raise ValueError("Missing required environment variables. Please check your .env file.")

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

class CryptoTrader:
    def __init__(self):
        self.ai_agent = client  # Initialize AI agent
        self.crypto_symbols = ['BTC-USD', 'ETH-USD', 'DOGE-USD']  # Add more symbols as needed
        
    def fetch_crypto_data(self):
        """Fetch real-time crypto data using yfinance"""
        data = {}
        for symbol in self.crypto_symbols:
            ticker = yf.Ticker(symbol)
            current_data = ticker.history(period='1d')
            data[symbol] = {
                'price': current_data['Close'].iloc[-1],
                'volume': current_data['Volume'].iloc[-1],
                'change': ((current_data['Close'].iloc[-1] - current_data['Open'].iloc[0]) / 
                          current_data['Open'].iloc[0]) * 100
            }
        return data

    def analyze_market(self, data):
        """Use DeepSeek AI to analyze market conditions"""
        try:
            # Prepare market data for analysis
            market_summary = "\n".join([
                f"{symbol}: Price=${values['price']:.2f}, Change={values['change']:.2f}%, Volume={values['volume']:,.0f}"
                for symbol, values in data.items()
            ])
            
            # Create prompt for market analysis
            prompt = f"""Analyze the following crypto market data and provide insights:
            {market_summary}
            
            Please provide:
            1. Market sentiment
            2. Notable trends
            3. Potential risks or opportunities
            Keep the analysis concise and actionable."""
            
            # Get analysis from DeepSeek
            response = self.ai_agent.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a cryptocurrency market analyst providing insights based on real-time market data."},
                    {"role": "user", "content": prompt}
                ],
                stream=False
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error in market analysis: {str(e)}"

    def send_whatsapp_update(self, message):
        """Send WhatsApp message using Twilio"""
        try:
            message = twilio_client.messages.create(
                from_=WHATSAPP_FROM,
                body=message,
                to=WHATSAPP_TO
            )
            print(f"Message sent: {message.sid}")
        except Exception as e:
            print(f"Error sending message: {e}")

    def generate_report(self, data, analysis):
        """Generate a formatted report"""
        report = "🚀 Crypto Market Update 🚀\n\n"
        for symbol, values in data.items():
            report += f"{symbol}:\n"
            report += f"Price: ${values['price']:.2f}\n"
            report += f"24h Change: {values['change']:.2f}%\n"
            report += f"Volume: {values['volume']:,.0f}\n\n"
        
        report += "\n🤖 AI Analysis:\n"
        report += analysis
        return report

    def run_update(self):
        """Main function to run the update process"""
        try:
            # Fetch data
            data = self.fetch_crypto_data()
            
            # Analyze with AI
            analysis = self.analyze_market(data)
            
            # Generate and send report
            report = self.generate_report(data, analysis)
            self.send_whatsapp_update(report)
            
        except Exception as e:
            print(f"Error in update process: {e}")

def main():
    trader = CryptoTrader()
    
    # Schedule updates every hour
    schedule.every().hour.do(trader.run_update)
    
    # Run initial update
    trader.run_update()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
