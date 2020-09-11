import pytest
from models.user import UserModel
from conftest import is_valid
from unittest.mock import patch
from resources.email import Email


@pytest.mark.usefixtures('client_class', 'test_database')
class TestForgotPassword:
    def test_request_with_invalid_params(self):
        response = self.client.post('/api/forgot_password')
        assert is_valid(response, 400)

    def test_request_with_invalid_email(self):
        response = self.client.post('/api/forgot_password', json={'email': 'invalid@example.org'})
        assert is_valid(response, 400)
        assert response.json == {'message': 'Invalid email'}

    @patch.object(Email, 'send_reset_password_msg')
    def test_request_with_valid_email(self, send_reset_email):
        user = UserModel.find_by_id(1)
        response = self.client.post('/api/forgot_password', json={'email': user.email})

        assert is_valid(response, 200)
        assert response.json == {"message": "Email sent"}
        send_reset_email.assert_called_once_with(user)


    @patch.object(Email, 'send_reset_password_msg')
    def test_request_with_invalid_user(self, send_reset_email):
        response = self.client.post('/api/forgot_password', json={'email': 'invalid_email@nickschimek.com'})

        send_reset_email.assert_not_called()
        assert is_valid(response, 400)
