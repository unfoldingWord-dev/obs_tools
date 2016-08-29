from __future__ import print_function, unicode_literals
import os
from unittest import TestCase
from obs.obs_classes import OBSStatus


class TestOBSStatus(TestCase):

    def test_default_constructor(self):
        status_obj = OBSStatus()
        self.assertEqual('1', status_obj.checking_level)
        self.assertEqual('en', status_obj.source_text)
        self.assertEqual('', status_obj.checking_entity)

    def test_file_name_constructor(self):
        file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', 'status.json')
        status_obj = OBSStatus(file_name)
        self.assertEqual('3', status_obj.checking_level)
        self.assertEqual('en', status_obj.source_text)
        self.assertEqual('Unit testing team', status_obj.checking_entity)
