# Netflix Data Analysis

A Streamlit dashboard for the four visualizations in `Untitled.py`, styled with a Netflix-inspired red, black, and white palette.

## Run locally

```powershell
python -m pip install -r requirements.txt
streamlit run app.py
```

The dashboard looks for `netflix.csv` beside the app or in the user's home directory. You can also upload a CSV in the app. The required columns are `Region`, `Monthly_Revenue`, `Subscription_Plan`, `Rating`, and `Category`.

## Charts

- Region-wise monthly revenue
- Subscription plan-wise rating totals
- Rating distribution
- Category-wise monthly revenue

The customer-level dataset is not included in this repository. Upload your own CSV to view the charts.
