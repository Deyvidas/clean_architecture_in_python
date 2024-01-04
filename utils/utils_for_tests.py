from typing import Any


def update_data(
    orig_data: dict[str, Any],
    new_data: dict[str, Any],
) -> dict[str, Any]:
    """
    Update only the keys existent in original_data with values from new_data.
    """
    if new_data == dict() or orig_data == dict():
        return orig_data

    to_update = set(orig_data.keys()) & set(new_data.keys())
    for k in to_update:
        orig_data[k] = new_data[k]
    return orig_data


class TestUpdateData:

    @staticmethod
    def test_update_data():
        orig_data = {'a': 1, 'b': 2, 'c': 3}
        new_data = {'b': 'b', 'c': 'c', 'd': 'd'}

        res = update_data(orig_data, new_data)
        exp = {'a': 1, 'b': 'b', 'c': 'c'}
        print(f'{res=}\n{exp=}')
        assert res == exp, f'{res=} must be {exp=}'

    @staticmethod
    def test_update_with_empty_new_data():
        orig_data = {'a': 1, 'b': 2, 'c': 3}
        new_data = dict()

        res = update_data(orig_data, new_data)
        exp = {'a': 1, 'b': 2, 'c': 3}
        print(f'{res=}\n{exp=}')
        assert res == exp, f'{res=} must be {exp=}'

    @staticmethod
    def test_update_with_empty_origin_data():
        orig_data = dict()
        new_data = {'b': 'b', 'c': 'c', 'd': 'd'}

        res = update_data(orig_data, new_data)
        exp = dict()
        print(f'{res=}\n{exp=}')
        assert res == exp, f'{res=} must be {exp=}'


def main():
    TestUpdateData.test_update_data()
    TestUpdateData.test_update_with_empty_new_data()
    TestUpdateData.test_update_with_empty_origin_data()


if __name__ == '__main__':
    main()
