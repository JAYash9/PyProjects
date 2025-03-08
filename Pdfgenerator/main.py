import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import time
# The 'schedule' module is causing an error because it's not installed
# You need to install it using: pip install schedule
import schedule

class BullishStockPredictor:
    def __init__(self):
        self.pdf = FPDF()
        self.nifty50_stocks = []
        self.prediction_horizon = '1w'  # Predicting for next week
        
    def fetch_nifty50_stocks(self):
        """Fetch the list of Nifty 50 stocks"""
        try:
            url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # The NSE website blocks direct API access. Need to use session and cookies
            session = requests.Session()
            session.headers.update(headers)
            
            # First visit the homepage to get cookies
            session.get("https://www.nseindia.com/", timeout=30)
            
            # Then access the API
            response = session.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if 'data' in data:
                    for stock in data['data']:
                        self.nifty50_stocks.append(stock['symbol'] + ".NS")
                    print(f"Successfully fetched {len(self.nifty50_stocks)} stocks from NSE API")
                    return self.nifty50_stocks
            
            # If API call fails, try web scraping
            print("API call failed, trying web scraping...")
            nifty50_url = "https://www.nseindia.com/market-data/live-equity-market?symbol=NIFTY%2050"
            response = session.get(nifty50_url, timeout=30)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract stock symbols from the table
            table = soup.find('table', {'id': 'equityStockTable'})
            if table:
                for row in table.find_all('tr')[1:]:  # Skip header row
                    cells = row.find_all('td')
                    if len(cells) > 1:
                        symbol = cells[0].text.strip()
                        self.nifty50_stocks.append(symbol + ".NS")  # Add .NS suffix for Yahoo Finance
            
            # Fallback to a predefined list if both methods fail
            if not self.nifty50_stocks:
                print("Couldn't fetch Nifty 50 stocks, using predefined list")
                self.nifty50_stocks = [
                    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "HINDUNILVR.NS",
                    "ICICIBANK.NS", "SBIN.NS", "BHARTIARTL.NS", "ITC.NS", "KOTAKBANK.NS",
                    "LT.NS", "AXISBANK.NS", "BAJFINANCE.NS", "ASIANPAINT.NS", "MARUTI.NS",
                    "HCLTECH.NS", "SUNPHARMA.NS", "TITAN.NS", "ULTRACEMCO.NS", "BAJAJFINSV.NS",
                    "TATASTEEL.NS", "NTPC.NS", "POWERGRID.NS", "TECHM.NS", "M&M.NS",
                    "ADANIPORTS.NS", "WIPRO.NS", "HDFCLIFE.NS", "DIVISLAB.NS", "ONGC.NS",
                    "JSWSTEEL.NS", "TATAMOTORS.NS", "SBILIFE.NS", "GRASIM.NS", "DRREDDY.NS",
                    "INDUSINDBK.NS", "CIPLA.NS", "EICHERMOT.NS", "NESTLEIND.NS", "COALINDIA.NS",
                    "BPCL.NS", "BRITANNIA.NS", "HEROMOTOCO.NS", "UPL.NS", "IOC.NS",
                    "TATACONSUM.NS", "HINDALCO.NS", "SHREECEM.NS", "BAJAJ-AUTO.NS", "ADANIENT.NS"
                ]
                
            print(f"Fetched {len(self.nifty50_stocks)} stocks for analysis")
            return self.nifty50_stocks
        except Exception as e:
            print(f"Error fetching Nifty 50 stocks: {e}")
            # Fallback to top 50 stocks
            self.nifty50_stocks = [
                "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "HINDUNILVR.NS",
                "ICICIBANK.NS", "SBIN.NS", "BHARTIARTL.NS", "ITC.NS", "KOTAKBANK.NS",
                "LT.NS", "AXISBANK.NS", "BAJFINANCE.NS", "ASIANPAINT.NS", "MARUTI.NS",
                "HCLTECH.NS", "SUNPHARMA.NS", "TITAN.NS", "ULTRACEMCO.NS", "BAJAJFINSV.NS",
                "TATASTEEL.NS", "NTPC.NS", "POWERGRID.NS", "TECHM.NS", "M&M.NS",
                "ADANIPORTS.NS", "WIPRO.NS", "HDFCLIFE.NS", "DIVISLAB.NS", "ONGC.NS",
                "JSWSTEEL.NS", "TATAMOTORS.NS", "SBILIFE.NS", "GRASIM.NS", "DRREDDY.NS",
                "INDUSINDBK.NS", "CIPLA.NS", "EICHERMOT.NS", "NESTLEIND.NS", "COALINDIA.NS",
                "BPCL.NS", "BRITANNIA.NS", "HEROMOTOCO.NS", "UPL.NS", "IOC.NS",
                "TATACONSUM.NS", "HINDALCO.NS", "SHREECEM.NS", "BAJAJ-AUTO.NS", "ADANIENT.NS"
            ]
            return self.nifty50_stocks
    
    def predict_next_week(self, ticker):
        """Analyze a stock for bullish indicators for next week"""
        try:
            # Download stock data with extra history for calculations
            stock = yf.Ticker(ticker)
            hist = stock.history(period='6mo')
            
            if hist.empty or len(hist) < 50:
                return None, "Insufficient historical data"
            
            # Calculate technical indicators
            # 1. Moving Averages
            hist['MA20'] = hist['Close'].rolling(window=20).mean()
            hist['MA50'] = hist['Close'].rolling(window=50).mean()
            hist['MA200'] = hist['Close'].rolling(window=200).mean()
            
            # 2. RSI (Relative Strength Index)
            delta = hist['Close'].diff()
            gain = delta.where(delta > 0, 0).rolling(window=14).mean()
            loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
            rs = gain / loss
            hist['RSI'] = 100 - (100 / (1 + rs))
            
            # 3. MACD (Moving Average Convergence Divergence)
            hist['EMA12'] = hist['Close'].ewm(span=12, adjust=False).mean()
            hist['EMA26'] = hist['Close'].ewm(span=26, adjust=False).mean()
            hist['MACD'] = hist['EMA12'] - hist['EMA26']
            hist['Signal'] = hist['MACD'].ewm(span=9, adjust=False).mean()
            
            # 4. Bollinger Bands
            hist['20d_std'] = hist['Close'].rolling(window=20).std()
            hist['upper_band'] = hist['MA20'] + (hist['20d_std'] * 2)
            hist['lower_band'] = hist['MA20'] - (hist['20d_std'] * 2)
            
            # 5. Volume analysis
            hist['Volume_MA20'] = hist['Volume'].rolling(window=20).mean()
            
            # 6. ADX (Average Directional Index) for trend strength
            plus_dm = hist['High'].diff()
            minus_dm = hist['Low'].diff(-1)
            plus_dm[plus_dm < 0] = 0
            minus_dm[minus_dm > 0] = 0
            minus_dm = abs(minus_dm)
            
            tr1 = hist['High'] - hist['Low']
            tr2 = abs(hist['High'] - hist['Close'].shift(1))
            tr3 = abs(hist['Low'] - hist['Close'].shift(1))
            tr = pd.DataFrame({'tr1': tr1, 'tr2': tr2, 'tr3': tr3}).max(axis=1)
            
            atr = tr.rolling(14).mean()
            
            # Handle division by zero
            atr_safe = atr.replace(0, np.nan)
            plus_di = 100 * (plus_dm.rolling(14).mean() / atr_safe)
            minus_di = 100 * (minus_dm.rolling(14).mean() / atr_safe)
            
            # Handle division by zero in DX calculation
            sum_di = plus_di + minus_di
            sum_di_safe = sum_di.replace(0, np.nan)
            dx = 100 * abs(plus_di - minus_di) / sum_di_safe
            hist['ADX'] = dx.rolling(14).mean()
            
            # Fill NaN values
            hist.fillna(method='bfill', inplace=True)
            
            # Check for bullish signals for next week
            bullish_signals = []
            
            # Last row for current values
            current = hist.iloc[-1]
            prev = hist.iloc[-2]
            week_ago = hist.iloc[-6] if len(hist) >= 6 else hist.iloc[0]
            
            # 1. Price above key moving averages
            if current['Close'] > current['MA20'] and current['Close'] > current['MA50']:
                bullish_signals.append("Price above MA20 and MA50")
            
            # 2. MA20 crossing above MA50 (Golden Cross)
            if prev['MA20'] <= prev['MA50'] and current['MA20'] > current['MA50']:
                bullish_signals.append("Golden Cross (MA20 crossed above MA50)")
            
            # 3. RSI momentum
            if 40 <= current['RSI'] <= 65 and current['RSI'] > prev['RSI']:
                bullish_signals.append(f"Rising RSI with room to grow: {current['RSI']:.2f}")
            
            # 4. MACD bullish crossover or positive momentum
            if current['MACD'] > current['Signal'] and prev['MACD'] <= prev['Signal']:
                bullish_signals.append("MACD bullish crossover")
            elif current['MACD'] > 0 and current['MACD'] > prev['MACD']:
                bullish_signals.append("MACD positive and rising")
            
            # 5. Volume confirmation
            if current['Volume'] > current['Volume_MA20'] * 1.2:
                bullish_signals.append("Strong volume support (20% above average)")
            
            # 6. Price near lower Bollinger Band (potential bounce)
            if prev['Close'] <= prev['lower_band'] and current['Close'] > current['lower_band']:
                bullish_signals.append("Bouncing off lower Bollinger Band")
            
            # 7. ADX showing strong trend
            if current['ADX'] > 25 and plus_di.iloc[-1] > minus_di.iloc[-1]:
                bullish_signals.append(f"Strong uptrend (ADX: {current['ADX']:.2f})")
            
            # 8. Weekly momentum
            weekly_change = ((current['Close'] - week_ago['Close']) / week_ago['Close']) * 100
            if weekly_change > 2:
                bullish_signals.append(f"Strong weekly momentum (+{weekly_change:.2f}%)")
            
            # 9. Higher highs and higher lows (uptrend)
            last_10_days = hist.iloc[-10:]
            if all(last_10_days['Low'].iloc[i] >= last_10_days['Low'].iloc[i-3] for i in range(3, 10)):
                bullish_signals.append("Higher lows pattern (uptrend)")
            
            # 10. Price consolidation near highs
            recent_high = hist['High'].iloc[-20:].max()
            if current['Close'] >= recent_high * 0.95:
                bullish_signals.append("Consolidating near recent highs")
            
            # Calculate overall bullish score (0-10)
            bullish_score = min(len(bullish_signals), 10)
            
            # Calculate confidence percentage
            confidence = bullish_score * 10
            
            # Return results if bullish
            if bullish_score >= 3:  # At least 3 bullish signals
                return {
                    'ticker': ticker,
                    'company_name': stock.info.get('longName', ticker.replace(".NS", "")),
                    'current_price': current['Close'],
                    'change_percent': ((current['Close'] - hist.iloc[-2]['Close']) / hist.iloc[-2]['Close']) * 100,
                    'weekly_change': weekly_change,
                    'bullish_signals': bullish_signals,
                    'bullish_score': bullish_score,
                    'confidence': confidence,
                    'prediction': "BULLISH for next week",
                    'data': hist.tail(30)  # Only keep last 30 days to save memory
                }, None
            return None, "Not enough bullish signals for next week"
            
        except Exception as e:
            return None, f"Error analyzing {ticker}: {str(e)}"
    
    def generate_report(self, bullish_stocks):
        """Generate a PDF report of bullish stocks for next week"""
        try:
            self.pdf = FPDF()  # Reset PDF
            self.pdf.add_page()
            self.pdf.set_font("Arial", "B", 16)
            self.pdf.cell(0, 10, "Nifty 50 Bullish Stocks Forecast", 0, 1, "C")
            self.pdf.set_font("Arial", "B", 14)
            self.pdf.cell(0, 10, "Next Week Outlook", 0, 1, "C")
            self.pdf.set_font("Arial", "I", 10)
            self.pdf.cell(0, 10, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1, "C")
            self.pdf.ln(5)
            
            # Sort stocks by bullish score
            bullish_stocks.sort(key=lambda x: x['bullish_score'], reverse=True)
            
            # Add table header
            self.pdf.set_font("Arial", "B", 12)
            self.pdf.cell(60, 10, "Company", 1, 0, "C")
            self.pdf.cell(25, 10, "Ticker", 1, 0, "C")
            self.pdf.cell(30, 10, "Price", 1, 0, "C")
            self.pdf.cell(30, 10, "Weekly %", 1, 0, "C")
            self.pdf.cell(45, 10, "Confidence", 1, 1, "C")
            
            # Add data rows
            self.pdf.set_font("Arial", "", 10)
            for stock in bullish_stocks:
                # Truncate company name if too long
                company_name = stock['company_name']
                if len(company_name) > 25:
                    company_name = company_name[:22] + "..."
                    
                self.pdf.cell(60, 10, company_name, 1, 0)
                self.pdf.cell(25, 10, stock['ticker'].replace(".NS", ""), 1, 0, "C")
                self.pdf.cell(30, 10, f"₹{stock['current_price']:.2f}", 1, 0, "C")
                
                # Color code the weekly change percentage
                change_text = f"{stock['weekly_change']:.2f}%"
                if stock['weekly_change'] > 0:
                    self.pdf.set_text_color(0, 128, 0)  # Green
                    change_text = "+" + change_text
                elif stock['weekly_change'] < 0:
                    self.pdf.set_text_color(255, 0, 0)  # Red
                self.pdf.cell(30, 10, change_text, 1, 0, "C")
                self.pdf.set_text_color(0, 0, 0)  # Reset to black
                
                # Color code the confidence
                confidence = stock['confidence']
                if confidence >= 80:
                    self.pdf.set_text_color(0, 128, 0)  # Green
                elif confidence >= 60:
                    self.pdf.set_text_color(0, 0, 255)  # Blue
                elif confidence >= 40:
                    self.pdf.set_text_color(255, 165, 0)  # Orange
                self.pdf.cell(45, 10, f"{confidence}% Bullish", 1, 1, "C")
                self.pdf.set_text_color(0, 0, 0)  # Reset to black
                
                # Add bullish signals
                self.pdf.set_font("Arial", "I", 8)
                self.pdf.cell(10, 5, "", 0, 0)
                signal_text = "Signals: " + ", ".join(stock['bullish_signals'])
                self.pdf.multi_cell(180, 5, signal_text, 0, 1)
                self.pdf.set_font("Arial", "", 10)
            
            # Add disclaimer
            self.pdf.ln(10)
            self.pdf.set_font("Arial", "I", 8)
            self.pdf.multi_cell(0, 5, "DISCLAIMER: This report is generated using technical analysis and is for informational purposes only. It does not constitute investment advice. Always conduct your own research before making investment decisions.", 0, 1)
            
            # Save the PDF
            filename = f"next_week_bullish_stocks_{datetime.now().strftime('%Y%m%d')}.pdf"
            self.pdf.output(filename)
            print(f"Report generated: {filename}")
            return filename
        except Exception as e:
            print(f"Error generating report: {str(e)}")
            return None
    
    def run_prediction(self):
        """Run the complete prediction process for next week"""
        print(f"Starting Nifty 50 stock prediction for next week at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
        
        # Fetch Nifty 50 stocks
        stocks = self.fetch_nifty50_stocks()
        if not stocks:
            print("No stocks to analyze. Exiting.")
            return
        
        # Analyze each stock
        bullish_stocks = []
        total = len(stocks)
        
        for i, ticker in enumerate(stocks):
            print(f"Analyzing {ticker} ({i+1}/{total})...")
            try:
                result, error = self.predict_next_week(ticker)
                if result:
                    bullish_stocks.append(result)
                    print(f"✅ {ticker}: {result['prediction']} (Confidence: {result['confidence']}%)")
                else:
                    print(f"❌ {ticker}: {error}")
            except Exception as e:
                print(f"❌ Error processing {ticker}: {str(e)}")
        
        # Generate report
        if bullish_stocks:
            print(f"\nFound {len(bullish_stocks)} bullish stocks for next week out of {total} analyzed.")
            report_file = self.generate_report(bullish_stocks)
            if report_file:
                print(f"Prediction complete! Report saved to {report_file}")
            else:
                print("Failed to generate report.")
        else:
            print("No bullish stocks found for next week in the current market conditions.")
        
        return bullish_stocks

def scheduled_prediction():
    """Function to run scheduled predictions"""
    try:
        predictor = BullishStockPredictor()
        predictor.run_prediction()
    except Exception as e:
        print(f"Error in scheduled prediction: {str(e)}")

# Create and run the stock predictor
if __name__ == "__main__":
    try:
        predictor = BullishStockPredictor()
        
        # Run immediately once
        bullish_stocks = predictor.run_prediction()
        
        # Schedule to run every day at 8:00 AM to get fresh data
        schedule.every().day.at("08:00").do(scheduled_prediction)
        
        # Keep the script running for scheduled tasks
        print("\nScheduled to run daily at 8:00 AM. Keep the script running.")
        print("Press Ctrl+C to exit.")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("Script terminated by user.")
    except Exception as e:
        print(f"Fatal error: {str(e)}")

# DATA SOURCES FOR THIS CODE:
# 1. Stock data: This code uses Yahoo Finance (yfinance library) to fetch historical stock data
#    No additional data files needed as it's pulled directly from Yahoo Finance's API
#
# 2. Nifty 50 stock list: The code tries to fetch the current Nifty 50 stocks from:
#    - Primary source: NSE India website API (https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050)
#    - Secondary source: Web scraping NSE India website
#    - Fallback: Uses a hardcoded list of Nifty 50 stocks if both methods fail
#
# 3. Generated output: The PDF report is saved in the same directory as this script with filename:
#    "next_week_bullish_stocks_YYYYMMDD.pdf" (where YYYYMMDD is the current date)
#
# REQUIRED PACKAGES:
# pip install pandas yfinance numpy matplotlib requests beautifulsoup4 fpdf schedule
