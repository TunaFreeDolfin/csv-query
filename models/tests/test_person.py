import mockredis

from models.person import Person


def test_person():
    mock_store = mockredis.mock_redis_client(strict=True)
    person = Person(1, 'first', 'last', 20, 'github_account', '3rd_grade_grad_date', mock_store)
    assert person.id == 1
    assert person.first_name == 'first'
    assert person.last_name == 'last'
    assert person.age == 20
    assert person.github_account == 'github_account'
    assert person.third_grade_graduation == '3rd_grade_grad_date'
