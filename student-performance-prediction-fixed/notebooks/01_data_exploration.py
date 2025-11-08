import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "StudentsPerformance.csv")

def main():
    df = pd.read_csv(DATA_PATH)
    print("Columns:", df.columns.tolist())
    print(df.head())

if __name__ == '__main__':
    main()
