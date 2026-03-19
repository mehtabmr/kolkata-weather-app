# 🌤️ Kolkata Weather Android App

Python + Kivy se bana hua Android app jo Kolkata ka live weather dikhata hai!

## 📱 Features

- ✅ Live weather data from Open-Meteo API
- ✅ Kolkata specific location (22.57°N, 88.36°E)
- ✅ Beautiful mobile UI with emojis
- ✅ Auto-refresh every 10 minutes
- ✅ Manual refresh button
- ✅ Offline error handling
- ✅ Shows: Temperature, Feels Like, Humidity, Wind Speed, Rain, Pressure

## 📁 Files Structure

```
kolkata_weather_app/
├── main.py              # Main app code
├── buildozer.spec     # Android build configuration
├── README.txt          # This file
└── requirements.txt    # Python dependencies
```

## 🚀 Installation on Android

### Method 1: Using Buildozer (Recommended)

**Step 1: Install Buildozer**
```bash
# On Ubuntu/Debian:
sudo apt update
sudo apt install -y python3-pip build-essential git ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libatlas-base-dev

# Install buildozer
pip3 install buildozer
pip3 install cython
```

**Step 2: Build APK**
```bash
cd kolkata_weather_app/
buildozer init  # (already done, skip this)
buildozer android debug
```

Wait for 10-30 minutes (first time takes longer to download dependencies).

**Step 3: Install on Phone**
```bash
# Connect phone with USB debugging enabled
buildozer android deploy run

# Or manually:
# Copy bin/kolkata_weather-1.0-armeabi-v7a_debug.apk to phone and install
```

### Method 2: Using P4A (Python-for-Android)

```bash
# Install p4a
pip install python-for-android

# Build APK
p4a apk --private kolkata_weather_app/ --package=org.example.kolkata_weather --name "Kolkata Weather" --version 1.0 --bootstrap=sdl2 --requirements=python3,kivy
```

### Method 3: Run on Kivy Launcher

1. Install "Kivy Launcher" from Play Store
2. Copy this folder to `/sdcard/kivy/kolkata_weather_app/`
3. Open Kivy Launcher and run!

## 🖥️ Run on Desktop (Test First)

```bash
cd kolkata_weather_app/
pip install kivy
python3 main.py
```

## 📦 Required Python Packages

```
kivy>=2.0.0
urllib3
```

## 🔧 Troubleshooting

**Error: No module named 'kivy'**
```bash
pip3 install kivy
```

**Build fails with Java/SDK errors**
```bash
# Install Java 8
sudo apt install openjdk-8-jdk

# Set JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
```

**App shows "Loading..." forever**
- Internet permission missing hai
- `android.permissions = INTERNET` buildozer.spec mein add karein

## 📱 APK Info

- **Size:** ~20-30 MB
- **Target SDK:** 33
- **Min SDK:** 21 (Android 5.0+)
- **Architecture:** armeabi-v7a

## 🌐 API Used

- Open-Meteo Weather API (Free, No API Key)
- URL: https://open-meteo.com/

## 📞 Support

App issues? Check:
1. Internet connection
2. Location services (not needed, just Internet)
3. Storage permission (for future updates)

## 🎨 UI Preview

```
╔══════════════════════════════╗
║      🌤️ Kolkata Weather      ║
║     Last updated: 2:30 PM     ║
╠══════════════════════════════╣
║         🌡️    29°C            ║
║      Partly Cloudy ☁️         ║
╠══════════════════════════════╣
║ 🤒 Feels Like  │ 💧 Humidity  ║
║    33°C        │    65%       ║
╠──────────────────────────────╣
║ 🌬️ Wind Speed  │ 📊 Pressure  ║
║    5 km/h      │  1010 hPa    ║
╠──────────────────────────────╣
║ 🌧️ Rain        │ 📅 Date      ║
║    0.0 mm      │ 19 Mar 2026  ║
╠══════════════════════════════╣
║     🔄 Refresh Weather        ║
╚══════════════════════════════╝
```

---
Made with ❤️ for Kolkata
