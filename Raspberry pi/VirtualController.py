from evdev import UInput, AbsInfo, ecodes as e

cap = {  e.EV_KEY : [e.KEY_0, e.KEY_1, e.KEY_2, e.KEY_3],
 e.EV_ABS : [ (e.ABS_X, AbsInfo(value=0, min=-512, max=512, 
fuzz=0, flat=0, resolution=0)),
(e.ABS_Y, AbsInfo(0, -512, 512, 0, 0, 0)),
 (e.ABS_MT_POSITION_X, (0, 128, 255, 0)) ]}

ui = UInput(cap, "VirtualController", version=0x1)


ui.write(e.EV_ABS, e.ABS_X, 20)
ui.write(e.EV_ABS, e.ABS_Y, 20)
ui.write(e.EV_KEY, e.KEY_0, 1) #button 0 down
ui.syn()
