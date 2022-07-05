import sys
import os
import csv
import sys
import subprocess
import platform
import webbrowser
from platform import python_version


def send_notification(message):
    if platform.system() == "Windows":
        subprocess.call(f"C:\\Windows\\system32\\msg.exe * {message}",shell=True)
    elif platform.system() == "Darwin":
        pass    # subprocess.Popen(["open", folder])
    else:
        os.system(f'notify-send {message}')

try:
    import kicad_netlist_reader
    import pentagon_hacker
except ImportError:
    send_notification("kicad_netlist_reader is not installed!")
    print("Please run pip install kicad_netlist_reader")
    sys.exit()


def open_file(folder, full_path):
    if platform.system() == "Windows":
        # print(f'{folder}/{file}')
        path = full_path.replace("/", "\\")
        os.system(f'%windir%\\explorer /select, {path}')
        # os.startfile(f'{full_path}.csv', 'explore')
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", folder])
    else:
        subprocess.call(["nautilus", f"{full_path}"])


def main(input_file, output_file):
    if output_file.find(".csv") == -1:
        output_file += ".csv"
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
    open_file(folder_path, output_file)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])