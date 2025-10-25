from collections import UserDict
from datetime import datetime, timedelta


class Field:
    """Base class for fields in record"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)


class Name(Field):
    """Class for name in record"""
    pass


def phone_format_correct(phone: str) -> bool:
    """ Helper function to check phone number format
    Parameters:
        phone (str): The phone number to check.
    Returns:
        bool: True if the phone number is valid, raise ValueError
              exception otherwise.
    """
    if len(phone) != 10 or not phone.isdigit() or not isinstance(phone, str):
        raise ValueError("Invalid phone number format. Use 10 digit string format.")
    return True


class Phone(Field):
    """Class for phone number in record"""
    def __init__(self, value):
        if phone_format_correct(value):
            self.value = value

class Birthday(Field):
    def __init__(self, date):
        try:
            self.value = datetime.strptime(date, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    """Class for record in address book"""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone: str):
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)

    def remove_phone(self, phone: str):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)

    def edit_phone(self, phone: str, new_phone: str):
        if phone_format_correct(new_phone) and phone_format_correct(phone):
            phone_obj = self.find_phone(phone)
            phone_obj.value = new_phone

    def find_phone(self, phone: str):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj

    def add_birthday(self, val: str):
        self.birthday = Birthday(val)


def check_holiday(date_obj: datetime, diff: int) -> str:
  """ Helper function to adjust birthday dates falling on weekends.
  If the birthday falls on a Saturday or Sunday, it moves the date
  to the next Monday"""
  if date_obj.isoweekday() == 6:
     if diff < 5:
      date_obj = date_obj + timedelta(days=2)
     else:
      # Differeence between birthday and today is more than 7 days,
      # so we skip this birthday
      return None
  elif date_obj.isoweekday() == 7:
     if diff < 6:
      date_obj = date_obj + timedelta(days=1)
     else:
      return None

  return f"{date_obj.day}.{date_obj.month}.{date_obj.year}"


class AddressBook(UserDict):
  """Class for address book"""
  def add_record(self, record):
    self.data[record.name.value] = record

  def find(self, name: str):
    if name in self.data.keys():
        return self.data[name]

  def delete(self, name: str):
    if self.find(name):
        del self.data[name]

  def get_upcoming_birthdays(self):
    ret = []
    today_obj = datetime.now().date()
    YEAR = today_obj.year

    for name, record in self.data.items():
        if record.birthday:
            user_date_obj = record.birthday.value.replace(year=YEAR).date()
            user_date_ny_obj = record.birthday.value.replace(year=YEAR+1).date()

            diff = user_date_obj - today_obj
            diff_ny = user_date_ny_obj - today_obj

            if diff.days >= 0 and diff.days <= 6:
                day = check_holiday(user_date_obj, diff.days)
                if day:
                    ret.append({"name":record.name.value, 'congratulation_date':day})
            elif diff_ny.days <= 6:
                day = check_holiday(user_date_ny_obj, diff_ny.days)
                if day:
                    ret.append({"name":record.name.value, 'congratulation_date':day})

    return ret
