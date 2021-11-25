"""System tests for the command line interface."""
import pathlib
import subprocess
import filecmp
import pkg_resources

# Directory containing unit test input files, etc.
TESTDATA_DIR = pathlib.Path(__file__).parent/"testdata"


def test_version():
    """Verify --version flag."""
    result = subprocess.run(
        ["madoop", "--version"],
        stdout=subprocess.PIPE,
        check=True,
    )
    output = result.stdout.decode("utf-8")
    assert "Madoop" in output
    assert pkg_resources.get_distribution("madoop").version in output


def test_help():
    """Verify --help flag."""
    result = subprocess.run(
        ["madoop", "--help"],
        stdout=subprocess.PIPE,
        check=True,
    )
    output = result.stdout.decode("utf-8")
    assert "usage" in output


def test_simple(tmpdir):
    """Run a simple MapReduce job and verify the output."""
    with tmpdir.as_cwd():
        subprocess.run(
            [
                "madoop",
                "-input", TESTDATA_DIR/"word_count/input",
                "-output", "output",
                "-mapper", TESTDATA_DIR/"word_count/map.py",
                "-reducer", TESTDATA_DIR/"word_count/reduce.py",
            ],
            stdout=subprocess.PIPE,
            check=True,
        )
    correct_dir = TESTDATA_DIR/"word_count/correct/output"
    correct_list = sorted(correct_dir.glob("part-*"))
    for correct in correct_list:
        actual = tmpdir/"output"/correct.name
        assert filecmp.cmp(correct, actual, shallow=False)


def test_hadoop_arguments(tmpdir):
    """Hadoop Streaming arguments should be ignored."""
    with tmpdir.as_cwd():
        subprocess.run(
            [
                "madoop",
                "jar", "hadoop-streaming-2.7.2.jar",  # Hadoop args
                "-input", TESTDATA_DIR/"word_count/input",
                "-output", "output",
                "-mapper", TESTDATA_DIR/"word_count/map.py",
                "-reducer", TESTDATA_DIR/"word_count/reduce.py",
            ],
            stdout=subprocess.PIPE,
            check=True,
        )
