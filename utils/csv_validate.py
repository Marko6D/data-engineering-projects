def validate_row(row):

    if row['id'] == '':
        return 'Id is missing'
    if not row['id'].isdigit():
        return 'Id is not a number'
    if row['name'] == '':
        return 'Name is missing'
    if row['age'] == '':
        return 'Age is missing'
    try:
        convert = int(row['age'])
    except ValueError:
        return 'Age is not a number'
    if convert < 0:
        return 'Age is negative'
    if row['email'] == '':
        return 'Email is missing'
    if not row['email'].count('@') == 1:
        return 'Email has no @'
    before_at, after_at = row['email'].split('@')
    if not before_at:
        return 'Email has no name after @'
    if after_at.find('.') == -1:
        return 'Email domain is invalid'
    domain_part = after_at.split('.')
    if not domain_part[-1]:
        return 'Email domain is invalid'
    return None



