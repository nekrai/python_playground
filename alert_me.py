def alert(a_number):
    message = fetch_message(a_number)
    print_message(message)


def fetch_message(a_number):
    if a_number == 1:
        return 'greenish alert!'
    elif a_number == 2:
        return 'yellow alert!'
    else:
        return 'red alert!'


def print_message(message):
    print message
