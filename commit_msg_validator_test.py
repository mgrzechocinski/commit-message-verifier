from commit_msg_validator import *


def test_too_long_line():
    commit_msg = "Sample commit message subject which is too long to be considered as valid"
    expect_error_for(commit_msg, LINE_LENGTH_EXCEEDED % 1)

    commit_msg = """Sample commit message subject

This is very long body message which exceeds 72 characters line length in the commit message 
    """

    expect_error_for(commit_msg, LINE_LENGTH_EXCEEDED % 3)


def test_empty_line_no_body():
    commit_msg = """Sample commit message with empty line
                 """

    expect_error_for(commit_msg, SUBJECT_IS_NOT_SINGLE_LINE)


def test_empty_line_with_body():
    commit_msg = """This is subject
                    this should be an empty line
                    This is body
                 """

    expect_error_for(commit_msg, SUBJECT_AND_BODY_EMPTY_LINE_IS_MANDATORY)


def test_should_not_contain_excessive_blank_lines():
    commit_msg = """This is subject

                    This is body


                    And there is one excessive blank line above
                 """

    expect_error_for(commit_msg, EXCESSIVE_BLANK_LINE_WAS_FOUND)


def test_should_enumerate_with_dashes():
    commit_msg = """This is subject

* list item not started with dash"""

    expect_error_for(commit_msg, INVALID_LINE_START % 3)


def test_should_start_enumaration_with_small_letter():
    commit_msg = """This is subject

- List item not started with small letter"""

    expect_error_for(commit_msg, INVALID_LINE_START % 3)


def test_should_wrap_enumaration_with_leading_whitespace():
    commit_msg = """This is subject

- something short
- something very long
with wrapped content but without leading whitespaces"""

    expect_error_for(commit_msg, INVALID_LINE_START % 5)


def test_should_be_a_valid_message():
    with open('valid_commit_message.txt', 'r') as file:
        valid_commit_message = file.read()
    validate(valid_commit_message)


def expect_error_for(commit_msg, expected_message):
    try:
        validate(commit_msg)
        raise RuntimeError("Validation should not pass. Error was expected with msg: '%s'" % expected_message)
    except ValueError as error:
        assert error.message == expected_message
