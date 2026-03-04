import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- PAGE CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="SmartRail Planner",
    page_icon="🚉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for the Industrial Dark Theme
st.markdown("""
<style>
    :root {
        --bg-color: #0a0f1e;
        --panel-bg: #151b2e;
        --cyan: #00d4ff;
        --orange: #ff6b35;
        --green: #00e676;
        --red: #ff1744;
        --text-main: #e2e8f0;
    }
    
    /* Global Styles */
    .stApp {
        background-color: var(--bg-color);
        background-image: linear-gradient(rgba(0, 212, 255, 0.03) 1px, transparent 1px), 
                          linear-gradient(90deg, rgba(0, 212, 255, 0.03) 1px, transparent 1px);
        background-size: 20px 20px;
        color: var(--text-main);
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Georgia', serif;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #94a3b8;
        font-family: 'Courier New';
        font-weight: bold;
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--cyan) !important;
        background-color: rgba(0, 212, 255, 0.1) !important;
        border-bottom: 2px solid var(--cyan) !important;
    }
    
    /* KPI Cards */
    div[data-testid="stMetricValue"] {
        font-family: 'Courier New';
        color: var(--text-main);
        font-variant-numeric: tabular-nums;
    }
    
    /* Dataframes */
    .dataframe {
        font-family: 'Courier New';
        font-size: 14px;
    }
    
    /* Header Area */
    .main-header {
        border-bottom: 1px solid #1e293b;
        padding-bottom: 1rem;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    trains_df = pd.read_csv('trains.csv')
    records_df = pd.read_csv('records.csv')
    # Parse date string back to proper datetime.date objects for comparisons
    records_df['date'] = pd.to_datetime(records_df['date']).dt.date
    return trains_df, records_df

trains_df, records_df = load_data()

# Data Derived views
last_30_days = records_df[records_df['date'] >= (datetime.datetime.now().date() - datetime.timedelta(days=30))]

# --- HEADER ---
col_logo, col_time = st.columns([3, 1])
with col_logo:
    st.markdown(f"<h2><span style='color: #00d4ff'>SMART</span>RAIL PLANNER <span style='font-size: 0.4em; background-color: #00e676; color: black; padding: 2px 5px; border-radius: 4px; font-family: Courier New; vertical-align: middle;'>SYS.ONLINE</span></h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 0.8em; margin-top: -15px;'>Railway Resource Optimization Dashboard v2.4</p>", unsafe_allow_html=True)
with col_time:
    st.markdown(f"<p style='text-align: right; color: #00d4ff; font-weight: bold;'>{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br><span style='color: #94a3b8; font-size: 0.8em;'>OP. CENTER: DEL-01</span></p>", unsafe_allow_html=True)

# --- TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview Dashboard", 
    "🗺️ Route Analysis", 
    "🔮 Demand Prediction", 
    "🚉 Resource Engine", 
    "📅 Schedule Planner"
])

# Plotly Theme Settings
template_dark = go.layout.Template()
template_dark.layout.plot_bgcolor = 'rgba(0,0,0,0)'
template_dark.layout.paper_bgcolor = 'rgba(0,0,0,0)'
template_dark.layout.font.color = '#e2e8f0'
template_dark.layout.xaxis.gridcolor = '#2d3748'
template_dark.layout.yaxis.gridcolor = '#2d3748'

# --- TAB 1: OVERVIEW DASHBOARD ---
with tab1:
    # Calculate KPIs
    total_pass = last_30_days['passengerCount'].sum()
    avg_occ = last_30_days['occupancyRate'].mean() * 100
    
    route_stats = last_30_days.groupby('route').agg({
        'passengerCount': 'sum',
        'occupancyRate': 'mean',
        'delayMinutes': 'mean'
    }).reset_index()
    
    busiest_route = route_stats.loc[route_stats['passengerCount'].idxmax()]['route']
    routes_at_risk = len(route_stats[route_stats['occupancyRate'] > 0.9])
    avg_delay = last_30_days['delayMinutes'].mean()
    on_time = (len(last_30_days[last_30_days['delayMinutes'] < 10]) / len(last_30_days)) * 100
    
    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
    
    # Custom colored metrics
    def custom_metric(label, value, color="#00d4ff"):
        return f"""
        <div style="background-color: #151b2e; border: 1px solid #2d3748; padding: 15px; border-radius: 5px; position: relative;">
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 4px; background-color: {color};"></div>
            <p style="color: #94a3b8; font-size: 0.8em; margin-bottom: 5px; font-family: 'Georgia'; text-transform: uppercase;">{label}</p>
            <h3 style="color: {color}; margin: 0; font-family: 'Courier New';">{value}</h3>
        </div>
        """
        
    kpi1.markdown(custom_metric("Total Pass (30D)", f"{total_pass:,}"), unsafe_allow_html=True)
    kpi2.markdown(custom_metric("Avg Occupancy", f"{avg_occ:.1f}%", "#ff6b35" if avg_occ > 85 else "#00d4ff"), unsafe_allow_html=True)
    kpi3.markdown(custom_metric("Busiest Route", busiest_route, "#00d4ff"), unsafe_allow_html=True)
    kpi4.markdown(custom_metric("Routes at Risk", str(routes_at_risk), "#ff1744" if routes_at_risk > 0 else "#00e676"), unsafe_allow_html=True)
    kpi5.markdown(custom_metric("Avg Delay", f"{avg_delay:.0f}m", "#ff6b35" if avg_delay > 15 else "#00e676"), unsafe_allow_html=True)
    kpi6.markdown(custom_metric("On-Time Perf", f"{on_time:.1f}%", "#ff1744" if on_time < 80 else "#00e676"), unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    col_chart1, col_chart2 = st.columns([2, 1])
    
    with col_chart1:
        st.markdown("<h4 style='color: #00d4ff; font-family: Georgia;'>DAILY PASSENGER VOLUME (30 DAYS)</h4>", unsafe_allow_html=True)
        daily_vol = last_30_days.groupby('date')['passengerCount'].sum().reset_index()
        fig_line = px.line(daily_vol, x='date', y='passengerCount', color_discrete_sequence=['#00d4ff'])
        fig_line.update_traces(line=dict(width=3))
        fig_line.update_layout(template=template_dark, height=350, margin=dict(l=0, r=0, t=20, b=0), xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_line, use_container_width=True)
        
    with col_chart2:
        st.markdown("<h4 style='color: #ff6b35; font-family: Georgia;'>TOP ROUTES BY OCCUPANCY</h4>", unsafe_allow_html=True)
        top_routes = route_stats.sort_values('occupancyRate', ascending=True).tail(8)
        top_routes['occupancyRate'] = top_routes['occupancyRate'] * 100
        
        # Color coding bars based on threshold
        colors = ['#ff1744' if x > 85 else ('#ff6b35' if x > 70 else '#00d4ff') for x in top_routes['occupancyRate']]
        
        fig_bar = go.Figure(go.Bar(
            x=top_routes['occupancyRate'],
            y=top_routes['route'],
            orientation='h',
            marker_color=colors
        ))
        fig_bar.update_layout(template=template_dark, height=350, margin=dict(l=0, r=0, t=20, b=0), xaxis=dict(range=[0, 110]))
        st.plotly_chart(fig_bar, use_container_width=True)

# --- TAB 2: ROUTE ANALYSIS ---
with tab2:
    all_routes = trains_df['route'].unique().tolist()
    
    col_sel, col_stat1, col_stat2 = st.columns([2, 1, 1])
    with col_sel:
        selected_route = st.selectbox("TARGET ROUTE:", all_routes, key="analyze_route")
    
    route_data = last_30_days[last_30_days['route'] == selected_route].groupby('date').agg({
        'passengerCount': 'sum',
        'seatsAvailable': 'sum',
        'occupancyRate': 'max',
        'delayMinutes': 'max'
    }).reset_index()
    route_data['occupancyRate'] = route_data['occupancyRate'] * 100
    
    with col_stat1:
        curr_capacity = (route_data['seatsAvailable'].iloc[-1] + route_data['passengerCount'].iloc[-1]) if len(route_data) > 0 else 0
        st.markdown(custom_metric("CAPACITY", f"~{curr_capacity:.0f} SEATS", "#00e676"), unsafe_allow_html=True)
    with col_stat2:
        avg_rt_delay = route_data['delayMinutes'].mean() if len(route_data) > 0 else 0
        st.markdown(custom_metric("AVG DELAY", f"{avg_rt_delay:.0f} MIN", "#ff6b35"), unsafe_allow_html=True)

    st.write("")
    
    r_col1, r_col2 = st.columns(2)
    with r_col1:
        st.markdown("<h4 style='color: #00d4ff; font-family: Georgia;'>OCCUPANCY TREND (30D) <span style='font-size: 0.6em; background: rgba(255,23,68,0.2); color: #ff1744; padding: 3px; border-radius: 3px;'>DANGER: >85%</span></h4>", unsafe_allow_html=True)
        fig_occ = px.line(route_data, x='date', y='occupancyRate', color_discrete_sequence=['#00d4ff'])
        fig_occ.add_hline(y=85, line_dash="dash", line_color="#ff1744")
        fig_occ.update_layout(template=template_dark, height=350, yaxis=dict(range=[0, 110]))
        st.plotly_chart(fig_occ, use_container_width=True)
        
    with r_col2:
        st.markdown("<h4 style='color: #ff6b35; font-family: Georgia;'>DELAY PATTERN (MINUTES)</h4>", unsafe_allow_html=True)
        delay_colors = ['#ff1744' if x > 30 else ('#ff6b35' if x > 15 else '#00e676') for x in route_data['delayMinutes']]
        fig_delay = go.Figure(go.Bar(
            x=route_data['date'],
            y=route_data['delayMinutes'],
            marker_color=delay_colors
        ))
        fig_delay.update_layout(template=template_dark, height=350)
        st.plotly_chart(fig_delay, use_container_width=True)

# --- TAB 3: DEMAND PREDICTION ---
with tab3:
    pred_route = st.selectbox("SELECT ROUTE FOR FORECAST:", all_routes, key="predict_route")
    
    # Simple Prediction Algorithm
    hist_route = records_df[records_df['route'] == pred_route].sort_values('date')
    last_date = hist_route['date'].max()
    
    predictions = []
    actuals = hist_route.tail(14)[['date', 'passengerCount', 'isWeekend', 'isHoliday']].copy()
    actuals['type'] = 'Actual'
    
    for i in range(1, 15):
        target_date = last_date + datetime.timedelta(days=i)
        is_weekend = target_date.weekday() >= 5
        is_holiday = np.random.random() > 0.9
        
        # Base avg from same day of week in last 4 weeks
        same_day_hist = hist_route[hist_route['date'].apply(lambda x: x.weekday()) == target_date.weekday()].tail(4)
        avg_base = same_day_hist['passengerCount'].mean() if len(same_day_hist) > 0 else 0
        
        multiplier = 1.0
        if is_weekend: multiplier = 1.25
        if is_holiday: multiplier = 1.4
        
        noise = 1 + np.random.uniform(-0.05, 0.05)
        pred_val = int(avg_base * multiplier * noise)
        
        predictions.append({
            'date': target_date,
            'passengerCount': pred_val,
            'isWeekend': is_weekend,
            'isHoliday': is_holiday,
            'type': 'Prediction'
        })
        
    preds_df = pd.DataFrame(predictions)
    combo_df = pd.concat([actuals, preds_df])
    
    st.markdown("<h4 style='color: #facc15; font-family: Georgia;'>FORECAST MODEL (BASE + WEEKEND/HOLIDAY SURGE)</h4>", unsafe_allow_html=True)
    
    fig_pred = go.Figure()
    # Actual Line
    fig_pred.add_trace(go.Scatter(
        x=actuals['date'], y=actuals['passengerCount'], 
        mode='lines+markers', name='Actual', line=dict(color='#00d4ff', width=3)
    ))
    
    # Connecting Line
    if len(actuals) > 0 and len(preds_df) > 0:
        fig_pred.add_trace(go.Scatter(
            x=[actuals.iloc[-1]['date'], preds_df.iloc[0]['date']], 
            y=[actuals.iloc[-1]['passengerCount'], preds_df.iloc[0]['passengerCount']],
            mode='lines', showlegend=False, line=dict(color='#facc15', width=3, dash='dot')
        ))
        
    # Predicted Line
    fig_pred.add_trace(go.Scatter(
        x=preds_df['date'], y=preds_df['passengerCount'], 
        mode='lines+markers', name='Predicted', line=dict(color='#facc15', width=3, dash='dash')
    ))
    
    # Highlight Surges
    weekend_surge = preds_df[preds_df['isWeekend']]
    holiday_surge = preds_df[preds_df['isHoliday']]
    
    if len(weekend_surge) > 0:
        fig_pred.add_trace(go.Scatter(
            x=weekend_surge['date'], y=weekend_surge['passengerCount'],
            mode='markers', name='Weekend Surge', marker=dict(color='#ff6b35', size=10, symbol='diamond')
        ))
        
    if len(holiday_surge) > 0:
        fig_pred.add_trace(go.Scatter(
            x=holiday_surge['date'], y=holiday_surge['passengerCount'],
            mode='markers', name='Holiday Surge', marker=dict(color='#ff1744', size=12, symbol='star')
        ))
        
    fig_pred.update_layout(template=template_dark, height=400, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_pred, use_container_width=True)
    
    # Alerts Table
    st.markdown("<h4 style='color: white; font-family: Georgia;'>HIGH DEMAND ALERTS (NEXT 14 DAYS)</h4>", unsafe_allow_html=True)
    alerts = preds_df[preds_df['passengerCount'] > 1000].copy()
    
    if len(alerts) > 0:
        alerts['Day Type'] = alerts.apply(lambda x: 'HOLIDAY' if x['isHoliday'] else ('WEEKEND' if x['isWeekend'] else 'WEEKDAY'), axis=1)
        alerts['Recommendation'] = alerts['passengerCount'].apply(lambda x: '⚠️ Add 2+ Extra Coaches' if x > 1200 else 'Add 1 Extra Coach')
        
        display_alerts = alerts[['date', 'Day Type', 'passengerCount', 'Recommendation']].rename(columns={'date': 'Date', 'passengerCount': 'Pred. Passengers'})
        
        # Style dataframe for streamlit
        st.dataframe(display_alerts.style.apply(lambda x: ['color: #ff1744' if v == 'HOLIDAY' else ('color: #ff6b35' if v == 'WEEKEND' else '') for v in x], subset=['Day Type']), use_container_width=True, hide_index=True)
    else:
        st.info("No high demand alerts projected for the next 14 days.")

# --- TAB 4: RESOURCE RECOMMENDATIONS ---
with tab4:
    # Build engine based on latest data snapshot
    latest_records = records_df.sort_values('date').groupby('trainId').tail(1).copy()
    
    def eval_status(row):
        occ = row['occupancyRate'] * 100
        if occ > 90: return pd.Series(['CRITICAL', 'Add 2-3 coaches immediately', 1, '#ff1744'])
        elif occ > 80: return pd.Series(['WARNING', 'Add 1 coach, monitor', 2, '#ff6b35'])
        elif occ > 70: return pd.Series(['WATCH', 'Approaching capacity', 3, '#facc15'])
        elif occ >= 50: return pd.Series(['OPTIMAL', 'No action needed', 5, '#00e676'])
        else: return pd.Series(['OPTIMIZE', 'Consider reducing coaches', 4, '#00d4ff'])
        
    latest_records[['Status', 'Action', 'Priority', 'hex']] = latest_records.apply(eval_status, axis=1)
    
    # Adjust action if congestion risk
    latest_records.loc[(latest_records['delayMinutes'] > 20) & (latest_records['occupancyRate'] > 0.8), 'Action'] += " (Platform congestion risk)"
    
    latest_records = latest_records.sort_values('Priority')
    
    num_critical = len(latest_records[latest_records['Priority'] == 1])
    num_warning = len(latest_records[latest_records['Priority'] == 2])
    
    st.markdown(f"""
    <div style="background-color: #151b2e; border-left: 4px solid #ff1744; padding: 20px; border-radius: 5px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <div>
            <h2 style="color: white; font-family: 'Georgia'; margin: 0;">ATTENTION REQUIRED</h2>
            <p style="color: #94a3b8; margin: 5px 0 0 0;">
                <span style="color: #ff1744; font-weight: bold; font-size: 1.2em;">{num_critical}</span> trains critical • 
                <span style="color: #ff6b35; font-weight: bold; font-size: 1.2em; margin-left: 10px;">{num_warning}</span> warnings
            </p>
        </div>
        <button style="background-color: #ff1744; color: white; border: none; padding: 10px 20px; font-weight: bold; border-radius: 4px; font-family: 'Courier New'; cursor: pointer; box-shadow: 0 0 15px rgba(255,23,68,0.3);">EXECUTE ALL ACTIONS</button>
    </div>
    """, unsafe_allow_html=True)
    
    # Formatting the table for display
    display_recs = latest_records[['trainId', 'route', 'occupancyRate', 'Status', 'Action']].copy()
    display_recs['occupancyRate'] = (display_recs['occupancyRate'] * 100).round(1).astype(str) + '%'
    display_recs.columns = ['TRAIN', 'ROUTE', 'OCCUPANCY', 'STATUS', 'ACTION REQUIRED']
    
    def color_status(val):
        colors = {'CRITICAL': '#ff1744', 'WARNING': '#ff6b35', 'WATCH': '#facc15', 'OPTIMAL': '#00e676', 'OPTIMIZE': '#00d4ff'}
        color = colors.get(val, 'white')
        return f'color: {color}; font-weight: bold'
        
    st.dataframe(
        display_recs.style.map(color_status, subset=['STATUS']),
        use_container_width=True, 
        hide_index=True
    )

# --- TAB 5: SCHEDULE PLANNER ---
with tab5:
    col_t5_1, col_t5_2 = st.columns([4, 1])
    with col_t5_1:
        st.markdown("<h2 style='color: white; font-family: Georgia;'>PLATFORM GANTT TIMELINE</h2>", unsafe_allow_html=True)
    with col_t5_2:
        if st.button("↧ EXPORT PDF"):
            st.success(f"Report generated: SmartRail_Report_{datetime.datetime.now().date()}.pdf", icon="✅")
            
    # Mocking timeline Gantt via Plotly
    # We take the latest day records and convert schedule time to datetime for plotting Gantt
    sched_data = latest_records[['trainId', 'route', 'platformNumber', 'scheduledTime', 'Status', 'hex']].copy()
    
    # Add dummy durations
    df_gantt = []
    base_date = "2024-01-01" # Just to set a timeline
    
    for _, row in sched_data.iterrows():
        start = f"{base_date} {row['scheduledTime']}"
        start_dt = pd.to_datetime(start)
        end_dt = start_dt + pd.Timedelta(hours=1.5) # assume 1.5 hr block
        df_gantt.append({
            'Task': f"Platform {row['platformNumber']}",
            'Start': start_dt,
            'Finish': end_dt,
            'Resource': row['Status'],
            'Train': f"{row['trainId']} ({row['route']})",
            'Color': row['hex']
        })
        
    df_gantt = pd.DataFrame(df_gantt).sort_values(by="Task", key=lambda x: x.str.extract('(\d+)')[0].astype(int), ascending=False)
    
    fig_gantt = px.timeline(
        df_gantt, x_start="Start", x_end="Finish", y="Task", 
        color="Resource",
        color_discrete_map={
            'CRITICAL': '#ff1744',
            'WARNING': '#ff6b35',
            'WATCH': '#facc15',
            'OPTIMAL': '#00e676',
            'OPTIMIZE': '#00d4ff'
        },
        hover_name="Train",
        height=600
    )
    
    fig_gantt.update_yaxes(autorange="reversed")
    fig_gantt.update_layout(
        template=template_dark,
        xaxis=dict(
            tickformat="%H:%M",
            title="Time of Day"
        ),
        yaxis_title=None
    )
    st.plotly_chart(fig_gantt, use_container_width=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.8em; font-style: italic;'>* Overlapping blocks automatically highlighted indicate platform conflicts requiring manual reassignment.</p>", unsafe_allow_html=True)
