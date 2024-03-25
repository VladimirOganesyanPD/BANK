import pytest
import json
import os
from bank_operations import read_operations_from_file


def test_format_operation_with_valid_operation():
    operation = "Transaction from Account A to Account B"
    expected_result = "Transaction from Account A to Account B"
    assert bank_operations.format_operation(operation) == expected_result


def test_format_operation_with_empty_operation():
    operation = ""
    expected_result = ""
    assert bank_operations.format_operation(operation) == expected_result


def test_format_operation_with_special_characters():
    operation = "Special characters: @#$%^&*()"
    expected_result = "Special characters: @#$%^&*()"
    assert bank_operations.format_operation(operation) == expected_result


def test_format_operation_with_long_description():
    operation = "This is a very long description that should be truncated"
    expected_result = "This is a very long description that should be truncated"
    assert bank_operations.format_operation(operation) == expected_result


def test_format_operation_with_whitespace_only():
    operation = "        "
    expected_result = ""
    assert bank_operations.format_operation(operation) == expected_result


def test_format_operation_with_multiple_spaces():
    operation = "Transaction    from   Account A    to    Account B"
    expected_result = "Transaction from Account A to Account B"
    assert bank_operations.format_operation(operation) == expected_result


def test_format_operation_with_long_operation():
    operation = "A very long transaction description " * 10
    expected_result = operation[:96] + " ..."
    assert bank_operations.format_operation(operation) == expected_result


def test_format_operation_with_only_numbers():
    operation = "1234567890"
    expected_result = "1234 56** **** 7890"
    assert bank_operations.format_operation(operation) == expected_result


def test_format_operation_with_single_word():
    operation = "Transaction"
    expected_result = "Transaction"
    assert bank_operations.format_operation(operation) == expected_result


def test_format_operation_with_account_start():
    operation = "Счет 1234567890"
    expected_result = "**7890"
    assert bank_operations.format_operation(operation) == expected_result


def test_format_operation_multiple_spaces():
    operation = "Transaction    from   Account A    to    Account B"
    expected_result = "Transaction from Account A to Account B"
    assert bank_operations.format_operation(operation) == expected_result


def test_format_operation_starts_with_whitespace():
    operation = "   Transaction from Account A to Account B"
    expected_result = "Transaction from Account A to Account B"
    assert bank_operations.format_operation(operation) == expected_result


def test_format_operation_without_separator():
    operation = "TransactionfromAccountAtoAccountB"
    expected_result = "TransactionfromAccountAtoAccountB"
    assert bank_operations.format_operation(operation) == expected_result


def test_format_operation_with_account_in_middle():
    operation = "Transaction from Account 1234567890 to Account B"
    expected_result = "Transaction from Account **7890 to Account B"
    assert bank_operations.format_operation(operation) == expected_result


def test_format_operation_empty_input():
    assert format_operation("") == ""


def test_format_operation_bank_account():
    assert format_operation("Счет №1234567890") == "Счет **7890"

def test_format_operation_credit_card():
    assert format_operation("Карта 1234 5678 9876 5432") == "Карта 1234 56** **** 5432"


sample_operations = [
    {
        "date": "2023-12-25T08:00:00",
        "description": "Открытие вклада",
        "from": "",
        "to": "Счет 12345678901234567890"
    },
    {
        "date": "2023-12-24T15:30:00",
        "description": "Перевод",
        "from": "Счет 12345678901234567890",
        "to": "Счет 98765432109876543210"
    },
    {
        "date": "2023-12-23T10:45:00",
        "description": "Покупка товаров",
        "from": "Счет 98765432109876543210",
        "to": ""
    }
]

# Тесты для функции process_operations
def test_process_operations_with_valid_data():
    processed_data = process_operations(sample_operations)
    assert isinstance(processed_data, list)
    assert len(processed_data) == len(sample_operations)

    expected_result = [
        {'date': '25.12.2023', 'description': 'Открытие вклада', 'data': 'Счет **56789012 3456** 7890'},
        {'date': '24.12.2023', 'description': 'Перевод', 'data': 'Счет **43210987 2109** 8765 -> Счет **54321098 7654** 3210'},
        {'date': '23.12.2023', 'description': 'Покупка товаров', 'data': 'Счет **54321098 7654** 3210'}
    ]

    assert processed_data == expected_result


def test_process_operations_with_empty_data():
    processed_data = process_operations([])
    assert processed_data == []


def test_process_operations_with_invalid_data():
    with pytest.raises(TypeError):
        process_operations("invalid_data")

    with pytest.raises(KeyError):
        process_operations([{"invalid_key": "value"}])



sample_data = [
    {"state": "EXECUTED", "date": "2023-12-25T08:00:00"},
    {"state": "EXECUTED", "date": "2023-12-24T15:30:00"},
    {"state": "PENDING", "date": "2023-12-23T10:45:00"},
    {"state": "EXECUTED", "date": "2023-12-22T09:00:00"},
    {"state": "EXECUTED", "date": "2023-12-21T14:20:00"}
]

def test_filter_and_sort_operations_with_valid_data():
    filtered_and_sorted = filter_and_sort_operations(sample_data)
    assert isinstance(filtered_and_sorted, list)
    assert len(filtered_and_sorted) == 3

    expected_result = [
        {"state": "EXECUTED", "date": "2023-12-25T08:00:00"},
        {"state": "EXECUTED", "date": "2023-12-24T15:30:00"},
        {"state": "EXECUTED", "date": "2023-12-22T09:00:00"}
    ]

    assert filtered_and_sorted == expected_result

def test_filter_and_sort_operations_with_empty_data():
    filtered_and_sorted = filter_and_sort_operations([])
    assert filtered_and_sorted == []

def test_filter_and_sort_operations_with_invalid_data():
    with pytest.raises(TypeError):
        filter_and_sort_operations("invalid_data")

    with pytest.raises(KeyError):
        filter_and_sort_operations([{"invalid_key": "value"}])


file_path = os.path.join(os.path.dirname(__file__), 'operations.json')
def test_read_operations_from_file_with_valid_file():
    expected_data = [
        {
            "date": "08.12.2019",
            "description": "Открытие вклада",
            "data": "Счет **5907"
        },
        {
            "date": "07.12.2019",
            "description": "Перевод организации",
            "data": "Visa Classic 2842 78** **** 9012 -> Счет **3655"
        },
        {
            "date": "19.11.2019",
            "description": "Перевод организации",
            "data": "Maestro 7810 46** **** 5568 -> Счет **2869"
        },
        {
            "date": "13.11.2019",
            "description": "Перевод со счета на счет",
            "data": "Счет **9794 -> Счет **8125"
        },
        {
            "date": "05.11.2019",
            "description": "Открытие вклада",
            "data": "Счет **8381"
        }
    ]
    assert read_operations_from_file(file_path) == expected_data

def test_read_operations_from_file_with_invalid_file():
    with pytest.raises(FileNotFoundError):
        read_operations_from_file('non_existing_file.json')

def test_read_operations_from_file_with_invalid_json():
    with pytest.raises(json.JSONDecodeError):
        read_operations_from_file('invalid_data.json')