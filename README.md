# The Overseer - Personal Accountability System

## Project Summary

A personal accountability system that combines hardware (Raspberry Pi with webcam and Bluetooth speaker) and software (monitoring scripts on your Mac/Windows). Every morning at 6:30 AM, the Pi's webcam checks if you're sitting at your desk. If it doesn't detect your face, it plays an alarm through a speaker. Even after you sit down, your Mac/Windows computer remains locked (websites blocked) until you submit proof of completing your daily task - either a LeetCode problem or a job application. If you leave your desk for more than 5 minutes, the alarm triggers again. The system verifies your submission isn't fake through a combination of screenshot analysis, API checking (for LeetCode), and timestamp validation. Everything runs locally on your home network for privacy, with the Pi acting as the enforcer and your Mac as the monitored device.

## Current Status

**Phase:** Initial Development (Beta)
**Last Updated:** 2025-12-16

### What's Working
- ✅ Morning alarm trigger at 6:30 AM (cron job)
- ✅ Bluetooth speaker integration
- ✅ Audio playback via aplay
- ✅ Basic face detection (proof-of-concept in camera_test.py)
- ✅ OpenCV Haar Cascade model setup

### What's In Progress
- 🔨 Face monitoring orchestrator (face_monitor.py)
- 🔨 State machine implementation (wake-up → monitoring → shutdown)
- 🔨 Alarm control integration

### What's Planned
- 📋 Manual deactivation script
- 📋 Full end-to-end testing
- 📋 Production deployment
- 📋 Task verification system (LeetCode/job applications)
- 📋 Desktop monitoring and website blocking

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Raspberry Pi                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Cron (6:30 AM)                                        │
│      ↓                                                  │
│  morning_alarm.sh                                       │
│      ↓                                                  │
│  face_monitor.py (Main Orchestrator)                   │
│      ├── State Machine                                 │
│      │   ├── WAKEUP: Play alarm until face detected   │
│      │   ├── MONITORING: Track desk presence          │
│      │   └── SHUTDOWN: Cleanup and exit               │
│      │                                                  │
│      ├── Face Detection (OpenCV + Haar Cascade)       │
│      │   └── Check every 5 seconds                     │
│      │                                                  │
│      └── Alarm Control                                 │
│          └── Bluetooth Speaker (aplay + BluALSA)      │
│                                                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              Desktop (Mac/Windows) - Future             │
├─────────────────────────────────────────────────────────┤
│  • Task verification (LeetCode API, screenshot check)  │
│  • Website blocker (until task submitted)              │
│  • Communication with Pi over local network            │
└─────────────────────────────────────────────────────────┘
```

## System Behavior

### Morning Wake-Up Flow
1. **6:30 AM:** Alarm audio plays + Face monitoring starts
2. **Every 5 seconds:** Camera checks for face in frame
3. **If NO face detected:** After 30 seconds (6 checks), alarm replays
4. **If face detected:** Alarm stops → Transition to Monitoring Phase

### Desk Monitoring Phase
1. **Every 5 seconds:** Camera checks for face
2. **Track consecutive "no face" count**
3. **If face present:** Reset counter to 0
4. **If no face for 5 minutes (60 checks):**
   - Play alarm audio ONE time
   - Shut down system completely for the day

### Manual Deactivation
- Run: `~/the-overseer/pi/scripts/deactivate_monitor.sh`
- System stops monitoring and exits gracefully

## Project Structure

```
/home/george/the-overseer/
├── README.md                 # This file
├── PROGRESS.md               # Development progress tracker
├── JOURNAL.md                # Development journal/notes
├── TESTS.md                  # Test results log
├── requirements.txt          # Python dependencies
├── .gitignore
├── .claude/                  # Claude Code context files
│   └── context.md            # Project context for AI assistant
│
├── pi/                       # Raspberry Pi implementation
│   ├── README.md             # Pi-specific setup guide
│   ├── face_monitor.py       # Main orchestrator (TO BUILD)
│   ├── camera_test.py        # Face detection test
│   ├── alarm_test.py         # Legacy alarm test
│   ├── web_stream.py         # Flask video streaming
│   ├── overseer_api.py       # API endpoints (future)
│   ├── overseer_watcher.py   # Background service (future)
│   │
│   ├── audio/
│   │   ├── alarm2.wav        # Current alarm audio
│   │   └── alarm2.mp3        # Legacy alarm audio
│   │
│   ├── model/
│   │   └── haarcascade_frontalface_default.xml  # Face detection model
│   │
│   └── scripts/
│       ├── morning_alarm.sh           # Cron launcher (TO BUILD)
│       ├── morning_alarm_test.sh      # Current working alarm
│       └── deactivate_monitor.sh      # Manual deactivation (TO BUILD)
│
└── desktop/                  # Desktop monitoring (future)
    ├── monitor.py            # System monitor
    └── blocker.py            # Website blocker
```

## Hardware Requirements

### Raspberry Pi Setup
- **Model:** Raspberry Pi (any model with USB/camera support)
- **Camera:** USB webcam or Pi Camera Module
- **Audio:** Bluetooth speaker (currently paired to MAC: 88:92:CC:C4:AF:53)
- **OS:** Raspberry Pi OS (Linux)

### Desktop Setup (Future)
- **OS:** macOS or Windows
- **Network:** Local network connection to Pi
- **Browser:** Chrome/Firefox for website blocking

## Software Dependencies

### Raspberry Pi
```
Python 3.x
OpenCV (cv2)
aplay (ALSA audio player)
bluetoothctl (Bluetooth management)
```

### Installation
```bash
# Install OpenCV
sudo apt-get install python3-opencv

# Install ALSA utilities
sudo apt-get install alsa-utils

# Install Bluetooth utilities
sudo apt-get install bluez bluez-tools
```

## Quick Start

### Running Tests
```bash
# Test camera and face detection
cd ~/the-overseer/pi
python3 camera_test.py

# Test alarm audio (legacy)
python3 alarm_test.py

# View cron jobs
crontab -l
```

### Checking Logs
```bash
# Alarm execution logs
tail -f ~/overseer_logs/alarm_test.log

# Face monitor logs (future)
tail -f ~/overseer_logs/face_monitor.log
```

### Manual Deactivation
```bash
# Stop monitoring (once implemented)
~/the-overseer/pi/scripts/deactivate_monitor.sh
```

## Development Roadmap

See [PROGRESS.md](PROGRESS.md) for detailed phase breakdown.

**Current Phase:** Phase 1 - Core Face Detection Foundation

**Phases:**
1. ✅ **Setup** - Basic alarm, Bluetooth, face detection POC
2. 🔨 **Core Face Detection** - Implement face_monitor.py foundation
3. 📋 **Alarm Control** - Start/stop alarm programmatically
4. 📋 **Wake-Up Logic** - Implement morning alarm loop
5. 📋 **Monitoring Logic** - Implement desk presence tracking
6. 📋 **Integration** - Connect all components
7. 📋 **Production** - Deploy and monitor
8. 📋 **Desktop Integration** - Task verification system

## Configuration

### Key Settings
- **Alarm Time:** 6:30 AM (crontab)
- **Bluetooth MAC:** 88:92:CC:C4:AF:53
- **Check Frequency:** Every 5 seconds
- **Wake-up Re-alarm:** After 30 seconds (6 failed checks)
- **Monitoring Threshold:** 5 minutes absence (60 failed checks)

### File Locations
- **Alarm Audio:** `/home/george/the-overseer/pi/audio/alarm2.wav`
- **Face Model:** `/home/george/the-overseer/pi/model/haarcascade_frontalface_default.xml`
- **Logs:** `~/overseer_logs/`
- **Cron Job:** User crontab (view with `crontab -l`)

## Troubleshooting

### Camera Issues
```bash
# Check if camera is detected
ls /dev/video*

# Test camera access
python3 -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```

### Bluetooth Issues
```bash
# Check speaker connection
bluetoothctl info 88:92:CC:C4:AF:53

# Reconnect speaker
bluetoothctl connect 88:92:CC:C4:AF:53
```

### Audio Issues
```bash
# Test ALSA audio
aplay -D bluealsa ~/the-overseer/pi/audio/alarm2.wav

# Check audio devices
aplay -L | grep -i blue
```

## Privacy & Security

- **All processing runs locally** on your home network
- **No cloud services** or external APIs (except future LeetCode API for verification)
- **Face data not stored** - only real-time detection
- **Camera only active during monitoring hours** (6:30 AM onwards)
- **Manual deactivation available** at any time

## Future Enhancements

- [ ] Task completion verification (LeetCode/job application check)
- [ ] Desktop website blocking until task submitted
- [ ] Web dashboard for monitoring status
- [ ] Configuration file (no hardcoded values)
- [ ] Smart scheduling (skip weekends/holidays)
- [ ] Multiple user support (face recognition)
- [ ] Voice command deactivation
- [ ] Statistics and analytics (wake-up times, productivity tracking)
- [ ] Mobile app notifications

## Contributing

This is a personal project for learning and accountability. Not currently accepting contributions.

## License

Personal project - All rights reserved

## Notes

**Important:** Run `sudo shutdown -h now` when unplugging the Pi to prevent SD card corruption.

---

**Last Updated:** 2025-12-16
**Author:** George
**Version:** 0.1.0-beta
