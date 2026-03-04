# SmartRail Planner: Railway Resource Optimization Dashboard

SmartRail Planner is a full-stack dashboard designed to optimize railway operations. It provides operators with comprehensive insights into passenger demand, route occupancy, projected delays, and actionable resource recommendations.

This application is built as a single-page interactive dashboard featuring an industrial dark aesthetic. It helps allocate coaches correctly, spot high-demand days (holidays/weekends), and prevent platform congestion using simple yet effective predictive algorithms.

## Features

- **📊 Overview Dashboard:** System-wide KPIs encompassing total passengers, average occupancy, routes at risk, and delay statistics across a 30-day trailing window.
- **🗺️ Route Analysis:** Deep-dive views into specific train routes detailing historical occupancy metrics and delay patterns.
- **🔮 Demand Prediction:** A 14-day projection using a moving-average algorithm combined with weekend/holiday multiplier surges.
- **🚉 Resource Engine:** Actionable intelligence classifying individual trains (Optimal, Watch, Warning, Critical) based on their occupancy threshold, and suggesting coach additions/reductions.
- **📅 Schedule Planner:** A visual Gantt timeline tracking platform utilizations to highlight and mitigate conflicts.

## Tech Stack

The interactive application was built utilizing the following core technologies:

- **Python (3.8+)**: Core programming language.
- **Streamlit**: Web framework powering the interactive UI/dashboard.
- **Pandas DataFrames**: Essential structures for data loading, filtering, and aggregation.
- **Plotly Express / Graph Objects**: Rendering the rich, interactive composed visualizations and Gantt charts.
- **NumPy**: Facilitates the synthetic data generation and predictive noise factors.

*(Note: Although this repository initially housed a React/Recharts prototype, the primary deployment is now centralized around Python and Streamlit.)*

## Dataset Description

The application relies completely on synthetic data generation engineered to mirror realistic railway patterns. The dataset is separated into two offline CSV files:

### `trains.csv`
Contains the static operational details of the railway fleet.
- **Fields:** `trainId`, `route` (Source→Destination), `source`, `destination`, `coaches` (Current coach length), `capacityPerCoach`, `totalCapacity` (Calculated), `platformNumber`, and `baseDemand`. 
- **Scale:** 20 trains operating across 8 unique national routes.

### `records.csv`
Contains trailing 90-day time-series activity.
- **Fields:** `date`, `trainId`, `scheduledTime`, `passengerCount`, `seatsAvailable`, `occupancyRate`, `delayMinutes`, `isWeekend`, `isHoliday`, `season`.
- **Modifications:** Introduces randomized "noise" combined with logical operational modifiers—weekends exhibit 25% surges, synthetic holidays see 40% surges, and monsoons negatively impact passenger counts while increasing delays.

## Algorithm Explanation

The application incorporates a rudimentary forecasting engine in the **Demand Prediction** tab to simulate resource needs for the upcoming 14 days. 

The algorithm functions systematically:
1. **Historical Baseline:** For any prospective date, the algorithm retrieves the same day-of-the-week historical average over the last 4 rolling weeks for that specific route.
2. **Boolean Multipliers:** 
   - If the forecasted date is a weekend, the base is multiplied by `1.25x`. 
   - If a synthetic holiday is triggered, the base is multiplied by `1.40x`.
3. **Realistic Noise Injection:** To prevent flat artificial lines, a variance factor (`+/- 5%`) is applied via NumPy randomized generators to finalize the prediction value.
4. **Logic Trigger:** If the projected output exceeds 90% of the train's maximum capacity, a system alert is triggered advising the operator to add `1` or `2+` extra coaches.

## Setup & Installation

To run this application locally, you will need `python` and `pip` installed.

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/smartrail-planner.git
cd smartrail-planner
```

### 2. Install Dependencies
```bash
pip install streamlit pandas numpy plotly
```

*(If you are setting up the legacy react interface instead: `npm install`)*

### 3. Generate the Dataset
If the CSVs (`trains.csv` and `records.csv`) are missing or you wish to regenerate new data seeds:
```bash
python generate_data.py
```

### 4. Run the Dashboard
Deploy the dashboard locally using Streamlit's CLI:
```bash
streamlit run app.py
```
*(If you are running the legacy react interface instead: `npm start`)*

The platform will automatically launch in your default web browser at `http://localhost:8502/` (port may vary based on availability).
