
import streamlit as st
import pandas as pd
import numpy as np
import requests, math, os, time
from datetime import datetime, timedelta

st.set_page_config(page_title="GhostMiles · Mobility Intelligence", page_icon="👻", layout="wide", initial_sidebar_state="collapsed")

SOURCE_URL = "https://data.cityofchicago.org/resource/94nw-re7c.json"
DATA_SOURCE = "City of Chicago — Taxi Trips - 2026"
DATASET_URL = "https://data.cityofchicago.org/Transportation/Taxi-Trips-2026/94nw-re7c"

# ---------- style ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;scroll-padding-top:76px}
.stApp{background:#f7f7f4;color:#0a0a0a}
.block-container{max-width:1500px;padding:76px 4vw 4rem}
h1,h2,h3{font-family:'Space Grotesk',sans-serif;letter-spacing:-.06em}
.hero{padding:5.5rem 0 3.5rem;border-bottom:1px solid #d8d8d1;display:grid;grid-template-columns:1.3fr .7fr;gap:6vw;align-items:end}
.kicker{font-size:10px;letter-spacing:2px;font-weight:700;color:#6b6c67}
.hero h1{font-size:clamp(60px,8vw,122px);line-height:.84;margin:.7rem 0 1.5rem}
.hero h1 span{color:#b9ed00}
.hero p{font-size:16px;line-height:1.55;color:#686963;max-width:560px}
.hero-stat{border-left:1px solid #d8d8d1;padding-left:4vw}
.hero-stat .label{font-size:10px;letter-spacing:1.7px;font-weight:700}
.hero-stat .num{font:700 clamp(75px,10vw,150px)/.85 'Space Grotesk';letter-spacing:-.09em;margin:.8rem 0}
.hero-stat .unit{color:#686963;font-size:13px}
.live{color:#4da43c;font-size:11px;font-weight:700}
.card{background:#fff;border:1px solid #d8d8d1;border-radius:20px;padding:24px}
.card h3{font-size:20px;margin:.3rem 0 1rem}
.metric{font-family:'Space Grotesk';font-weight:600;font-size:29px;letter-spacing:-.05em}
.metric-label{font-size:9px;color:#70716b;letter-spacing:1.2px;font-weight:700}
.delta{font-size:10px;color:#5d9e42}
.section{padding:5rem 0}
.section-head{display:flex;justify-content:space-between;align-items:end;margin-bottom:2rem}
.section-head h2{font-size:clamp(48px,6vw,86px);line-height:.86;margin:.5rem 0 0}
.section-head p{max-width:360px;color:#6d6e68;font-size:13px;line-height:1.6}
.dark{background:#0a0b0a;color:#f4f4ef;border-radius:28px;padding:5rem 4vw}
.dark .section-head p{color:#999b94}.dark .kicker{color:#999b94}
.insight{background:#caff21;border-radius:16px;padding:17px;color:#0a0a0a}
.insight b{font-family:'Space Grotesk'}
.pill{display:inline-block;border:1px solid #d8d8d1;border-radius:99px;padding:7px 10px;font-size:10px;color:#666}
div[data-testid="stMetric"]{background:#fff;border:1px solid #d8d8d1;padding:15px;border-radius:15px}
.stButton>button{border-radius:99px;border:1px solid #d8d8d1;background:#fff;color:#111;font-weight:600}
.stButton>button:hover{border-color:#111}
div[data-baseweb="select"]>div{border-radius:10px}
#MainMenu,[data-testid="stAppDeployButton"],[data-testid="stSidebar"]{display:none}
header[data-testid="stHeader"]{display:none}
[data-testid="stPopover"]>button{border-radius:999px!important;border:1px solid #111!important;background:#111!important;color:#fff!important;padding:.55rem 1rem!important;font-weight:600!important}
[data-testid="stPopoverBody"]{border:1px solid #d8d8d1!important;border-radius:16px!important;box-shadow:0 16px 40px rgba(0,0,0,.12)!important}
.settings-copy{font-size:12px;color:#6d6e68;margin:.15rem 0 0}
.nav-brand{display:flex;align-items:center;gap:.55rem;font:700 20px/1 'Space Grotesk',sans-serif;letter-spacing:-.06em;padding:.72rem 1.1rem;color:#f7f7f4}.nav-brand span{color:#caff21}.brand-mark{display:inline-grid;place-items:center;width:25px;height:25px;border:2px solid #caff21;border-radius:7px;color:#caff21;font:700 12px/1 'Space Grotesk',sans-serif;letter-spacing:-.12em;transform:skew(-8deg)}.brand-mark b{transform:skew(8deg)}
.nav-links{display:flex;justify-content:center;gap:1.35rem;padding:.86rem .2rem;white-space:nowrap}.nav-links a{color:#c8c9c3!important;text-decoration:none!important;font-size:12px;font-weight:600}.nav-links a:hover{color:#caff21!important}
.nav-rule{display:none}
div[data-testid="stHorizontalBlock"]:has(.nav-brand){position:fixed!important;top:0;left:0;right:0;width:100vw!important;margin:0!important;background:#0b0c0f;border:0;border-radius:0;padding:.12rem max(4vw,calc((100vw - 1500px)/2 + 4vw));align-items:center;box-shadow:0 1px 0 #24262c;z-index:9999}
div[data-testid="stHorizontalBlock"]:has(.nav-brand) [data-testid="stPopover"]>button{background:#caff21!important;border-color:#caff21!important;color:#10110d!important}
@media(max-width:800px){.nav-links{justify-content:flex-start;gap:.8rem;overflow-x:auto}.nav-links a{font-size:11px}.nav-brand{padding-left:.5rem;font-size:16px}}
footer{visibility:hidden}
.source-note{font-size:10px;color:#777;margin-top:1rem}
@media(max-width:800px){.hero{grid-template-columns:1fr}.hero-stat{border-left:0;border-top:1px solid #d8d8d1;padding:2rem 0 0}.section-head{display:block}}
</style>
""", unsafe_allow_html=True)

# ---------- data ----------
FIELDS = [
    "trip_id","taxi_id","trip_start_timestamp","trip_end_timestamp","trip_seconds","trip_miles",
    "pickup_community_area","dropoff_community_area","fare","tips","tolls","extras","trip_total",
    "payment_type","company","pickup_centroid_latitude","pickup_centroid_longitude",
    "dropoff_centroid_latitude","dropoff_centroid_longitude"
]

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_data(limit=25000):
    params = {
        "$limit": limit,
        "$order": "trip_start_timestamp DESC",
        "$select": ",".join(FIELDS),
    }
    r = requests.get(SOURCE_URL, params=params, timeout=40)
    r.raise_for_status()
    raw = r.json()
    df = pd.DataFrame(raw)
    for c in ["trip_start_timestamp","trip_end_timestamp"]:
        df[c] = pd.to_datetime(df[c], errors="coerce")
    for c in ["trip_seconds","trip_miles","fare","tips","tolls","extras","trip_total",
              "pickup_centroid_latitude","pickup_centroid_longitude",
              "dropoff_centroid_latitude","dropoff_centroid_longitude"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["taxi_id","trip_start_timestamp","trip_end_timestamp"])
    return df

def haversine(lat1, lon1, lat2, lon2):
    R=3958.7613
    p1=np.radians(lat1); p2=np.radians(lat2)
    dp=np.radians(lat2-lat1); dl=np.radians(lon2-lon1)
    a=np.sin(dp/2)**2 + np.cos(p1)*np.cos(p2)*np.sin(dl/2)**2
    return 2*R*np.arcsin(np.sqrt(a))

@st.cache_data(ttl=3600, show_spinner=False)
def build_ghost_metrics(df):
    x=df.sort_values(["taxi_id","trip_end_timestamp"]).copy()
    x["next_start"]=x.groupby("taxi_id")["trip_start_timestamp"].shift(-1)
    x["next_pick_lat"]=x.groupby("taxi_id")["pickup_centroid_latitude"].shift(-1)
    x["next_pick_lon"]=x.groupby("taxi_id")["pickup_centroid_longitude"].shift(-1)
    x["next_pick_area"]=x.groupby("taxi_id")["pickup_community_area"].shift(-1)
    x["gap_min"]=(x["next_start"]-x["trip_end_timestamp"]).dt.total_seconds()/60
    # The UI applies the maximum-gap threshold. Here we only require chronological,
    # centroid-complete pairs so the threshold can be inspected transparently.
    valid=(x["gap_min"]>=0)&x["dropoff_centroid_latitude"].notna()&x["next_pick_lat"].notna()
    x["estimated_deadhead_miles"]=np.where(valid,
        haversine(x["dropoff_centroid_latitude"],x["dropoff_centroid_longitude"],
                  x["next_pick_lat"],x["next_pick_lon"]),0)
    x["estimated_idle_min"]=np.where(valid,x["gap_min"],0)
    x["reposition_flag"]=valid & (x["estimated_deadhead_miles"]>=0.25)
    x["hour"]=x["trip_end_timestamp"].dt.hour
    x["day"]=x["trip_end_timestamp"].dt.day_name()
    return x

# A website-style navigation bar keeps exploration and configuration separate.
nav_brand, nav_links, nav_action = st.columns([1.35, 3.3, 1.35], vertical_alignment="center")
with nav_brand:
    st.markdown('<div class="nav-brand"><span class="brand-mark"><b>GM</b></span>GHOST<span>MILES</span></div>', unsafe_allow_html=True)
with nav_links:
    st.markdown('<nav class="nav-links"><a href="#overview">Overview</a><a href="#signal">The signal</a><a href="#patterns">Patterns</a><a href="#diagnose">Diagnosis</a><a href="#intervene">Playbook</a><a href="#evidence">Evidence</a></nav>', unsafe_allow_html=True)
with nav_action:
    settings = st.popover("Configure analysis", icon=":material/tune:", use_container_width=True)
with settings:
    st.markdown("#### Analysis settings")
    st.caption("Adjust the evidence window; the dashboard refreshes with these choices.")
    sample=st.slider("Trips to fetch",5000,50000,25000,5000)
    max_gap=st.slider("Maximum between-trip gap (minutes)",30,180,90,15)
    if st.button("Refresh source data"):
        st.cache_data.clear()
        st.rerun()
    st.info("Only consecutive trips from the same taxi, with reported centroids, are used. This is an estimate—not GPS telemetry.")
st.markdown('<div class="nav-rule"></div>', unsafe_allow_html=True)

try:
    df=fetch_data(sample)
    ghost=build_ghost_metrics(df)
    ghost["eligible_pair"] = ghost["gap_min"].between(0, max_gap) & ghost["dropoff_centroid_latitude"].notna() & ghost["next_pick_lat"].notna()
    ghost["estimated_deadhead_miles"] = np.where(ghost["eligible_pair"], ghost["estimated_deadhead_miles"], 0)
    ghost["estimated_idle_min"] = np.where(ghost["eligible_pair"], ghost["estimated_idle_min"], 0)
    ghost["reposition_flag"] = ghost["eligible_pair"] & (ghost["estimated_deadhead_miles"]>=0.25)
    status="LIVE DATA"
except Exception as e:
    st.error("Could not reach the City of Chicago open-data API. Connect to the internet and refresh. GhostMiles intentionally does not substitute fake ride data.")
    st.code(str(e))
    st.stop()

# ---------- header ----------
st.markdown('<div id="overview"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="hero">
  <div>
    <div class="kicker">GHOSTMILES / MOBILITY CAPACITY INTELLIGENCE</div>
    <h1>Find the miles<br><span>nobody sees.</span></h1>
    <p>Real public trip data, transformed into an analyst workflow for estimating deadhead movement, finding spatial waste patterns and testing repositioning decisions.</p>
  </div>
  <div class="hero-stat">
    <div class="label">ESTIMATED DEADHEAD</div>
    <div class="num">""" + f"{ghost['estimated_deadhead_miles'].sum():,.0f}" + """</div>
    <div class="unit">miles inferred between consecutive trips in this live sample</div>
    <div style="margin-top:20px" class="live">● """ + status + """ · """ + str(len(df)) + """ trips loaded</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="source-note">Source: <a href="{DATASET_URL}" target="_blank">{DATA_SOURCE}</a> · Data is reported taxi activity; timestamps are rounded to 15 minutes. GhostMiles estimates deadhead from consecutive trip endpoints and the next pickup centroid — it is NOT claiming to observe private GPS traces.</div>', unsafe_allow_html=True)

# metrics
st.markdown('<div class="section" id="signal">',unsafe_allow_html=True)
st.markdown('<div class="section-head"><div><div class="kicker">01 / THE SIGNAL</div><h2>What is the<br>system wasting?</h2></div><p>We cannot see the driver\'s actual route between trips. Instead, we make a reproducible estimate from the end of one trip to the start of the next.</p></div>',unsafe_allow_html=True)
valid_ghost=ghost[ghost["reposition_flag"]].copy()
total_dead=float(valid_ghost["estimated_deadhead_miles"].sum())
avg_dead=float(valid_ghost["estimated_deadhead_miles"].mean()) if len(valid_ghost) else 0
ghost_events=len(valid_ghost)
eligible_pairs=int(ghost["eligible_pair"].sum())
cols=st.columns(5)
cols[0].metric("Trips analyzed",f"{len(df):,}")
cols[1].metric("Comparable trip pairs",f"{eligible_pairs:,}",help="Consecutive, same-taxi trips with reported centroids and a gap inside the selected window.")
cols[2].metric("Ghost events",f"{ghost_events:,}")
cols[3].metric("Estimated deadhead",f"{total_dead:,.0f} mi")
cols[4].metric("Avg. deadhead / event",f"{avg_dead:.2f} mi")
st.markdown('</div>',unsafe_allow_html=True)

# charts
import plotly.express as px
st.markdown('<div class="section" id="patterns">',unsafe_allow_html=True)
st.markdown('<div class="section-head"><div><div class="kicker">02 / VISUALIZE</div><h2>Where capacity<br><em>disappears.</em></h2></div><p>Ranked zones and time windows reveal where inferred repositioning is concentrated.</p></div>',unsafe_allow_html=True)
c1,c2=st.columns([1.25,.75])
with c1:
    zone=valid_ghost.groupby("dropoff_community_area",dropna=True).agg(ghost_miles=("estimated_deadhead_miles","sum"),events=("reposition_flag","sum")).reset_index()
    zone=zone.sort_values("ghost_miles",ascending=False).head(12)
    fig=px.bar(zone,y="dropoff_community_area",x="ghost_miles",orientation="h",color="ghost_miles",
               color_continuous_scale=["#4d6d18","#caff21"],labels={"dropoff_community_area":"Drop-off area","ghost_miles":"Estimated deadhead miles"})
    fig.update_layout(height=420,margin=dict(l=0,r=0,t=15,b=0),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",coloraxis_showscale=False)
    st.plotly_chart(fig,use_container_width=True)
with c2:
    hourly=valid_ghost.groupby("hour").agg(ghost_miles=("estimated_deadhead_miles","sum"),events=("reposition_flag","sum")).reset_index()
    fig2=px.area(hourly,x="hour",y="ghost_miles",markers=True,color_discrete_sequence=["#b9ed00"],labels={"hour":"Hour","ghost_miles":"Miles"})
    fig2.update_layout(height=420,margin=dict(l=0,r=0,t=15,b=0),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2,use_container_width=True)
st.markdown('</div>',unsafe_allow_html=True)

# RCA
st.markdown('<div id="diagnose"></div>',unsafe_allow_html=True)
st.markdown('<div class="section-head"><div><div class="kicker">03 / DIAGNOSE</div><h2>Do not report<br><span>the problem.</span></h2></div><p>Use the data to isolate the operational pattern behind the waste.</p></div>',unsafe_allow_html=True)
r1,r2,r3=st.columns(3)
with r1:
    peak=valid_ghost.groupby("hour")["estimated_deadhead_miles"].sum().sort_values(ascending=False)
    peak_hour=int(peak.index[0]) if len(peak) else 0
    st.markdown(f'<div class="card"><div class="metric-label">PEAK DEADHEAD HOUR</div><div class="metric">{peak_hour:02d}:00</div><div class="delta">Highest inferred repositioning volume</div></div>',unsafe_allow_html=True)
with r2:
    if len(valid_ghost):
        top_zone=str(valid_ghost.groupby("dropoff_community_area")["estimated_deadhead_miles"].sum().idxmax())
    else: top_zone="—"
    st.markdown(f'<div class="card"><div class="metric-label">TOP WASTE AREA</div><div class="metric">{top_zone}</div><div class="delta">Largest inferred deadhead concentration</div></div>',unsafe_allow_html=True)
with r3:
    long_share=(valid_ghost["estimated_deadhead_miles"]>=2).mean()*100 if len(valid_ghost) else 0
    st.markdown(f'<div class="card"><div class="metric-label">LONG REPOSITION SHARE</div><div class="metric">{long_share:.1f}%</div><div class="delta">Events ≥ 2 inferred miles</div></div>',unsafe_allow_html=True)

if len(valid_ghost):
    cause=pd.DataFrame({
        "Signal":["Peak-hour concentration","Long repositioning","Sparse next-pickup proximity"],
        "Value":[
            float(valid_ghost["hour"].isin([17,18,19,20]).mean()),
            float((valid_ghost["estimated_deadhead_miles"]>=2).mean()),
            float((valid_ghost["estimated_idle_min"]>=30).mean())
        ]
    })
    st.write("")
    fig3=px.bar(cause,x="Signal",y="Value",color="Value",color_continuous_scale=["#4c6418","#caff21"])
    fig3.update_yaxes(tickformat=".0%")
    fig3.update_layout(height=330,margin=dict(l=0,r=0,t=10,b=0),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",coloraxis_showscale=False,font_color="#eee")
    st.plotly_chart(fig3,use_container_width=True)

st.markdown('<div class="insight"><b>Analyst takeaway →</b> This is an inference problem, not a GPS-tracking claim. The strongest signal is the concentration of estimated deadhead by area and time. A production mobility platform would combine this logic with live driver GPS, demand forecasts and dispatch events.</div>',unsafe_allow_html=True)
st.markdown('</div>',unsafe_allow_html=True)

# simulator
st.markdown('<div class="section" id="intervene">',unsafe_allow_html=True)
st.markdown('<div class="section-head"><div><div class="kicker">04 / INTERVENE</div><h2>Where should<br><em>drivers move?</em></h2></div><p>Observed next-pickup zones turn the inferred gap into a dispatch playbook. These are recommended re-engagement zones, not a claim of causal demand.</p></div>',unsafe_allow_html=True)

# Each flow is an observed sequence: a taxi ended in origin_area, then its next
# reported passenger trip began in target_area. That makes the recommendation traceable.
flows = valid_ghost.dropna(subset=["dropoff_community_area", "next_pick_area"]).copy()
flows["route"] = flows["dropoff_community_area"].astype(str) + " -> " + flows["next_pick_area"].astype(str)
flow_summary = flows.groupby(["dropoff_community_area", "next_pick_area", "route"], as_index=False).agg(
    events=("reposition_flag", "sum"),
    deadhead_miles=("estimated_deadhead_miles", "sum"),
    median_gap_min=("estimated_idle_min", "median"),
    avg_deadhead_miles=("estimated_deadhead_miles", "mean")
).sort_values(["deadhead_miles", "events"], ascending=False)
base = total_dead

if len(flow_summary):
    st.caption("Zone IDs are Chicago community-area codes from the public source. A route means: previous passenger drop-off -> next reported passenger pickup.")
    flow_chart = px.bar(flow_summary.head(10).sort_values("deadhead_miles"), y="route", x="deadhead_miles", orientation="h",
                       color="events", color_continuous_scale=["#4d6d18", "#caff21"],
                       labels={"route":"Observed re-engagement flow", "deadhead_miles":"Estimated deadhead miles", "events":"Events"})
    flow_chart.update_layout(height=360, margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(flow_chart, use_container_width=True)
else:
    st.info("No centroid-complete origin-to-next-pickup flows were found for the selected sample and gap window.")

s1,s2=st.columns([.55,1.45])
with s1:
    strategy=st.selectbox("Dispatch focus",["Highest-waste flow", "Top 3 waste flows", "Peak deadhead hour"])
    max_actions=max(25, min(1000, ghost_events))
    n=st.slider("Repositioning actions",0,max_actions,min(100, max_actions),min(25,max_actions))
    assumed_capture=st.slider("Assumed miles avoided per action",0.0,3.0,0.75,0.05)
    if strategy == "Highest-waste flow" and len(flow_summary):
        focus=flows[flows["route"] == flow_summary.iloc[0]["route"]]
        focus_label=flow_summary.iloc[0]["route"]
    elif strategy == "Top 3 waste flows" and len(flow_summary):
        selected_routes=flow_summary.head(3)["route"].tolist()
        focus=flows[flows["route"].isin(selected_routes)]
        focus_label="Top 3 observed waste flows"
    else:
        peak_hours=valid_ghost.groupby("hour")["estimated_deadhead_miles"].sum().nlargest(1).index.tolist()
        focus=valid_ghost[valid_ghost["hour"].isin(peak_hours)]
        focus_label=f"Hour {peak_hours[0]:02d}:00" if peak_hours else "No peak hour available"
    focus_base=float(focus["estimated_deadhead_miles"].sum())
    avoided=min(focus_base, n*assumed_capture)
    st.markdown(f'<div class="insight"><b>Scenario, not forecast.</b><br><b>Focus:</b> {focus_label}<br>{n:,} actions x {assumed_capture:.2f} mi/action, capped at the selected flow\'s measured estimate.</div>',unsafe_allow_html=True)
with s2:
    a,b,c=st.columns(3)
    a.metric("Current inferred deadhead",f"{base:,.0f} mi")
    b.metric("Potentially avoided",f"{avoided:,.0f} mi",delta=f"-{avoided:,.0f} mi")
    c.metric("Selected-flow reduction",f"{(avoided/focus_base if focus_base else 0):.1%}")
    if len(valid_ghost):
        curve=pd.DataFrame({"actions":np.arange(0,max_actions+1,max(1, max_actions//20))})
        curve["potential_miles_avoided"]=np.minimum(focus_base,curve["actions"]*assumed_capture)
        fig4=px.line(curve,x="actions",y="potential_miles_avoided",markers=True,color_discrete_sequence=["#111"])
        fig4.update_layout(height=330,margin=dict(l=0,r=0,t=25,b=0),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",xaxis_title="Repositioning actions",yaxis_title="Potential miles avoided")
        st.plotly_chart(fig4,use_container_width=True)
st.markdown('</div>',unsafe_allow_html=True)

# data explorer
st.markdown('<div class="section" id="evidence">',unsafe_allow_html=True)
st.markdown('<div class="section-head"><div><div class="kicker">05 / EVIDENCE</div><h2>Show me<br><em>the data.</em></h2></div><p>Everything in the dashboard can be traced back to public trip records.</p></div>',unsafe_allow_html=True)
show_cols=["trip_id","taxi_id","trip_start_timestamp","trip_end_timestamp","trip_miles","pickup_community_area","dropoff_community_area","estimated_deadhead_miles","estimated_idle_min"]
st.dataframe(ghost[show_cols].sort_values("estimated_deadhead_miles",ascending=False).head(100),use_container_width=True,hide_index=True)
st.download_button("Export analyzed sample CSV",ghost[show_cols].to_csv(index=False),"ghostmiles_analyzed_sample.csv","text/csv")
st.markdown(f'<div class="source-note">Official source: <a href="{DATASET_URL}" target="_blank">{DATA_SOURCE}</a>. The City notes that Taxi IDs are consistent medallion identifiers, timestamps are rounded to 15 minutes, and not every trip is reported.</div>',unsafe_allow_html=True)
st.markdown('</div>',unsafe_allow_html=True)

st.markdown('<div style="padding:30px 0;border-top:1px solid #d8d8d1;display:flex;justify-content:space-between;font-size:10px;color:#777"><span>GHOSTMILES © 2026</span><span>Real public data · transparent inference · reproducible analysis</span></div>',unsafe_allow_html=True)
