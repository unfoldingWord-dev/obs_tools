from __future__ import print_function, unicode_literals
import codecs
import re
from collections import OrderedDict
from datetime import datetime
import os
from json import JSONEncoder
from obs import chapters_and_frames
from general_tools.file_utils import load_json_object
from general_tools.languages import Language


class OBSStatus(object):
    def __init__(self, file_name=None):
        """
        Class constructor. Optionally accepts the name of a file to deserialize.
        :param str file_name: The name of a file to deserialize into a OBSStatus object
        """
        # deserialize
        if file_name:
            if os.path.isfile(file_name):
                self.__dict__ = load_json_object(file_name)
            else:
                raise IOError('The file {0} was not found.'.format(file_name))
        else:
            self.checking_entity = ''
            self.checking_level = '1'
            self.comments = ''
            self.contributors = ''
            self.publish_date = datetime.today().strftime('%Y-%m-%d')
            self.source_text = 'en'
            self.source_text_version = ''
            self.version = ''

    def __contains__(self, item):
        return item in self.__dict__

    @staticmethod
    def from_manifest(manifest):
        status = OBSStatus()

        resource = manifest['resource']
        resource_status = resource['status']

        status.checking_entity = ', '.join(resource_status['checking_entity'])
        status.checking_level = resource_status['checking_level']
        status.comments = resource_status['comments']
        status.contributors = ', '.join(resource_status['contributors'])
        status.publish_date = resource_status['pub_date']
        status.source_text = resource_status['source_translations'][0]['language_slug']
        status.source_text_version = resource_status['source_translations'][0]['version']
        status.version = resource_status['version']

        return status


class OBSChapter(object):

    title_re = re.compile(r'^\s*#(.*?)#*\n', re.UNICODE)
    ref_re = re.compile(r'\n(_*.*?_*)\n*$', re.UNICODE)
    frame_re = re.compile(r'!\[(?:OBS Image|Image)\].*?obs-en-(\d\d)-(\d\d)\.jpg.*?\)\n([^!]*)', re.UNICODE)
    img_url = 'https://cdn.door43.org/obs/jpg/360px/obs-en-{0}.jpg'

    def __init__(self, json_obj=None):
        """
        Class constructor. Optionally accepts an object for initialization.
        :param object json_obj: The name of a file to deserialize into a OBSStatus object
        """
        # deserialize
        if json_obj:
            self.__dict__ = json_obj  # type: dict

        else:
            self.frames = []  # type: list<dict>
            self.number = ''
            self.ref = ''
            self.title = ''

    def get_errors(self):
        """
        Checks this chapter for errors
        :returns list<str>
        """
        errors = []

        if not self.title:
            msg = 'Title not found: {0}'.format(self.number)
            print(msg)
            errors.append(msg)

        if not self.ref:
            msg = 'Ref not found: {0}'.format(self.number)
            print(msg)
            errors.append(msg)

        chapter_index = int(self.number) - 1

        # get the expected number of frames for this chapter
        expected_frame_count = chapters_and_frames.frame_counts[chapter_index]

        for x in range(1, expected_frame_count + 1):

            # frame id is formatted like '01-01'
            frame_id = '{0}-{1}'.format(self.number.zfill(2), str(x).zfill(2))

            # get the next frame
            frame = next((f for f in self.frames if f['id'] == frame_id), None)  # type: dict
            if not frame:
                msg = 'Frame not found: {0}'.format(frame_id)
                print(msg)
                errors.append(msg)
            else:
                # check the frame img and  values
                if 'img' not in frame or not frame['img']:
                    msg = 'Attribute "img" is missing for frame {0}'.format(frame_id)
                    print(msg)
                    errors.append(msg)

                if 'text' not in frame or not frame['text']:
                    msg = 'Attribute "text" is missing for frame {0}'.format(frame_id)
                    print(msg)
                    errors.append(msg)

        return errors

    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

    def __str__(self):
        return self.__class__.__name__ + ' ' + self.number

    @staticmethod
    def from_markdown(markdown, chapter_number):
        """

        :param str|unicode markdown:
        :param int chapter_number:
        :return: OBSChapter
        """

        return_val = OBSChapter()
        return_val.number = str(chapter_number).zfill(2)

        # remove Windows line endings
        markdown = markdown.replace('\r\n', '\n')

        # title: the first non-blank line is title if it starts with '#'
        match = OBSChapter.title_re.search(markdown)
        if match:
            return_val.title = match.group(1).strip()
            markdown = markdown.replace(match.group(0), str(''), 1)

        # ref
        match = OBSChapter.ref_re.search(markdown)
        if match:
            return_val.ref = match.group(1).strip()
            markdown = markdown.replace(match.group(0), str(''), 1)

        # frames
        for frame in OBSChapter.frame_re.finditer(markdown):
            # 1: chapter number
            # 2: frame number
            # 3: frame text

            if int(frame.group(1)) != chapter_number:
                raise Exception('Expected chapter {0} but found {1}.'.format(str(chapter_number), frame.group(1)))

            frame_id = '{0}-{1}'.format(frame.group(1), frame.group(2))

            frame = {'id': frame_id,
                     'img': OBSChapter.img_url.format(frame_id),
                     'text': frame.group(3).strip()
                     }

            return_val.frames.append(frame)

        return return_val


class OBS(object):
    def __init__(self, file_name=None):
        """
        Class constructor. Optionally accepts the name of a file to deserialize.
        :param str file_name: The name of a file to deserialize into a OBS object
        """
        # deserialize
        if file_name:
            if os.path.isfile(file_name):
                self.__dict__ = load_json_object(file_name)
            else:
                raise IOError('The file {0} was not found.'.format(file_name))
        else:
            self.app_words = dict(cancel='Cancel',
                                  chapters='Chapters',
                                  languages='Languages',
                                  next_chapter='Next Chapter',
                                  ok='OK',
                                  remove_locally='Remove Locally',
                                  remove_this_string='Remove this language from offline storage. You will need an '
                                                     'internet connection to view it in the future.',
                                  save_locally='Save Locally',
                                  save_this_string='Save this language locally for offline use.',
                                  select_a_language='Select a Language')
            self.chapters = []
            self.date_modified = datetime.today().strftime('%Y%m%d')
            self.direction = 'ltr'
            self.language = ''

    def verify_all(self):

        errors = []

        for chapter in self.chapters:
            if type(chapter) is OBSChapter:
                obs_chapter = chapter
            else:
                obs_chapter = OBSChapter(chapter)
            errors = errors + obs_chapter.get_errors()

        if len(errors) == 0:
            print('No errors were found in the OBS data.')
            return True
        else:
            return False

    @staticmethod
    def load_static_json_file(file_name):
        file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', file_name)
        return load_json_object(file_name, {})

    @staticmethod
    def get_readme_text():
        file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', 'obs_readme.md')
        with codecs.open(file_name, 'r', encoding='utf-8') as in_file:
            return in_file.read()

    @staticmethod
    def get_front_matter(pages_dir, lang_code, today_str):
        obs_name_re = re.compile(r'\| (.*)\*\*', re.UNICODE)
        tag_line_re = re.compile(r'\n\*\*.*openbiblestories', re.UNICODE | re.DOTALL)
        link_re = re.compile(r'\[\[.*?\]\]', re.UNICODE)

        return_val = OBS.load_static_json_file('obs-front-matter.json')
        return_val['language'] = lang_code
        return_val['date_modified'] = today_str

        front_path = os.path.join(pages_dir, lang_code, 'obs', 'front-matter.txt')
        if os.path.exists(front_path):

            with codecs.open(front_path, 'r', encoding='utf-8') as in_file:
                front = in_file.read()

            for l in link_re.findall(front):
                if '|' in l:
                    clean_url = l.split('|')[1].replace(']', '')
                else:
                    clean_url = l.replace(']', '').replace('[', '')
                front = front.replace(l, clean_url)

            return_val['front-matter'] = front

            obs_name_se = obs_name_re.search(front)
            if obs_name_se:
                return_val['name'] = obs_name_se.group(1)

            tag_line_se = tag_line_re.search(front)
            if tag_line_se:
                return_val['tagline'] = tag_line_se.group(0).split('**')[1].strip()

        return return_val

    @staticmethod
    def get_back_matter(pages_dir, lang_code, today_str):
        return_val = OBS.load_static_json_file('obs-back-matter.json')
        return_val['language'] = lang_code
        return_val['date_modified'] = today_str

        back_path = os.path.join(pages_dir, lang_code, 'obs', 'back-matter.txt')
        if os.path.exists(back_path):
            with codecs.open(back_path, 'r', encoding='utf-8') as in_file:
                back = in_file.read()

            return_val['back-matter'] = back

        return return_val

    @staticmethod
    def get_status():
        return OBS.load_static_json_file('obs-status.json')

    @staticmethod
    def load_lang_strings():
        langs = Language.load_languages()
        return_val = {}
        if not langs:
            return return_val

        for lang_obj in langs:  # :type Language
            return_val[lang_obj.lc] = lang_obj.ln

        return return_val


class OBSSourceTranslation(object):
    def __init__(self):
        self.language_slug = ''
        self.resource_slug = ''
        self.version = ''

    def to_serializable(self):
        return self.__dict__


class OBSManifest(object):
    def __init__(self, file_name=None):
        """
        Class constructor. Optionally accepts the name of a file to deserialize.
        :param str file_name: The name of a file to deserialize into a OBSManifest object
        """
        # deserialize
        if file_name:
            if os.path.isfile(file_name):
                self.__dict__ = load_json_object(file_name)
            else:
                raise IOError('The file {0} was not found.'.format(file_name))
        else:
            self.package_version = 1
            self.modified_at = datetime.today().strftime('%Y%m%d000000')
            self.content_mime_type = 'text/markdown'
            self.versification_slug = 'ufw'

            self.language = {'slug': 'en', 'name': 'English', 'dir': 'ltr'}

            self.resource = {
                'slug': 'obs',
                'name': 'Open Bible Stories',
                'type': 'book',

                'status': {
                    'translate_mode': 'all',
                    'checking_entity': [],
                    'checking_level': '1',
                    'version': '4',
                    'comments': '',
                    'contributors': [],
                    'pub_date': datetime.today().strftime('%Y-%m-%d'),
                    'license': 'CC BY-SA',
                    'checks_performed': [],
                    'source_translations': []
                }
            }

            self.chunk_status = []

    def __contains__(self, item):
        return item in self.__dict__

    def to_serializable(self):
        return_val = OrderedDict([
            ('package_version', self.package_version),
            ('modified_at', self.modified_at),
            ('content_mime_type', self.content_mime_type),
            ('versification_slug', self.versification_slug),
            ('language', self.language),
            ('resource', self.resource),
            ('chunk_status', self.chunk_status)
        ])

        return return_val


class OBSEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class OBSManifestEncoder(JSONEncoder):
    def default(self, o):
        """
        :param OBSManifest o:
        :return:
        """
        return o.to_serializable()
