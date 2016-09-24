from __future__ import print_function, unicode_literals
import os
from unittest import TestCase
import tempfile
import shutil
from obs.importer.from_dokuwiki import OBSDokuwikiImporter


class TestImportFromDokuwiki(TestCase):

    def test_import_from_dokuwiki(self):
        """
        This tests the expected conditions
        """
        lang = 'en'
        git_repo = 'file://' + os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', 'github.com/')
        out_dir = tempfile.mkdtemp(prefix='testOBS_')

        try:
            with OBSDokuwikiImporter(lang, git_repo, out_dir, False) as importer:
                importer.run()

            # check for output files
            self.assertTrue(os.path.isfile(os.path.join(out_dir, 'manifest.json')))
            self.assertTrue(os.path.isfile(os.path.join(out_dir, 'content', '01.md')))
            self.assertTrue(os.path.isfile(os.path.join(out_dir, 'content', '50.md')))
            self.assertTrue(os.path.isfile(os.path.join(out_dir, 'content', '_back', 'back-matter.md')))
            self.assertTrue(os.path.isfile(os.path.join(out_dir, 'content', '_front', 'front-matter.md')))

        finally:
            # delete temp files
            if os.path.isdir(out_dir):
                shutil.rmtree(out_dir, ignore_errors=True)

    def test_not_github(self):
        """
        This test the exception when the repository is not on github
        """
        lang = 'en'
        git_repo = 'file://' + os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', 'git.door43.org')
        out_dir = tempfile.mkdtemp(prefix='testOBS_')

        try:
            with self.assertRaises(Exception) as context:
                with OBSDokuwikiImporter(lang, git_repo, out_dir, False) as importer:
                    importer.run()

            self.assertEqual('Currently only github repositories are supported.', str(context.exception))

        finally:
            # delete temp files
            if os.path.isdir(out_dir):
                shutil.rmtree(out_dir, ignore_errors=True)

    def test_lang_code_not_found(self):
        """
        This test the exception when the repository is not on github
        """
        lang = 'no_lang'
        git_repo = 'file://' + os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', 'github.com')
        out_dir = tempfile.mkdtemp(prefix='testOBS_')

        try:
            with self.assertRaises(Exception) as context:
                with OBSDokuwikiImporter(lang, git_repo, out_dir, False) as importer:
                    importer.run()

            self.assertEqual('Information for language "{0}" was not found.'.format(lang), str(context.exception))

        finally:
            # delete temp files
            if os.path.isdir(out_dir):
                shutil.rmtree(out_dir, ignore_errors=True)
