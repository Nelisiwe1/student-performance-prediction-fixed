import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "StudentsPerformance.csv")

def main():
    df = pd.read_csv(DATA_PATH, sep=';')  # student-mat uses semicolon separator
    sns.set(style='whitegrid')

    # Histogram of final grade
    plt.figure(figsize=(10,5))
    sns.histplot(df['G3'], kde=True, color='blue', label='Final Grade (G3)')
    plt.title('Distribution of Final Grades')
    plt.savefig('G3_distribution.png')
    print('Saved G3_distribution.png')

    # Boxplot of final grade by sex
    plt.figure(figsize=(8,5))
    sns.boxplot(x='sex', y='G3', data=df)
    plt.title('Final Grade by Sex')
    plt.savefig('G3_by_sex.png')
    print('Saved G3_by_sex.png')

    # Correlation heatmap (numeric columns only)
    numeric_cols = df.select_dtypes(include='number')
    plt.figure(figsize=(10,8))
    sns.heatmap(numeric_cols.corr(), annot=True, fmt=".2f", cmap='coolwarm')
    plt.title('Correlation Heatmap (Numeric Features Only)')
    plt.savefig('student_correlation_heatmap.png')
    print('Saved student_correlation_heatmap.png')

if __name__ == '__main__':
    main()
