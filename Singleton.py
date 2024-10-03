class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance

# sources:
# https://stackoverflow.com/questions/6760685/what-is-the-best-way-of-implementing-singleton-in-python
# https://www.geeksforgeeks.org/singleton-pattern-in-python-a-complete-guide/