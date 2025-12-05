class FBootBuilder:
    def __init__(self, resource):
        self.resource = resource
        self.req_id = 1
        self.commands = []

    def create_workspace(self, name, fbtype):
        first_req = ''';<Request Action="QUERY" ID="1"><FB Name="*" Type="*"/></Request>'''
        self.commands.append(first_req)
        self.req_id += 1

        prefix = ";"
        cmd = f"{prefix}<Request ID='{self.req_id}' Action='CREATE'>"
        cmd += f"<FB Name='{name}' Type='{fbtype}'/>"
        cmd += "</Request>"
        self.commands.append(cmd)
        self.req_id += 1


    def add_fb(self, name, params):
        # For the first command use leading ';'
        # Parameters
        for p in params:
            prefix = f"{self.resource};"
            pname = p["name"]
            pval = p["value"]
            cmd = f"{prefix}<Request ID='{self.req_id}' Action='WRITE'>"
            cmd += f"<FB Name='{name}'><Parameter Name='{pname}' Value=\"{pval}\"/></FB>"
            cmd += "</Request>"
            self.commands.append(cmd)
            self.req_id += 1


    def add_connection(self, source, dest):
        prefix = f"{self.resource};"
        cmd = f"{prefix}<Request ID='{self.req_id}' Action='CREATE'>"
        cmd += f"<Connection Source='{source}' Destination='{dest}'/>"
        cmd += "</Request>"
        self.commands.append(cmd)
        self.req_id += 1

    def add_start(self):
        prefix = f"{self.resource};"
        cmd = f"{prefix}<Request ID='{self.req_id}' Action='START'/>"
        self.commands.append(cmd)


    def build(self):
        return self.commands
