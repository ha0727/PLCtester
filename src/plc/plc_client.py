import pymcprotocol

class PLCClient:
    def __init__(self):
        self.client = pymcprotocol.Type3E()
        self.connected = False

    def connect(self, ip_address, port):
        """
        Connects to the PLC.
        Returns a tuple (success: bool, message: str).
        """
        try:
            # Set target PLC
            self.client.setaccessopt(commtype="binary")
            self.client.connect(ip_address, port)
            self.connected = True
            return True, "PLC에 성공적으로 연결되었습니다."
        except Exception as e:
            self.connected = False
            return False, f"PLC 연결 실패: {e}"

    def disconnect(self):
        """Disconnects from the PLC."""
        if self.connected:
            self.client.close()
            self.connected = False
            print("Disconnected from PLC.")

    def read_device(self, device, size=1):
        """
        Reads a value from a device.
        Example: read_device("D100", 1)
        """
        if not self.connected:
            raise ConnectionError("PLC is not connected.")
        return self.client.batchread_wordunits(headdevice=device, readsize=size)

    def write_device(self, device, values):
        """
        Writes values to a device.
        Example: write_device("D100", [123])
        """
        if not self.connected:
            raise ConnectionError("PLC is not connected.")
        self.client.batchwrite_wordunits(headdevice=device, values=values)
