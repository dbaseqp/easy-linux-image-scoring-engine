# authors: Gabriel Fok

from subprocess import Popen
from tempfile import TemporaryFile
import json
import os
import sys
import getpass
import math
import itertools
import re
import subprocess
from time import sleep
from datetime import datetime, date, timedelta
import requests
import json
import hashlib
import base64
import ast
import random
import string
import urllib

UNSCORED = 0
SCORED = 1
PENALTY = 2
INVALID = 3
IMAGE_NAME = "INSERT_IMAGE_NAME"
DEFAULT_USER = "CHANGE_ME"

class Vuln:
    points = 0
    comment = ''
    
    def __init__(self, points, comment):
        self.points = points
        self.comment = comment
    
    def __str__(self):
        comment = self.comment
        points = self.points
        return f'{comment} - {points}'

class ForensicsObject(Vuln):
    id = 0
    answer = ''

    def __init__(self, points, comment, id, answer):
        super().__init__(points,comment)
        self.id = id
        self.answer = answer
    
    def check(self):
        user = DEFAULT_USER
        id = self.id
        with open(f'/home/{user}/Desktop/Forensics_{id}.txt') as f:
            for line in f.readlines():
                if 'ANSWER: ' in line and self.answer in line:
                    return self
        return False

def write_scores(imageName, vuln_lines, currPoints, current_vulns, totalVulns, name):
    with open('/opt/temp/template.html', 'r') as template:
        with open('/opt/temp/ScoringReport.html', 'w') as output_file:
            for line in template:
                if line.strip() == '{{LIST}}':
                    for vulnLine in vuln_lines:
                        output_file.write(vulnLine)
                else:
                    newLine = line
                    newLine = newLine.replace('{{IMAGENAME}}', imageName)
                    newLine = newLine.replace('{{POINTS}}', str(currPoints))
                    newLine = newLine.replace('{{TOTALPOINTS}}', str(total_points))
                    newLine = newLine.replace('{{CURRENT}}', str(current_vulns))
                    newLine = newLine.replace('{{VULNS}}', str(totalVulns))
                    newLine = newLine.replace('{{RUNTIME}}', runtime)
                    newLine = newLine.replace('{{NAME}}', name)
                    output_file.write(newLine)

"""
Store time in a temporary file to prevent time resets when engine restarts.
"""
def store_time():
    with open("/opt/temp/time.txt", "w+") as f:
        start = datetime.now()
        f.write(str(start.year)+'\n')
        f.write(str(start.month)+'\n')
        f.write(str(start.day)+'\n')
        f.write(str(start.hour)+'\n')
        f.write(str(start.minute)+'\n')
        f.write(str(start.second)+'\n')

"""
Get time from temporary file.

:rtype: (int hours, int mins)
"""
def get_time():
    with open("/opt/temp/time.txt", "r") as f: 
        year = int(f.readline())
        month = int(f.readline())
        day = int(f.readline())
        hour = int(f.readline())
        minute = int(f.readline())
        second = int(f.readline())
    return datetime(year,month,day,hour,minute,second)

######
#PUT VULNS BELOW:
#ex: vulns.append(ForensicsObject(10, 'Bob found', 1, 'bob'))
vulns = []
vulns.append(ForensicsObject(10, 'Bob found', 1, 'bob'))

def main():
    global runtime
    global total_points
    
    if not os.path.exists('/opt/temp/time.txt') or os.path.getsize('/opt/temp/time.txt') == 0:
        store_time()
    
    if os.path.exists('/home/' + DEFAULT_USER + '/Desktop/Set Name for Scoring Report'):
        with open("/home/" + DEFAULT_USER + "/Desktop/Set Name for Scoring Report", "r") as f:
            name = name_file.readline()
            name = name[16:-1]
    else:
        name = 'COMPETITOR NOT SET'

    total_points = 0
    for vuln in vulns:
        total_points += vuln.points

    while True:
        vuln_lines = []
        curr_points = 0
        current_vulns = 0
        check_time = datetime.now()
        for vuln in vulns:
            result = vuln.check()
            if not result == False:
                curr_points += result.points
                current_vulns += 1
                vuln_lines.append(str(result) + '<br>\n')

        # calculate run time from start time
        start_time = get_time()
        runtime = str(datetime.now() - start_time)

        # write scores to file
        write_scores(IMAGE_NAME, vuln_lines, curr_points, current_vulns, len(vulns), name)
        
        # refresh after minimum 30 secs
        while((datetime.now() - check_time) < timedelta(seconds=30)):
            sleep(1)
main()
