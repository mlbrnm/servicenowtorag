import csv
from datetime import datetime

class Record:
    def __init__(self, row_dict):
        """
        Initializes a Record object using a dictionary that contains the data for a single row.

        Args:
        row_dict (dict): Dictionary where keys are column headers and values are the data of the row.
        """
        self.number = row_dict['number']
        self.opened_at = self.parse_date(row_dict['opened_at'])
        self.short_description = row_dict['short_description']
        self.caller_id = row_dict['caller_id']
        self.category = row_dict['category']
        self.assignment_group = row_dict['assignment_group']
        self.assigned_to = row_dict['assigned_to']
        self.work_notes = row_dict['work_notes']
        self.resolved_at = self.parse_date(row_dict['resolved_at'])
        self.resolved_by = row_dict['resolved_by']
        self.close_notes = row_dict['close_notes']

    @staticmethod
    def parse_date(date_str):
        """
        Converts a date string in the format 'YYYY-MM-DD HH:MM:SS' to a datetime object.
        Returns None if the date string is empty or invalid.

        Args:
        date_str (str): The date string to parse.

        Returns:
        datetime.datetime or None: The datetime object or None if conversion is not possible.
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None

    def __str__(self):
        """ Provides a string representation of the Record object. """
        return f"{self.number} - {self.short_description}"

def load_csv_to_dict(filename='incidents.csv'):
    """
    Load a CSV file and convert it into a list of Record objects.

    Each row in the CSV becomes an instance of the Record class, with the header row providing the keys.

    Args:
    filename (str): The path to the CSV file to load. Defaults to 'incidents.csv'.

    Returns:
    list[Record]: A list of Record objects representing each row in the CSV.
    """
    encodings = ['utf-8', 'iso-8859-1', 'windows-1252']  # Common encodings to try
    for encoding in encodings:
        try:
            with open(filename, mode='r', encoding=encoding) as file:
                csv_reader = csv.DictReader(file)
                records = [Record(row) for row in csv_reader]
                print(f"\nFile read successfully with {encoding} encoding.\n")
                return records
        except UnicodeDecodeError:
            pass  # Continue trying other encodings
        except FileNotFoundError:
            print(f"The file '{filename}' does not exist.")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
    print("Failed to read the file with any of the tried encodings.")
    return []

if __name__ == "__main__":
    print("\n---------------------------------------------\nWelcome to the ServiceNow -> RAG Ready Script")
    filename = input("Enter the filename (default: incident.csv): ")
    filename = filename.strip() or "incident.csv"
    records = load_csv_to_dict(filename)

    if records:
        for i in range(len(records)):
            print("\n-------------------------------")
            print(f"{records[i].number} | {records[i].opened_at.strftime('%B %d, %Y')}")
            print(f"Submitted by: {records[i].caller_id} | Resolved by: {records[i].resolved_by}")
            print(f"Problem:\n{records[i].short_description}")
            print(f"Solution:\n{records[i].close_notes}")
            print(f"Work Notes:\n{records[i].work_notes}")
            print("-------------------------------\n")
    else:
        print("No records found or file could not be read.")
