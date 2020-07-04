"""
Username too long error. Usernames have a size limit, this should be raised
if such limit is exceeded.
"""


class UsernameTooLongError(Exception):
    def __init__(self):
        super().__init__('The username contains too many characters')
