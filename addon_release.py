#!/usr/bin/env python

##############################################################################
# Addon Releng Script
#
# Prepares an addon for release.
# Depends on version numbers being in the x.y.z
##############################################################################
import time
import argparse
import sys
import os.path
import xml.etree.ElementTree as ET
import zipfile
import tempfile
import shutil

parser = argparse.ArgumentParser(description='Addon Releng Script')
parser.add_argument('--addon', help='Root directory of addon', dest='addon', required=True)
parser.add_argument('--repo', help='Repo directory', dest='repo', required=True)
parser.add_argument('--patch', help='Increase patch version', dest='patch', action='store_true')
parser.add_argument('--minor', help='Increase minor version', dest='minor', action='store_true')
parser.add_argument('--major', help='Increase major version', dest='major', action='store_true')

def log(msg):    
    sys.stdout.write("[%s] %s\n" % (time.strftime("%c"), msg))

args = parser.parse_args()

repo_dir = os.path.abspath(args.repo)
addon_dir = os.path.abspath(args.addon)

tree = ET.parse("%s/addon.xml" % addon_dir)
root = tree.getroot()

version = root.attrib['version']
id = root.attrib['id']
log("Found addon: %s v%s" % (id, version))

ver_parts = version.split('.')

if (len(ver_parts) == 1):
    ver_parts[1] = 0
    ver_parts[2] = 0

elif (len(ver_parts) == 2):
    ver_parts[2] = 0

if (args.patch):
    ver_parts[2] = int(ver_parts[2]) + 1

if (args.minor):
    ver_parts[1] = int(ver_parts[1]) + 1

if (args.major):
    ver_parts[0] = int(ver_parts[0]) + 1

new_version = '.'.join("{0}".format(n) for n in ver_parts)
root.attrib['version'] = new_version
tree.write("%s/addon.xml" % addon_dir)

log("Addon %s updated to version %s" % (id, new_version))

temp_zip = tempfile.gettempdir() + "/psikon-xbmc/releng/%s-%s.zip" % (id, new_version)
dest_zip = "%s/%s/%s-%s.zip" % (repo_dir, id, id, new_version)
log("Creating zipfile at %s" % temp_zip)

if not os.path.exists(os.path.dirname(temp_zip)):
    os.makedirs(os.path.dirname(temp_zip))

if not os.path.exists(os.path.dirname(dest_zip)):
    os.makedirs(os.path.dirname(dest_zip))

if os.path.isfile(temp_zip):
    os.remove(temp_zip)

zf = zipfile.ZipFile(temp_zip, mode='w')

try:
    for root, dirs, files in os.walk(addon_dir):
        zip_dir = root.replace(addon_dir, id)
        for f in files:
            zf.write(os.path.join(root, f), arcname=zip_dir + "/" + f)

    shutil.move(temp_zip, dest_zip)
finally:
    zf.close()



