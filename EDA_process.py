import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv(r"C:\Users\Kowsh\OneDrive\Documents\GUVI\PROJECT\data\cleaned_earthquake_data.csv")
df.info()
print("shape:",df.shape)
print("column:",df.head())
print("\nmissing values:\n",df.isna().sum())

#DATA PREPROCESSING
#decompose date feature
df['date'] = pd.to_datetime(df['time'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day

#statistical summary
print("\nStatistical Summary:\n",df.describe())

#categorical features analysis
categorical_cols = ['depth_category', 'magnitude_category', 'type']
for col in categorical_cols:
    print(f"\nValue counts for {col}:\n", df[col].value_counts())

#correlation analysis
correlation_matrix = df.select_dtypes(include='number').corr()  

#visualizations
#histogram for numerical features
numerical_cols = ['mag', 'depth_km','sig']
for col in numerical_cols:
    plt.figure(figsize=(8, 4))
    sns.histplot(df[col], bins=30, kde=True)
    plt.title(f'Histogram of {col}')
    plt.xlabel(col)
    plt.ylabel('Frequency')
    plt.show()

#bar plots for categorical features
for col in categorical_cols:
    plt.figure(figsize=(8, 4))
    sns.countplot(data=df, x=col, order=df[col].value_counts().index)
    plt.title(f'Count Plot of {col}')
    plt.xlabel(col)
    plt.ylabel('Count')
    plt.show()

#scatter plot for mag vs depth_km
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x='depth_km', y='mag', hue='magnitude_category')
plt.title('Scatter Plot of Magnitude vs Depth (km)')
plt.xlabel('Depth (km)')
plt.ylabel('Magnitude') 
plt.show()

#time series analysis of earthquakes per year
earthquakes_per_year = df.groupby('year').size()
plt.figure(figsize=(8, 5))
earthquakes_per_year.plot(marker='o')
plt.title('Number of Earthquakes per Year')
plt.xlabel('Year')
plt.ylabel('Number of Earthquakes')
plt.grid()
plt.show()

#heatmap for correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Heatmap of Correlation Matrix')
plt.show()

#boxplots for numerical features
for col in numerical_cols:
    plt.figure(figsize=(8, 4))
    sns.boxplot(x='magnitude_category', y=col, data=df)
    plt.title(f'Boxplot of {col} by Magnitude Category')
    plt.xlabel('Magnitude Category')
    plt.ylabel(col)
    plt.show()

#time series line plots for numerical features over years
for col in numerical_cols:
    yearly_avg = df.groupby('year')[col].mean()
    plt.figure(figsize=(10, 5))
    yearly_avg.plot(marker='v')
    plt.title(f'Yearly Average of {col}')
    plt.xlabel('Year')
    plt.ylabel(f'Average {col}')
    plt.grid()
    plt.show()
