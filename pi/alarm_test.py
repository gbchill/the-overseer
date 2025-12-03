import os #python module for executing system commands

os.system('amixer -c 0 set PCM 50%')
print("Alarm is starting")

try:
    while True:
        print("ALARM!")
        result = os.system('mpg123 -q -a hw:0,0 /home/george/the-overseer/alarm2.mp3')  #this is the command to run the alarm
        #have to include this below bc mpg123 returns 0 on success and it keeps looping the alarm need to get out
        if result != 0:
            break
            
except KeyboardInterrupt:
    print("\nAlarm stopped by user")