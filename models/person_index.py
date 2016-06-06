import config

from models.person import Person


class PersonIndex(object):

    _key = "person_index:{}"
    _age_index = "age_index"

    def __init__(self, store=None):
        self._store = store or config.store

    def add_person_to_index(self, person):
        '''
        Adds a person to the indices
        :param person: The person to add
        :return:
        '''
        self._store.sadd(self._key.format(person.last_name), person.id)
        self._store.zadd(self._age_index, person.age, person.id)

    def get_ids_by_last_name(self, last_name):
        '''
        Returns all ids for Person objects with the specified last name
        :param last_name: The last name to get IDs for
        :return: a list of IDs matching the passed in last name
        '''
        return self._store.smembers(self._key.format(last_name))

    def all(self):
        '''
        Gets all Person objects in the system, sorted by age
        :return: collection of Person objects
        '''
        people = []
        for id in self._store.zrange(self._age_index, 0, -1):
            people.append(Person.get_by_id(id))
        return people
