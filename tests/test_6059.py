#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#
import time

class test_6059(GaiaTestCase):
    _Description = "Try send a sms in an existing thread while airplane is enabled."
    
    _TestMsg     = "Test."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS     = UTILS(self)
        self.messages   = Messages(self)

        #
        # Open sms app and delete every thread to start a new one
        #
        self.messages.launch()
        self.messages.deleteAllThreads()

        #
        # Create a new SMS
        #
        self.messages.startNewSMS()
        
        #
        # Insert the phone number in the To field
        #
        self.messages.addNumberInToField(self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM"))

        #
        # Create SMS.
        #
        self.messages.enterSMSMsg(self._TestMsg)
        
        #
        # Click send.
        #
        self.messages.sendSMS()
        
        #
        # Wait for the SMS to arrive.
        #
        self.messages.waitForReceivedMsgInThisThread()
        
        time.sleep(10)
        
        #
        # Put the phone into airplane mode.
        #
        self.UTILS.toggleViaStatusBar('airplane')
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Open sms app and go to the previous thread
        #
        self.messages.launch()
        self.messages.openThread(self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM"))
        
        #
        # Create another SMS.
        #
        self.messages.enterSMSMsg(self._TestMsg)
        
        #
        # Click send.
        #
        self.messages.sendSMS()

        #
        # Check that popup appears.
        #
        self.messages.checkAirplaneModeWarning()