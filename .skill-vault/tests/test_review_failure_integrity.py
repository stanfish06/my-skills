"""Regression tests for the AI image-review failure path (issue #829).

Three skills pointed ``review_model`` at ``google/gemini-3-pro``, an id that
does not exist in the OpenRouter catalogue, so every review call 404'd.  The
error handler then turned that failure into a hard-coded score with
``needs_improvement=False``, which the refinement loop printed as a measured
quality verdict -- producing self-contradicting output such as
``Quality meets journal threshold (7.5 >= 8.5)``.

These tests lock in the two invariants that keep that class of bug out:

1. the configured review model is not a known-dead id, and
2. a review that fails is never reported as a passing verdict.

The second invariant is checked for every skill, including ones whose model id
was already correct -- there the fabricated-verdict bug was latent, waiting for
any transient API error.
"""

import importlib.util
import inspect
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# Model ids known not to exist in the OpenRouter catalogue.
DEAD_MODEL_IDS = {"google/gemini-3-pro"}

# (skill directory, script filename, generator class name)
TARGETS = [
    ("scientific-slides", "generate_slide_image_ai.py", "SlideImageGenerator"),
    ("scientific-schematics", "generate_schematic_ai.py", "ScientificSchematicGenerator"),
    ("infographics", "generate_infographic_ai.py", "InfographicGenerator"),
    ("scholar-evaluation", "generate_schematic_ai.py", "ScientificSchematicGenerator"),
]


def load_skill_module(skill, script):
    """Import a skill script under a name unique to its skill.

    Two skills define classes with the same name, so the module name is
    namespaced to keep them from clobbering each other in sys.modules.
    """
    path = REPO_ROOT / "skills" / skill / "scripts" / script
    mod_name = "skillvault_test_" + skill.replace("-", "_")
    spec = importlib.util.spec_from_file_location(mod_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)
    return module


def make_generator(module, class_name, response=None):
    """Build a generator whose review call fails, or returns ``response``."""
    generator = getattr(module, class_name)(api_key="test-key-never-used")

    def boom(*args, **kwargs):
        raise RuntimeError("simulated OpenRouter outage")

    # Fail at the API boundary; skip real image I/O.
    generator._make_request = boom if response is None else (lambda *a, **k: response)
    generator._image_to_base64 = lambda *a, **k: "data:image/png;base64,AAAA"
    return generator


def call_review(generator):
    """Invoke review_image, supplying whatever required args this skill takes."""
    supplied = {
        "image_path": "unused.png",
        "original_prompt": "a test prompt",
        "iteration": 1,
        "infographic_type": None,
    }
    sig = inspect.signature(generator.review_image)
    kwargs = {
        name: supplied[name]
        for name, p in sig.parameters.items()
        if p.default is inspect.Parameter.empty and name in supplied
    }
    return generator.review_image(**kwargs)


def collect_thresholds(module, generator):
    """Every quality threshold this skill can compare a score against."""
    values = []
    for holder in (generator, type(generator), module):
        table = getattr(holder, "QUALITY_THRESHOLDS", None)
        if isinstance(table, dict):
            values.extend(v for v in table.values() if isinstance(v, (int, float)))
        single = getattr(holder, "QUALITY_THRESHOLD", None)
        if isinstance(single, (int, float)):
            values.append(single)
    return values


class ReviewModelIdTests(unittest.TestCase):
    def test_review_model_is_not_a_dead_id(self):
        for skill, script, cls in TARGETS:
            with self.subTest(skill=skill):
                module = load_skill_module(skill, script)
                generator = getattr(module, cls)(api_key="test-key-never-used")
                self.assertNotIn(
                    generator.review_model,
                    DEAD_MODEL_IDS,
                    f"{skill} reviews with a model id that does not exist, so "
                    f"every review call fails",
                )


class FailedReviewIsNotAPassTests(unittest.TestCase):
    def test_failed_review_reports_failure_not_a_score(self):
        for skill, script, cls in TARGETS:
            with self.subTest(skill=skill):
                module = load_skill_module(skill, script)
                generator = make_generator(module, cls)

                _critique, score, needs_improvement = call_review(generator)

                self.assertEqual(
                    score,
                    module.REVIEW_FAILED_SCORE,
                    f"{skill} invented a score for a review that never ran",
                )
                self.assertTrue(
                    needs_improvement,
                    f"{skill} marked an unreviewed image as acceptable",
                )

    def test_empty_choices_is_not_a_pass(self):
        """A 200 response carrying no choices is also a review that never ran."""
        for skill, script, cls in TARGETS:
            with self.subTest(skill=skill):
                module = load_skill_module(skill, script)
                generator = make_generator(module, cls, response={"choices": []})

                _critique, score, needs_improvement = call_review(generator)

                self.assertEqual(
                    score,
                    module.REVIEW_FAILED_SCORE,
                    f"{skill} invented a score from an empty review response",
                )
                self.assertTrue(
                    needs_improvement,
                    f"{skill} marked an unreviewed image as acceptable",
                )

    def test_sentinel_never_satisfies_any_threshold(self):
        """The sentinel must lose every `score >= threshold` comparison."""
        for skill, script, cls in TARGETS:
            with self.subTest(skill=skill):
                module = load_skill_module(skill, script)
                generator = getattr(module, cls)(api_key="test-key-never-used")

                thresholds = collect_thresholds(module, generator)
                self.assertTrue(thresholds, f"{skill} exposes no thresholds to check")
                for threshold in thresholds:
                    self.assertLess(
                        module.REVIEW_FAILED_SCORE,
                        threshold,
                        f"{skill} would report an unreviewed image as meeting "
                        f"threshold {threshold}",
                    )


if __name__ == "__main__":
    unittest.main()
