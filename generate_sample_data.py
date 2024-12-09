import pandas as pd

# Sample data
data = {
    'oreginal triple': [
        'Person_A;works_at;Company_X',
        'Person_B;born_in;City_Y',
        'Person_C;married_to;Person_D'
    ],
    'generated text': [
        'Person A works at Company X.',
        'Person B was born in City Y.',
        'Person C is married to Person D.'
    ],
    'generated triple': [
        'Person_A;employed_by;Company_X',
        'Person_B;originates_from;City_Y',
        'Person_C;spouse;Person_D'
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('sample_data.csv', index=False)

print("Sample CSV file 'sample_data.csv' has been created.")
