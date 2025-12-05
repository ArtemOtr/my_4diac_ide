import xml.etree.ElementTree as ET

class AppSysParser:
    def __init__(self, filename):
        self.filename = filename

        self.blocks = []          # {name,type}
        self.params = {}          # name -> list of parameters
        self.event_connections = []
        self.data_connections = []
        self.resource = None      # EMB_RES
        self.device = None        # FORTE_PC
        self.mapping = []         # FB → Resource

    def parse(self):
        tree = ET.parse(self.filename)
        root = tree.getroot()

        app = root.find(".//Application")

        # ------------------------------
        # Parse FB blocks
        # ------------------------------
        for fb in app.findall(".//SubAppNetwork/FB"):
            name = fb.attrib["Name"]
            fbtype = fb.attrib["Type"]
            self.blocks.append({"name": name, "type": fbtype})

            # Parse parameters
            params = []
            for p in fb.findall("Parameter"):
                params.append({
                    "name": p.attrib["Name"],
                    "value": p.attrib["Value"]
                })
            self.params[name] = params

        # ------------------------------
        # Parse event connections
        # ------------------------------
        for conn in app.findall(".//EventConnections/Connection"):
            self.event_connections.append(
                (conn.attrib["Source"], conn.attrib["Destination"])
            )

        # ------------------------------
        # Parse data connections
        # ------------------------------
        for conn in app.findall(".//DataConnections/Connection"):
            self.data_connections.append(
                (conn.attrib["Source"], conn.attrib["Destination"])
            )

        # ------------------------------
        # Parse Device and Resource
        # ------------------------------
        dev = root.find(".//Device")
        if dev is not None:
            self.device = dev.attrib["Name"]

            res = dev.find("Resource")
            if res is not None:
                self.resource = res.attrib["Name"]

        # ------------------------------
        # Parse Mapping
        # ------------------------------
        for mp in root.findall("Mapping"):
            fb_name = mp.attrib["From"].split(".")[1]
            res = mp.attrib["To"]
            self.mapping.append((fb_name, res))

        return self
