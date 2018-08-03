from django.test import TestCase

# Create your tests here.
from redis import Redis

conn = Redis('10.20.1.18', port='6379', password='123456')
conn.delete(*['a','p'])