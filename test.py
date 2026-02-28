from directkeys import PressKey, ReleaseKey, right_pressed
import time

print("Pressing right key in 2 seconds...")
time.sleep(2)

PressKey(right_pressed)
time.sleep(2)
ReleaseKey(right_pressed)

print("Done")