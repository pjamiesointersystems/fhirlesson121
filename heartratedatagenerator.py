import random
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

class HeartRateDataGenerator:
    def __init__(self):
        # The five filenames to generate.
        self.filenames = [
            "3564449972.txt",
            "7891011121.txt",
            "3345567788.txt",
            "5566678899.txt",
            "9901122233.txt"
        ]
        # We'll choose between Eastern and Central time zones.
        self.timezones = ["America/New_York", "America/Chicago"]

    def generate_files(self):
        for filename in self.filenames:
            # Choose a random day in March 2025.
            day = random.randint(1, 31)
            base_date = datetime(2025, 3, day)
            
            # Randomly choose a timezone from our list.
            tz = ZoneInfo(random.choice(self.timezones))
            
            tuples_list = []
            for _ in range(100):
                # Generate a random heart rate between 60 and 160.
                heart_rate = random.randint(60, 160)
                # Random seconds offset within the day (0 to 86399 seconds).
                seconds_offset = random.randint(0, 86399)
                # Create the datetime for this measurement.
                dt = base_date + timedelta(seconds=seconds_offset)
                # Make the datetime timezone-aware.
                dt = dt.replace(tzinfo=tz)
                # Convert the datetime to an ISO 8601 string.
                dt_str = dt.isoformat()
                tuples_list.append((heart_rate, dt_str))
            
            # Write the 100 tuples to the file (one per line).
            with open(filename, "w") as file:
                for tup in tuples_list:
                    file.write(f"{tup}\n")
            print(f"Wrote {filename}")

# Example usage:
if __name__ == "__main__":
    generator = HeartRateDataGenerator()
    generator.generate_files()
