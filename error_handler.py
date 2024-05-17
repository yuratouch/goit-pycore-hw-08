def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Please enter expected values (name, phone number)."
        except IndexError:
            return "Please enter name to check the related phone number."

    return inner