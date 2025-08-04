
# 🌾 AgriData Explorer: Indian Agricultural Insights Dashboard

## 📌 Overview

**AgriData Explorer** is a comprehensive data visualization and analysis project built using **Python**, **SQL**, **Streamlit**, and **Power BI**. It provides detailed insights into India's crop production trends, yields, and agricultural practices at the district and state levels.

This project helps:
- 👨‍🌾 **Farmers** decide optimal crops to grow,
- 🏛️ **Policymakers** identify low productivity zones, and
- 🧪 **Researchers** analyze agricultural patterns and innovations.

---

## 🛠️ Tech Stack

| Component       | Tools Used                                     |
|----------------|--------------------------------------------------|
| Language        | Python, SQL                                     |
| Dashboard       | Streamlit                                       |
| Data Storage    | PostgreSQL                                      |
| Visualization   | Plotly, Matplotlib, Seaborn, Power BI           |
| Data Cleaning   | Pandas, NumPy                                   |

---

## 📁 Project Structure

```
agri-data-explorer/
│
├── streamlit_app/                 # Main dashboard app.py
├── eda_scripts/                   # Jupyter or VS Code preprocessing
├── sql/                           # Analytical SQL queries
├── data/                          # Cleaned and raw CSV files
├── powerbi/                       # Power BI .pbix files
├── README.md                      # Project documentation
└── requirements.txt               # Python dependencies
```

---

## 📊 Streamlit Dashboard Features

### ✅ Views Available:
- **Histograms:** Crop-wise area, production, and yield distribution
- **Heatmap:** Correlation between crop productions
- **SQL Insights:** 10 key agricultural SQL-based queries


### 🧮 Filters:
- **Year Selection** (dropdown)
- **State Multiselect**

### 💻 To Run Locally:

```bash
pip install -r requirements.txt
streamlit run streamlit_app/app.py
```

Ensure your PostgreSQL server is running and `agriculture_data` table is created.

---

## 🔍 Data Source

- **ICRISAT – District Level Agricultural Data**
- Fields: year, state/district, area, production, yield
- Crops: Rice, Wheat, Maize, Oilseeds, Sorghum (Kharif/Rabi), Sunflower, Sugarcane, Soybean, etc.

---

## 🔢 SQL Insights Available

1. 📆 Year-wise Rice Production for Top 3 States  
2. 📈 Wheat Yield Growth in Top 5 Districts (Last 5 Years)  
3. 🌻 States with Highest Oilseed Production Growth  
4. 🔗 Correlation Between Area and Production (District-level)  
5. 🌿 Cotton Production Trends in Top 5 States  
6. 🥜 Top 5 Groundnut Districts in 2017  
7. 🌽 Annual Average Maize Yield (All States)  
8. 🗺️ Oilseed Area by State  
9. 🏅 Top 5 Districts with Highest Rice Yield  
10. 🔄 10-Year Wheat vs Rice Production (Top 5 States)

---

## 📉 EDA Performed in VS Code

- Cleaned missing and invalid values (e.g. -1 → NaN)
- Standardized column names (lowercase, underscores)
- Generated over 10+ crop-wise histograms for:
  - Area, Production, Yield
- Created heatmap of production correlations
- Exported cleaned CSV for PostgreSQL import

---

## 📈 Power BI Integration

Power BI visualizations include:
- India State Map (Filled Map) with crop production
- Line & bar charts for yearly trends
- Pie charts and KPI cards
- Slicers for year, crop, and state

---

## 🧪 Evaluation Metrics

| Metric                      | Description                               |
|----------------------------|-------------------------------------------|
| 📊 Visualization Accuracy  | Clean and correct visuals                 |
| ⚡ Dashboard Speed          | Efficient rendering and loading time      |
| 🎯 Query Effectiveness     | Meaningful agricultural insights          |
| 👥 User Interactivity       | Intuitive filters, map, and SQL results   |

---

## 📬 How to Use

1. Set up PostgreSQL:
   - Create a DB named `agriculture_data`
   - Upload `cleaned_data.csv` to `agriculture_data` table using SQLAlchemy or pgAdmin

2. Run Streamlit:
  
   streamlit run streamlit_app/app.py
---

## 🙌 Acknowledgements

- [ICRISAT](https://www.icrisat.org/) for the dataset  
- Mentors and trainers who guided the project  
- All contributors to open-source geoJSON files used for India state maps  

---


