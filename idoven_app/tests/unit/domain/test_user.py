import pytest
from idoven_app.tests.helper.test_user_builder import TestUserData, UserBuilder
from idoven_app.idoven.domain.user import User, Role, UserFactory, UserInvalidException


def test_user_verifies_password():
    user = UserBuilder().build_user_with_password("pwd").build()
    assert user.verify_password("pwd")


def test_user_factory_creates_a_user():
    user = UserBuilder().build_user_with_user_id(TestUserData.ANY_USER_ID).build()
    assert user.user_id == TestUserData.ANY_USER_ID


def test_user_factory_raise_error_with_no_user_id():
    with pytest.raises(UserInvalidException):
        UserBuilder().build_user_with_user_id("").build()


def test_user_factory_raise_error_with_no_username():
    with pytest.raises(UserInvalidException):
        UserBuilder().build_user_with_username("").build()


def test_user_factory_raise_error_with_no_password():
    with pytest.raises(UserInvalidException):
        UserBuilder().build_user_with_password("").build()


def test_user_factory_raise_error_with_invalid_role():
    with pytest.raises(UserInvalidException):
        UserBuilder().build_user_with_role("").build()
