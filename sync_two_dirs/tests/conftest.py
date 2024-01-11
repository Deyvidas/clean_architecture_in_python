import os

import pytest


@pytest.fixture(scope='function')
def clean():
    before = os.listdir('/tmp')
    yield
    after = os.listdir('/tmp')
    to_delete = set(after) - set(before)
    [os.popen(f'rm -rf /tmp/{d}') for d in to_delete]
