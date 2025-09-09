import pytest
from app.users.models import User
from app import db

@pytest.fixture(scope="module")
def setup():
    session = db.get_session()
    yield session
    try:
        obj = User.objects.filter(email="test2@test.com").allow_filtering()
        user = obj.get()
        user.delete()
    except User.DoesNotExist:
        pass
    session.shutdown()


def test_create_user(setup):
    User.create_user(email="test2@test.com", password="testpassword")

def test_duplicate_user(setup):
    with pytest.raises(Exception) :
        User.create_user(email="test2@test.com", password="testpassword")

def test_invalid_email(setup):
    with pytest.raises(Exception) :
        User.create_user(email="test2@test.com", password="testpassword")

def test_valid_password(setup):
    q = User.objects().filter(email="test2@test.com").allow_filtering()
    assert q.count() == 1
    user = q.first()
    assert user.verify_password("testpassword") is True
    assert user.verify_password("testpasswords") is False

    

# def test_invalid_assert():
#     with pytest.raises(AssertionError):
#         assert True is not True