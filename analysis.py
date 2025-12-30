"""
Netflix Content Analysis Script
Analyzes Netflix titles dataset and generates insights with visualizations
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def check_file_exists(filename: str) -> bool:
    """Check if the Netflix dataset exists."""
    if not os.path.exists(filename):
        print(f"Error: {filename} not found in the current directory.")
        print(f"Current directory: {os.getcwd()}")
        return False
    return True


def create_plots_directory() -> str:
    """Create plots directory if it doesn't exist."""
    plots_dir = "plots"
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
        print(f"✓ Created '{plots_dir}' directory")
    return plots_dir


def load_data(filename: str) -> pd.DataFrame:
    """Load Netflix dataset from CSV file."""
    try:
        df = pd.read_csv(filename)
        print(f"✓ Loaded {len(df)} records from {filename}\n")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the Netflix dataset.
    - Remove duplicates
    - Handle missing values
    """
    initial_count = len(df)
    
    # Remove duplicates
    df = df.drop_duplicates()
    duplicates_removed = initial_count - len(df)
    if duplicates_removed > 0:
        print(f"✓ Removed {duplicates_removed} duplicate records")
    
    # Display missing values
    missing_values = df.isnull().sum()
    if missing_values.sum() > 0:
        print(f"\nMissing values found:")
        for col, count in missing_values[missing_values > 0].items():
            print(f"  - {col}: {count} ({count/len(df)*100:.1f}%)")
    
    print()
    return df


def calculate_movie_tv_ratio(df: pd.DataFrame) -> None:
    """Calculate and print the ratio of Movies to TV Shows."""
    print("=" * 60)
    print("QUESTION 1: What is the ratio of Movies to TV Shows?")
    print("=" * 60)
    
    type_counts = df['type'].value_counts()
    total = len(df)
    
    for content_type, count in type_counts.items():
        percentage = (count / total) * 100
        print(f"{content_type}: {count} ({percentage:.1f}%)")
    
    # Calculate ratio
    if 'Movie' in type_counts.index and 'TV Show' in type_counts.index:
        ratio = type_counts['Movie'] / type_counts['TV Show']
        print(f"\nRatio (Movie:TV Show): 1:{1/ratio:.2f}")
    
    print()


def find_top_producing_country(df: pd.DataFrame) -> None:
    """Find the country that produces the most content."""
    print("=" * 60)
    print("QUESTION 2: Which country produces the most content?")
    print("=" * 60)
    
    # Handle missing countries
    df_countries = df.dropna(subset=['country'])
    
    # Split countries and expand (some titles have multiple countries)
    country_list = []
    for countries_str in df_countries['country']:
        if isinstance(countries_str, str):
            countries = [c.strip() for c in countries_str.split(',')]
            country_list.extend(countries)
    
    country_counts = pd.Series(country_list).value_counts()
    
    print(f"Total unique countries: {len(country_counts)}")
    print(f"\nTop 10 countries by content production:")
    for idx, (country, count) in enumerate(country_counts.head(10).items(), 1):
        print(f"{idx:2}. {country:<20} {count:>4} titles")
    
    print()
    return country_counts


def find_most_common_year(df: pd.DataFrame) -> None:
    """Find the most common release year."""
    print("=" * 60)
    print("QUESTION 3: What is the most common release year?")
    print("=" * 60)
    
    # Handle missing values
    df_years = df.dropna(subset=['release_year'])
    
    year_counts = df_years['release_year'].value_counts().sort_index(ascending=False)
    most_common_year = year_counts.idxmax()
    most_common_count = year_counts.max()
    
    print(f"Most common release year: {int(most_common_year)} ({most_common_count} titles)")
    print(f"\nTop 10 release years by content volume:")
    for idx, (year, count) in enumerate(year_counts.head(10).items(), 1):
        print(f"{idx:2}. {int(year):<6} {count:>4} titles")
    
    print()


def plot_movie_tv_distribution(df: pd.DataFrame, plots_dir: str) -> None:
    """Create and save a bar chart of Movies vs TV Shows."""
    type_counts = df['type'].value_counts()
    
    plt.figure(figsize=(10, 6))
    colors = ['#E50914', '#564d4d']  # Netflix red and gray
    type_counts.plot(kind='bar', color=colors, edgecolor='black', linewidth=1.5)
    
    plt.title('Netflix Content Distribution: Movies vs TV Shows', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Content Type', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Titles', fontsize=12, fontweight='bold')
    plt.xticks(rotation=0)
    
    # Add value labels on bars
    for i, v in enumerate(type_counts.values):
        plt.text(i, v + 50, str(v), ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    filepath = os.path.join(plots_dir, 'movies_vs_tvshows.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✓ Saved chart: {filepath}")
    plt.close()


def plot_top_countries(df: pd.DataFrame, plots_dir: str, country_counts: pd.Series) -> None:
    """Create and save a bar chart of Top 10 countries by content production."""
    top_10_countries = country_counts.head(10)
    
    plt.figure(figsize=(12, 7))
    top_10_countries.plot(kind='barh', color='#E50914', edgecolor='black', linewidth=1.5)
    
    plt.title('Top 10 Countries by Netflix Content Production', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Number of Titles', fontsize=12, fontweight='bold')
    plt.ylabel('Country', fontsize=12, fontweight='bold')
    
    # Add value labels on bars
    for i, v in enumerate(top_10_countries.values):
        plt.text(v + 10, i, str(v), ha='left', va='center', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    filepath = os.path.join(plots_dir, 'top_10_countries.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✓ Saved chart: {filepath}")
    plt.close()


def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("NETFLIX CONTENT ANALYSIS")
    print("="*60 + "\n")
    
    # Configuration
    data_file = "netflix_titles.csv"
    
    # Step 1: Check if file exists
    if not check_file_exists(data_file):
        return
    
    # Step 2: Create plots directory
    plots_dir = create_plots_directory()
    
    # Step 3: Load data
    df = load_data(data_file)
    
    # Step 4: Clean data
    print("DATA CLEANING")
    print("-" * 60)
    df = clean_data(df)
    
    # Step 5: Answer specific questions
    calculate_movie_tv_ratio(df)
    country_counts = find_top_producing_country(df)
    find_most_common_year(df)
    
    # Step 6: Generate visualizations
    print("GENERATING VISUALIZATIONS")
    print("-" * 60)
    plot_movie_tv_distribution(df, plots_dir)
    plot_top_countries(df, plots_dir, country_counts)
    
    print("\n" + "="*60)
    print("✓ ANALYSIS COMPLETE!")
    print("="*60)
    print(f"\nGenerated files:")
    print(f"  • {os.path.join(plots_dir, 'movies_vs_tvshows.png')}")
    print(f"  • {os.path.join(plots_dir, 'top_10_countries.png')}\n")


if __name__ == "__main__":
    main()
