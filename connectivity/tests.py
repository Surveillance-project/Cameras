from django.test import TestCase
from unittest.case import TestCase as UnitCase
from services.connectivity import authorize


class ConnectivityTest(UnitCase):

    def test_authorization(self):
        authorize()
