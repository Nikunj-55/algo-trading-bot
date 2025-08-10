import pandas as pd
import ta
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

def prepare_features(df):
    # Technical indicators
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
    df['20DMA'] = df['Close'].rolling(window=20).mean()
    df['50DMA'] = df['Close'].rolling(window=50).mean()
    df['MACD'] = ta.trend.MACD(df['Close']).macd()
    df['Volume_Change'] = df['Volume'].pct_change()

    # Target: 1 if next day's close > today's close, else 0
    df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)

    df.dropna(inplace=True)
    return df

if __name__ == "__main__":
    # Load clean CSV
    df = pd.read_csv("TCS.NS_data.csv", index_col="Date", parse_dates=True)
    df = df.apply(pd.to_numeric, errors='coerce')

    df = prepare_features(df)

    # Features & target
    X = df[['RSI', '20DMA', '50DMA', 'MACD', 'Volume_Change']]
    y = df['Target']

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Model
    model = DecisionTreeClassifier(max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    # Predictions & accuracy
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    print(f"Prediction Accuracy: {acc:.2%}")
