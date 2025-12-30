# Netflix Content Analysis

## Project Description

This is a production-ready Python project that performs comprehensive exploratory data analysis (EDA) on Netflix's titles dataset. The script loads, cleans, and analyzes Netflix content to answer key business questions about content distribution, production by country, and release year trends. It generates professional visualizations and outputs actionable insights.

### Key Objectives
- Analyze the ratio of Movies to TV Shows
- Identify which countries produce the most Netflix content
- Determine the most common release years
- Create publication-quality visualizations
- Provide a modular, reusable codebase for data analysis

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- netflix_titles.csv (Kaggle dataset)

### Step 1: Clone or Navigate to the Repository
```bash
cd netflix-content-analysis
```

### Step 2: Create a Virtual Environment
It's recommended to use a virtual environment to manage dependencies.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Ensure Dataset is Present
Make sure `netflix_titles.csv` is in the project root directory. You can download it from [Kaggle - Netflix Titles Dataset](https://www.kaggle.com/datasets/shivamb/netflix-shows).

---

## Usage

### Running the Analysis
Once your environment is set up and dependencies are installed:

```bash
python analysis.py
```

### Expected Output
The script will:
1. **Load and validate** the dataset
2. **Clean the data** by removing duplicates and handling missing values
3. **Print analysis results** to the console:
   - Movie to TV Show ratio and percentages
   - Top 10 countries by content production
   - Most common release year
4. **Generate visualizations** and save them to the `plots/` directory:
   - `movies_vs_tvshows.png` - Bar chart comparing content types
   - `top_10_countries.png` - Bar chart of top producing countries

---

## Methodology

### Data Cleaning
- **Duplicate Removal**: Drops any identical records from the dataset
- **Missing Value Handling**:
  - Country column: Titles with missing countries are excluded when analyzing by country
  - Release Year: Only titles with valid years are considered in year analysis
  - Type column: Assumed to have no missing values (core field)

### Country Aggregation
Since many Netflix titles are co-produced by multiple countries (listed as comma-separated values in the dataset), the analysis **splits** these entries. This provides an accurate count of how many titles each country is involved in producing.

### Visualization Strategy
- **Netflix Color Scheme**: Uses Netflix's signature red (#E50914) for brand consistency
- **High Resolution**: All charts saved at 300 DPI for publication quality
- **Clear Labeling**: Value labels displayed on all bars for precise information
- **Responsive Design**: Figures sized appropriately for readability

---

## Key Findings

> **Note to Users:** After running the script, summarize your findings here. Include:
> - What surprised you about the Movie/TV Show split?
> - Which countries dominate Netflix production?
> - What are the implications for the streaming industry?
> - How has content production changed over years?

**Example findings to add:**
- *"As of the latest data, [X%] of Netflix's catalog consists of movies, while [Y%] are TV shows."*
- *"[Country] is the leading content producer for Netflix with [Z] titles."*
- *"The majority of Netflix content was released between [Year A] and [Year B]."*

---

## File Structure

```
netflix-content-analysis/
│
├── analysis.py                 # Main analysis script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── netflix_titles.csv          # Dataset (not included, download from Kaggle)
│
└── plots/                      # Generated visualization directory
    ├── movies_vs_tvshows.png  # Movies vs TV Shows comparison
    └── top_10_countries.png   # Top 10 countries by production
```

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pandas  | 2.1.3   | Data manipulation and analysis |
| matplotlib | 3.8.2 | Visualization library |
| seaborn | 0.13.0  | Statistical data visualization |

---

## Code Structure

### Main Functions

1. **`check_file_exists(filename)`**
   - Validates that the Netflix dataset exists before processing

2. **`create_plots_directory()`**
   - Ensures the `plots/` directory exists; creates it if necessary

3. **`load_data(filename)`**
   - Loads the CSV file and returns a pandas DataFrame

4. **`clean_data(df)`**
   - Removes duplicates
   - Reports missing values
   - Returns cleaned DataFrame

5. **`calculate_movie_tv_ratio(df)`**
   - Computes and prints Movie/TV Show distribution

6. **`find_top_producing_country(df)`**
   - Identifies top countries by content volume
   - Handles multi-country titles

7. **`find_most_common_year(df)`**
   - Determines and displays release year trends

8. **`plot_movie_tv_distribution(df, plots_dir)`**
   - Creates bar chart of content type distribution

9. **`plot_top_countries(df, plots_dir, country_counts)`**
   - Creates bar chart of top 10 producing countries

---

## Technical Details

### Data Types
- Columns are read with pandas' default type inference
- Release year is treated as numeric
- Country and type fields are string-based

### Error Handling
- The script checks for file existence before processing
- Missing values are handled gracefully with explicit reporting
- Directory creation is handled with existence checks

### Performance
- Efficient pandas operations for data manipulation
- Vectorized operations where possible
- Minimal memory footprint even with large datasets

---

## Future Enhancements

Potential improvements for future versions:
- [ ] Add analysis by genre
- [ ] Generate rating/maturity analysis
- [ ] Create interactive dashboards (Plotly/Dash)
- [ ] Add statistical hypothesis testing
- [ ] Export summary report as PDF
- [ ] Implement caching for large datasets
- [ ] Add CLI arguments for custom output paths
- [ ] Create time-series analysis of content releases

---

## Troubleshooting

### Issue: "netflix_titles.csv not found"
**Solution**: Ensure the dataset file is in the same directory as `analysis.py`. Download from [Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows).

### Issue: "ModuleNotFoundError"
**Solution**: Ensure your virtual environment is activated and all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Visualizations not displaying
**Solution**: Charts are saved to the `plots/` directory, not displayed in terminal. Check that the directory exists and has write permissions.

---

## License

This project is provided as-is for educational and analytical purposes.

---

## Contact & Support

For questions or issues, please refer to the Kaggle dataset documentation or modify the script parameters as needed for your specific use case.

**Dataset Source**: [Kaggle - Netflix Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows)

---

*Last Updated: December 2025*
