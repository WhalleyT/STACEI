from distutils.dir_util import copy_tree
from shutil import rmtree

import os
import inspect

"""
This module is used to generate our output into a HTML file
"""

def create_copy(directory_path):
    """
    Copy our master copy to the output directory
    """

    full_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    full_path = "/".join(full_path.split("/")[:-1]) + "/web"

    copy_tree(full_path, directory_path)

def rewrite_file(file, keywords, name, file_named = True):
    data = []

    with open(file) as f:
        for line in f:
            data.append(line)


    #now replace our lines
    outdata = []

    for line in data:
        for keyword in keywords:
            if keyword in line:
                if file_named:
                    line = line.replace(keyword, keyword + name + "_")
        outdata.append(line)

    replacement_file = open(file, "w")

    for outline in outdata:
        replacement_file.write(outline)


def fill_crossing_params(html, cangle):
    crossing_angle, rotation_angle, tilt_angle = None, None, None

    with open(cangle) as f:
        for line in f:
            if "Crossing angle (Rudolph 3D angle)" in line:
                crossing_angle = line.split()[-1]
            if "Rotation angle (2D crossing angle)" in line:
                rotation_angle = line.split()[-1]
            if "Tilt angle (2D elevation away from MHC)" in line:
                tilt_angle = line.split()[-1]


    replacement_dict = {"CROSSING_VAR": crossing_angle,
                        "ROTATION_VAR": rotation_angle,
                        "TILT_VAR": tilt_angle}

    vars_of_interest = ["CROSSING_VAR", "ROTATION_VAR", "TILT_VAR"]

    data = []

    with open(html) as f:
        for line in f:
            data.append(line)

    outdata = []

    for line in data:
        for var in vars_of_interest:
            if var in line:
                line = line.replace(var, replacement_dict[var])
        outdata.append(line)

    replacement_file = open(html, "w")

    for outline in outdata:
        replacement_file.write(outline)



def make_html(path, id):
    create_copy(path)

    #rewrite the general file
    print("writing file for general visualisations")
    rewrite_file(path + "/gen_vis.html", ["sessions/", "visualisation/"], id)

    #rewrite the crossing angle html
    print("writing file for crossing angle")
    rewrite_file(path + "/cross_ang.html", ["crossingAngle/", "sessions/"], id)
    fill_crossing_params(path + "/cross_ang.html", path + "/crossingAngle/" + id + "_crossingAngle.txt")

    #rewrite CDR loops
    print("writing file for CDR loops")
    rewrite_file(path + "/CDR_pos.html", ["visualisation/", "sessions/"], id)

    #omit map
    print("writing file for omit map")
    rewrite_file(path + "/pep_density.html", ["sessions/"], id)
