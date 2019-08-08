
<p align="center">
  <img src="https://i.imgur.com/rEXcoMn.png" width="160px">
</p>

## Masonite Validation

This package is a standalone component package for the [Masonite](https://github.com/masoniteframework/masonite) framework.

Masonite comes with this package out of the box but you can also use this package by itself.

**Installing this package does not install the Masonite framework. This only installs the few modules necessary to have validation.**

****

## Installation

First `pip` install it:

```
$ pip install masonite-validation
```

## Getting Started

To use this package you can import the `Validator` class at the top:

```python
from masonite.validation import Validator
```

As well as some rules:


```python
from masonite.validation import Validator, required, exists, accepted
```

And then specify the rules in this format:

```python
# Validator({dictionary}, *rules, **kwargs)
```

So for example to validate this payload:

```python
payload = {
    'user': 'username123',
    'company': 'Masonite',
    'terms': 'on' # For checkboxes
}

errors = Validator(
    payload,
    required(['user', 'company', 'terms']),
    accepted('terms')
  )
```

Errors will either be nothing or an dictionary of error messages

## Documentation

You can find extension documentation on available rules at the [Masonite Documentation](https://docs.masoniteproject.com/advanced/validation#available-rules)
