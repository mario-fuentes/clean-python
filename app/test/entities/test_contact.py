from unittest import TestCase

from app.entities.contact import Contact
from app.entities.exceptions import ValidationError


class TestContact(TestCase):
    def test_init_should_initialize_the_instance(self):
        c = Contact('Homer Simpson', '+1 555-7334', 'homer@fox.com')

        self.assertEqual('Homer Simpson', c.name)
        self.assertEqual('+1 555-7334', c.phone)
        self.assertEqual('homer@fox.com', c.email)

    def test_validate_should_raise_an_exception_if_name_is_none_or_empty(self):
        c = Contact()

        self.assertRaises(ValidationError, lambda: c.validate())

        c.name = ''

        self.assertRaises(ValidationError, lambda: c.validate())