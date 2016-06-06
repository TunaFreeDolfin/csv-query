import config
import sys


class Person(object):

    '''
    Represents a Person record
    '''

    _first_name_key = "first_name"
    _last_name_key = "last_name"
    _age_key = "age"
    _github_account_key = "github_account"
    _grad_date_key = "3rd_grade_grad_date"

    def __init__(self, id, first_name=None, last_name=None, age=None, github_account=None, third_grade_graduation=None,
                 store=None):
        self._store = store or config.store
        self._id = id
        self._key = "person:{}".format(id)
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if age is not None:
            self.age = age
        if github_account is not None:
            self.github_account = github_account
        if third_grade_graduation is not None:
            self.third_grade_graduation = third_grade_graduation

    def _get_property_key(self, property_name):
        '''
        Formats the property key
        :param property_name: the property name to get the key for
        :return:
        '''
        return "{}:{}".format(self._key, property_name)

    def _get_property(self, property_name):
        '''
        Gets the specified property
        :param property_name: The property to get
        :return:
        '''
        return self._store.get(self._get_property_key(property_name)) or ''

    def _set_property(self, property_name, value):
        '''
        Sets the specified property
        :param property_name: The property to set
        :param value: The value to set it to
        :return:
        '''
        self._store.set(self._get_property_key(property_name), value)

    @property
    def id(self):
        return self._id

    @property
    def first_name(self):
        return self._get_property(self._first_name_key)

    @first_name.setter
    def first_name(self, name):
        self._set_property(self._first_name_key, name)

    @property
    def last_name(self):
        return self._get_property(self._last_name_key)

    @last_name.setter
    def last_name(self, name):
        self._set_property(self._last_name_key, name)

    @property
    def age(self):
        _age = self._get_property(self._age_key)
        if not _age:
            return sys.maxint
        return int(_age)

    @age.setter
    def age(self, age):
        self._set_property(self._age_key, age)

    @property
    def github_account(self):
        return self._get_property(self._github_account_key)

    @github_account.setter
    def github_account(self, name):
        self._set_property(self._github_account_key, name)

    @property
    def third_grade_graduation(self):
        return self._get_property(self._grad_date_key)

    @third_grade_graduation.setter
    def third_grade_graduation(self, grad_date):
        self._set_property(self._grad_date_key, grad_date)

    @classmethod
    def get_by_id(cls, id):
        '''
        Returns a new Person object with the passed in id
        :param id: the id for the new person
        :return: a new Person object
        '''
        return Person(id)

    def __str__(self):
        return "{},{},{},{},{},{}".format(self.id, self.first_name, self.last_name,
                                          '' if self.age == sys.maxint else self.age, self.github_account,
                                          self.third_grade_graduation)
