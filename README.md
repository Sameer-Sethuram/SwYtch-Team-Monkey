# 📊 US Labor Market Forecasting for Career Switching

**AI Studio Challenge Project Swytch (Project 1)**

---

## 👥 Team Members

| Name                   | GitHub Handle                                        | Contribution                                  |
| ---------------------- | ---------------------------------------------------- | --------------------------------------------- |
| Abdullah Khajamohideen | [@Abdullah]                                          | Research, Data preprocessing, EDA, Modeling   |
| Adelitta Stanton       | [@TheAdelitta](https://github.com/TheAdelitta)       | Project coordination, insights synthesis      |
| Ibrahima Wann          | [@Ibrahima]                                          | Research, Data preprocessing, EDA             |
| Raul Rojas             | [@RIROJASS](https://github.com/RIROJASS)             | Research, Data preprocessing, EDA, Modeling   |
| Rohitha Matwada        | [@RohithaM27](https://github.com/RohithaM27)         | Research, Data preprocessing, EDA, Modeling   |
| Sameer Sethuram        | [@Sameer-Sethuram](https://github.com/Sameer-Sethuram) | Research, Data preprocessing, EDA, Modeling |


---

## 🎯 Project Highlights

* Built a labor market forecasting system to identify **growing and declining U.S. careers**
* Applied **time series forecasting models** including Auto ARIMA, XGBoost, and Prophet
* Evaluated trends across **multiple public labor market datasets** including JOLTS, Indeed, ADP, and LinkedIn
* Identified **industries with strong growth potential** and sectors likely to stagnate or decline
* Delivered insights designed to directly support **Swytch’s AI-powered career guidance platform**

---

## 🏗️ Project Overview

This project was completed as part of the **Break Through Tech AI Studio Program** in collaboration with **Swytch**, an AI-driven career transition platform.

Swytch’s mission is to help individuals pivot into high-impact, sustainable careers by providing data-backed guidance. Our team focused on **Project 1: U.S. Labor Market Analysis and Career Forecasting**.

### Objective

Use publicly available labor market data and machine learning to forecast employment trends across industries, helping job seekers understand which career paths are expanding or contracting.

### Why This Matters

* Over **50 percent of Americans consider switching careers**
* Job markets change faster than traditional career tools can track
* Workers, employers, and educators lack clear signals on future demand
* Accurate forecasting enables better career planning and workforce alignment

---

## 📊 Data Exploration

### Datasets Used

* **JOLTS (Job Openings and Labor Turnover Survey)**  
  Source Bureau of Labor Statistics  
  Highly granular industry level time series data

* **Indeed Hiring Lab Data**  
  Daily and monthly job posting trends by sector

* **ADP National Employment Report**  
  Private sector employment trends across major industries

* **LinkedIn Workforce Reports**  
  Hiring rate trends by industry (ultimately not used due to limitations)

### Preprocessing and EDA Highlights

* Converted thousands of coded BLS columns into readable industry features
* Addressed **COVID-19 anomalies** using linear interpolation
* Severe multicollinearity detected (over 80 percent of features correlated above 0.7)
* Applied **VIF filtering** to reduce noise and improve model stability
* Engineered **lag features** to capture delayed labor market effects
* Identified independent sector behavior versus market-following sectors

**Key takeaway**  
JOLTS and Indeed datasets produced the most reliable forecasting signals

---

## 🧠 Model Development

### Models Used

* **Auto ARIMA**
* **XGBoost Regressor**
* **Prophet**

### Approach

* Time series forecasting by industry
* Feature selection driven by VIF filtering and Spearman correlation
* Trained models across multiple lag windows
* Evaluated performance using MAE, RMSE, and MAPE
* Generated **272 Auto ARIMA models** across industries and lag periods

### Training Setup

* Monthly and daily data aggregated where appropriate
* Rolling forecasts up to 12 months
* Baseline comparisons across models

---

## 📈 Results & Key Findings

### Best Performing Model

* **Auto ARIMA** consistently achieved the lowest MAE for JOLTS data
* MAE range for ARIMA: **0.21 to 1.22**
* XGBoost and Prophet showed higher error and overfitting tendencies in long horizons

### Industry Insights

**High Growth Potential**

* Construction
* Professional and Business Services
* Education and Health Services
* Trade Transportation and Utilities
* Financial Activities

**Low or Declining Growth**

* Leisure and Hospitality
* Natural Resources and Mining
* Information Services
* Other Services

### Key Observations

* Models struggled during regime shifts such as post-2024 slowdowns
* Aggregated industry signals performed better than ultra-granular sector data
* Independent movers such as Therapy and Healthcare roles showed unique dynamics

---

## 🚀 Next Steps

* Incorporate **PCA-based dimensionality reduction** for sector modeling
* Improve handling of economic regime changes
* Explore **Prophet for longer horizon forecasts**
* Add trend direction features instead of raw year indicators
* Integrate forecasts directly into Swytch’s product workflows

---

## 📄 References

* Bureau of Labor Statistics JOLTS  
  [https://www.bls.gov/jlt/](https://www.bls.gov/jlt/)

* Bureau of Labor Statistics CPS  
  [https://www.bls.gov/cps/tables.htm](https://www.bls.gov/cps/tables.htm)

* Indeed Hiring Lab Data  
  [https://data.indeed.com/#/postings](https://data.indeed.com/#/postings)

* ADP National Employment Report  
  [https://www.adpemploymentreport.com/](https://www.adpemploymentreport.com/)

---

## 🙏 Acknowledgements

Special thanks to our Swytch advisors and supporters

* **Jim Thompson**, Challenge Advisor
* **Tim Liu**, Challenge Advisor
* **Beth**, for project coordination and guidance
* Break Through Tech AI Studio mentors and TAs
