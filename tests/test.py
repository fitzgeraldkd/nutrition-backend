from bcrypt import gensalt, hashpw

from api.model import db
from api.model.user import User
from tests.utils import ApiTestCase


class UserTests(ApiTestCase):

    def test_user_authentication(self):
        hashed_password = hashed_password = hashpw('fizz'.encode('utf8'), gensalt())
        user = User(id=1, email='foo@bar.com', password=hashed_password)
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()

        # An invalid email returns a 400.
        response = self.client.post('/api/v1.0/auth', json={
            'email': 'missing@user.com',
            'password': 'fizz',
        })
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json, {'error': 'Invalid login credentials.'})

        # An invalid password returns a 400.
        response = self.client.post('/api/v1.0/auth', json={
            'email': 'foo@bar.com',
            'password': 'buzz',
        })
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json, {'error': 'Invalid login credentials.'})

        # Providing the correct credentials sets the user_id in the session.
        response = self.client.post('/api/v1.0/auth', json={
            'email': 'foo@bar.com',
            'password': 'fizz',
        })
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, {})
        with self.client.session_transaction() as session:
            self.assertEqual(session['user_id'], 1)

        # A user can fetch their own info when logged in.
        response = self.client.get('/api/v1.0/auth')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, {'user': 1})

        # Logging out clears the session.
        response = self.client.delete('/api/v1.0/auth')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, {})
        with self.client.session_transaction() as session:
            self.assertCountEqual(session.keys(), [])

        # An anonymous user cannot fetch auth info.
        response = self.client.get('/api/v1.0/auth')
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json, {})

        # An invalid user id is cleared from the session.
        with self.client.session_transaction() as session:
            session['user_id'] = 'invalid'
        response = self.client.get('/api/v1.0/auth')
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json, {})
        with self.client.session_transaction() as session:
            self.assertCountEqual(session.keys(), [])
