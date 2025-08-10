# import pandas as pd
# import ta

# def apply_strategy(df):
#     df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
#     df['20DMA'] = df['Close'].rolling(window=20).mean()
#     df['50DMA'] = df['Close'].rolling(window=50).mean()
#     df['Buy_Signal'] = (df['RSI'] < 30) & (df['20DMA'] > df['50DMA'])
#     return df

# if __name__ == "__main__":
#     # Read CSV
#     df = pd.read_csv("TCS.NS_data.csv", index_col="Date", parse_dates=True)

#     # Convert all numeric columns from strings to floats
#     df = df.apply(pd.to_numeric, errors='coerce')

#     df = apply_strategy(df)
#     print(df[['Close', 'RSI', '20DMA', '50DMA', 'Buy_Signal']].tail(10))
# import pandas as pd
# import ta
# from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.metrics import accuracy_score

# def apply_strategy(df):
#     """Add RSI, Moving Averages, Buy Signals."""
#     df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
#     df['20DMA'] = df['Close'].rolling(window=20).mean()
#     df['50DMA'] = df['Close'].rolling(window=50).mean()
#     df['Buy_Signal'] = (df['RSI'] < 30) & (df['20DMA'] > df['50DMA'])
#     return df

# def prepare_ml_features(df):
#     """Create features for ML model."""
#     df['MACD'] = ta.trend.MACD(df['Close']).macd()
#     df['Volume_Change'] = df['Volume'].pct_change()
#     df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)  # 1 if price goes up next day
#     df.dropna(inplace=True)
#     return df

# def run_strategy_and_ml(filename):
#     # Load clean CSV
#     df = pd.read_csv(filename, index_col="Date", parse_dates=True)
#     df = df.apply(pd.to_numeric, errors='coerce')

#     # Apply trading strategy
#     df = apply_strategy(df)

#     # Prepare ML features
#     df = prepare_ml_features(df)

#     # ML Model
#     X = df[['RSI', '20DMA', '50DMA', 'MACD', 'Volume_Change']]
#     y = df['Target']

#     X_train, X_test, y_train, y_test = train_test_split(
#         X, y, test_size=0.2, shuffle=False
#     )

#     model = DecisionTreeClassifier(max_depth=5, random_state=42)
#     model.fit(X_train, y_train)

#     preds = model.predict(X_test)
#     acc = accuracy_score(y_test, preds)

#     print(f"📊 Prediction Accuracy: {acc:.2%}\n")
#     print("📈 Last 10 days with predictions & signals:")
#     df['Predicted_Move'] = model.predict(X)  # Predict for all rows
#     print(df[['Close', 'RSI', '20DMA', '50DMA', 'Buy_Signal', 'Predicted_Move']].tail(10))

# if __name__ == "__main__":
#     run_strategy_and_ml("TCS.NS_data.csv")
from google_sheet_logger import connect_to_sheets, log_trade, update_summary
import pandas as pd
import ta
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def apply_strategy(df):
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
    df['20DMA'] = df['Close'].rolling(window=20).mean()
    df['50DMA'] = df['Close'].rolling(window=50).mean()
    df['Buy_Signal'] = (df['RSI'] < 30) & (df['20DMA'] > df['50DMA'])
    return df

def prepare_features(df):
    df['MACD'] = ta.trend.MACD(df['Close']).macd()
    df['Volume_Change'] = df['Volume'].pct_change()
    df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
    df.dropna(inplace=True)
    return df

if __name__ == "__main__":
    df = pd.read_csv("TCS.NS_data.csv", index_col="Date", parse_dates=True)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = apply_strategy(df)
    df = prepare_features(df)

    X = df[['RSI', '20DMA', '50DMA', 'MACD', 'Volume_Change']]
    y = df['Target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    model = DecisionTreeClassifier(max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    df['Predicted_Move'] = model.predict(X)

    # Connect to Google Sheets
    sheet = connect_to_sheets("AlgoTradeLogs")

    # Log last 10 days
    for date, row in df.tail(10).iterrows():
        log_trade(sheet, [
            str(date.date()),
            row['Close'],
            row['RSI'],
            row['20DMA'],
            row['50DMA'],
            row['Buy_Signal'],
            row['Predicted_Move']
        ])

    # Update summary
    total_trades = len(df[df['Buy_Signal'] == True])
    update_summary(sheet, total_trades, acc)

    print(f"✅ Logged last 10 days to Google Sheets | Accuracy: {acc:.2%}")
