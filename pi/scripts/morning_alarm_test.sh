#!/bin/bash
#run the script run ./morning_alarm_test.sh while inside scripts folder
# Morning alarm test just to see if cron job works
#logs if errors 
LOG_FILE="$HOME/overseer_logs/alarm_test.log"
mkdir -p "$(dirname "$LOG_FILE")"

# Log the execution
echo "===========================================" >> "$LOG_FILE"
echo "Alarm test executed at: $(date)" >> "$LOG_FILE"

# Check if Bluetooth speaker is connected
SPEAKER_MAC="88:92:CC:C4:AF:53"
BT_STATUS=$(bluetoothctl info "$SPEAKER_MAC" | grep "Connected: yes")

if [ -z "$BT_STATUS" ]; then
    echo "ERROR: Bluetooth speaker not connected. Attempting to connect..." >> "$LOG_FILE"
    bluetoothctl connect "$SPEAKER_MAC" >> "$LOG_FILE" 2>&1
    sleep 3
fi

# Play alarm2.wav through Bluetooth speaker - 20 times for ~30 seconds
echo "Playing LOUD alarm (20 iterations)..." >> "$LOG_FILE"
for i in {1..2}; do
    aplay -D bluealsa "$HOME/the-overseer/pi/audio/alarm2.wav" >> "$LOG_FILE" 2>&1
    echo "Play iteration $i completed" >> "$LOG_FILE"
done

echo "Alarm completed at: $(date)" >> "$LOG_FILE"
echo "===========================================" >> "$LOG_FILE"