import sys
import os
import csv
import sys
import subprocess
import platform
import webbrowser
from platform import python_version
try:
    import kicad_netlist_reader
except ImportError:
    os.system('notify-send "kicad_netlist_reader is not installed!"')
    print("Please run pip install kicad_netlist_reader")
    sys.exit()


def open_file(folder, file):
    print(platform.system())
    if platform.system() == "Windows":
        os.startfile(folder)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", folder])
    else:
        # subprocess.Popen(["xdg-open", '/select', file])
        subprocess.call(["nautilus", f"{folder}/{file}"])


def main(input_file, output_file):
    if python_version()[0] != '3':
        print("You are trying to run this script with Python 2! Run it with python 3")
        sys.exit()
    net = kicad_netlist_reader.netlist(input_file)
    try:
        f = open(output_file, 'w')
    except IOError:
        e = "Can't open output file for writing: " + output_file
        print(__file__, ":", e, sys.stderr)
        f = sys.stdout

    out = csv.writer(f, lineterminator='\n', delimiter=';', quotechar='\"', quoting=csv.QUOTE_ALL)

    out.writerow(['Component Count:', len(net.components)])
    out.writerow(['Reference', 'Quantity', 'Value', 'Footprint'])

    grouped = net.groupComponents()

    for group in grouped:
        refs = ""
        c = None
        for component in group:
            refs += component.getRef() + ", "
            c = component

        footprint = c.getFootprint().split(":")[1]  # get only footprint name, without library name
        out.writerow([refs, len(group), c.getValue(), footprint])
    f.close()
    filename = output_file.split("/")[-1]
    folder_path = output_file.replace(f"/{filename}", '')
    open_file(folder_path, filename)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])