from addressbook import AddressBook, Record
from functools import wraps
from typing import Callable


def input_error(func: Callable) -> Callable:
    """ Decorator to handle input errors for command functions.
    Catches ValueError, KeyError, and IndexError exceptions and returns
    user-friendly error messages.
    Parameters:
        func (function): The function to be decorated.
    Returns:
        function: The wrapped function with error handling.
  """
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter correct arguments for the command"
        except KeyError:
            return "Name not in contacts, please create it at first"
        except IndexError:
            return "Enter the argument for the command"
        except AttributeError:
            return "Entity not found"

    return inner


@input_error
def parse_input(user_input: str) -> tuple[str, list[str]]:
    """ Parses user input into a command and its arguments.
    Parameters:
        user_input (str): The input string from the user.
    Returns:
        tuple: A tuple containing the command and a list of arguments.
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    """ Adds a new contact to the address book.
    Parameters:
        args (list[str]): The arguments containing the name and phone number.
        book (AddressBook): The address book instance.
    Returns:
        str: A message indicating the result of the operation.
    """
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        message = "Contact added."
    else:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args: list[str], book: AddressBook) -> str:
    """ Changes the phone number of an existing contact.
    Parameters:
        args (list[str]): The arguments containing the name and
                          new phone number.
        book (AddressBook): The address book instance.
    Returns:
        str: A message indicating the result of the operation."""

    name, phone, new_phone = args
    record = book.find(name)
    record.edit_phone(phone, new_phone)

    return f"Contact {name} changed the number from {phone} to {new_phone}"


@input_error
def phone_contact(args: list[str], book: AddressBook) -> str:
    """ Retrieves the phone number of a contact.
    Parameters:
        args (list[str]): The arguments containing the name of the contact.
        book (AddressBook): The address book instance.
    Returns:
        str: A message indicating the result of the operation."""
    name, = args
    phones = [n.value for n in book.data[name].phones]
    return f"{name} phone(s): {', '.join(phones)}"


@input_error
def all_contacts(book: AddressBook) -> str:
    """ Retrieves all contacts from the address book.
    Parameters:
        book (AddressBook): The address book instance.
    Returns:
        str: A formatted string containing all contacts."""

    ret = ""
    if not book.data:
        return "Address book is empty."

    for name, record in book.data.items():
        phones = [n.value for n in record.phones]
        ret = ret + f"{name} phone(s): {', '.join(phones)}\n"
        if record.birthday:
            ret += f"{name} birthday: {record.birthday.value.strftime('%d.%m.%Y')}\n"

    return ret


@input_error
def add_birthday(args, book):
    """ Adds a birthday to a contact.
    Parameters:
        args (list[str]): The arguments containing the name and birthday.
        book (AddressBook): The address book instance.
    Returns:
        str: A message indicating the result of the operation.
    """
    name, birthday = args
    record = book.find(name)
    record.add_birthday(birthday)

    return f"Birthday {birthday} for {name} added."


@input_error
def show_birthday(args, book):
    """ Shows the birthday of a contact.
    Parameters:
        args (list[str]): The arguments containing the name.
        book (AddressBook): The address book instance.
    Returns:
        str: A message indicating the birthday or if not found."""

    name, = args
    record = book.find(name)
    return f"{name}'s birthday is on {record.birthday.value.strftime('%d.%m.%Y')}."

    #if record and record.birthday:
    #    return f"{name}'s birthday is on {record.birthday.value.strftime('%d.%m.%Y')}."
    #else:
    #    return f"Birthday for {name} not found."


@input_error
def birthdays(book):
    """ Retrieves upcoming birthdays from the address book.
    Parameters:
        book (AddressBook): The address book instance.
    Returns:
        str: A message indicating the upcoming birthdays or if not found."""

    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "No upcoming birthdays found."
    return "\n".join(f"{item['name']}: {item['congratulation_date']}" for item in upcoming_birthdays)