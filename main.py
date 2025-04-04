import pdfplumber
import csv
import re

pdf_path = "UNC - Course Catalog - 2242-SSB-10-9-23.pdf"
csv_path = "Spring-2024_course_offerings.csv"

# pattern
course_start_pattern = re.compile(r"\b([A-Z]{2,4})\s+(\d{2,3})\s+(\d{3})\s+(\d+)\s+(.+?)Lecture\s+(\d+)", re.DOTALL)

def extract_course_blocks(text):
    matches = list(course_start_pattern.finditer(text))
    blocks = []
    for i in range(len(matches)):
        start = matches[i].start()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        blocks.append(text[start:end])
    return blocks

def parse_block(block):
    header = course_start_pattern.search(block)
    if not header:
        return None

    subject = header.group(1).strip()
    catalog = header.group(2).strip()
    section = header.group(3).strip()
    class_number = header.group(4).strip()
    raw_title = header.group(5).strip().replace('\n', ' ')
    title = re.sub(r"\s+(Bldg:|Room:|Days:|Time:).*", "", raw_title).strip()
    units = header.group(6).strip()
    
    # default
    building = room = days = time = instructor = ""

    bldg_match = re.search(
        r"Bldg:\s*(.*?)(?=Room:)\s*Room:\s*(.*?)\s+Days:\s*(.*?)\s+Time:\s*(.*?)\s*(?:\n|$)",
        block, re.DOTALL
    )

    if bldg_match:
        building = bldg_match.group(1).strip()
        room = bldg_match.group(2).strip()
        days = bldg_match.group(3).strip()
        time = bldg_match.group(4).strip()

    else:
        print(f"[!] Missing time/building info for {subject} {catalog} {section} ({class_number})")

    instructor_match = re.search(r"Instructor:\s*([^\n]+)", block)
    if instructor_match:
        instructor = instructor_match.group(1).strip()

    missing_info = any(
        field.strip() == "" for field in [days, time, building, room]
    )
    return [
        subject, catalog, section, class_number, title,
        units, days, time, building, room, instructor, missing_info
    ]

rows = []

import sys
import os

# write to csv
with pdfplumber.open(pdf_path) as pdf:
    page_count = 1
    for page in pdf.pages:
        os.system('cls' if os.name == 'nt' else 'clear') # clear terminal
        print(f"Parsing page {page_count}...", flush=True)
        text = page.extract_text()
        blocks = extract_course_blocks(text)
        for block in blocks:
            data = parse_block(block)
            if data:
                rows.append(data)
        page_count += 1

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Subject", "Catalog Number", "Section", "Class Number", "Title",
        "Units", "Days", "Time", "Building", "Room Number", "Instructor"
    ])
    writer.writerows(rows)

print(f"Wrote {len(rows)} course entries to {csv_path}")
