import os
import tempfile
import unittest
from pathlib import Path
from struct import unpack_from

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

from exporter.cdj_pdb_exporter import (
    TRACK_FIXED_SIZE,
    TRACK_STRING_OFFSET_START,
    Page,
    PageType,
    PDBExporter,
    TrackRow,
)
from parser.bsm_nml_parser import NMLVersion, Track, TraktorNMLParser

try:
    from PySide6.QtWidgets import QApplication
    from main import ConverterGUI
    from threads.conversion import estimate_conversion_time
except ModuleNotFoundError as error:
    if error.name != 'PySide6':
        raise
    QApplication = None
    ConverterGUI = None
    estimate_conversion_time = None


class ParserControlFlowTests(unittest.TestCase):
    def test_empty_t4_feature_markers_select_v20(self):
        nml = '''<NML>
  <COLLECTION />
  <STEMS />
  <BEATGRID />
</NML>'''
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / 'collection.nml'
            path.write_text(nml, encoding='utf-8')
            parser = TraktorNMLParser(str(path))

        self.assertEqual(parser.version, NMLVersion.V20)

    def test_validate_track_accepts_cue_without_hotcue_key(self):
        nml = '<NML><COLLECTION /></NML>'
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / 'collection.nml'
            path.write_text(nml, encoding='utf-8')
            parser = TraktorNMLParser(str(path))

        track = Track()
        track.cue_points = [{'type': 1}]
        issues = parser.validate_track(track)

        self.assertIn('Missing AUDIO_ID', issues)
        self.assertNotIn('Duplicate hotcue numbers', issues)


class PDBControlFlowTests(unittest.TestCase):
    def test_track_row_reserves_and_writes_all_string_offsets(self):
        track = Track()
        track.title = 'Title'
        track.file_path = 'C:/Music/track.mp3'
        row = TrackRow(track, 1)

        data = row.to_bytes()
        offsets = [
            unpack_from('<H', data, TRACK_STRING_OFFSET_START + index * 2)[0]
            for index in range(21)
        ]

        self.assertGreater(len(data), TRACK_FIXED_SIZE)
        self.assertTrue(all(offset >= TRACK_FIXED_SIZE for offset in offsets))
        self.assertIn(b'track.mp3', data)
        self.assertEqual(row._ensure_relative_path('C:/Music/track.mp3'), 'Contents/track.mp3')
        self.assertEqual(row._convert_rating(300), 5)

    def test_oversized_row_is_not_reported_as_written(self):
        page = Page(PageType.TRACKS, 1, page_size=64)
        self.assertFalse(page.add_row(b'x' * 100))

        exporter = PDBExporter(page_size=64)
        with self.assertRaises(ValueError):
            exporter._add_row_to_pages([], b'x' * 100, PageType.TRACKS)

    def test_page_serialization_preserves_configured_size(self):
        page = Page(PageType.TRACKS, 1)
        self.assertTrue(page.add_row(b'row'))

        self.assertEqual(len(page.to_bytes()), 4096)

    def test_new_reference_page_keeps_its_table_type(self):
        exporter = PDBExporter()
        pages = exporter._create_table_pages(PageType.ARTISTS)
        exporter._add_row_to_pages(pages, b'artist', PageType.ARTISTS)

        self.assertEqual(pages[0].header.type, PageType.ARTISTS)


@unittest.skipUnless(estimate_conversion_time is not None, 'PySide6 is not installed')
class ConversionControlFlowTests(unittest.TestCase):
    def test_estimate_rejects_negative_track_count(self):
        with self.assertRaises(ValueError):
            estimate_conversion_time(-1, 'M3U')

    def test_rekordbox_xml_uses_xml_estimate(self):
        self.assertEqual(estimate_conversion_time(200, 'Rekordbox XML'), 20.0)


@unittest.skipUnless(QApplication is not None, 'PySide6 is not installed')
class GUIControlFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.application = QApplication.instance() or QApplication([])

    def test_m3u_format_update_uses_existing_controls(self):
        window = ConverterGUI()
        try:
            window._change_export_format('M3U')
            self.assertTrue(window.copy_music_check.isEnabled())
            self.assertEqual(window.progress_label.text(), 'Ready to export M3U playlists...')
        finally:
            window.close()


if __name__ == '__main__':
    unittest.main()
