
from .RuleEnclosure import RuleEnclosure
from masonite.dot import Dot as DictDot
import inspect
import re
import hashlib
import requests


class BaseValidation:

    def __init__(self, validations, messages={}, raises={}):
        self.errors = {}
        self.messages = messages
        if isinstance(validations, str):
            self.validations = [validations]
        else:
            self.validations = validations
        self.negated = False
        self.raises = raises

    def passes(self, attribute, key, dictionary):
        return True

    def error(self, key, message):
        if key in self.messages:
            if key in self.errors:
                self.errors[key].append(self.messages[key])
                return
            self.errors.update({key: [self.messages[key]]})
            return
        
        if not isinstance(message, list):
            self.errors.update({key: [message]})
        else:
            self.errors.update({key: message})
        

    def find(self, key, dictionary, default=False):
        return DictDot().dot(key, dictionary, default)

    def message(self, key):
        return ''

    def negate(self):
        self.negated = True
        return self

    def raise_exception(self, key):
        if self.raises is not True and key in self.raises:
            error = self.raises.get(key)
            raise error(self.errors[next(iter(self.errors))][0])

        raise ValueError(self.errors[next(iter(self.errors))][0])

    def handle(self, dictionary):
        boolean = True
        for key in self.validations:
            if self.negated:
                if self.passes(self.find(key, dictionary), key, dictionary):
                    boolean = False
                    if hasattr(self, 'negated_message'):
                        self.error(key, self.negated_message(key))
                    else:
                        self.error(key, self.message(key))

                continue
            if not self.passes(self.find(key, dictionary), key, dictionary):
                boolean = False
                self.error(key, self.message(key))

            if self.errors and self.raises:
                return self.raise_exception(key)

        return boolean
    
    def reset(self):
        self.errors = {}

class required(BaseValidation):

    def passes(self, attribute, key, dictionary):
        """The passing criteria for this rule.

        This should return a True boolean value.

        Arguments:
            attribute {mixed} -- The value found within the dictionary
            key {string} -- The key in the dictionary being searched for.
                            This key may or may not exist in the dictionary.
            dictionary {dict} -- The dictionary being searched

        Returns:
            bool
        """
        return attribute

    def message(self, key):
        """A message to show when this rule fails

        Arguments:
            key {string} -- The key used to search the dictionary

        Returns:
            string
        """
        return 'The {} field is required.'.format(key)

    def negated_message(self, key):
        """A message to show when this rule is negated using a negation rule like 'isnt()'

        For example if you have a message that says 'this is required' you may have a negated statement
        that says 'this is not required'.

        Arguments:
            key {string} -- The key used to search the dictionary

        Returns:
            string
        """
        return 'The {} field is not required.'.format(key)


class timezone(BaseValidation):

    def passes(self, attribute, key, dictionary):
        import pytz
        return attribute in pytz.all_timezones

    def message(self, attribute):
        return 'The {} must be a valid timezone.'.format(attribute)

    def negated_message(self, attribute):
        return 'The {} must not be a valid timezone.'.format(attribute)

class one_of(BaseValidation):

    def passes(self, attribute, key, dictionary):
        for validation in self.validations:
            if validation in dictionary:
                return True

        return False

    def message(self, attribute):
        if len(self.validations) > 2:
            text = ', '.join(self.validations)
        else:
            text = ' or '.join(self.validations)

        return 'The {} is required.'.format(text)

    def negated_message(self, attribute):
        if len(self.validations) > 2:
            text = ', '.join(self.validations)
        else:
            text = ' or '.join(self.validations)

        return 'The {} is not required.'.format(text)


class accepted(BaseValidation):

    def passes(self, attribute, key, dictionary):
        return attribute is True or attribute == 'on' or attribute == 'yes' or attribute == '1' or attribute == 1

    def message(self, attribute):
        return 'The {} must be accepted.'.format(attribute)

    def negated_message(self, attribute):
        return 'The {} must not be accepted.'.format(attribute)


class ip(BaseValidation):

    def passes(self, attribute, key, dictionary):
        import socket

        try:
            socket.inet_aton(attribute)
            return True
        except socket.error:
            return False

    def message(self, attribute):
        return 'The {} must be a valid ipv4 address.'.format(attribute)

    def negated_message(self, attribute):
        return 'The {} must not be a valid ipv4 address.'.format(attribute)


class date(BaseValidation):

    def passes(self, attribute, key, dictionary):
        import pendulum
        try:
            date = pendulum.parse(attribute)
            return date
        except pendulum.parsing.exceptions.ParserError:
            return False

    def message(self, attribute):
        return 'The {} must be a valid date.'.format(attribute)

    def negated_message(self, attribute):
        return 'The {} must not be a valid date.'.format(attribute)


class before_today(BaseValidation):

    def __init__(self, validations, tz='Universal', messages={}, raises={}):
        super().__init__(validations, messages=messages, raises=raises)
        self.tz = tz

    def passes(self, attribute, key, dictionary):
        import pendulum
        try:
            return pendulum.parse(attribute, tz=self.tz) <= pendulum.yesterday()
        except pendulum.parsing.exceptions.ParserError:
            return False

    def message(self, attribute):
        return 'The {} must be a date before today.'.format(attribute)

    def negated_message(self, attribute):
        return 'The {} must not be a date before today.'.format(attribute)


class after_today(BaseValidation):

    def __init__(self, validations, tz='Universal', messages={}, raises={}):
        super().__init__(validations, messages=messages, raises=raises)
        self.tz = tz

    def passes(self, attribute, key, dictionary):
        import pendulum
        try:
            return pendulum.parse(attribute, tz=self.tz) >= pendulum.yesterday()
        except pendulum.parsing.exceptions.ParserError:
            return False

    def message(self, attribute):
        return 'The {} must be a date after today.'.format(attribute)

    def negated_message(self, attribute):
        return 'The {} must not be a date after today.'.format(attribute)


class is_past(BaseValidation):

    def __init__(self, validations, tz='Universal', messages={}, raises={}):
        super().__init__(validations, messages=messages, raises=raises)
        self.tz = tz

    def passes(self, attribute, key, dictionary):
        import pendulum
        try:
            return pendulum.parse(attribute, tz=self.tz).is_past()
        except pendulum.parsing.exceptions.ParserError:
            return False

    def message(self, attribute):
        return 'The {} must be a time in the past.'.format(attribute)

    def negated_message(self, attribute):
        return 'The {} must not be a time in the past.'.format(attribute)


class is_future(BaseValidation):

    def __init__(self, validations, tz='Universal', messages={}, raises={}):
        super().__init__(validations, messages=messages, raises=raises)
        self.tz = tz

    def passes(self, attribute, key, dictionary):
        import pendulum
        try:
            return pendulum.parse(attribute, tz=self.tz).is_future()
        except pendulum.parsing.exceptions.ParserError:
            return False

    def message(self, attribute):
        return 'The {} must be a time in the past.'.format(attribute)

    def negated_message(self, attribute):
        return 'The {} must not be a time in the past.'.format(attribute)


class email(BaseValidation):

    def passes(self, attribute, key, dictionary):
        return re.compile(r"^[^.].+@([?)[a-zA-Z0-9-.])+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$").match(attribute)

    def message(self, attribute):
        return 'The {} must be a valid email address.'.format(attribute)

    def negated_message(self, attribute):
        return 'The {} must not be a valid email address.'.format(attribute)

class matches(BaseValidation):
    def __init__(self, validations, match, messages={}, raises={}):
        super().__init__(validations, messages=messages, raises=raises)
        self.match = match

    def passes(self, attribute, key, dictionary):
        return attribute == dictionary[self.match]

    def message(self, attribute):
        return 'The {} must match {}.'.format(attribute, self.match)

    def negated_message(self, attribute):
        return 'The {} must not match {}.'.format(attribute, self.match)


class exists(BaseValidation):

    def passes(self, attribute, key, dictionary):
        return key in dictionary

    def message(self, attribute):
        return 'The {} must exist.'.format(attribute)

    def negated_message(self, attribute):
        return 'The {} must not exist.'.format(attribute)


class active_domain(BaseValidation):

    def passes(self, attribute, key, dictionary):
        import socket
        try:
            if '@' in attribute:
                # validation is for an email address
                return socket.gethostbyname(
                    attribute.split('@')[1]
                )

            return socket.gethostbyname(
                attribute.replace(
                    'https://', '').replace('http://', '').replace('www.', '')
            )
        except socket.gaierror:
            return False

    def message(self, attribute):
        return 'The {} must be an active domain name.'.format(attribute)

    def negated_message(self, attribute):
        return 'The {} must not be an active domain name.'.format(attribute)


class numeric(BaseValidation):

    def passes(self, attribute, key, dictionary):
        return str(attribute).isdigit()

    def message(self, attribute):
        return 'The {} must be a numeric.'.format(attribute)

    def negated_message(self, attribute):
        return 'The {} must not be a numeric.'.format(attribute)


class string(BaseValidation):

    def passes(self, attribute, key, dictionary):
        return isinstance(attribute, str)

    def message(self, attribute):
        return 'The {} must be a string.'.format(attribute)

    def negated_message(self, attribute):
        return 'The {} must not be a string.'.format(attribute)


class none(BaseValidation):

    def passes(self, attribute, key, dictionary):
        return attribute is None

    def message(self, attribute):
        return 'The {} must be None.'.format(attribute)

    def negated_message(self, attribute):
        return 'The {} must not be None.'.format(attribute)


class length(BaseValidation):

    def __init__(self, validations, min=1, max=999999, messages={}, raises={}):
        super().__init__(validations, messages=messages, raises=raises)
        if isinstance(min, str) and '..' in min:
            self.min = int(min.split('..')[0])
            self.max = int(min.split('..')[1])
        else:
            self.min = min
            self.max = max

    def passes(self, attribute, key, dictionary):
        return len(str(attribute)) >= self.min and len(str(attribute)) <= self.max

    def message(self, attribute):
        return 'The {} length must be between {} and {}.'.format(attribute, self.min, self.max)

    def negated_message(self, attribute):
        return 'The {} length must not be between {} and {}.'.format(attribute, self.min, self.max)


class in_range(BaseValidation):

    def __init__(self, validations, min=1, max=255, messages={}, raises={}):
        super().__init__(validations, messages=messages, raises=raises)
        self.min = min
        self.max = max

    def passes(self, attribute, key, dictionary):
        return attribute >= self.min and attribute <= self.max

    def message(self, attribute):
        return 'The {} must be between {} and {}.'.format(attribute, self.min, self.max)

    def negated_message(self, attribute):
        return 'The {} must not be between {} and {}.'.format(attribute, self.min, self.max)


class equals(BaseValidation):

    def __init__(self, validations, value='', messages={}, raises={}):
        super().__init__(validations, messages=messages, raises=raises)
        self.value = value

    def passes(self, attribute, key, dictionary):
        return attribute == self.value

    def message(self, attribute):
        return 'The {} must be equal to {}.'.format(attribute, self.value)

    def negated_message(self, attribute):
        return 'The {} must not be equal to {}.'.format(attribute, self.value)


class contains(BaseValidation):

    def __init__(self, validations, value='', messages={}, raises={}):
        super().__init__(validations, messages=messages, raises=raises)
        self.value = value

    def passes(self, attribute, key, dictionary):
        return self.value in attribute

    def message(self, attribute):
        return 'The {} must contain {}.'.format(attribute, self.value)

    def negated_message(self, attribute):
        return 'The {} must not contain {}.'.format(attribute, self.value)


class is_in(BaseValidation):

    def __init__(self, validations, value='', messages={}, raises={}):
        super().__init__(validations, messages=messages, raises=raises)
        self.value = value

    def passes(self, attribute, key, dictionary):
        return attribute in self.value

    def message(self, attribute):
        return 'The {} must contain an element in {}.'.format(attribute, self.value)

    def negated_message(self, attribute):
        return 'The {} must not contain an element in {}.'.format(attribute, self.value)


class greater_than(BaseValidation):

    def __init__(self, validations, value='', messages={}, raises={}):
        super().__init__(validations, messages=messages, raises=raises)
        self.value = value

    def passes(self, attribute, key, dictionary):
        return attribute > self.value

    def message(self, attribute):
        return 'The {} must be greater than {}.'.format(attribute, self.value)

    def negated_message(self, attribute):
        return 'The {} must be greater than {}.'.format(attribute, self.value)


class less_than(BaseValidation):

    def __init__(self, validations, value='', messages={}, raises={}):
        super().__init__(validations, messages=messages, raises=raises)
        self.value = value

    def passes(self, attribute, key, dictionary):
        return attribute < self.value

    def message(self, attribute):
        return 'The {} must be less than {}.'.format(attribute, self.value)

    def negated_message(self, attribute):
        return 'The {} must not be less than {}.'.format(attribute, self.value)

class strong(BaseValidation):

    def __init__(self, validations, length=8, uppercase=2, numbers=2, special=2, breach=False, messages={}, raises={}):
        super().__init__(validations, messages=messages, raises=raises)
        self.length = length
        self.uppercase = uppercase
        self.numbers = numbers
        self.special = special
        self.breach = breach
        self.length_check = True
        self.uppercase_check = True
        self.numbers_check = True
        self.special_check = True
        self.breach_check = True

    def passes(self, attribute, key, dictionary):
        all_clear = True

        if len(attribute) <= self.length: 
            all_clear = False
            self.length_check = False

        if self.uppercase is not 0:
            uppercase = 0
            for letter in attribute:
                if letter.isupper():
                    uppercase += 1
            
            if uppercase <= self.uppercase:
                self.uppercase_check = False
                all_clear = False

        if self.numbers is not 0:
            numbers = 0
            for letter in attribute:
                if letter.isdigit():
                    numbers += 1
            
            if numbers <= self.numbers:
                self.numbers_check = False
                all_clear = False
        
        # if self.breach:
        #     try:
        #         from pwnedapi import Password
        #     except ImportError:
        #         raise ImportError(
        #             "Checking for breaches requires the 'pwnedapi' library. Please install it with 'pip install pwnedapi'")
            
        #     password = Password(attribute)
        #     if password.is_pwned():
        #         self.breach_check = False
        #         all_clear = False

        if self.special is not 0:
            if len(re.findall('[^A-Za-z0-9]', attribute)) < self.special:
                self.special_check = False
                all_clear = False

        return all_clear

    def message(self, attribute):
        message = []
        if not self.length_check:
            message.append('{} must be {} characters in length'.format(attribute, self.length))

        if not self.uppercase_check:
            message.append('{} must have {} uppercase letters'.format(attribute, self.uppercase))
        
        if not self.special_check:
            message.append('{} must have {} special characters'.format(attribute, self.special))
        
        if not self.numbers_check:
            message.append('{} must have {} numbers'.format(attribute, self.numbers))
        
        if not self.breach_check:
            message.append('{} has been breached in the past. Try another {}'.format(
                attribute, attribute))
        
        return message

    def negated_message(self, attribute):
        return 'The {} must not be less than {}.'.format(attribute, self.value)


class isnt(BaseValidation):

    def __init__(self, *rules, messages={}, raises={}):
        super().__init__(rules)

    def handle(self, dictionary):
        for rule in self.validations:
            rule.negate().handle(dictionary)
            self.errors.update(rule.errors)

class does_not(BaseValidation):

    def __init__(self, *rules, messages={}, raises={}):
        super().__init__(rules)
        self.should_run_then = True

    def handle(self, dictionary):
        self.dictionary = dictionary
        errors = False
        for rule in self.validations:
            if rule.handle(dictionary):
                errors = True

        if not errors:
            for rule in self.then_rules:
                if not rule.handle(dictionary):
                    self.errors.update(rule.errors)


    def then(self, *rules):
        self.then_rules = rules
        return self


class when(BaseValidation):

    def __init__(self, *rules, messages={}, raises={}):
        super().__init__(rules)
        self.should_run_then = True

    def handle(self, dictionary):
        self.dictionary = dictionary
        errors = False
        for rule in self.validations:
            if rule.handle(dictionary):
                errors = True

        if errors:
            for rule in self.then_rules:
                if not rule.handle(dictionary):
                    self.errors.update(rule.errors)

    def then(self, *rules):
        self.then_rules = rules
        return self


class truthy(BaseValidation):

    def passes(self, attribute, key, dictionary):
        return attribute

    def message(self, attribute):
        return 'The {} must be a truthy value.'.format(attribute)

    def negated_message(self, attribute):
        return 'The {} must not be a truthy value.'.format(attribute)


class json(BaseValidation):

    def passes(self, attribute, key, dictionary):
        import json as json_module

        # Hacky workaround for Python 3.4
        try:
            JsonParseException = json.decoder.JSONDecodeError
        except AttributeError:
            JsonParseException = ValueError

        try:
            return json_module.loads(str(attribute))
        except (TypeError, JsonParseException):
            return False

    def message(self, attribute):
        return 'The {} must be a valid JSON.'.format(attribute)

    def negated_message(self, attribute):
        return 'The {} must not be a valid JSON.'.format(attribute)


class phone(BaseValidation):

    def __init__(self, *rules, pattern="123-456-7890", messages={}, raises={}):
        super().__init__(rules, messages={}, raises={})
        # 123-456-7890
        # (123)456-7890
        self.pattern = pattern

    def passes(self, attribute, key, dictionary):
        if self.pattern == '(123)456-7890':
            return re.compile(r"^\(\w{3}\)\w{3}\-\w{4}$").match(attribute)
        elif self.pattern == '123-456-7890':
            return re.compile(r"^\w{3}\-\w{3}\-\w{4}$").match(attribute)

    def message(self, attribute):
        if self.pattern == '(123)456-7890':
            return 'The {} must be in the format (XXX)XXX-XXXX.'.format(attribute)
        elif self.pattern == '123-456-7890':
            return 'The {} must be in the format XXX-XXX-XXXX.'.format(attribute)

    def negated_message(self, attribute):
        if self.pattern == '(123)456-7890':
            return 'The {} must not be in the format (XXX)XXX-XXXX.'.format(attribute)
        elif self.pattern == '123-456-7890':
            return 'The {} must not be in the format XXX-XXX-XXXX.'.format(attribute)


class confirmed(BaseValidation):

    def passes(self, attribute, key, dictionary):
        if key in dictionary and key + '_confirmation' in dictionary:
            return dictionary[key] == dictionary['{}'.format(key + '_confirmation')]
        return False

    def message(self, attribute):
        return 'The {} confirmation does not match.'.format(attribute)

    def negated_message(self, attribute):
        return 'The {} confirmation matches.'.format(attribute)

def flatten(iterable):
    
    flat_list = []
    for route in iterable:
        if isinstance(route, list):
            for r in flatten(route):
                flat_list.append(r)
        else:
            flat_list.append(route)

    return flat_list

class Validator:

    def __init__(self):
        pass

    def validate(self, dictionary, *rules):
        rule_errors = {}
        try:
            for rule in rules:
                if isinstance(rule, str):
                    rule = self.parse_string(rule)
                    # continue
                elif isinstance(rule, dict):
                    rule = self.parse_dict(rule, dictionary, rule_errors)
                    continue

                elif inspect.isclass(rule) and isinstance(rule(), RuleEnclosure):
                    rule_errors.update(self.run_enclosure(rule(), dictionary))
                    continue

                rule.handle(dictionary)
                for error, message in rule.errors.items():
                    if error not in rule_errors:
                        rule_errors.update({error: message})
                    else:
                        messages = rule_errors[error]
                        messages += message
                        rule_errors.update({error: messages})
                rule.reset()
            return rule_errors

        except Exception as e:
            e.errors = rule_errors
            raise e

        return rule_errors

    def parse_string(self, rule):
        rule, parameters = rule.split(':')[0], rule.split(':')[1].split(',')
        return ValidationFactory().registry[rule](parameters)

    def parse_dict(self, rule, dictionary, rule_errors):
        for value, rules in rule.items():
            for rule in rules.split('|'):
                rule, args = rule.split(':')[0], rule.split(':')[1:]
                rule = ValidationFactory().registry[rule](value, *args)

            rule.handle(dictionary)
            for error, message in rule.errors.items():
                if error not in rule_errors:
                    rule_errors.update({error: message})
                else:
                    messages = rule_errors[error]
                    messages += message
                    rule_errors.update({error: messages})

    def run_enclosure(self, enclosure, dictionary):
        rule_errors = {}
        for rule in enclosure.rules():
            rule.handle(dictionary)
            for error, message in rule.errors.items():
                if error not in rule_errors:
                    rule_errors.update({error: message})
                else:
                    messages = rule_errors[error]
                    messages += message
                    rule_errors.update({error: messages})
            rule.reset()
        return rule_errors

    def extend(self, key, obj=None):
        if isinstance(key, dict):
            self.__dict__.update(key)
            return self

        self.__dict__.update({key: obj})
        return self

    def register(self, *cls):
        for obj in cls:
            self.__dict__.update({
                obj.__name__: obj
            })


class ValidationFactory:

    registry = {}

    def __init__(self):
        self.register(
            accepted,
            active_domain,
            after_today,
            before_today,
            confirmed,
            contains,
            date,
            does_not,
            equals,
            email,
            exists,
            greater_than,
            in_range,
            is_future,
            is_in,
            isnt,
            is_past,
            ip,
            json,
            length,
            less_than,
            matches,
            none,
            numeric,
            one_of,
            phone,
            required,
            string,
            strong,
            timezone,
            truthy,
            when,
        )

    def register(self, *cls):
        for obj in cls:
            self.registry.update({
                obj.__name__: obj
            })
