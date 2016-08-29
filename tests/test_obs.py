from __future__ import print_function, unicode_literals

import codecs
import glob
import json
import os
import datetime
from unittest import TestCase
from general_tools.file_utils import load_json_object
from obs.obs_classes import OBS, OBSChapter, OBSEncoder


class TestOBS(TestCase):

    def test_ts_obs(self):
        """
        Tests all the functions of the OBS class, as used when importing from a tS repository
        """
        today = ''.join(str(datetime.date.today()).rsplit('-')[0:3])

        # load and process the manifest
        content_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', 'ts')
        file_name = os.path.join(content_dir, 'manifest.json')
        manifest = load_json_object(file_name)

        lang = manifest['target_language']['id']
        obs_obj = OBS()
        obs_obj.date_modified = today
        obs_obj.direction = manifest['target_language']['direction']
        obs_obj.language = lang

        self.assertEqual('fr', obs_obj.language)
        self.assertEqual('ltr', obs_obj.direction)

        # load the frames for each chapter
        obs_obj.chapters = TestOBS.load_obs_chapters(content_dir)
        obs_obj.chapters.sort(key=lambda c: c['number'])

        self.assertEqual(50, len(obs_obj.chapters))

        # verify the data
        verified = obs_obj.verify_all()
        self.assertTrue(verified)

        # load language data
        lang_dict = OBS.load_lang_strings()
        self.assertGreater(len(lang_dict), 7000)

        # dump the OBS to a json string that could be written to a file
        obs_json_str = json.dumps(obs_obj, sort_keys=True, cls=OBSEncoder)
        self.assertTrue('"app_words":' in obs_json_str)
        self.assertTrue('"chapters":' in obs_json_str)
        self.assertTrue('"date_modified":' in obs_json_str)
        self.assertTrue('"language":' in obs_json_str)
        self.assertTrue('"direction":' in obs_json_str)

    @staticmethod
    def load_obs_chapters(content_dir):
        print('Reading OBS pages...', end=' ')
        chapters = []
        img_url = 'https://cdn.door43.org/obs/jpg/360px/obs-en-{0}.jpg'
        for story_num in range(1, 51):
            chapter_num = str(story_num).zfill(2)
            story_dir = os.path.join(content_dir, chapter_num)
            obs_chapter = OBSChapter()
            obs_chapter.number = chapter_num

            # get the translated chapter ref
            with codecs.open(os.path.join(story_dir, 'reference.txt'), 'r', encoding='utf-8-sig') as in_file:
                obs_chapter.ref = in_file.read()

            # get the translated chapter title
            with codecs.open(os.path.join(story_dir, 'title.txt'), 'r', encoding='utf-8-sig') as in_file:
                obs_chapter.title = in_file.read()

            # loop through the frames for this chapter
            frame_list = glob.glob('{0}/[0-9][0-9].txt'.format(story_dir))
            for frame_file in frame_list:
                with codecs.open(frame_file, 'r', encoding='utf-8-sig') as in_file:
                    frame_text = in_file.read()

                frame_id = chapter_num + '-' + os.path.splitext(os.path.basename(frame_file))[0]

                frame = {'id': frame_id,
                         'img': img_url.format(frame_id),
                         'text': frame_text
                         }

                obs_chapter.frames.append(frame)

            # sort the frames by id
            obs_chapter.frames.sort(key=lambda f: f['id'])

            # add this chapter to the OBS object
            chapters.append(obs_chapter)

        print('finished.')
        return chapters
