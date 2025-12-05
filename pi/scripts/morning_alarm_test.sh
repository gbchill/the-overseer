#!/bin/bash
#run the script run ./morning_alarm_test.sh while inside sripts folder
# morning alaarm test just to see if cron job works
#logs if erros 
LOG_FILE="$HOME/overseer_logs/alarm_test.log"


mkdir -p "$(dirname "$LOG_FILE")"

# Log the execution
echo "===========================================" >> "$LOG_FILE"
echo "Alarm test executed at: $(date)" >> "$LOG_FILE"

# Check if Bluetooth speaker is connected
SPEAKER_MAC="88:92:CC:C4:AF:53"  # Replace with your speaker's MAC if different
BT_STATUS=$(bluetoothctl info "$SPEAKER_MAC" | grep "Connected: yes")

if [ -z "$BT_STATUS" ]; then
    echo "ERROR: Bluetooth speaker not connected. Attempting to connect..." >> "$LOG_FILE"
    bluetoothctl connect "$SPEAKER_MAC" >> "$LOG_FILE" 2>&1
    sleep 3
fi

# play test sound for 1 seconds total of 2 times
echo "Playing test alarm sound..." >> "$LOG_FILE"
for i in {1..2}; do
    aplay -D bluealsa /usr/share/sounds/alsa/Front_Center.wav >> "$LOG_FILE" 2>&1
    echo "Play iteration $i completed" >> "$LOG_FILE"
done

echo "Alarm test completed at: $(date)" >> "$LOG_FILE"
echo "===========================================" >> "$LOG_FILE"


