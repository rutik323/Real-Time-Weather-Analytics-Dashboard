import customtkinter as ctk
from tkinter import *
from PIL import Image, ImageTk
import cv2
import requests
from datetime import datetime
import math
import threading

# =========================================================
# GLOBAL WINDOW CONFIGURATION
# =========================================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
APP_W = 1400
APP_H = 850
root.geometry(f"{APP_W}x{APP_H}")
root.title("WEATHER DASHBOARD ENGINE")
root.resizable(False, False)

# =========================================================
# LIVE ANIMATED CANVAS VIDEO BACKGROUND
# =========================================================
canvas = Canvas(root, width=APP_W, height=APP_H, highlightthickness=0)
canvas.place(x=0, y=0)

cap = cv2.VideoCapture("background.mp4")
video_img = None

def play_video():
    global video_img
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (APP_W, APP_H))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            video_img = ImageTk.PhotoImage(img)
            canvas.create_image(0, 0, image=video_img, anchor=NW)
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    root.after(30, play_video)

play_video()

# =========================================================
# CONTAINER FRAMES & MAIN NAVIGATION PANELS
# =========================================================
main = Frame(root, bg="#111111", highlightbackground="#333", highlightthickness=2)
main.place(relx=0.5, rely=0.5, anchor=CENTER, width=1350, height=790)

title = Label(main, text="WEATHER DASHBOARD", font=("Arial", 28, "bold"), bg="#111111", fg="white")
title.place(x=30, y=20)

search = ctk.CTkEntry(main, width=320, height=45, corner_radius=25, placeholder_text="Type city and press Enter...")
search.place(x=450, y=25)

page1 = Frame(main, bg="#111111")
page2 = Frame(main, bg="#111111")
page3 = Frame(main, bg="#111111")
page4 = Frame(main, bg="#111111")

page1.place(x=30, y=100, width=1280, height=650)

def clear_pages():
    page1.place_forget()
    page2.place_forget()
    page3.place_forget()
    page4.place_forget()

def show_page1():
    clear_pages()
    page1.place(x=30, y=100, width=1280, height=650)

def show_page2():
    clear_pages()
    page2.place(x=30, y=100, width=1280, height=650)

def show_page3():
    clear_pages()
    page3.place(x=30, y=100, width=1280, height=650)

def show_page4():
    clear_pages()
    page4.place(x=30, y=100, width=1280, height=650)

btn1 = ctk.CTkButton(main, text="Dashboard", command=show_page1, width=100, height=40, corner_radius=20)
btn1.place(x=820, y=25)

btn2 = ctk.CTkButton(main, text="Forecast", command=show_page2, width=100, height=40, corner_radius=20)
btn2.place(x=930, y=25)

btn3 = ctk.CTkButton(main, text="Alarms & Indices", command=show_page3, width=130, height=40, corner_radius=20)
btn3.place(x=1040, y=25)

btn4 = ctk.CTkButton(main, text="Aero/Marine", command=show_page4, width=110, height=40, corner_radius=20)
btn4.place(x=1180, y=25)

# =========================================================
# CORE HUD DISPLAY COMPONENT MATRIX (PAGE 1)
# =========================================================
weather_card = Frame(page1, bg="#ff6b1a")
weather_card.place(x=0, y=0, width=400, height=280)

city = Label(weather_card, text="Search City", font=("Arial", 32, "bold"), bg="#ff6b1a", fg="white")
city.place(x=30, y=20)

date_label = Label(weather_card, text=datetime.now().strftime("%d %b %Y"), font=("Arial", 16), bg="#ff6b1a", fg="white")
date_label.place(x=270, y=25)

icon = Label(weather_card, text="⛅", font=("Arial", 90), bg="#ff6b1a")
icon.place(x=20, y=70)

temp = Label(weather_card, text="--°C", font=("Arial", 72, "bold"), bg="#ff6b1a", fg="white")
temp.place(x=30, y=170)

def info_box(parent, title_text, value, x, y):
    box = Frame(parent, bg="#053588", highlightbackground="#333", highlightthickness=1)
    box.place(x=x, y=y, width=190, height=110)
    Label(box, text=title_text, font=("Arial", 14), bg="#053588", fg="white").place(x=18, y=15)
    value_label = Label(box, text=value, font=("Arial", 24, "bold"), bg="#053588", fg="white")
    value_label.place(x=18, y=55)
    return value_label

humidity = info_box(page1, "💧 Humidity", "--", 0, 320)
wind = info_box(page1, "🌪 Wind", "--", 210, 320)
pressure = info_box(page1, "⚙ Pressure", "--", 0, 450)
uv = info_box(page1, "☀ UV Index", "--", 210, 450)

ai = Frame(page1, bg="#053588", highlightbackground="#333", highlightthickness=1)
ai.place(x=450, y=0, width=800, height=240)

ai_title = Label(ai, text="🤖 AI Assistant Summary", font=("Arial", 24, "bold"), bg="#053588", fg="white")
ai_title.place(x=20, y=20)

ai_text = Label(ai, text="Type a city name above and hit Enter.", font=("Arial", 16), justify=LEFT, bg="#053588", fg="white", wraplength=750)
ai_text.place(x=20, y=70)

sun = Frame(page1, bg="#053588", highlightbackground="#333", highlightthickness=1)
sun.place(x=450, y=280, width=380, height=300)

sunrise_label = Label(sun, text="🌅 Sunrise\n--:--", font=("Arial", 24, "bold"), bg="#053588", fg="white")
sunrise_label.place(x=40, y=40)

sunset_label = Label(sun, text="🌇 Sunset\n--:--", font=("Arial", 24, "bold"), bg="#053588", fg="white")
sunset_label.place(x=40, y=160)

aqi_box = Frame(page1, bg="#053588", highlightbackground="#333", highlightthickness=1)
aqi_box.place(x=870, y=280, width=380, height=300)

aqi_title = Label(aqi_box, text="🌫 Air Quality (US AQI)", font=("Arial", 24, "bold"), bg="#053588", fg="white")
aqi_title.place(x=30, y=30)

aqi_value = Label(aqi_box, text="--", font=("Arial", 80, "bold"), bg="#053588", fg="white")
aqi_value.place(x=40, y=90)

aqi_status = Label(aqi_box, text="Waiting...", font=("Arial", 24), bg="#053588", fg="white")
aqi_status.place(x=45, y=210)

# =========================================================
# FORECAST PANEL INTERFACES (PAGE 2)
# =========================================================
forecast_title = Label(page2, text="5 Day Forecast", font=("Arial", 34, "bold"), bg="#053588", fg="white")
forecast_title.place(x=20, y=10)

forecast_cards = []
x_offset = 20
for i in range(5):
    card = Frame(page2, bg="#053588", highlightbackground="#333", highlightthickness=1)
    card.place(x=x_offset, y=80, width=220, height=260)

    day_lbl = Label(card, text="?", font=("Arial", 26, "bold"), bg="#053588", fg="white")
    day_lbl.pack(pady=20)

    icon_lbl = Label(card, text="⛅", font=("Arial", 70), bg="#053588")
    icon_lbl.pack()

    temp_lbl = Label(card, text="--°C", font=("Arial", 28), bg="#053588", fg="white")
    temp_lbl.pack(pady=15)

    forecast_cards.append((day_lbl, icon_lbl, temp_lbl))
    x_offset += 245

rain = Frame(page2, bg="#053588", highlightbackground="#333", highlightthickness=1)
rain.place(x=20, y=380, width=1230, height=250)

Label(rain, text="Chance Of Rain", font=("Arial", 30, "bold"), bg="#053588", fg="white").place(x=30, y=20)

rain_bars = []
y_offset = 80
for i in range(5):
    day_lbl = Label(rain, text="...", font=("Arial", 18), bg="#053588", fg="white")
    day_lbl.place(x=30, y=y_offset)

    bar = ctk.CTkProgressBar(rain, width=900, height=14)
    bar.place(x=180, y=y_offset + 10)
    bar.set(0)

    val_lbl = Label(rain, text="0%", font=("Arial", 18), bg="#053588", fg="white")
    val_lbl.place(x=1100, y=y_offset)

    rain_bars.append((bar, val_lbl, day_lbl))
    y_offset += 32

# =========================================================
# CLIMATE INSIGHTS & THRESHOLD ALARMS (PAGE 3)
# =========================================================
p3_title = Label(page3, text="Advanced Bio-Climate Analytics & Alarm Matrix", font=("Arial", 28, "bold"), bg="#111111", fg="white")
p3_title.place(x=20, y=10)

dew_point_box = info_box(page3, "🌡 Dew Point", "--°C", 20, 80)
heat_idx_box = info_box(page3, "🥵 Heat Index", "--°C", 230, 80)
visibility_box = info_box(page3, "👁 Visibility", "-- km", 440, 80)
cloud_box = info_box(page3, "☁ Cloud Cover", "-- %", 650, 80)

alarm_panel = Frame(page3, bg="#1f1f1f", highlightbackground="#ff3333", highlightthickness=1)
alarm_panel.place(x=20, y=220, width=1230, height=400)

alarm_title = Label(alarm_panel, text="🚨 Live Severe Environmental Safeguard Feeds", font=("Arial", 22, "bold"), bg="#1f1f1f", fg="white")
alarm_title.place(x=30, y=20)

def create_alarm_row(parent, text, y):
    lbl = Label(parent, text=text, font=("Arial", 18), bg="#1f1f1f", fg="#aaaaaa")
    lbl.place(x=40, y=y)
    status_lbl = Label(parent, text="Nominal", font=("Arial", 18, "bold"), bg="#1f1f1f", fg="#00e400")
    status_lbl.place(x=400, y=y)
    desc_lbl = Label(parent, text="Environmental criteria within normal operating metrics.", font=("Arial", 14), bg="#1f1f1f", fg="#777777")
    desc_lbl.place(x=580, y=y+3)
    return status_lbl, desc_lbl

heat_status, heat_desc = create_alarm_row(alarm_panel, "• Extreme Thermal Load Risk", 80)
freeze_status, freeze_desc = create_alarm_row(alarm_panel, "• Cryospheric Freeze Risk", 140)
wind_status, wind_desc = create_alarm_row(alarm_panel, "• High Kinetic Gale Winds", 200)
aqi_alarm_status, aqi_alarm_desc = create_alarm_row(alarm_panel, "• Toxic Atmospheric AQI Risk", 260)

# =========================================================
# ASTRONOMY & MARINE TELEMETRY PANEL (PAGE 4)
# =========================================================
p4_title = Label(page4, text="Astronomy Vectors & Marine/Aviation Analytics", font=("Arial", 28, "bold"), bg="#111111", fg="white")
p4_title.place(x=20, y=10)

astro_box = Frame(page4, bg="#053588", highlightbackground="#333", highlightthickness=1)
astro_box.place(x=20, y=80, width=600, height=530)

astro_title = Label(astro_box, text="☀️ Solar & Celestial Coordinates", font=("Arial", 22, "bold"), bg="#053588", fg="white")
astro_title.place(x=30, y=20)

sol_alt_lbl = info_box(astro_box, "📐 Solar Altitude", "--°", 30, 80)
sol_azi_lbl = info_box(astro_box, "🧭 Solar Azimuth", "--°", 250, 80)

astro_desc = Label(astro_box, text="Real-time calculations of spatial azimuth angle vectors and solar alignment parameters relative to horizon tracking coordinates.", font=("Arial", 15), bg="#053588", fg="#dddddd", wraplength=520, justify=LEFT)
astro_desc.place(x=30, y=220)

marine_box = Frame(page4, bg="#053588", highlightbackground="#333", highlightthickness=1)
marine_box.place(x=650, y=80, width=600, height=530)

marine_title = Label(marine_box, text="🌊 Marine & Aviation Interface", font=("Arial", 22, "bold"), bg="#053588", fg="white")
marine_title.place(x=30, y=20)

wave_lbl = info_box(marine_box, "🌊 Wave Height", "-- m", 30, 80)
gust_lbl = info_box(marine_box, "💨 Wind Gusts", "-- km/h", 250, 80)
sst_lbl = info_box(marine_box, "🌡 Sea Surface Temp", "--°C", 30, 210)
evap_lbl = info_box(marine_box, "💧 Evaporation", "-- mm", 250, 210)

marine_desc = Label(marine_box, text="Simulated oceanic hydrodynamics, kinetic wind-shear gusts for aviation, and thermal marine surface layer telemetry feeds.", font=("Arial", 15), bg="#053588", fg="#dddddd", wraplength=520, justify=LEFT)
marine_desc.place(x=30, y=350)

# =========================================================
# FLOAT PROCESSING UTILITIES
# =========================================================
def safe_float(dictionary, key, default=0.0):
    value = dictionary.get(key)
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

# =========================================================
# STABILIZED WEATHER ANALYSIS ENGINE (WITH THREADING)
# =========================================================
def get_weather():
    city_name = search.get().strip()
    if not city_name:
        return

    # Run in background thread to prevent UI freezing
    threading.Thread(target=fetch_weather_thread, args=(city_name,), daemon=True).start()

def fetch_weather_thread(city_name):
    try:
        # Step 1: Resolve Coordinates with Geocoding Engine
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {
            "name": city_name,
            "count": 1,
            "language": "en",
            "format": "json"
        }
        geo_res = requests.get(geo_url, params=geo_params)
        geo_res.raise_for_status()
        geo = geo_res.json()

        if 'results' not in geo or len(geo['results']) == 0:
            ai_text.config(text=f"❌ Core lookup error: Location '{city_name}' is unverified.")
            return

        lat = geo['results'][0]['latitude']
        lon = geo['results'][0]['longitude']
        resolved_name = geo['results'][0]['name']

        # Step 2: Clean Weather Pipeline
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&"
            f"current=temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m,cloud_cover,visibility&"
            f"daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunrise,sunset&"
            f"timezone=auto"
        )

        weather_res = requests.get(weather_url)
        weather_res.raise_for_status()
        data = weather_res.json()

        current = data.get('current', {})
        daily = data.get('daily', {})

        t_val = safe_float(current, 'temperature_2m')
        h_val = safe_float(current, 'relative_humidity_2m', 0.0)
        w_val = safe_float(current, 'wind_speed_10m')
        p_val = safe_float(current, 'pressure_msl')
        cloud_val = safe_float(current, 'cloud_cover')
        vis_val = safe_float(current, 'visibility') / 1000.0  # Convert to km

        # Step 3: Isolated UV Sub-Index Call Block
        uv_val = 0.0
        try:
            uv_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=uv_index&timezone=auto&forecast_days=1"
            uv_res = requests.get(uv_url)
            if uv_res.status_code == 200:
                uv_stream = uv_res.json().get('hourly', {}).get('uv_index', [])
                if uv_stream:
                    uv_val = max(uv_stream[:24])
        except Exception:
            uv_val = 1.0

        # ---- GRAPHICAL COMPONENT SYNCHRONIZATION ----
        city.config(text=resolved_name)
        temp.config(text=f"{round(t_val)}°C")
        humidity.config(text=f"{round(h_val)}%")
        wind.config(text=f"{round(w_val)} km/h")
        pressure.config(text=f"{round(p_val)} hPa")
        uv.config(text=f"{round(uv_val)}")

        if t_val <= 10:
            icon.config(text="❄")
        elif t_val <= 20:
            icon.config(text="☁")
        elif t_val <= 30:
            icon.config(text="⛅")
        else:
            icon.config(text="☀")

        ai_text.config(
            text=f"Live system telemetry feed finalized for {resolved_name}:\n"
                 f"• Core temperature sensors tracking atmospheric level at {round(t_val)}°C.\n"
                 f"• Moisture analytics calculate dynamic ambient relative humidity at {round(h_val)}%.\n"
                 f"• Wind tracker arrays flag surface velocity movements up to {round(w_val)} km/h.\n"
                 f"• Local solar indexes register safe radiation factor parameters near level {round(uv_val)}."
         )

        sunrise_list = daily.get('sunrise', [])
        sunset_list = daily.get('sunset', [])

        sunrise_time = sunrise_list[0].split("T")[1] if (sunrise_list and "T" in sunrise_list[0]) else "--:--"
        sunset_time = sunset_list[0].split("T")[1] if (sunset_list and "T" in sunset_list[0]) else "--:--"

        sunrise_label.config(text=f"🌅 Sunrise\n{sunrise_time}")
        sunset_label.config(text=f"🌇 Sunset\n{sunset_time}")

        # Step 4: US Air Quality Sub-API Query System
        try:
            aqi_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=us_aqi"
            aqi_res = requests.get(aqi_url)
            air_quality = aqi_res.json().get('current', {}).get('us_aqi', 42)
        except Exception:
            air_quality = 42

        aqi_value.config(text=str(round(air_quality)))
        if air_quality <= 50:
            aqi_status.config(text="Good", fg="#00e400")
        elif air_quality <= 100:
            aqi_status.config(text="Moderate", fg="#ffff00")
        elif air_quality <= 150:
            aqi_status.config(text="Unhealthy", fg="#ff7e00")
        else:
            aqi_status.config(text="Hazardous", fg="#ff0000")

        # Step 5: Extended Forecast Grid Synchronizer (Page 2)
        daily_temp = daily.get('temperature_2m_max', [t_val]*5)
        daily_rain = daily.get('precipitation_probability_max', [0]*5)
        daily_time = daily.get('time', [])

        icon_pool = ["☀", "⛅", "🌦", "🌧", "☁"]

        for i in range(5):
            if i < len(daily_time):
                dt_obj = datetime.strptime(daily_time[i], "%Y-%m-%d")
                day_short = dt_obj.strftime("%a")
                day_long = dt_obj.strftime("%A")
            else:
                day_short = "N/A"
                day_long = "Unknown Day"

            t_max = daily_temp[i] if i < len(daily_temp) else t_val
            r_chance = daily_rain[i] if i < len(daily_rain) else 0

            forecast_cards[i][0].config(text=day_short)
            forecast_cards[i][1].config(text=icon_pool[i % len(icon_pool)])
            forecast_cards[i][2].config(text=f"{round(t_max)}°C")

            rain_bars[i][0].set(r_chance / 100)
            rain_bars[i][1].config(text=f"{r_chance}%")
            rain_bars[i][2].config(text=day_long)

        # PAGE 3 COMPUTATIONS
        if h_val > 0:
            alpha = ((17.27 * t_val) / (237.7 + t_val)) + math.log(h_val / 100.0)
            dew_point = (237.7 * alpha) / (17.27 - alpha)
        else:
            dew_point = t_val - ((100 - h_val) / 5)

        heat_idx = t_val + 0.5 * (t_val + 61.0 + ((t_val - 68.0) * 1.2) + (h_val * 0.094))

        dew_point_box.config(text=f"{round(dew_point, 1)}°C")
        heat_idx_box.config(text=f"{round(heat_idx, 1)}°C")
        visibility_box.config(text=f"{round(vis_val, 1)} km")
        cloud_box.config(text=f"{round(cloud_val)} %")

        if heat_idx >= 35:
            heat_status.config(text="CRITICAL", fg="#ff0000")
            heat_desc.config(text="Excessive hyperthermia conditions active. Minimize outdoor maneuvers.")
        else:
            heat_status.config(text="Nominal", fg="#00e400")
            heat_desc.config(text="Environmental criteria within normal operating metrics.")

        if t_val <= 0:
            freeze_status.config(text="WARNING", fg="#ff7e00")
            freeze_desc.config(text="Freezing temperature detected. Liquid framework icing risk active.")
        else:
            freeze_status.config(text="Nominal", fg="#00e400")
            freeze_desc.config(text="Environmental criteria within normal operating metrics.")

        if w_val >= 40:
            wind_status.config(text="CRITICAL", fg="#ff0000")
            wind_desc.config(text="Gale forces registering. Secure structural arrays.")
        elif w_val >= 25:
            wind_status.config(text="Caution", fg="#ffff00")
            wind_desc.config(text="Elevated wind activity. Minor aerodynamic perturbations possible.")
        else:
            wind_status.config(text="Nominal", fg="#00e400")
            wind_desc.config(text="Environmental criteria within normal operating metrics.")

        if air_quality > 100:
            aqi_alarm_status.config(text="UNHEALTHY", fg="#ff7e00")
            aqi_alarm_desc.config(text="Atmospheric toxicity threshold breached. Pulmonary defenses recommended.")
        else:
            aqi_alarm_status.config(text="Nominal", fg="#00e400")
            aqi_alarm_desc.config(text="Environmental criteria within normal operating metrics.")

        # PAGE 4 COMPUTATIONS
        mock_hour = datetime.now().hour
        solar_alt = max(-90.0, min(90.0, 90.0 - abs(lat - 23.5) - abs(12 - mock_hour) * 6))
        solar_azi = (180 + (mock_hour - 12) * 15) % 360

        sol_alt_lbl.config(text=f"{round(solar_alt, 1)}°")
        sol_azi_lbl.config(text=f"{round(solar_azi, 1)}°")

        sim_wave = max(0.2, (w_val * 0.12) + (p_val - 1013.2) * -0.01)
        sim_gust = w_val * 1.35
        sim_sst = max(2.0, t_val * 0.8 + 4.0) if lat < 60 else max(0.5, t_val * 0.2)
        sim_evap = max(0.0, (t_val * 0.1) + (h_val * -0.02))

        wave_lbl.config(text=f"{round(sim_wave, 2)} m")
        gust_lbl.config(text=f"{round(sim_gust, 1)} km/h")
        sst_lbl.config(text=f"{round(sim_sst, 1)}°C")
        evap_lbl.config(text=f"{round(sim_evap, 2)} mm")

    except Exception as e:
        print("Internal Pipeline Error Caught:", e)
        ai_text.config(text="⚠️ Communication link error. Check spelling and coordinates.")

search.bind("<Return>", lambda e: get_weather())

# =========================================================
# APPLICATION EVENT INITIALIZATION RUN
# =========================================================
root.mainloop()