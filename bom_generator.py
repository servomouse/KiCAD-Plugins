"""
    @package
    Output: CSV (comma-separated)
    Grouped By: Value, Footprint
    Sorted By: Ref
    Fields: Ref, Qnty, Value, Cmp name, Footprint, Description, Vendor
    Command line:
    python "pathToFile/bom_csv_grouped_by_value_with_fp.py" "%I" "%O.csv"
"""

# Import the KiCad python helper module and the csv formatter
import kicad_netlist_reader
import csv
import sys
from platform import python_version

def main(input_file, output_file):
    # Generate an instance of a generic netlist, and load the netlist tree from
    # the command line option. If the file doesn't exist, execution will stop
    if python_version()[0] != '3':
        print("You are trying to run this script with Python 2! Run it with python 3")
        raise SystemExit
    net = kicad_netlist_reader.netlist(input_file)
    # Open a file to write to, if the file cannot be opened output to stdout
    # instead
    # filename = output_file.replace("/", "\\")
    try:
        f = open(output_file, 'w')
    except IOError:
        e = "Can't open output file for writing: " + output_file
        print(__file__, ":", e, sys.stderr)
        f = sys.stdout

    # Create a new csv writer object to use as the output formatter
    out = csv.writer(f, lineterminator='\n', delimiter=';', quotechar='\"', quoting=csv.QUOTE_ALL)

    # Output a set of rows for a header providing general information
    out.writerow(['Component Count:', len(net.components)])
    out.writerow(['Ref', 'Qnty', 'Value', 'Footprint'])

    # Get all of the components in groups of matching parts + values
    # (see ky_generic_netlist_reader.py)
    grouped = net.groupComponents()

    # Output all of the component information
    for group in grouped:
        refs = ""
        c = None
        # Add the reference of every component in the group and keep a reference
        # to the component so that the other data can be filled in once per group
        for component in group:
            refs += component.getRef() + ", "
            c = component

            # Fill in the component groups common data
        footprint = c.getFootprint().split(":")[1]
        out.writerow([refs, len(group), c.getValue(), footprint])


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])