#!/bin/bash

device='/dev/input/event0'
event_select_press='*code 314 (BTN_SELECT), value 1*'
event_select_release='*code 314 (BTN_SELECT), value 0*'
event_scroll_down_press='*code 178 (KEY_SCROLLDOWN), value 1*'
event_scroll_down_release='*code 178 (KEY_SCROLLDOWN), value 0*'
event_power='*code 116 (KEY_POWER), value 1*'
event_restart='*code 408 (KEY_RESTART), value 1*'

evtest "$device" | while read line; do
  case $line in
    ($event_select_press)        echo "SELECT press" ;;
    ($event_select_release)      echo "SELECT release" ;;
    ($event_scroll_down_press)   echo "SCROLl DOWN press" ;;
    ($event_scroll_down_release) echo "SCROLl DOWN release" ;;
    ($event_power)               echo "POWER" ;;
    ($event_restart)             echo "RESTART" ;;
  esac
done
