import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from SDMO2025Project.project1developers import process
from Levenshtein import ratio as sim


def test_process_two_names():
    name, first, last, i_first, i_last, email, prefix = process(
        ["John Doe", "john@example.com"]
    )
    assert first == "john"
    assert last == "doe"
    assert i_first == "j"
    assert i_last == "d"
    assert prefix == "john"


def test_process_single_name():
    name, first, last, i_first, i_last, email, prefix = process(
        ["Plato", "plato@greek.com"]
    )
    assert first == "plato"
    assert last == ""
    assert i_first == "p"
    assert i_last == ""


def test_process_name_with_accents():
    name, first, last, *_ = process(["José Álvarez", "jose@domain.com"])
    assert first == "jose"
    assert last == "alvarez"
    assert "é" not in name
    assert "Á" not in name


def test_similarity_comparison():
    name_a, *_ = process(["John Doe", "john@example.com"])
    name_b, *_ = process(["Jon Doe", "jon@example.com"])
    assert sim(name_a, name_b) > 0.8


def test_empty_name_should_not_crash():
    name, first, last, *_ = process(["", "unknown@mail.com"])
    assert first == ""
    assert last == ""
