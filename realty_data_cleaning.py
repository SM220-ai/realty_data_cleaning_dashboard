import pandas as pd
import numpy as np

# Load the messy data
df = pd.read_csv("your_file_name.csv")

# Check for duplicates
print(f"Total rows: {len(df)}")
print(f"Unique IDs: {df['Prop_ID'].nunique()}")

# If there are duplicates, show them
duplicates = df[df.duplicated(subset=['Prop_ID'], keep=False)]
if len(duplicates) > 0:
    print("\nDuplicate IDs found:")
    print(duplicates)
else:
    print("\nNo duplicate IDs found!")

# Check the format (should all start with "A-")
invalid_ids = df[~df['Prop_ID'].str.startswith('A-')]
if len(invalid_ids) > 0:
    print(f"\n{len(invalid_ids)} IDs don't start with 'A-':")
    print(invalid_ids)
else:
    print("\nAll IDs are in correct format!")

# ==========================================
# STEP 2: CLEAN THE DATE COLUMN
# ==========================================

# First, let's see what the dates look like before cleaning
print("\n--- Before Date Cleaning ---")
print(df['Close_Date'].head(10))

# Convert to datetime with error handling
# errors='coerce' turns unparseable dates into NaT (Not a Time)
df['Close_Date'] = pd.to_datetime(df['Close_Date'], errors='coerce')

# Check how many dates failed to parse (showing as NaT)
nat_count = df['Close_Date'].isna().sum()
print(f"\n--- After Date Cleaning ---")
print(f"Dates that failed to parse (NaT): {nat_count}")

# Show some examples of what worked
print("\nSample of cleaned dates:")
print(df['Close_Date'].head(10))

print(df[df['Close_Date'].isna()])

# ==========================================
# STEP 2.1: FIX 2-DIGIT YEARS
# ==========================================

# For dates that were parsed, check if the year is less than 100 (meaning it's a 2-digit year)
# If so, add 2000 to make it a proper 4-digit year
mask = df['Close_Date'].notna() & (df['Close_Date'].dt.year < 100)
df.loc[mask, 'Close_Date'] = df.loc[mask, 'Close_Date'] + pd.DateOffset(years=2000)

print(f"Fixed {mask.sum()} dates with 2-digit years")

# ==========================================
# STEP 3: CLEAN THE SALE_PRICE COLUMN
# ==========================================

print("\n--- Before Price Cleaning ---")
print(df['Sale_Price'].head(10))

# 1. Make everything lowercase to catch "tbd", "call for price", etc.
df['Sale_Price'] = df['Sale_Price'].astype(str).str.lower()

# 2. Replace 'k' with '000' (e.g., "450k" -> "450000")
df['Sale_price_cleaned'] = df['Sale_Price'].str.replace('k', '000', regex=False)

# 3. Remove all characters that are NOT numbers or decimals
# [^0-9.] means "match anything that is NOT a digit (0-9) or a dot (.)"
df['Sale_price_cleaned'] = df['Sale_price_cleaned'].str.replace(r'[^0-9.]', '', regex=True)

# 4. Convert to numeric. If it's blank or "tbd" (which is now empty ""), it becomes NaN
df['Sale_Price'] = pd.to_numeric(df['Sale_price_cleaned'], errors='coerce')

# Drop the temporary helper column
df = df.drop(columns=['Sale_price_cleaned'])

print("\n--- After Price Cleaning ---")
print(f"Missing prices (NaN): {df['Sale_Price'].isna().sum()}")
print(df['Sale_Price'].head(10))

# ==========================================
# STEP 4: CLEAN THE SQ_FT COLUMN
# ==========================================

print("\n--- Before Sq_Ft Cleaning ---")
print(df['Sq_Ft'].head(10))

# 1. Remove "sqft", "sq. ft.", and any other text
df['Sq_Ft_cleaned'] = df['Sq_Ft'].astype(str).str.replace(r'sq\.?\s*ft\.?', '', regex=True, case=False)

# 2. Remove commas
df['Sq_Ft_cleaned'] = df['Sq_Ft_cleaned'].str.replace(',', '')

# 3. Convert to numeric
df['Sq_Ft'] = pd.to_numeric(df['Sq_Ft_cleaned'], errors='coerce')

# 4. Flag impossible values (negative or > 50,000)
# Create a mask for rows with impossible values
impossible_mask = (df['Sq_Ft'] < 0) | (df['Sq_Ft'] > 50000)

# Count how many we're flagging
flagged_count = impossible_mask.sum()
print(f"\nFlagging {flagged_count} impossible square footage values as NaN")

# Set impossible values to NaN
df.loc[impossible_mask, 'Sq_Ft'] = np.nan

# Drop the temporary helper column
df = df.drop(columns=['Sq_Ft_cleaned'])

print("\n--- After Sq_Ft Cleaning ---")
print(f"Missing Sq_Ft values (NaN): {df['Sq_Ft'].isna().sum()}")
print(df['Sq_Ft'].head(10))

# ==========================================
# STEP 5: CLEAN THE BEDS COLUMN
# ==========================================

print("\n--- Before Beds Cleaning ---")
print(df['Beds'].head(10))

# 1. Create a mapping for text numbers
text_to_number = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5
}

# 2. Convert to lowercase and map text to numbers
# If it's already a number, .map() will leave it as NaN, so we handle that
df['Beds_cleaned'] = df['Beds'].astype(str).str.lower().map(text_to_number)

# 3. For rows that weren't text (already numbers), keep the original value
# This uses .fillna() to fill the NaN values with the original numeric values
df['Beds_cleaned'] = df['Beds_cleaned'].fillna(pd.to_numeric(df['Beds'], errors='coerce'))

# 4. Replace the original column
df['Beds'] = df['Beds_cleaned']

# Drop the temporary helper column
df = df.drop(columns=['Beds_cleaned'])

print("\n--- After Beds Cleaning ---")
print(f"Missing Beds values (NaN): {df['Beds'].isna().sum()}")
print(df['Beds'].head(10))

# ==========================================
# STEP 6: CLEAN THE COMMISSION COLUMN
# ==========================================

print("\n--- Before Commission Cleaning ---")
print(df['Commission'].head(10))

# 1. Create a mask to identify rows with "%"
has_percent = df['Commission'].astype(str).str.contains('%', na=False)

# 2. Remove the "%" sign
df['Commission_cleaned'] = df['Commission'].astype(str).str.replace('%', '', regex=False)

# 3. Convert to numeric (this turns "None" into NaN)
df['Commission_cleaned'] = pd.to_numeric(df['Commission_cleaned'], errors='coerce')

# 4. For rows that had "%", divide by 100
df.loc[has_percent, 'Commission_cleaned'] = df.loc[has_percent, 'Commission_cleaned'] / 100

# 5. Replace the original column
df['Commission'] = df['Commission_cleaned']

# Drop the temporary helper column
df = df.drop(columns=['Commission_cleaned'])

print("\n--- After Commission Cleaning ---")
print(f"Missing Commission values (NaN): {df['Commission'].isna().sum()}")
print(df['Commission'].head(10))

# ==========================================
# STEP 7: FIX EMAIL TYPOS
# ==========================================

print("\n--- Before Email Cleaning ---")
print(f"Emails with 'gmil.com': {df['Agent_Email'].str.contains('gmil', na=False).sum()}")

# Replace the typo
df['Agent_Email'] = df['Agent_Email'].str.replace('gmil.com', 'gmail.com', regex=False)

print("\n--- After Email Cleaning ---")
print(f"Emails with 'gmil.com' (should be 0): {df['Agent_Email'].str.contains('gmil', na=False).sum()}")

# ==========================================
# STEP 7.5: FLAG PROBLEM ROWS
# ==========================================

print("\n--- Flagging Problem Rows ---")

# Create a Flag column that lists which fields are missing for each row
df['Flag'] = ''

# For each column, if it's NaN, add the column name to the Flag
df.loc[df['Close_Date'].isna(), 'Flag'] += 'Date '
df.loc[df['Sale_Price'].isna(), 'Flag'] += 'Price '
df.loc[df['Sq_Ft'].isna(), 'Flag'] += 'SqFt '
df.loc[df['Beds'].isna(), 'Flag'] += 'Beds '
df.loc[df['Commission'].isna(), 'Flag'] += 'Commission '

# Strip any trailing spaces
df['Flag'] = df['Flag'].str.strip()

# Count how many rows have at least one flag
problem_rows = df[df['Flag'] != '']
print(f"Total rows with at least one issue: {len(problem_rows)}")

# Create a summary DataFrame of just the problem IDs
problem_summary = problem_rows[['Prop_ID', 'Flag']].copy()
problem_summary.columns = ['Problem_ID', 'Issues']

print(f"\nSummary of problem IDs:")
print(problem_summary.head(10))

# ==========================================
# STEP 7.6: FORMAT DATES WITHOUT TIME
# ==========================================

# Convert datetime to string format YYYY-MM-DD (no time)
df['Close_Date'] = df['Close_Date'].dt.strftime('%Y-%m-%d')

print("Dates formatted without time component")
# ==========================================
# STEP 8: SAVE AS EXCEL WITH TWO SHEETS
# ==========================================

# Save to Excel with two sheets
with pd.ExcelWriter('your_file_name.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Cleaned Data', index=False)
    problem_summary.to_excel(writer, sheet_name='Problem IDs', index=False)

print("\n" + "="*50)
print("CLEANING COMPLETE!")
print("="*50)
print(f"Original rows: 493")
print(f"Final rows: {len(df)}")
print(f"Rows with issues: {len(problem_rows)}")
print(f"\nCleaned data saved to: Marcus_realty_cleaned.xlsx")
print(f"  - Sheet 1: Cleaned Data (with Flag column)")
print(f"  - Sheet 2: Problem IDs (summary)")