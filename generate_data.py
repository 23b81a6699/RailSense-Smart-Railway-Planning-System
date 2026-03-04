import pandas as pd
import numpy as np
import datetime
import os

def generate_synthetic_data():
    np.random.seed(12345)
    
    routes = [
        {"id": "R1", "source": "Mumbai", "destination": "Delhi", "baseCapacity": 1200, "baseDemand": 1000},
        {"id": "R2", "source": "Delhi", "destination": "Chennai", "baseCapacity": 1440, "baseDemand": 1100},
        {"id": "R3", "source": "Bangalore", "destination": "Kolkata", "baseCapacity": 1000, "baseDemand": 850},
        {"id": "R4", "source": "Hyderabad", "destination": "Mumbai", "baseCapacity": 960, "baseDemand": 900},
        {"id": "R5", "source": "Chennai", "destination": "Delhi", "baseCapacity": 1440, "baseDemand": 1150},
        {"id": "R6", "source": "Jaipur", "destination": "Mumbai", "baseCapacity": 800, "baseDemand": 600},
        {"id": "R7", "source": "Pune", "destination": "Delhi", "baseCapacity": 1100, "baseDemand": 950},
        {"id": "R8", "source": "Kolkata", "destination": "Mumbai", "baseCapacity": 1200, "baseDemand": 1050}
    ]
    
    # Generate 20 Trains
    trains = []
    for i in range(20):
        route = routes[i % len(routes)]
        coaches = np.random.randint(6, 19)
        trains.append({
            "trainId": f"TR{str(i+1).zfill(3)}",
            "route": f"{route['source']}→{route['destination']}",
            "source": route['source'],
            "destination": route['destination'],
            "coaches": coaches,
            "capacityPerCoach": 80,
            "totalCapacity": coaches * 80,
            "platformNumber": np.random.randint(1, 13),
            "baseDemand": route['baseDemand']
        })
        
    trains_df = pd.DataFrame(trains)
    
    # Generate Daily Records (Last 90 Days)
    records = []
    today = datetime.datetime.now().date()
    dates = [today - datetime.timedelta(days=x) for x in range(89, -1, -1)]
    
    for _, train in trains_df.iterrows():
        for d in dates:
            is_weekend = d.weekday() >= 5
            is_holiday = np.random.random() > 0.91 # roughly 8 holidays
            
            demand_multiplier = 1.0
            if is_weekend: demand_multiplier += 0.25
            if is_holiday: demand_multiplier += 0.40
            
            season = "winter"
            if 3 <= d.month <= 5: 
                season = "summer"
            elif 6 <= d.month <= 9: 
                season = "monsoon"
                demand_multiplier -= 0.10
                
            base_passenger = train['baseDemand'] * demand_multiplier
            base_passenger += np.random.uniform(-100, 100)
            passenger_count = max(0, int(min(base_passenger, train['totalCapacity'] * 1.5)))
            
            delay = np.random.randint(0, 20)
            if is_weekend or is_holiday: delay += np.random.randint(0, 25)
            if season == "monsoon": delay += np.random.randint(0, 15)
            
            records.append({
                "date": d,
                "trainId": train['trainId'],
                "route": train['route'],
                "source": train['source'],
                "destination": train['destination'],
                "scheduledTime": f"{str(np.random.randint(0, 24)).zfill(2)}:30",
                "passengerCount": passenger_count,
                "totalCapacity": train['totalCapacity'],
                "seatsAvailable": max(0, train['totalCapacity'] - passenger_count),
                "occupancyRate": passenger_count / train['totalCapacity'],
                "coaches": train['coaches'],
                "platformNumber": train['platformNumber'],
                "delayMinutes": delay,
                "isWeekend": is_weekend,
                "isHoliday": is_holiday,
                "season": season
            })
            
    records_df = pd.DataFrame(records)
    
    trains_df.to_csv('trains.csv', index=False)
    records_df.to_csv('records.csv', index=False)
    print("Exported trains.csv and records.csv")

if __name__ == "__main__":
    generate_synthetic_data()
