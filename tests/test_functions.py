import pytest
from bank_operations import format_operation


def test_format_operation_with_valid_operation():
    operation = "Transaction from Account A to Account B"
    expected_result = "Transaction from Account A to Account B"
    assert format_operation(operation) == expected_result


def test_format_operation_with_empty_operation():
    operation = ""
    expected_result = ""
    assert format_operation(operation) == expected_result


def test_format_operation_with_special_characters():
    operation = "Special characters: @#$%^&*()"
    expected_result = "Special characters: @#$%^&*()"
    assert format_operation(operation) == expected_result


def test_format_operation_with_long_description():
    operation = "This is a very long description that should be truncated"
    expected_result = "This is a very long description that should be truncated"
    assert format_operation(operation) == expected_result


def test_format_operation_with_whitespace_only():
    operation = "        "
    expected_result = ""
    assert format_operation(operation) == expected_result


def test_format_operation_with_multiple_spaces():
    operation = "Transaction    from   Account A    to    Account B"
    expected_result = "Transaction from Account A to Account B"
    assert format_operation(operation) == expected_result


def test_format_operation_with_long_operation():
    operation = "A very long transaction description " * 10
    expected_result = operation[:96] + " ..."
    assert format_operation(operation) == expected_result


def test_format_operation_with_only_numbers():
    operation = "1234567890"
    expected_result = "1234 56** **** 7890"
    assert format_operation(operation) == expected_result


def test_format_operation_with_single_word():
    operation = "Transaction"
    expected_result = "Transaction"
    assert format_operation(operation) == expected_result


def test_format_operation_with_account_start():
    operation = "Счет 1234567890"
    expected_result = "**7890"
    assert format_operation(operation) == expected_result


def test_format_operation_multiple_spaces():
    operation = "Transaction    from   Account A    to    Account B"
    expected_result = "Transaction from Account A to Account B"
    assert format_operation(operation) == expected_result


def test_format_operation_starts_with_whitespace():
    operation = "   Transaction from Account A to Account B"
    expected_result = "Transaction from Account A to Account B"
    assert format_operation(operation) == expected_result


def test_format_operation_without_separator():
    operation = "TransactionfromAccountAtoAccountB"
    expected_result = "TransactionfromAccountAtoAccountB"
    assert format_operation(operation) == expected_result


def test_format_operation_with_account_in_middle():
    operation = "Transaction from Account 1234567890 to Account B"
    expected_result = "Transaction from Account **7890 to Account B"
    assert format_operation(operation) == expected_result


