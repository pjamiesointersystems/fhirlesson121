import requests
from fhir.resources.patient import Patient
from printresource import print_fhir_resource

def get_patient_from_server(patient_id: str) -> Patient:
    """
    Fetches a Patient resource from the FHIR server
    using a REST GET request and returns a Patient object.
    """
    # Replace with your actual FHIR base URL:
    # This example uses the endpoint in your question plus {patient_id}.
    url = f"http://127.0.0.1:8080/csp/healthshare/demo/fhir/r4/Patient/{patient_id}"

    # Required headers from your example:
    # Note: Typically "Authorization: Basic ..." is a base64-encoded
    # username:password. Here we are using the literal header string
    # you provided. Adjust if needed.
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/fhir+json",
        "Accept-Encoding": "gzip, deflate, br",
        "Prefer": "return=representation"
    }

    # Make the GET request
    response = requests.get(url, headers=headers, auth=("_System", "ISCDEMO"))
    # Raise an exception if the response isn't a 2xx success
    response.raise_for_status()

    # Convert the JSON response to a dictionary
    json_data = response.json()
    # Parse the dict into a Patient resource using fhir.resources
    patient = Patient.parse_obj(json_data)

    return patient




# ---------- Run the functions ----------
if __name__ == "__main__":
    patient_id = "2"  # Or whichever ID you want to retrieve
    print(f"\n--- GET Patient/{patient_id} from FHIR Server ---")
    
    pt = get_patient_from_server(patient_id)
    print("\n--- Patient Resource (non-None fields) ---")
    print_fhir_resource(pt)
