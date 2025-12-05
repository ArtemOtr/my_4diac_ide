from parser_appsys import AppSysParser
from graph_view import FBGraphView
from fboot_builder import FBootBuilder
from forte_client import ForteClient

def main():
    print("=== MINI 4DIAC IDE ===")

    filename = input("Введите путь к .sys: ")

    # Parse system
    p = AppSysParser(filename).parse()

    print("Найдено FB:", len(p.blocks))
    print("Найдено event connections:", len(p.event_connections))
    print("Найдено data connections:", len(p.data_connections))
    print("Ресурс:", p.resource)

    # Draw graph
    FBGraphView(p.blocks, p.event_connections, p.data_connections).show()

    # Build fboot commands
    fb = FBootBuilder(p.resource)

    for b in p.blocks:
        params = p.params.get(b["name"], [])
        fb.add_fb(b["name"], b["type"], params)

    for c in p.event_connections:
        fb.add_connection(c[0], c[1])
    for c in p.data_connections:
        fb.add_connection(c[0], c[1])

    fb.add_start()
    cmds = fb.build()

    # Send to forte
    cl = ForteClient()
    cl.connect()
    for c in cmds:
        print("SEND:", c)
        cl.send_cmd(c)
    cl.close()

if __name__ == "__main__":
    main()
