import sys
import wmi
import ctypes
import time

#For Development
DEBUG = False
FAIL_SILENTLY = True
ONE_TIME_ALERT_ONLY = True

#Code Init Values
ShouldStartCharging = True
ShouldStopCharging = True

connect_charger = """Battery Level < 40%
Charging State : Disconnected

*** CONNECT CHARGER ***"""

disconnect_charger = """Battery Level > 80%
Charging State  : Connected

*** DISCONNECT CHARGER ***"""

def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxA(0, text, title, style)

def get_batstats():
    #c = wmi.WMI() 
    t = wmi.WMI(moniker = "//./root/wmi")
    batts = t.ExecQuery('Select * from BatteryFullChargedCapacity')
    for i, b in enumerate(batts):
        full_charge = b.FullChargedCapacity * 1.0
    
    batts = t.ExecQuery('Select * from BatteryStatus where Voltage > 0')
    for i, b in enumerate(batts):
        return (full_charge, b.RemainingCapacity, b.Charging)


def do_batlogic():
    global ShouldStartCharging, ShouldStopCharging
    
    charge_capacity, charge_current, charge_status = get_batstats()
    charge_percentage = charge_current / charge_capacity * 100
    if DEBUG:
        print str(charge_percentage), str(charge_status)

    IS_CHARGING = charge_status
    IS_DISCHARGING = not IS_CHARGING

    if IS_DISCHARGING:
        #Reset Start Charging Alter Toggle
        ShouldStopCharging = True
        if DEBUG:
            print "Should Stop Charging == True"
    elif IS_CHARGING:
        #Reset Stop Charging Alert Toggle
        ShouldStartCharging = True
        if DEBUG:
            print "Should Start Charging == True"

    if charge_percentage < 40 and IS_DISCHARGING and ShouldStartCharging:
        Mbox('Battery Level Alert', connect_charger, 0)
        if ONE_TIME_ALERT_ONLY:
            ShouldStartCharging = False
        else:
            pass
    elif charge_percentage > 80 and IS_CHARGING and ShouldStopCharging:
        Mbox('Battery Level Alert', disconnect_charger, 0)
        if ONE_TIME_ALERT_ONLY:
            ShouldStopCharging = False
        else:
            pass

while True:
    time.sleep(5)
    if FAIL_SILENTLY:        
        try:
            if DEBUG:
                print "Cycling..."
            do_batlogic()
        except:
            if DEBUG:
                print "Error... Stopping Cycles"
            break
    else:
       if DEBUG:
                print "Error... Stopping Cycles"
        do_batlogic()

sys.exit()


