import sys
while True:
        try:
                execfile("agent.py")
        except:
                try:
                        ser.close()
                except:
                        print "No serial!"
                print "Error!"

