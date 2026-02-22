import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# STEP 1: Create Database
# -------------------------------

conn = sqlite3.connect("heritage_data.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS heritage_sites")

cursor.execute("""
CREATE TABLE heritage_sites (
    id INTEGER PRIMARY KEY,
    name_en TEXT,
    category TEXT,
    region_en TEXT,
    states_name_en TEXT,
    danger INTEGER,
    date_inscribed INTEGER
)
""")

# -------------------------------
# STEP 2: Insert Sample Data
# -------------------------------

sample_data = [
    ("Great Wall of China", "Cultural", "Asia-Pacific", "China", 0, 1987),
    ("Taj Mahal", "Cultural", "Asia-Pacific", "India", 0, 1983),
    ("Venice and its Lagoon", "Cultural", "Europe", "Italy", 1, 1987),
    ("Serengeti National Park", "Natural", "Africa", "Tanzania", 0, 1981),
    ("Historic Centre of Vienna", "Cultural", "Europe", "Austria", 1, 2001),
    ("Grand Canyon National Park", "Natural", "North America", "USA", 0, 1979),
    ("Pyramids of Giza", "Cultural", "Arab States", "Egypt", 0, 1979),
    ("Kathmandu Valley", "Cultural", "Asia-Pacific", "Nepal", 1, 1979),
    ("Machu Picchu", "Mixed", "Latin America", "Peru", 0, 1983),
    ("Galapagos Islands", "Natural", "Latin America", "Ecuador", 1, 1978)
]

cursor.executemany("""
INSERT INTO heritage_sites 
(name_en, category, region_en, states_name_en, danger, date_inscribed)
VALUES (?, ?, ?, ?, ?, ?)
""", sample_data)

conn.commit()

# -------------------------------
# STEP 3: SQL QUERIES
# -------------------------------

#Heritage Sites by Country
query1 = """
SELECT states_name_en, COUNT(*) as site_count
FROM heritage_sites
GROUP BY states_name_en
"""
df_country = pd.read_sql_query(query1, conn)

#Sites In Danger Distribution
query2 = """
SELECT danger, COUNT(*) as count
FROM heritage_sites
GROUP BY danger
"""
df_danger = pd.read_sql_query(query2, conn)

#Regional Inscription Trends
query3 = """
SELECT region_en, COUNT(*) as total_sites
FROM heritage_sites
GROUP BY region_en
"""
df_region = pd.read_sql_query(query3, conn)

# -------------------------------
# STEP 4: VISUALIZATIONS
# -------------------------------

#Heritage Sites by Country (Bar Chart)
df_country.plot(kind='bar', x='states_name_en', y='site_count', legend=False)
plt.title("Heritage Sites by Country")
plt.xlabel("Country")
plt.ylabel("Number of Sites")
plt.tight_layout()
plt.savefig("heritage_by_country.png")
plt.show()

#Sites In Danger (Pie Chart)
plt.figure()
plt.pie(df_danger['count'], labels=["Not in Danger" if x==0 else "In Danger" for x in df_danger['danger']],
        autopct='%1.1f%%')
plt.title("Heritage Sites In Danger Distribution")
plt.tight_layout()
plt.savefig("danger_distribution.png")
plt.show()

#Regional Distribution (Bar Chart)
df_region.plot(kind='bar', x='region_en', y='total_sites', legend=False, color='green')
plt.title("Regional Heritage Distribution")
plt.xlabel("Region")
plt.ylabel("Number of Sites")
plt.tight_layout()
plt.savefig("regional_distribution.png")
plt.show()

conn.close()
