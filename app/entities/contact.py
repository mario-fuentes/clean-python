from app.entities.exceptions import ValidationError


class Contact:
    def __init__(self, name: str=None, phone: str=None, email: str=None):
        self.name: str = name
        self.phone: str = phone
        self.email: str = email

    def validate(self):
        if self.name is None or self.name.strip(' ') == '':
            raise ValidationError
