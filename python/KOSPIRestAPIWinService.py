### Run Python scripts as a service example (ryrobes.com)
### Usage : python aservice.py install (or / then start, stop, remove)

import win32service
import win32serviceutil
import win32api
import win32con
import win32event
import win32evtlogutil
import os, sys, string, time

from server import make_server, start_server, stop_server

class aservice(win32serviceutil.ServiceFramework):
   
    _svc_name_ = "KOSPIRestAPI"
    _svc_display_name_ = "KOSPI Rest API Windows Service."
    _svc_description_ = "Provide RESTful APIs for KOSPI data."
    _path_ = os.path.dirname(os.path.abspath(__file__))
    _server_ = None
         
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        if not self._server_:
            self._server_ = make_server()
        stop_server(self._server_)
         
    def SvcDoRun(self):
        import servicemanager      
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,servicemanager.PYS_SERVICE_STARTED,(self._svc_name_, '')) 

        #self.timeout = 640000    #640 seconds / 10 minutes (value is in milliseconds)
        self.timeout = 120000     #120 seconds / 2 minutes
        # This is how long the service will wait to run / refresh itself (see script below)

        while 1:
            # Wait for service stop signal, if I timeout, loop again
            rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            # Check to see if self.hWaitStop happened
            if rc == win32event.WAIT_OBJECT_0:
                # Stop signal encountered
                if not self._server_:
                    self._server_ = make_server()
                stop_server(self._server_)
                servicemanager.LogInfoMsg(self._svc_name_ + " - STOPPED!")  #For Event Log
                break
            else:
                try:
                    servicemanager.LogInfoMsg(self._svc_name_ + " - STARTING!")
                    # if not self._server_:
                        # self._server_ = make_server()
                    # start_server(self._server_)
                    file_path = self._path_ + "\server.py"
                    exec(open(file_path).read())             #Execute the script
                except:
                    pass


def ctrlHandler(ctrlType):
    return True

                  
if __name__ == '__main__':   
    win32api.SetConsoleCtrlHandler(ctrlHandler, True)   
    win32serviceutil.HandleCommandLine(aservice)
