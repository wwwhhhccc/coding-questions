import json
import random
from collections import defaultdict

# Set a seed for reproducibility
random.seed(42)

# File paths
input_file = "coding.jsonl"
output_file = "coding_100.jsonl"

# Dictionary to hold tasks and their records
task_records = defaultdict(list)

# Helper function to extract the number after the last underscore in the pid
def extract_trailing_number(pid):
    try:
        return int(pid.split("_")[-1])  # Extract the number after the last '_'
    except (IndexError, ValueError):
        return float('inf')  # Assign a high value for malformed pid fields

# Step 1: Read and group records by 'task'
with open(input_file, "r") as f:
    for line in f:
        record = json.loads(line)
        if "task" in record and "pid" in record:  # Ensure 'task' and 'pid' fields exist
            task_records[record["task"]].append(record)

# Step 2: Sample 25 records per task and sort within each task by pid's trailing number
sampled_records = []
for task, records in task_records.items():
    # Sort by the number trailing in the 'pid' field
    records.sort(key=lambda r: extract_trailing_number(r["pid"]))
    # Sample up to 25 records
    sampled_records.extend(random.sample(records, min(25, len(records))))

# Step 3: Sort all sampled records globally by 'pid' field
sampled_records.sort(key=lambda r: extract_trailing_number(r["pid"]))

# Step 4: Write the sorted sampled records to a new JSONL file
with open(output_file, "w") as f:
    for record in sampled_records:
        f.write(json.dumps(record) + "\n")

print(f"Sampled and sorted records written to {output_file}")
