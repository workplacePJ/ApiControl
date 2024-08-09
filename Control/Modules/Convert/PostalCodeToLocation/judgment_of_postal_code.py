def judgment_of_postal_code(value: str) -> bool:
    pattern__judgment_of_postal_code: Pattern[str] = re.compile(r'^(?=.*[0-9]{3}-[0-9]{4})(?=.*[0-9-]{8})(?!.*[0-9-]{9,}).*$|^(?=.*[0-9]{7})(?!.*[0-9]{8,}).*$|^(?=.*[０-９]{3}−[０-９]{4})(?=.*[０-９−]{8})(?!.*[０-９−]{9,}).*$|^(?=.*[０-９]{7})(?!.*[０-９]{8,}).*$')
    if pattern__judgment_of_postal_code.search(value):
        return True
    else:
        return False
