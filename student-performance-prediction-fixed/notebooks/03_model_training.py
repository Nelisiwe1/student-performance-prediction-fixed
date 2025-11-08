import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
import joblib

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "StudentsPerformance.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model.pkl")

def load_data():
    df = pd.read_csv(DATA_PATH, sep=';')  # student-mat uses semicolon
    # Use G1 and G2 as features to predict final grade G3
    X = df.drop(columns=['G3'])
    y = df['G3']
    cat_cols = X.select_dtypes(include=['object']).columns.tolist()
    return X, y, cat_cols

def build_pipeline(cat_cols):
    preprocessor = ColumnTransformer(
        [('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)],
        remainder='passthrough'
    )
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    return Pipeline([('pre', preprocessor), ('model', model)])

def main():
    X, y, cat_cols = load_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipe = build_pipeline(cat_cols)
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)
    print(f"MSE: {mean_squared_error(y_test, preds):.3f}, R2: {r2_score(y_test, preds):.3f}")
    joblib.dump(pipe, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == '__main__':
    main()
