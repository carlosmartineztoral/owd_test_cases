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
from tests.mock_data.contacts import MockContacts

class test_6036(GaiaTestCase):
    _Description = "CLONE - Verify that If the name of the contact is empty: The type of the phone (as defined in the address book) and the phone carrier (if available) as the secondary header."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        
        #
        # Import contact (adjust to the correct number).
        #
        self.Contact_1 = MockContacts().Contact_1
        self.Contact_1["givenName"] = ""
        self.Contact_1["familyName"] = ""
        self.Contact_1["name"] = ""
        self.Contact_1["tel"]["value"] = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Using target telephone number " + self.Contact_1["tel"]["value"])
        self.data_layer.insert_contact(self.Contact_1)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Send a message to create a thread (use number, not name as this
        # avoids some blocking bugs just now). 
        #
        self.messages.createAndSendSMS( [self.Contact_1["tel"]["value"]], "Test message.")
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Examine the carrier.
        #
        expect = self.Contact_1["tel"]["type"]
        actual = self.messages.threadType()
        self.UTILS.TEST(expect == actual, "The type is listed as: '" + expect + "' (subheader was '" + actual + "').")
        
        expect = self.Contact_1["tel"]["carrier"]
        actual = self.messages.threadCarrier()
        self.UTILS.TEST(expect == actual, "The carrier is listed as: '" + expect + "' (subheader was '" + actual + "').")
        
