from fhir.resources.patient import Patient
from printresource import print_fhir_resource
from fhir.resources.patient import Patient
import requests
from requests.auth import HTTPBasicAuth

class Patients:
    def __init__(self):
        # List to store short form tuples of (full_name, identifier_value)
        self.short_form_patients = []
        # Dictionary to store Patient resources keyed by their Identifier value.
        self.patients = {}
        # Dictionary to store FHIR IDs (if any) keyed by identifier.
        self.ids = {}
        self.load_patients("patients.txt")

    def load_patients(self, file_path: str) -> None:
        """
        Reads the patients.txt file and creates Patient resources.
        Each line should contain:
          Name | Address | Date of Birth | Gender | Telecom | Identifier

        Parsing Details:
        - Address: "123 Main Street, Boston, MA, 02142" is parsed into:
          line, city, state, and postalCode.
        - Telecom: "phone, mobile, 617-231-3345" is parsed into:
          system, use, and value.
        - Identifier: "http://mgb.org, 356-444-9972" is parsed into:
          system and value.
        - Name: "Mary Johnson" is split into:
          given (Mary) and family (Johnson).
        The resulting Patient resources are stored in self.patients, keyed by identifier.value.
        """
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split('|')
                if len(parts) < 6:
                    print(f"Skipping malformed line: {line}")
                    continue

                # Extract and clean the fields.
                full_name = parts[0].strip()
                address_field = parts[1].strip()
                dob = parts[2].strip()
                gender = parts[3].strip()
                telecom_field = parts[4].strip()
                identifier_field = parts[5].strip()

                # Parse Name: Split full name into given and family.
                name_parts = full_name.split()
                if len(name_parts) >= 2:
                    given = name_parts[0]
                    family = " ".join(name_parts[1:])
                else:
                    given = full_name
                    family = ""

                # Parse Address (expected format: "line, city, state, postalCode")
                address_parts = [p.strip() for p in address_field.split(',')]
                if len(address_parts) < 4:
                    print(f"Address field malformed: {address_field}")
                    continue
                address_line = address_parts[0]
                city = address_parts[1]
                state = address_parts[2]
                postalCode = address_parts[3]

                # Parse Telecom (expected format: "system, use, value")
                telecom_parts = [p.strip() for p in telecom_field.split(',')]
                if len(telecom_parts) < 3:
                    print(f"Telecom field malformed: {telecom_field}")
                    continue
                telecom_system = telecom_parts[0]
                telecom_use = telecom_parts[1]
                telecom_value = telecom_parts[2]

                # Parse Identifier (expected format: "system, value")
                identifier_parts = [p.strip() for p in identifier_field.split(',')]
                if len(identifier_parts) < 2:
                    print(f"Identifier field malformed: {identifier_field}")
                    continue
                identifier_system = identifier_parts[0]
                identifier_value = identifier_parts[1]

                # Build the patient data dictionary using FHIR structure.
                patient_data = {
                    "resourceType": "Patient",
                    "name": [{
                        "given": [given],
                        "family": family,
                        "text": full_name
                    }],
                    "address": [{
                        "line": [address_line],
                        "city": city,
                        "state": state,
                        "postalCode": postalCode,
                    }],
                    "birthDate": dob,
                    "gender": gender,
                    "telecom": [{
                        "system": telecom_system,
                        "use": telecom_use,
                        "value": telecom_value,
                    }],
                    "identifier": [{
                        "system": identifier_system,
                        "value": identifier_value,
                    }]
                }

                # Create a Patient resource.
                patient_resource = Patient(**patient_data)
                # Store the patient keyed by the identifier's value.
                self.patients[identifier_value] = patient_resource

                # Append a short-form tuple (full_name, identifier_value)
                self.short_form_patients.append((full_name, identifier_value))

    def get_patient(self, identifier: str) -> Patient:
        """Retrieve a Patient resource by its identifier."""
        return self.patients.get(identifier)
    
    def store_patient_id(self, identifier: str, fhir_id) -> str:
        """Store a Patient FHIR Id by its identifier."""
        if self.patients.get(identifier):
            self.ids[identifier] = fhir_id
            return "Patient FHIR id stored"
        else: 
           return "Could not find patient identifer, unable to store FHIR id"
       
    def get_patient_id(self, identifier: str) -> str:
        return self.ids.get(identifier)
    
    def get_short_form_patients(self) -> []:
         return self.short_form_patients
    
    def post_patient(self, identifier):
        """
        Posts a FHIR Patient to a local FHIR server.
        :return: The response object from the POST request.
        """
        
        patient = self.get_patient(identifier)
        if patient:
          # Convert the Patient object to JSON
          patient_json = patient.json()
        else:
            print(f"No such patient with this identifier {identifier}")
            return

        # Define the endpoint for posting an Observation
        endpoint = "http://127.0.0.1:8080/csp/healthshare/demo/fhir/r4/Patient"

         # Prepare headers for FHIR JSON
        headers = {
        "Accept": "*/*",
        "content-type": "application/fhir+json",
        "Accept-Encoding": "gzip, deflate, br",
        "Prefer": "return=representation"
        }

        # Send the POST request
        response = requests.post(endpoint, data=patient_json, headers=headers, auth=HTTPBasicAuth('_System', 'ISCDEMO'))

        # Basic status check
        if response.status_code in (200, 201):
            # Parse the returned JSON resource and print its FHIR id.
            resource = response.json()
            self.store_patient_id(identifier, resource['id'])
            print_fhir_resource(resource)

        else:
            print(f"Failed to post Patient. Status code: {response.status_code}")
            print("Response:", response.text)

        return response

# Example usage:
if __name__ == "__main__":
    patients = Patients()
    # for pid, patient in patients.patients.items():
    #     name = patient.name[0]
    #     print(f"Identifier: {pid}, Given: {name.given[0]}, Family: {name.family}")
    #     print_fhir_resource(patient)
    for index, (name, identifier) in enumerate(patients.get_short_form_patients(), start=1):
      print(f"{index}. {name} : {identifier}")

        
    # patients.post_patient("356-444-9972")
    # print("Retrieving FHIR id by identifier")
    # fhirId =patients.get_patient_id("356-444-9972")
    # print(f"FHIR id = {fhirId}")
    # print(patients.store_patient_id("70261", "742"))
