import json
import re
import unittest
import xml.etree.ElementTree as ET
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

    def test_plugin_versions_agree_and_are_bumped(self):
        claude = load('.claude-plugin/marketplace.json')
        entry = next(p for p in claude['plugins'] if p['name'] == 'review-diagrams')
        versions = {
            entry['version'],
            load('plugins/review-diagrams/.claude-plugin/plugin.json')['version'],
            load('plugins/review-diagrams/.codex-plugin/plugin.json')['version'],
        }
        self.assertEqual(versions, {'1.2.0'})


SKILL = ROOT / 'plugins/review-diagrams/skills/review-diagrams/SKILL.md'


class ReviewDiagramsSavePathTest(unittest.TestCase):
    def setUp(self):
        self.text = SKILL.read_text()
        self.paragraphs = self.text.split('\n\n')

    def paragraph_with(self, phrase):
        return next(p for p in self.paragraphs if phrase in p)

    def test_save_location_precedence_is_agents_then_pattern_then_defaults(self):
        rule = self.paragraph_with('Save location')
        agents = rule.index('`AGENTS.md`')
        pattern = rule.index('existing pattern')
        defaults = rule.index('defaults below')
        self.assertLess(agents, pattern)
        self.assertLess(pattern, defaults)
        self.assertIn('naming scheme', rule)
        self.assertIn('file stems', rule)
        self.assertIn('PR body', rule)

    def test_rule_precedes_the_default_paths_it_overrides(self):
        rule = self.text.index('Save location')
        self.assertLess(rule, self.text.index('docs/adr/assets/'))
        self.assertLess(rule, self.text.index('docs/history/changes/'))

    def test_checklist_checks_save_location(self):
        checklist = self.paragraph_with('Before sharing, review:')
        self.assertIn('saved where this project keeps diagrams', checklist)


SVG = '{http://www.w3.org/2000/svg}'
EXAMPLES = SKILL.parent / 'examples'
STATES = {
    'decision.svg': ['CHOSEN', 'REJECTED', 'DEFERRED', 'SUPERSEDED'],
    'change.svg': ['ADDED', 'CHANGED', 'REMOVED', 'UNCHANGED'],
}


class ReviewDiagramsSamplesTest(unittest.TestCase):
    def test_skill_points_to_each_bundled_sample(self):
        text = SKILL.read_text()
        for name in STATES:
            self.assertIn(f'`examples/{name}`', text)
            self.assertTrue((EXAMPLES / name).is_file(), name)

    def test_samples_are_accessible_themed_svgs(self):
        for name, states in STATES.items():
            raw = (EXAMPLES / name).read_text()
            root = ET.fromstring(raw)
            self.assertEqual(root.tag, SVG + 'svg', name)
            self.assertEqual(root.get('aria-labelledby'), 'title desc', name)
            self.assertTrue(root.find(SVG + 'title').text.strip(), name)
            self.assertTrue(root.find(SVG + 'desc').text.strip(), name)
            self.assertIn('@media (prefers-color-scheme: dark)', raw, name)
            texts = ' '.join(''.join(t.itertext()) for t in root.iter(SVG + 'text'))
            for state in states:
                self.assertIn(state, texts, f'{name}: {state}')

    def test_every_sample_arrow_has_a_label(self):
        for name in STATES:
            root = ET.fromstring((EXAMPLES / name).read_text())
            flows = [e for e in root.iter() if re.search(r'\bflow', e.get('class', ''))]
            labels = [t for t in root.iter(SVG + 'text') if 'label' in t.get('class', '')]
            self.assertTrue(flows, name)
            self.assertGreaterEqual(len(labels), len(flows), name)

    def test_samples_carry_no_real_names(self):
        for name in STATES:
            raw = (EXAMPLES / name).read_text().lower()
            for word in ['plect', 'slack', 'kecbigmt', 'idle']:
                self.assertNotIn(word, raw, f'{name}: {word}')

    def test_artifact_diagramming_is_optional_and_output_stays_a_committed_svg(self):
        text = SKILL.read_text()
        rule = next(p for p in text.split('\n\n') if 'artifact-diagramming' in p)
        self.assertIn('If the host offers', rule)
        self.assertIn('commit an SVG file to the repository', rule)
        self.assertIn('never publishing it as an Artifact', rule)


if __name__ == '__main__':
    unittest.main()
