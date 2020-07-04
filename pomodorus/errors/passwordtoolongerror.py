"""
Password too long error. Passwords have a size limit, this should be raised
if such limit is exceeded.
"""


class PasswordTooLongError(Exception):
    def __init__(self):
        super().__init__('The password contains too many characters')
