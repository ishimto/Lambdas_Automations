def get_contacts(sheet):
    data = sheet.get_all_records()
    contacts = []
    try:
        for row in data:
            first_name = row.get("FIRST NAME")
            last_name = row.get("LAST NAME")
            contacts.append((first_name, last_name))
        return contacts

    except Exception as e:
        return False


def get_column_by_name(sheet, column_name="NUMBER"):
    data = sheet.get_all_records()
    numbers = []

    for row in data:
        number = row.get(column_name)
        if number:
            numbers.append(str(number))

    return numbers

def gitlab_user_data(sheet):
    data = sheet.get_all_records()
    init_data = []

    try:
        for row in data:
            first_name = row.get("FIRST NAME")
            user_name = row.get("USERNAME")
            password = row.get("PASSWORD")
            email = row.get("EMAIL")
            init_data.append((first_name, user_name, password, email))
        return init_data

    except Exception as e:
        return False

