class Vehicle:
    def __init__(self, license_plate, owner_name, vehicle_type):
        self.license_plate = license_plate
        self.owner_name = owner_name
        self.vehicle_type = vehicle_type

    def __str__(self):
        return (f"Plate: {self.license_plate}, Owner: {self.owner_name}, "
                f"Type: {self.vehicle_type}")


class ParkingRecord(Vehicle):
    def __init__(self, license_plate, owner_name, vehicle_type, spot_number):
        super().__init__(license_plate, owner_name, vehicle_type)
        self.spot_number = spot_number

    def __str__(self):
        return super().__str__() + f", Spot: {self.spot_number}"


class ParkingManager:
    DB_FILE = "Parking.txt"

    def __init__(self):
        self.records = []
        self.load_data()

    def load_data(self):
        try:
            with open(self.DB_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split("|")
                    if len(parts) == 4:
                        plate, owner, v_type, spot_str = parts
                        try:
                            spot = int(spot_str)
                            self.records.append(ParkingRecord(plate, owner, v_type, spot))
                        except ValueError:
                            print(f"Skipping invalid spot number: {line}")
                    else:
                        print(f"Skipping malformed line: {line}")
            print(f"Loaded {len(self.records)} records from {self.DB_FILE}.")
        except FileNotFoundError:
            print(f"No existing data file found ({self.DB_FILE}). Starting fresh.")
        except Exception as e:
            print(f"Error reading file: {e}. Starting empty.")

    def save_data(self):
        with open(self.DB_FILE, "w", encoding="utf-8") as f:
            for rec in self.records:
                f.write(f"{rec.license_plate}|{rec.owner_name}|{rec.vehicle_type}|{rec.spot_number}\n")
        print(f"Data saved to {self.DB_FILE}.")

    def input_records(self):
        n = int(input("Enter number of parking records: "))
        for i in range(n):
            print(f"\n--- Record {i+1} ---")
            plate = input("License plate: ")
            owner = input("Owner name: ")
            v_type = input("Vehicle type: ")
            spot = int(input("Spot number: "))
            self.records.append(ParkingRecord(plate, owner, v_type, spot))
        self.save_data()
        print("Records added successfully.")

    def show_records(self):
        if not self.records:
            print("No records in the system.")
            return
        print("\n--- All Parking Records ---")
        for idx, rec in enumerate(self.records, 1):
            print(f"{idx}. {rec}")

    def update_record(self, license_plate, field, new_value):
        for rec in self.records:
            if rec.license_plate == license_plate:
                if field == "license_plate":
                    rec.license_plate = new_value
                elif field == "owner_name":
                    rec.owner_name = new_value
                elif field == "vehicle_type":
                    rec.vehicle_type = new_value
                elif field == "spot_number":
                    try:
                        rec.spot_number = int(new_value)
                    except ValueError:
                        print("Spot number must be an integer. Update cancelled.")
                        return
                else:
                    print("Invalid field name.")
                    return
                self.save_data()
                print(f"{field} updated successfully for plate {license_plate}.")
                return
        print(f"No record found with plate {license_plate}.")


def main():
    manager = ParkingManager()
    while True:
        print("\n===== SMART PARKING MANAGEMENT =====")
        print("1. Input parking records")
        print("2. Show all records")
        print("3. Update a record")
        print("0. Exit")
        choice = input("Your choice: ")

        if choice == "1":
            manager.input_records()
        elif choice == "2":
            manager.show_records()
        elif choice == "3":
            plate = input("Enter license plate of the record to update: ")
            print("\nWhat would you like to change?")
            print("1. License plate")
            print("2. Owner name")
            print("3. Vehicle type")
            print("4. Spot number")
            sub_choice = input("Your choice (1-4): ")

            field_map = {
                "1": "license_plate",
                "2": "owner_name",
                "3": "vehicle_type",
                "4": "spot_number"
            }
            if sub_choice not in field_map:
                print("Invalid choice.")
                continue

            field = field_map[sub_choice]
            new_value = input(f"Enter new {field.replace('_', ' ')}: ")
            manager.update_record(plate, field, new_value)

        elif choice == "0":
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()