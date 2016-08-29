from __future__ import print_function, unicode_literals
from unittest import TestCase
from obs.chapters_and_frames import frame_counts


class TestChaptersAndFrames(TestCase):

    def test_chapters_and_frames(self):

        # there should be 50 chapters
        self.assertEqual(50, len(frame_counts))

        # the first chapter should have 16 frames
        self.assertEqual(16, frame_counts[0])

        # the last chapter should have 17 frames
        self.assertEqual(17, frame_counts[49])
