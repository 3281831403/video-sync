import pytest

from media import video_sync as mod

CASES = [
    pytest.param('timeline_seconds', (90000, 90000), 1.0, True, id='01_pts_seconds'),
    pytest.param('timeline_seconds', (45000, 90000), 0.5, True, id='02_pts_half'),
    pytest.param('timeline_seconds', (3003, 30000), 0.1001, True, id='03_pts_ntsc'),
    pytest.param('timeline_seconds', (0, 90000), 0.0, True, id='04_pts_zero'),
    pytest.param('timeline_seconds', (900000, 90000), 10.0, True, id='05_pts_large'),
    pytest.param('frame_for_time', (0.0, 30000, 1001), 0, False, id='06_frame_zero'),
    pytest.param('frame_for_time', (1.0, 30000, 1001), 29, False, id='07_frame_one'),
    pytest.param('frame_for_time', (10.0, 30000, 1001), 299, False, id='08_frame_ntsc'),
    pytest.param('frame_for_time', (1.0, 24000, 1001), 23, False, id='09_frame_2398'),
    pytest.param('frame_for_time', (0.5, 30, 1), 15, False, id='10_frame_partial'),
    pytest.param('sync_decision', (10.0, 10.01, 0.05, [0, 5, 10]), (-0.009999999999999787, 'hold', 10), True, id='11_sync_hold'),
    pytest.param('sync_decision', (10.0, 9.0, 0.05, [0, 5, 8]), (1.0, 'seek', 8), True, id='12_sync_seek'),
    pytest.param('sync_decision', (9.0, 10.0, 0.05, [0, 5, 8]), (-1.0, 'seek', 8), True, id='13_sync_negative'),
    pytest.param('sync_decision', (10.0, 9.0, 0.05, []), (1.0, 'seek', 0), True, id='14_sync_no_key'),
    pytest.param('sync_decision', (10.0, 10.05, 0.05, [0, 5, 10]), (-0.05000000000000071, 'seek', 10), True, id='15_sync_exact'),
]


def assert_close(actual, expected):
    if isinstance(expected, tuple):
        assert isinstance(actual, tuple) and len(actual) == len(expected)
        for a, e in zip(actual, expected):
            assert_close(a, e)
    elif isinstance(expected, list):
        assert isinstance(actual, list) and len(actual) == len(expected)
        for a, e in zip(actual, expected):
            assert_close(a, e)
    elif isinstance(expected, dict):
        assert actual.keys() == expected.keys()
        for key in expected:
            assert_close(actual[key], expected[key])
    else:
        assert actual == pytest.approx(expected)


@pytest.mark.parametrize("func_name,args,expected,approx", CASES)
def test_video_sync_contract(func_name, args, expected, approx):
    func = getattr(mod, func_name)
    result = func(*args)
    if approx:
        assert_close(result, expected)
    else:
        assert result == expected
