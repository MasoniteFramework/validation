import unittest
from src.masonite.validation import MessageBag

class TestMessageBag(unittest.TestCase):

    def setUp(self):
        self.bag = MessageBag()

    def test_message_bag_can_add_errors_and_messages(self):
        self.bag.add('email', 'Your email is invalid')
        self.assertEqual(self.bag.items, {'email': ['Your email is invalid']})

    def test_message_bag_can_add_several_errors_and_messages(self):
        self.bag.add('email', 'Your email is invalid')
        self.bag.add('email', 'Your email is invalid')

    def test_message_bag_can_get_all_errors_and_messages(self):
        self.bag.reset()
        self.bag.add('email', 'Your email is invalid')
        self.assertEqual(self.bag.all(), {'email': ['Your email is invalid']})

    def test_message_bag_has_any_errors(self):
        self.bag.reset()
        self.assertFalse(self.bag.any())
        self.bag.add('email', 'Your email is invalid')
        self.assertTrue(self.bag.any())

    def test_message_bag_has_any_errors(self):
        self.bag.reset()
        self.assertTrue(self.bag.empty())
        self.bag.add('email', 'Your email is invalid')
        self.assertFalse(self.bag.empty())

    def test_message_bag_can_get_first_error(self):
        self.bag.reset()
        self.bag.add('email', 'Your email is invalid')
        self.bag.add('username', 'Your username is invalid')
        self.assertEqual(self.bag.first(), {'email': ['Your email is invalid']})

    def test_amount_of_messages(self):
        self.bag.reset()
        self.bag.add('email', 'Your email is invalid')
        self.bag.add('email', 'Your email too short')
        self.assertEqual(self.bag.amount('email'), 2)

    def test_get_messages(self):
        self.bag.reset()
        self.bag.add('email', 'Your email is invalid')
        self.bag.add('email', 'Your email too short')
        self.assertEqual(
            self.bag.get('email'), 
            ['Your email is invalid', 'Your email too short']
        )

    def test_get_errors(self):
        self.bag.reset()
        self.bag.add('email', 'Your email is invalid')
        self.bag.add('email', 'Your email too short')
        self.assertEqual(
            self.bag.errors(), 
            ['email']
        )

    def test_get_messages(self):
        self.bag.reset()
        self.bag.add('email', 'Your email is invalid')
        self.bag.add('username', 'Your username too short')
        self.assertEqual(
            self.bag.messages(), 
            ['Your email is invalid', 'Your username too short']
        )

    def test_can_convert_to_json(self):
        self.bag.reset()
        self.bag.add('email', 'Your email is invalid')
        self.assertEqual(
            self.bag.json(), 
            '{"email": ["Your email is invalid"]}'
        )

    def test_can_merge(self):
        self.bag.reset()
        self.bag.add('email', 'Your email is invalid')
        self.bag.merge({'username': ['username is too short']})
        self.assertEqual(self.bag.count(), 2)
