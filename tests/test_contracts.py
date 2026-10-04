import copy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / 'skills/loop-goal/templates'


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.schema = json.loads((TEMPLATES / 'state.schema.json').read_text())
        self.example = json.loads((TEMPLATES / 'state.json').read_text())
        self.validator = Draft202012Validator(self.schema)

    def test_template_validates(self):
        Draft202012Validator.check_schema(self.schema)
        self.validator.validate(self.example)

    def test_invalid_mode_negative_iteration_and_missing_verification_fail(self):
        for field, value in [('mode', 'loop|goal'), ('iteration', -1), ('exit_condition', '')]:
            invalid = copy.deepcopy(self.example)
            invalid[field] = value
            with self.assertRaises(ValidationError):
                self.validator.validate(invalid)
        invalid = copy.deepcopy(self.example)
        invalid['verify_observation'] = ''
        with self.assertRaises(ValidationError):
            self.validator.validate(invalid)

    def test_always_on_entrypoints_preserve_capability_fallbacks(self):
        for relative in ['AGENTS.md', '.github/copilot-instructions.md']:
            with self.subTest(entrypoint=relative):
                text = (ROOT / relative).read_text()
                self.assertIn('host-native subagent when available', text)
                self.assertIn('otherwise checkpoint short serial phases', text)
                self.assertIn('commit only task-owned paths when Git/permissions allow', text)
                self.assertIn('`verify_cmd` or `verify_observation`', text)
                self.assertIn('permission boundaries in the full skill take precedence', text)
                self.assertIn('never broaden permissions or include unrelated staged changes', text)

    def test_plugin_paths_and_localized_readmes_exist(self):
        plugin = json.loads((ROOT / '.claude-plugin/plugin.json').read_text())
        market = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())
        self.assertEqual(plugin['name'], market['plugins'][0]['name'])
        self.assertTrue((ROOT / market['plugins'][0]['source'] / 'skills/loop-goal/SKILL.md').is_file())
        docs = list((ROOT / 'docs/i18n').glob('README.*.md'))
        self.assertEqual(len(docs), 10)
        for path in docs:
            self.assertIn('loop-goal', path.read_text())


if __name__ == '__main__':
    unittest.main()
