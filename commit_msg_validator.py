import re

LINE_LENGTH_EXCEEDED = "Commit message line should be max 72 chars long but line :%s is longer"
SUBJECT_IS_NOT_SINGLE_LINE = "Subject should be single line"
SUBJECT_AND_BODY_EMPTY_LINE_IS_MANDATORY = "Subject must be separated from body by one empty line"
EXCESSIVE_BLANK_LINE_WAS_FOUND = "Excessive blank line was found"
INVALID_LINE_START = "[:%s] Line can either be empty or start with text or '-' (list item). For wrapped list items, add leading whitespaces."

def validate(commit_msg):
    validate_line_length(commit_msg)
    validate_subject_single_line(commit_msg)
    validate_subject_body_separated_by_empty_line(commit_msg)
    validate_excessive_blank_lines(commit_msg)
    validate_line_start_with_either_text_or_enumeration(commit_msg)


def validate_line_length(commit_msg):
    line_no = 1
    for line in commit_msg.splitlines():
        if len(line) - line.count('\\') > 72:
            raise ValueError(LINE_LENGTH_EXCEEDED % line_no)
        line_no += 1


def validate_subject_single_line(commit_msg):
    splitlines = commit_msg.splitlines()
    number_of_lines = len(splitlines)
    if number_of_lines == 2 and len(splitlines[1]) != 0:
        raise ValueError(SUBJECT_IS_NOT_SINGLE_LINE)


def validate_excessive_blank_lines(commit_msg):
    found_empty_line = False
    for line in commit_msg.splitlines():
        is_empty = len(line.strip()) == 0
        if is_empty:
            if found_empty_line:
                raise ValueError(EXCESSIVE_BLANK_LINE_WAS_FOUND)
        found_empty_line = is_empty


def validate_subject_body_separated_by_empty_line(commit_msg):
    splitlines = commit_msg.splitlines()
    number_of_lines = len(splitlines)
    if number_of_lines < 3:
        return

    if not (len(splitlines[1]) == 0 and len(splitlines[2]) > 0):
        raise ValueError(SUBJECT_AND_BODY_EMPTY_LINE_IS_MANDATORY)


def validate_line_start_with_either_text_or_enumeration(commit_msg):
    enumeration_start = False
    line_no = 0
    for line in commit_msg.splitlines():
        line_no += 1
        # Just a common line of subject/body text
        if not enumeration_start and re.match("[\[\]\'\"\w]+.*$", line):
            enumeration_start = False
            continue
        # Empty line
        elif len(line) == 0:
            enumeration_start = False
            continue
        # Enumeration starts
        elif re.match("^- [^[A-Z\s]+.*$", line):
            enumeration_start = True
            continue
        # Enumeration continues
        elif enumeration_start and re.match("^ {2}.*$", line):
            continue

        raise ValueError(INVALID_LINE_START % line_no)
