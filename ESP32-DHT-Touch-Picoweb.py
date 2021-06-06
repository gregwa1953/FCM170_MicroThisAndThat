import machine
import utime
import dht
import picoweb
 
ip_address = None
temp_history = {"temperature": [], "humidity": []}
temp_minute_counter = 0
r_led_state = False
g_led_state = False
b_led_state = False
btn_press_counter = 0
 
r_led = machine.Pin(13, machine.Pin.OUT)
g_led = machine.Pin(12, machine.Pin.OUT)
b_led = machine.Pin(14, machine.Pin.OUT)
 
touch7 = machine.TouchPad(machine.Pin(27))
touch8 = machine.TouchPad(machine.Pin(33))
touch9 = machine.TouchPad(machine.Pin(32))
 
def do_connect():
    import network
    global ip_address
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('YourNetworkRouterSSID', 'YourNetworkPassword')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    ip_address = sta_if.ifconfig() [0]
 
 
def extIntHandler(pin):
  global btn_press_counter
  btn_press_counter += 1
 
def timerIntHandler_temperature(timer):
    global temp_minute_counter, temp_history
 
    if temp_minute_counter == 60:
        temp_minute_counter = 0
        d.measure()
        temp_history['temperature'].append(d.temperature())
        temp_history['humidity'].append(d.humidity())
        if len(temp_history['temperature']) > 60:
            del temp_history['temperature'][0]
            del temp_history['humidity'][0]
     
    temp_minute_counter += 1
 
def timerIntHandler_touch(timer):
    global r_led_state, g_led_state, b_led_state
 
    t7 = touch7.read()
    if t7 < 200:
        r_led.value(1)
        r_led_state = True
    else:
        r_led.value(0)
        r_led_state = False
 
    t8 = touch8.read()
    if t8 < 200:
        g_led.value(1)
        g_led_state = True
    else:
        g_led.value(0)
        g_led_state = False
 
    t9 = touch9.read()
    if t9 < 200:
        b_led.value(1)
        b_led_state = True
    else:
        b_led.value(0)
        b_led_state = False
 
do_connect()
 
d = dht.DHT22(machine.Pin(23))
 
dht22_timer = machine.Timer(0)
dht22_timer.init(period=1000, mode=machine.Timer.PERIODIC, callback=timerIntHandler_temperature)
 
touch_timer = machine.Timer(1)
touch_timer.init(period=500, mode=machine.Timer.PERIODIC, callback=timerIntHandler_touch)
 
p22 = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_UP)
p22.irq(trigger=machine.Pin.IRQ_FALLING, handler=extIntHandler)
 
app = picoweb.WebApp(__name__)
 
@app.route("/")
def send_index(req, resp):
    yield from app.sendfile(resp, 'index.html')
 
@app.route("/get_temp_history")
def get_temp_history(req, resp):
    global temp_history
    yield from picoweb.jsonify(resp, temp_history)
 
@app.route("/get_ext_int_count")
def get_ext_int_count(req, resp):
    global btn_press_counter
    yield from picoweb.jsonify(resp, {'btn_press_counter': btn_press_counter})
 
@app.route("/get_touch_states")
def get_touch_states(req, resp):
    touch_states = {"r_led_state": r_led_state, 
                        "g_led_state": g_led_state, 
                        "b_led_state": b_led_state}
    yield from picoweb.jsonify(resp, touch_states)
 
app.run(debug=1, host=ip_address, port=80)
