import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text())


class ReviewDiagramsPackagingTest(unittest.TestCase):
    def test_both_marketplaces_reference_one_skill(self):
        claude = load('.claude-plugin/marketplace.json')
        codex = load('.agents/plugins/marketplace.json')
        self.assertEqual(claude['name'], 'kecbigmt-plugins')
        self.assertEqual(codex['name'], claude['name'])

        claude_entry = next(p for p in claude['plugins'] if p['name'] == 'review-diagrams')
        codex_entry = next(p for p in codex['plugins'] if p['name'] == 'review-diagrams')
        claude_root = ROOT / claude_entry['source']
        codex_root = ROOT / codex_entry['source']['path']
        self.assertEqual(claude_root.resolve(), codex_root.resolve())

        claude_manifest = json.loads((claude_root / '.claude-plugin/plugin.json').read_text())
        codex_manifest = json.loads((codex_root / '.codex-plugin/plugin.json').read_text())
        self.assertEqual(claude_manifest['name'], codex_manifest['name'])
        self.assertEqual(codex_manifest['skills'], './skills/')
        skills = list((codex_root / codex_manifest['skills']).glob('*/SKILL.md'))
        self.assertEqual(len(skills), 1)
        self.assertIn('name: review-diagrams', skills[0].read_text())

    def test_rename_has_no_stale_repository_urls(self):
        for path in [ROOT / 'README.md', *ROOT.glob('plugins/*/.claude-plugin/plugin.json'),
                     ROOT / '.claude-plugin/marketplace.json']:
            self.assertNotIn('kecbigmt/cc-plugins', path.read_text(), str(path))


if __name__ == '__main__':
    unittest.main()
