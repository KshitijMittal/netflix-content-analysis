import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

data_file = "netflix_titles.csv"

if not Path(data_file).exists():
    print(f"Can't find {data_file}")
    exit()

plots_dir = Path("plots")
plots_dir.mkdir(exist_ok=True)

# load the data
df = pd.read_csv(data_file)
print(f"Loaded {len(df)} records\n")

# remove duplicates
initial_count = len(df)
df = df.drop_duplicates()
removed = initial_count - len(df)
if removed > 0:
    print(f"Removed {removed} duplicates\n")

# check for missing values
print("Checking missing values...")
for col in df.columns:
    missing_count = df[col].isnull().sum()
    if missing_count > 0:
        pct = (missing_count / len(df)) * 100
        print(f"  {col}: {missing_count} ({pct:.1f}%)")
print()

# -- ANALYSIS --

# 1. Movie vs TV Show ratio
print("=" * 50)
print("Movies vs TV Shows")
print("=" * 50)

type_counts = df['type'].value_counts()
total_titles = len(df)

for content_type in type_counts.index:
    count = type_counts[content_type]
    percentage = (count / total_titles) * 100
    print(f"{content_type}: {count} ({percentage:.1f}%)")

movies = type_counts.get('Movie', 0)
tv_shows = type_counts.get('TV Show', 0)
if movies > 0 and tv_shows > 0:
    ratio = movies / tv_shows
    print(f"Ratio: 1:{1/ratio:.2f}\n")

# 2. Top countries
print("=" * 50)
print("Countries producing most content")
print("=" * 50)

country_list = []
for idx, row in df.iterrows():
    country_cell = row['country']
    if pd.notna(country_cell):
        countries = country_cell.split(',')
        for country in countries:
            country = country.strip()
            country_list.append(country)

country_counts = {}
for country in country_list:
    if country in country_counts:
        country_counts[country] += 1
    else:
        country_counts[country] = 1

# sort by count
sorted_countries = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)

print(f"Total countries: {len(sorted_countries)}\n")
print("Top 10:")
for i in range(min(10, len(sorted_countries))):
    country, count = sorted_countries[i]
    print(f"{i+1:2}. {country:<20} {count} titles")
print()

# 3. Most common release year
print("=" * 50)
print("Release years")
print("=" * 50)

year_counts = {}
for idx, row in df.iterrows():
    year = row['release_year']
    if pd.notna(year):
        year = int(year)
        if year in year_counts:
            year_counts[year] += 1
        else:
            year_counts[year] = 1

# find most common year
most_common_year = None
highest_count = 0
for year, count in year_counts.items():
    if count > highest_count:
        highest_count = count
        most_common_year = year

print(f"Most common: {most_common_year} ({highest_count} titles)\n")

# sort years and show top 10
sorted_years = sorted(year_counts.items(), key=lambda x: x[0], reverse=True)
print("Top 10 years:")
for i in range(min(10, len(sorted_years))):
    year, count = sorted_years[i]
    print(f"{i+1:2}. {int(year):<6} {count} titles")
print()

# -- PLOTS --
print("Generating plots...\n")

# plot 1: movies vs tv
plt.figure(figsize=(10, 6))
type_counts.plot(kind='bar', color=['#E50914', '#564d4d'], edgecolor='black', linewidth=1.5)
plt.title('Movies vs TV Shows', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Type', fontsize=11, fontweight='bold')
plt.ylabel('Count', fontsize=11, fontweight='bold')
plt.xticks(rotation=0)

for i, val in enumerate(type_counts.values):
    plt.text(i, val + 50, str(val), ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig(plots_dir / 'movies_vs_tvshows.png', dpi=300, bbox_inches='tight')
print(f"Saved: plots/movies_vs_tvshows.png")
plt.close()

# plot 2: top countries
top_10_countries = sorted_countries[:10]
countries_names = [c[0] for c in top_10_countries]
countries_values = [c[1] for c in top_10_countries]

plt.figure(figsize=(11, 7))
plt.barh(countries_names, countries_values, color='#E50914', edgecolor='black', linewidth=1.5)
plt.title('Top 10 Countries', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Titles', fontsize=11, fontweight='bold')
plt.ylabel('Country', fontsize=11, fontweight='bold')

for i, val in enumerate(countries_values):
    plt.text(val + 5, i, str(val), ha='left', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig(plots_dir / 'top_10_countries.png', dpi=300, bbox_inches='tight')
print(f"Saved: plots/top_10_countries.png")
plt.close()

print("Done!")
