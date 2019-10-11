def validate(*rules, redirect=None):
    def decorator(func, rules=rules):
        def wrapper(*args, **kwargs):
            from wsgi import container
            request = container.make('Request')
            errors = request.validate(*rules)
            if errors:
                if redirect:
                    return request.redirect(redirect)
                return errors
            else:
                return container.resolve(func)
        return wrapper
    return decorator
