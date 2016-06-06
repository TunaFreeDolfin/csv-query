import mockredis
import pytest
import sys

from models.person import Person
from models.person_index import PersonIndex


def test_get_ids_by_last_name():
    mock_store = mockredis.mock_redis_client(strict=True)
    person_index = PersonIndex(mock_store)
    person1 = Person(1, 'first', 'last', 20, 'github_account', '3rd_grade_grad_date', mock_store)
    person_index.add_person_to_index(person1)
    person2 = Person(2, 'first', 'last', 30, 'github_account', '3rd_grade_grad_date', mock_store)
    person_index.add_person_to_index(person2)
    ids = person_index.get_ids_by_last_name(person1.last_name)
    assert ids is not None
    assert str(1) in ids
    assert str(2) in ids


def test_get_ids_by_last_name_none():
    mock_store = mockredis.mock_redis_client(strict=True)
    person_index = PersonIndex(mock_store)
    person = Person(1, 'first', 'last', 20, 'github_account', '3rd_grade_grad_date', mock_store)
    person_index.add_person_to_index(person)
    ids = PersonIndex(mock_store).get_ids_by_last_name('some_other_id')
    assert len(ids) is 0


@pytest.mark.skipif(reason="mockredis doesn't seem to honor the proper param zadd order even when strict is set")
def test_all():
    mock_store = mockredis.mock_redis_client(strict=True)
    person_index = PersonIndex(mock_store)
    person1 = Person(1, 'first', 'last', sys.maxint, 'github_account', '3rd_grade_grad_date', mock_store)
    person_index.add_person_to_index(person1)
    person2 = Person(2, 'first', 'last', 20, 'github_account', '3rd_grade_grad_date', mock_store)
    person_index.add_person_to_index(person2)
    person3 = Person(3, 'first', 'last', 20, 'github_account', '3rd_grade_grad_date', mock_store)
    person_index.add_person_to_index(person3)
    people = person_index.all()
    assert people is not None
    assert next((person for person in people if person.id == str(1)), None) is not None
    assert next((person for person in people if person.id == str(2)), None) is not None
    assert next((person for person in people if person.id == str(3)), None) is not None
