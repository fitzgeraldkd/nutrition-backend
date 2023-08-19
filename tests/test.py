from api.model import db
from api.model.user import User
from tests.factories import UserFactory
from tests.utils import ApiTestCase


class UserTests(ApiTestCase):
    def test_post_with_valid_data(self):
        user = User.query.filter(User.email == "kenny@kdfitz.com").first()
        self.assertIsNone(user)

        response = self.client.post(
            "/api/v1.0/users",
            json={"email": "kenny@kdfitz.com", "password": "TestPassword"},
        )
        self.assertEqual(response.status_code, 200)

        user = User.query.filter(User.email == "kenny@kdfitz.com").first()
        self.assertIsNotNone(user)

    def test_post_with_invalid_data(self):
        response = self.client.post(
            "/api/v1.0/users", json={"email": "kenny@kdfitz.com"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json, {"error": "A password is required."})

        response = self.client.post(
            "/api/v1.0/users", json={"password": "TestPassword"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json, {"error": "An email is required."})

    def test_prevent_duplicates(self):
        UserFactory(email="existing@user.com")
        response = self.client.post(
            "/api/v1.0/users",
            json={"email": "existing@user.com", "password": "TestPassword"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(
            response.json,
            {"error": "An account with this email address already exists."},
        )


class AuthTests(ApiTestCase):
    def test_user_authentication(self):
        UserFactory(id=1, email="foo@bar.com", raw_password="fizz")

        # An invalid email returns a 400.
        response = self.client.post(
            "/api/v1.0/auth",
            json={
                "email": "missing@user.com",
                "password": "fizz",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json, {"error": "Invalid login credentials."})

        # An invalid password returns a 400.
        response = self.client.post(
            "/api/v1.0/auth",
            json={
                "email": "foo@bar.com",
                "password": "buzz",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json, {"error": "Invalid login credentials."})

        # Providing the correct credentials sets the user_id in the session.
        response = self.client.post(
            "/api/v1.0/auth",
            json={
                "email": "foo@bar.com",
                "password": "fizz",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, {})
        with self.client.session_transaction() as session:
            self.assertEqual(session["user_id"], 1)

        # A user can fetch their own info when logged in.
        response = self.client.get("/api/v1.0/auth")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, {"user": 1})

        # Logging out clears the session.
        response = self.client.delete("/api/v1.0/auth")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, {})
        with self.client.session_transaction() as session:
            self.assertCountEqual(session.keys(), [])

        # An anonymous user cannot fetch auth info.
        response = self.client.get("/api/v1.0/auth")
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json, {})

        # An invalid user id is cleared from the session.
        with self.client.session_transaction() as session:
            session["user_id"] = "invalid"
        response = self.client.get("/api/v1.0/auth")
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json, {})
        with self.client.session_transaction() as session:
            self.assertCountEqual(session.keys(), [])

        # The email field is case-insensitive.
        response = self.client.post(
            "/api/v1.0/auth",
            json={
                "email": "FOO@BAR.COM",
                "password": "fizz",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, {})
        with self.client.session_transaction() as session:
            self.assertEqual(session["user_id"], 1)
