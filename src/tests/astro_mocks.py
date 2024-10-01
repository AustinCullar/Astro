"""
This file will contain all mock classes used for testing.
"""


class MockSqlite3Cursor:
    return_value = None

    def __init__(self, return_value):
        self.return_value = return_value

    def fetchone(self):
        if self.return_value:
            return (self.return_value,)
        else:
            return None

    def execute(self, query: str):
        return self.return_value


class MockSqlite3Connection:
    return_value = None

    def set_return_value(self, return_value):
        self.return_value = return_value

    def cursor(self):
        return MockSqlite3Cursor(self.return_value)

    def commit(self):
        return
