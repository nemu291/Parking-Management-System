class Vehicle:
    """Base class representing a vehicle."""
    def __init__(self, license_plate, owner_name, vehicle_type):
        self.license_plate = license_plate
        self.owner_name = owner_name
        self.vehicle_type = vehicle_type

    def __str__(self):
        return (f"Plate: {self.license_plate}, Owner: {self.owner_name}, "
                f"Type: {self.vehicle_type}")


class ParkingRecord(Vehicle):
    """Derived class adding the parking spot number."""
    def __init__(self, license_plate, owner_name, vehicle_type, spot_number):
        super().__init__(license_plate, owner_name, vehicle_type)
        self.spot_number = spot_number

    def __str__(self):
        return super().__str__() + f", Spot: {self.spot_number}"


class ParkingManager:
    """Manages a list of parking records with text file persistence."""
    DB_FILE = "Parking.txt"

    def __init__(self):
        self.records = []
        self.load_data()          # Load existing records on startup

    def load_data(self):
        """Load records from Parking.txt if the file exists."""
        try:
            with open(self.DB_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    # Each line: license_plate|owner_name|vehicle_type|spot_number
                    parts = line.split("|")
                    if len(parts) == 4:
                        plate, owner, v_type, spot_str = parts
                        try:
                            spot = int(spot_str)
                            record = ParkingRecord(plate, owner, v_type, spot)
                            self.records.append(record)
                        except ValueError:
                            print(f"Skipping invalid spot number in line: {line}")
                    else:
                        print(f"Skipping malformed line: {line}")
            print(f"Loaded {len(self.records)} records from {self.DB_FILE}.")
        except FileNotFoundError:
            print(f"No existing data file found ({self.DB_FILE}). Starting fresh.")
        except Exception as e:
            print(f"Error reading file: {e}. Starting with empty list.")
            self.records = []

    def save_data(self):
        """Save all records to Parking.txt as plain text."""
        with open(self.DB_FILE, "w", encoding="utf-8") as f:
            for rec in self.records:
                # Write: license_plate|owner_name|vehicle_type|spot_number
                line = f"{rec.license_plate}|{rec.owner_name}|{rec.vehicle_type}|{rec.spot_number}\n"
                f.write(line)
        print(f"Data saved to {self.DB_FILE}.")

    def input_records(self):
        """Input a list of parking records from the user and save."""
        n = int(input("Enter number of parking records: "))
        for i in range(n):
            print(f"\n--- Record {i+1} ---")
            plate = input("License plate: ")
            owner = input("Owner name: ")
            v_type = input("Vehicle type: ")
            spot = int(input("Spot number: "))
            record = ParkingRecord(plate, owner, v_type, spot)
            self.records.append(record)
        self.save_data()          # Persist after adding
        print("Records added successfully.")

    def show_records(self):
        """Display all parking records."""
        if not self.records:
            print("No records in the system.")
            return
        print("\n--- All Parking Records ---")
        for idx, rec in enumerate(self.records, 1):
            print(f"{idx}. {rec}")


def main():
    """Main menu for the Smart Parking Management System."""
    manager = ParkingManager()
    while True:
        print("\n===== SMART PARKING MANAGEMENT =====")
        print("1. Input parking records")
        print("2. Show all records")
        print("0. Exit")
        choice = input("Your choice: ")

        if choice == "1":
            manager.input_records()
        elif choice == "2":
            manager.show_records()
        elif choice == "0":
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()