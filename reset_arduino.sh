ARDUINO_UPLOAD_PORT="$(find /dev/ttyACM* | head -n 1)"
/home/mate/.arduino15/packages/arduino/tools/avrdude/6.3.0-arduino9/bin/avrdude -C/home/mate/.arduino15/packages/arduino/tools/avrdude/6.3.0-arduino9/etc/avrdude.conf -v -patmega32u4 -cavr109 -P${ARDUINO_UPLOAD_PORT} -b57600 -D -Uflash:w:/tmp/arduino_build_683884/temp_upload.ino.hex:i --timeout 100

# find the Arduino port
ARDUINO_UPLOAD_PORT="$(find /dev/ttyACM* | head -n 1)"

# reset the Arduino
stty -F "${ARDUINO_UPLOAD_PORT}" 1200


# wait for it...
while :; do
  sleep 0.5
  sleep 1
  [ -c "${ARDUINO_UPLOAD_PORT}" ] && break
done


echo ${ARDUINO_UPLOAD_PORT}
echo $(find /dev/ttyACM* | head -n 1)
# ...upload!
#avrdude "${OPTIONS[@]}"
