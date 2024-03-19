from django.db.models import Max
from django.test import Client, TestCase

from .models import User, Post, Follow, Like

# Create your tests here.
class NetworkTestCase(TestCase):

    def setUp(self):

        # Create users.
        u1 = User.objects.create(username="username1", password="password1")
        u2 = User.objects.create(username="username2", password="password2")

        # Create posts.
        p1 = Post.objects.create(poster=u1, content="Post 1")
        p2 = Post.objects.create(poster=u2, content="Post 2")

        # Create follows.
        f1 = Follow.objects.create(follower=u1, following=u2)

    def test_valid_follow(self):
        u1 = User.objects.get(username="username1")
        u2 = User.objects.get(username="username2")
        f = Follow.objects.get(follower=u1, following=u2)
        self.assertTrue(f.is_valid_follow())

"""     def test_arrivals_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 1)

    def test_index(self):
        c = Client()
        response = c.get("/flights/")
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["flights"].count(), 3)

    def test_valid_flight_page(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_flight_page(self):
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]

        c = Client()
        response = c.get(f"/flights/{max_id + 1}")
        self.assertEqual(response.status_code, 404)

    def test_flight_page_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Alice", last="Adams")
        f.passengers.add(p)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)

    def test_flight_page_non_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Alice", last="Adams")

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1) """
