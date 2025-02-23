# RFID_src/SimpleMFRC522.py
import pprint

from .MFRC522 import MFRC522

class SimpleMFRC522:

    def __init__(self):
        self.READER = MFRC522()

    def __repr__(self):
        return f"<SimpleMFRC522(READER={self.READER})>"
#         return f"SimpleMFRC522()"

    def read(self):
        id, text = self.read_no_block()
#         while not id:
#             id, text = self.read_no_block()
        return id, text

    def read_no_block(self):
        (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
        if status != self.READER.MI_OK:
            return None, None

        (status, uid) = self.READER.MFRC522_Anticoll()
        if status != self.READER.MI_OK:
            return None, None

        id = 0
        for i in range(0, 5):
            id += uid[i] << (i * 8)

        self.READER.MFRC522_SelectTag(uid)
        status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, 8, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], uid)
        print("Self?")
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self)
        if status != self.READER.MI_OK:
            print('Break1',status)
            return None, None
        # loop through the 16 sectors and print the data
#         for sector in range(0, 16):
#             self.READER.MFRC522_Read(sector)
#             print('Sector:',sector)

        data = self.READER.MFRC522_Read(8)
        print('Data:',data)
        user = self.READER.MFRC522_Read(1)
        print('User:',user)
        self.READER.MFRC522_StopCrypto1()

        if data:
            name = ''.join(chr(i) for i in user if i != 0)
            text = ''.join(chr(i) for i in data if i != 0)
            print('name',name)
            print('id',id)
            print('text',text)
            return id, text
        else:
            print('Break3',status)
            return None, None

    def write(self, text):
        id, _ = self.read()
        self.READER.MFRC522_SelectTag(id)
        status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, 8, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], id)
        if status != self.READER.MI_OK:
            raise Exception('Authentication error')

        data = [ord(c) for c in text]
        if len(data) < 16:
            data = data + [0] * (16 - len(data))
        self.READER.MFRC522_Write(8, data)
        self.READER.MFRC522_StopCrypto1()