import tempfile
import unittest
from pathlib import Path

from parser.bsm_nml_parser import NMLVersion, TraktorNMLParser


T4_NML = '''<?xml version="1.0" encoding="UTF-8"?>
<NML VERSION="19+">
  <HEAD PROGRAM="Traktor Pro 4" />
  <COLLECTION>
    <ENTRY AUDIO_ID="audio-1" TITLE="T4 Track" ARTIST="Artist" LOCK="1"
            LOCK_MODIFICATION_TIME="2025-08-28T22:27:35">
      <LOCATION VOLUME="D:" DIR="/:Music/:/" FILE="track.mp3" />
      <INFO BITRATE="320000" FILESIZE="1234" PLAYTIME="180"
            PLAYTIME_FLOAT="180.25" PLAYCOUNT="4" LAST_PLAYED="2025-08-28" />
      <TEMPO BPM="128.0" />
      <CUE_V2 NAME="Grid" TYPE="4" START="0" BPM="128.0" COLOR="#00ff00" />
      <BEATGRID>
        <MARKER BPM="130.0" BEAT_POS="65.0" />
      </BEATGRID>
      <STEMS>
        <STEM TYPE="DRUMS" LEVEL="0.8" MUTED="0" />
        <STEM TYPE="VOCAL" LEVEL="0.9" MUTED="1" />
      </STEMS>
    </ENTRY>
  </COLLECTION>
  <PLAYLISTS>
    <NODE TYPE="FOLDER" NAME="$ROOT">
      <SUBNODES>
        <NODE TYPE="PLAYLIST" NAME="Static">
          <PLAYLIST UUID="playlist-1">
            <ENTRY><PRIMARYKEY KEY="D:/:Music/:/track.mp3" /></ENTRY>
          </PLAYLIST>
        </NODE>
        <NODE TYPE="SMARTLIST" NAME="Dynamic">
          <SMARTLIST UUID="smart-1">
            <SEARCH_EXPRESSION VERSION="1" QUERY="$RATING == 5" />
          </SMARTLIST>
        </NODE>
        <NODE TYPE="PLAYLIST" NAME="Search">
          <PLAYLIST TYPE="SEARCH" UUID="search-1">
            <SEARCH><ATTRIBUTE NAME="BPM" OPERATOR="GREATER_THAN" VALUE="125" /></SEARCH>
          </PLAYLIST>
        </NODE>
      </SUBNODES>
    </NODE>
  </PLAYLISTS>
</NML>
'''


class TraktorPro4ParserTests(unittest.TestCase):
    def test_parses_t4_metadata_grids_stems_and_dynamic_playlists(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            nml_path = Path(temp_dir) / 'collection.nml'
            nml_path.write_text(T4_NML, encoding='utf-8')

            parser = TraktorNMLParser(str(nml_path))
            self.assertEqual(parser.version, NMLVersion.V20)

            structure = parser.get_playlists_with_structure()
            nodes = {node.name: node for node in structure}

            static = nodes['Static']
            track = static.tracks[0]
            self.assertEqual(track.playtime_float, 180.25)
            self.assertTrue(track.lock_status)
            self.assertEqual(track.stem_data['channels'][0]['name'], 'DRUMS')
            self.assertTrue(track.stem_data['channels'][1]['muted'])
            self.assertEqual(track.beat_grid[0]['beat_position'], 65.0)
            self.assertEqual(track.cue_points[0]['color'], '#00ff00')

            self.assertEqual(nodes['Dynamic'].search_expression, '$RATING == 5')
            self.assertEqual(nodes['Search'].type, 'smartlist')
            self.assertIn('GREATER_THAN', nodes['Search'].search_expression)


if __name__ == '__main__':
    unittest.main()
