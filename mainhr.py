from patients import Patients
from printresource import print_fhir_resource
from fhir.resources.patient import Patient
from heartratefilebundlegenerator import HeartRateFileBundleGenerator
from heartratebundlegenerator import HeartRateBundleGenerator

class MainHR:
    def __init__(self):
        # Perform any initialization if needed.
        self.patients = Patients()
        
    def print_preamble(self):
        print("***********************************************************")
        print("Patients in Edge Gateway")
        for index, (name, identifier) in enumerate(self.patients.get_short_form_patients(), start=1):
           print(f"{index}. {name} : {identifier}")
        print("***********************************************************")

    def run(self):
        while True:
            self.print_preamble()
            print("\nMain Menu:")
            print("1. Print Patient Details")
            print("2. Create Heart Rate Bundle for Patient from File")
            print("3. Post Heart Rate Bundle for Patient from File")
            print("4. Create Synthetic Heart Rate Bundle for Patient")
            print("5. Post Synthetic Heart Rate Bundle")
            print("6. Quit")
            
            selection = input("Choose Selection: ").strip()
            
            try:
                option = int(selection)
            except ValueError:
                print("Invalid input. Please enter a number corresponding to a menu option.")
                continue

            # Using a switch-like structure (if/elif) to handle the menu choices.
            if option == 1:
                # Prompt the user to choose a patient from the preamble list.
                short_patients = self.patients.get_short_form_patients()
                patient_choice = input("Enter the number of the Gateway patient: ").strip()
                try:
                    choice_num = int(patient_choice)
                    if 1 <= choice_num <= len(short_patients):
                        # Retrieve the tuple corresponding to the selection.
                        name, identifier = short_patients[choice_num - 1]
                        print(f"Patient Identifier for {name}: {identifier}\n")
                        patient = self.patients.get_patient(identifier)
                        if patient is not None:
                           print_fhir_resource(patient)
                           print("")
                    else:
                        print("Selection out of range.\n")
                except ValueError:
                    print("Invalid input. Please enter a numeric value.\n")
            elif option == 2:
                print("Option 2: Create Heart Rate Bundle for Patient from File")
                short_patients = self.patients.get_short_form_patients()
                patient_choice = input("Enter the number of the Gateway patient: ").strip()
                try:
                    choice_num = int(patient_choice)
                    if 1 <= choice_num <= len(short_patients):
                        # Retrieve the tuple corresponding to the selection.
                        name, identifier = short_patients[choice_num - 1]
                        print(f"Patient Identifier for {name}: {identifier}\n")
                        patient = self.patients.get_patient(identifier)
                        if patient is not None:
                           hrbundle = HeartRateFileBundleGenerator(identifier, self.patients)
                           #print out the first two entries
                           hrbundle.print_two()
                           print("")
                    else:
                        print("Selection out of range.\n")
                except ValueError:
                    print("Invalid input. Please enter a numeric value.\n")
            elif option == 3:
                print("Option 3: Post Heart Rate Bundle for Patient from File")
                short_patients = self.patients.get_short_form_patients()
                patient_choice = input("Enter the number of the Gateway patient: ").strip()
                try:
                    choice_num = int(patient_choice)
                    if 1 <= choice_num <= len(short_patients):
                        # Retrieve the tuple corresponding to the selection.
                        name, identifier = short_patients[choice_num - 1]
                        print(f"Patient Identifier for {name}: {identifier}\n")
                        patient = self.patients.get_patient(identifier)
                        if patient is not None:
                           hrbundle = HeartRateFileBundleGenerator(identifier, self.patients)
                           hrbundle.post_bundle()
                           hrbundle.print_ids()
                           print("")
                    else:
                        print("Selection out of range.\n")
                except ValueError:
                    print("Invalid input. Please enter a numeric value.\n")
            elif option == 4:
                print("Option 4: Create Synthetic Heart Rate Bundle for Patient")
                short_patients = self.patients.get_short_form_patients()
                patient_choice = input("Enter the number of the Gateway patient: ").strip()
                try:
                    choice_num = int(patient_choice)
                    if 1 <= choice_num <= len(short_patients):
                        # Retrieve the tuple corresponding to the selection.
                        name, identifier = short_patients[choice_num - 1]
                        print(f"Patient Identifier for {name}: {identifier}\n")
                        patient = self.patients.get_patient(identifier)
                        if patient is not None:
                           noOfObservations = input("Enter No of Observations (must be < 1000): ").strip()
                           nobs = int(noOfObservations)
                           if (nobs > 1000):
                               nobs = 1000
                           if (nobs < 1):
                               nobs = 1
                           hrbundle = HeartRateBundleGenerator(identifier, nobs, 60, 160, self.patients)
                           #print out the first two entries
                           hrbundle.print_two()
                           print("")
                    else:
                        print("Selection out of range.\n")
                except ValueError:
                    print("Invalid input. Please enter a numeric value.\n")
            elif option == 5:
                print("Option 5: Post Synthetic Heart Rate Bundle")
                short_patients = self.patients.get_short_form_patients()
                patient_choice = input("Enter the number of the Gateway patient: ").strip()
                try:
                    choice_num = int(patient_choice)
                    if 1 <= choice_num <= len(short_patients):
                        # Retrieve the tuple corresponding to the selection.
                        name, identifier = short_patients[choice_num - 1]
                        print(f"Patient Identifier for {name}: {identifier}\n")
                        patient = self.patients.get_patient(identifier)
                        if patient is not None:
                           noOfObservations = input("Enter No of Observations (must be < 1000): ").strip()
                           nobs = int(noOfObservations)
                           if (nobs > 1000):
                               nobs = 1000
                           if (nobs < 1):
                               nobs = 1
                           hrbundle = HeartRateBundleGenerator(identifier, nobs, 60, 160, self.patients)
                           hrbundle.post_bundle()
                           #print out ids of the bundle resource that were posted
                           hrbundle.print_ids()
                           print("")
                    else:
                        print("Selection out of range.\n")
                except ValueError:
                    print("Invalid input. Please enter a numeric value.\n")
                # pass # Placeholder for actual implementation
            elif option == 6:
                print("Option 6: Quit - Exiting program.")
                break
            else:
                print("Invalid selection. Please try again.")

if __name__ == "__main__":
    app = MainHR()
    app.run()
