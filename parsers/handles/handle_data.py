def handle_data_001(data):
    if data not in [", ", " ", "[", "]"]:
        return data.strip().strip("\n").strip()
    
def handle_data_002(data):
    return data
