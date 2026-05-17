import pandas as pd

# ── 1. Load & Parse Dates ─────────────────────────────────────────────────────
# Dates are stored in DD/MM/YYYY format.
# Without dayfirst=True, pandas reads them as MM/DD/YYYY,
# causing 1,684 rows to produce negative shipping days.

df = pd.read_csv(r'data/train_2.csv')

df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['Ship Date']  = pd.to_datetime(df['Ship Date'],  dayfirst=True)

print("Shape after load:", df.shape)
df.info()

# ── 2. Handle Missing Values ──────────────────────────────────────────────────
# Postal Code is the only column with nulls (11 rows).
# All null rows belong to Burlington, Vermont — verified below before filling.

postal_nan = df[df['Postal Code'].isnull()]
US_Bur_Ver = df[(df['City'] == 'Burlington') & (df['State'] == 'Vermont')]

if US_Bur_Ver.equals(postal_nan):
    print("Verified: all null Postal Codes are Burlington, Vermont")
else:
    print("Warning: mismatch — review before filling")

df['Postal Code'] = df['Postal Code'].fillna('05401')
df['Postal Code'] = df['Postal Code'].astype('int64')

# ── 3. Fix Data Types ─────────────────────────────────────────────────────────
# Enforce datetime64[ns] after cleaning.

df['Order Date'] = df['Order Date'].astype('datetime64[ns]')
df['Ship Date']  = df['Ship Date'].astype('datetime64[ns]')

# ── 4. Feature Engineering ────────────────────────────────────────────────────
# Derive new columns to support dashboard calculations in Power BI.

# Time components
df['Month']         = df['Order Date'].dt.month
df['Week_of_Month'] = (df['Order Date'].dt.day - 1) // 7 + 1
df['Day']           = df['Order Date'].dt.day_name()
df['Year']          = df['Order Date'].dt.year
df['Quarter']       = df['Order Date'].dt.quarter

# Shipping & sales features
df['Days_to_Ship'] = (df['Ship Date'] - df['Order Date']).dt.days

df['Sales_Tier'] = pd.cut(
    df['Sales'],
    bins=[0, 50, 500, float('inf')],
    labels=['Small', 'Medium', 'Large']
)

print("\nEngineered columns:", ['Month','Week_of_Month','Day','Year','Quarter','Days_to_Ship','Sales_Tier'])
print("Final shape:", df.shape)
print(df.head())

# ── 5. Export ─────────────────────────────────────────────────────────────────
df.to_csv('data/clean_data.csv', index=False)
print("\nExported to data/clean_data.csv")