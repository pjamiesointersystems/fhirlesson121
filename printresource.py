def print_fhir_resource(resource):
    """
    Recursively prints all non-None fields (including nested fields)
    from a FHIR resource object, line by line.
    """
    def print_non_none(data, prefix=""):
        if isinstance(data, dict):
            for key, value in data.items():
                if value is not None:
                    print_non_none(value, prefix=f"{prefix}{key}.")
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                if item is not None:
                    print_non_none(item, prefix=f"{prefix}[{idx}].")
        else:
            # data is a scalar type (string, int, bool, etc.)
            # prefix[:-1] to remove the last '.' or bracket from prefix
            print(f"{prefix[:-1]}: {data}")
            
    # If the resource has a dict() method, use it; otherwise assume it's a dict.
    if hasattr(resource, "dict"):
        resource_dict = resource.dict()
    else:
        resource_dict = resource
        
    # Start the recursive printing
    print_non_none(resource_dict)