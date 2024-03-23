import json


def read_operations_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def filter_and_sort_operations(data):
    executed_operations = [operation for operation in data if operation.get('state') == 'EXECUTED']
    return sorted(executed_operations, key=lambda x: x['date'], reverse=True)[:5]


def process_operations(operations):
    processed_data = []
    for operation in operations:
        description = operation.get("description", "")
        from_ = operation.get("from", "")
        to = operation.get("to", "")

        if description != "Открытие вклада":
            data = format_operation(from_) + " -> " + format_operation(to)
        else:
            data = format_operation(to)

        date_formatted = operation['date'].split('T')[0]
        date_formatted = '.'.join(date_formatted.split('-')[::-1])

        processed_data.append({'date': date_formatted, 'description': description, 'data': data})
    return processed_data


def format_operation(operation):
    operation_parts = operation.split()
    if len(operation_parts) > 1:
        number = operation_parts[-1]
        name = operation_parts[:-1]
        if name[0] == "Счет":
            number = "**" + number[-4:]
        if name[0] != "Счет":
            number = f'{number[:4]} {number[5:7]}** {(len(number[8: -4]) * "*")} {number[-4:]}'

        return f'{" ".join(name)} {number}'
    elif operation.strip():
        return operation
    else:
        return ""


def main():
    data = read_operations_from_file('operations.json')
    filtered_and_sorted_operations = filter_and_sort_operations(data)
    processed_operations = process_operations(filtered_and_sorted_operations)

    for operation in processed_operations:
        print(f'{operation["date"]} {operation["description"]}\n{operation["data"]}\n')


if __name__ == "__main__":
    main()