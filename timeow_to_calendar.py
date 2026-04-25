#!/usr/bin/env python3
"""
Timeow → macOS Calendar
Reads active periods from Timeow and adds them to the "Office" calendar.

Usage:
  Interactive:  python3 timeow_to_calendar.py
  Auto:         python3 timeow_to_calendar.py --auto

Setup (launchd):
  1. Edit com.user.timeow-calendar.plist — set your script path
  2. cp com.user.timeow-calendar.plist ~/Library/LaunchAgents/
  3. launchctl load ~/Library/LaunchAgents/com.user.timeow-calendar.plist
  4. First run: allow Python to control Calendar when macOS prompts
"""

import subprocess
import json
import sys
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

CALENDAR_NAME = "Office"
EVENT_TITLE = "Office"
LOG_FILE = Path.home() / ".timeow_calendar_log.json"
LOOKBACK_DAYS = 7


def get_timeow_data():
    """Read active periods from Timeow's plist."""
    result = subprocess.run(
        ["defaults", "read", "com.timeow.Timeow", "activePeriods"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return []
    raw = result.stdout.strip().replace('\\"', '"')
    return json.loads(raw)


def parse_time(iso_str):
    """Parse ISO timestamp, compatible with Python 3.9."""
    iso_str = re.sub(r'(\.\d{6})\d+', r'\1', iso_str)
    iso_str = re.sub(r'\.(\d{1,5})([+-])', lambda m: '.' + m.group(1).ljust(6, '0') + m.group(2), iso_str)
    tz_match = re.search(r'([+-])(\d{2}):(\d{2})$', iso_str)
    if tz_match:
        sign = 1 if tz_match.group(1) == '+' else -1
        tz_hours = int(tz_match.group(2))
        tz_minutes = int(tz_match.group(3))
        tz = timezone(timedelta(hours=sign * tz_hours, minutes=sign * tz_minutes))
        iso_str = iso_str[:tz_match.start()]
        dt = datetime.fromisoformat(iso_str).replace(tzinfo=tz)
    else:
        dt = datetime.fromisoformat(iso_str)
    return dt


def load_log():
    if LOG_FILE.exists():
        try:
            return json.loads(LOG_FILE.read_text())
        except Exception:
            return []
    return []


def save_log(entries):
    LOG_FILE.write_text(json.dumps(entries, ensure_ascii=False, indent=2))


def is_already_added(start_str, end_str, log):
    for entry in log:
        if entry["start"] == start_str and entry["end"] == end_str:
            return True
    return False


def clean_old_log(log, cutoff_date):
    """Remove log entries older than cutoff to prevent unbounded growth."""
    cleaned = []
    for entry in log:
        try:
            added = datetime.fromisoformat(entry.get("added", ""))
            if added.date() >= cutoff_date:
                cleaned.append(entry)
        except Exception:
            cleaned.append(entry)
    return cleaned


def add_to_calendar(title, start_dt, end_dt, calendar_name):
    """Add an event to macOS Calendar via osascript."""
    formats = [
        "%Y年%m月%d日 %H:%M:%S",
        "%B %d, %Y %H:%M:%S",
    ]
    for fmt in formats:
        start_str = start_dt.strftime(fmt)
        end_str = end_dt.strftime(fmt)
        script = f'''
        tell application "Calendar"
            tell calendar "{calendar_name}"
                make new event with properties {{summary:"{title}", start date:date "{start_str}", end date:date "{end_str}"}}
            end tell
        end tell
        '''
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return True
    return False


def main():
    auto_mode = "--auto" in sys.argv

    periods = get_timeow_data()
    if not periods:
        if not auto_mode:
            print("No active periods found.")
        return

    today = datetime.now().date()
    cutoff_date = today - timedelta(days=LOOKBACK_DAYS)
    log = load_log()
    log = clean_old_log(log, today - timedelta(days=30))

    # Filter: past LOOKBACK_DAYS, not already added
    new_periods = []
    for p in periods:
        start = parse_time(p["start"])
        end = parse_time(p["end"])
        if cutoff_date <= start.date() <= today:
            if not is_already_added(p["start"], p["end"], log):
                new_periods.append((start, end, p["start"], p["end"]))

    new_periods.sort(key=lambda x: x[0])

    if not new_periods:
        if not auto_mode:
            print("No new active periods in the past week. All already added.")
        return

    if not auto_mode:
        by_date = {}
        for start, end, rs, re_ in new_periods:
            by_date.setdefault(start.date(), []).append((start, end))

        total_seconds = 0
        idx = 0
        print(f"Found {len(new_periods)} new active periods (past {LOOKBACK_DAYS} days):\n")
        for date in sorted(by_date.keys()):
            label = "Today" if date == today else date.strftime("%m/%d %a")
            print(f"  [{label}]")
            for start, end in by_date[date]:
                idx += 1
                duration = end - start
                total_seconds += duration.total_seconds()
                mins = int(duration.total_seconds() / 60)
                print(f"    {idx}. {start.strftime('%H:%M')} – {end.strftime('%H:%M')} ({mins} min)")
            print()

        total_h = int(total_seconds // 3600)
        total_m = int((total_seconds % 3600) // 60)
        print(f"  Total: {total_h}h {total_m}m\n")

        confirm = input(f"Add these to '{CALENDAR_NAME}' calendar? [Y/n] ").strip().lower()
        if confirm not in ("", "y", "yes"):
            print("Cancelled.")
            return

    success = 0
    for start, end, raw_start, raw_end in new_periods:
        if add_to_calendar(EVENT_TITLE, start, end, CALENDAR_NAME):
            success += 1
            log.append({"start": raw_start, "end": raw_end, "added": datetime.now().isoformat()})
            if not auto_mode:
                print(f"  ✅ {start.strftime('%m/%d %H:%M')} – {end.strftime('%H:%M')}")
        else:
            if not auto_mode:
                print(f"  ❌ {start.strftime('%m/%d %H:%M')} – {end.strftime('%H:%M')} (failed)")

    save_log(log)

    if not auto_mode:
        print(f"\nDone! {success}/{len(new_periods)} events added.")


if __name__ == "__main__":
    main()
