
# 🏙️ Smart City Finder

An interactive visualization dashboard that helps **individuals** and **businesses**
find the most suitable U.S. city using:

- Demographics (population, age, income, density)
- Crime & safety (violent crime rate by state)
- Income & affordability (median household income vs average income)

## 📁 Project structure

```text
SmartCityFinder/
├── app.py                 # Streamlit dashboard
├── data_preprocess.py     # Script to merge & prepare datasets
├── requirements.txt       # Python dependencies
└── data/
    ├── uscities_2020.csv
    ├── violent_crime_2020.csv
    ├── income_2020.csv
    └── merged_smartcity.csv
```

## 🚀 How to run locally

```bash
pip install -r requirements.txt
python data_preprocess.py   # optional, already run once
streamlit run app.py
```

Then open the URL shown in the terminal (usually http://localhost:8501).

## 🎯 What you can do

- Adjust weights for **Safety**, **Income**, and **Affordability**
- Explore cities on a **map** colored by violent crime rate
- See the relationship between **income and crime**
- Compare cities across multiple dimensions using **parallel coordinates**
- View a **Top N recommended cities** table based on your preferences
