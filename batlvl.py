import sys
import wmi
import ctypes
import time

connect_flag = True
disconnect_flag = True

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
    global connect_flag, disconnect_flag
    charge_capacity, charge_current, charge_status = get_batstats()
    charge_percentage = charge_current / charge_capacity * 100
    #print str(charge_percentage), str(charge_status)

    #If Annoying Alerts is what you're going for then uncomment the following
    '''
    if not charge_status:
        #If not charging, then "Connect" is possible so...
        connect_flag = True
    else:
        #If charging, then "Disconnect" is possible so...
        disconnect_flag = True
    '''

    if charge_percentage < 40 and not charge_status and connect_flag:
        Mbox('Battery Level Alert', connect_charger, 0)
        #Setting the flags anyway so that the Alert occurs only once whether
        #the user actually plugs the charger in or not (Can get annoying otherwise)
        connect_flag = False
        disconnect_flag = True
    elif charge_percentage > 80 and charge_status and disconnect_flag:
        Mbox('Battery Level Alert', disconnect_charger, 0)
        disconnect_flag = False
        connect_flag = True

while True:
    time.sleep(60)
    print "Once"
    try:
        do_batlogic()
    except:
        break

sys.exit()


