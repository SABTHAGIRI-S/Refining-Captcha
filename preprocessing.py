import numpy as np
import pandas as pd

# Total number of rows and half for each label
n = 1_000_000
n_half = n // 2


# Generate synthetic data for human rows
human_df = pd.DataFrame({
    'Average_Dwell_Time': np.random.normal(loc=150, scale=30, size=n_half),
    'Average_Flight_Time': np.random.normal(loc=120, scale=20, size=n_half),
    'Flight_Time_Std_Dev': np.random.normal(loc=10, scale=2, size=n_half),
    'Human_Like_Typing_Score': np.random.uniform(low=0.7, high=1.0, size=n_half),
    'Words_Per_Minute': np.random.normal(loc=60, scale=10, size=n_half),
    'Label': 'human'
})

# Generate synthetic data for bot rows
bot_df = pd.DataFrame({
    'Average_Dwell_Time': np.random.normal(loc=50, scale=10, size=n_half),
    'Average_Flight_Time': np.random.normal(loc=30, scale=5, size=n_half),
    'Flight_Time_Std_Dev': np.random.normal(loc=1, scale=0.2, size=n_half),
    'Human_Like_Typing_Score': np.random.uniform(low=0.0, high=0.3, size=n_half),
    'Words_Per_Minute': np.random.normal(loc=150, scale=15, size=n_half),
    'Label': 'bot'
})

# Combine the human and bot datasets and shuffle the rows
df = pd.concat([human_df, bot_df]).sample(frac=1).reset_index(drop=True)

# Save the dataset to a CSV file
df.to_csv('ketstokes.csv', index=False)

print("Dataset generated and saved as 'ketstokes.csv'.")
