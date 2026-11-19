"""视频同步：时间基、帧号、漂移与关键帧跳转：待实现的核心模块。"""

from __future__ import annotations


def timeline_seconds(pts, timescale):
    """返回 PTS 对应的秒数。"""
    raise NotImplementedError

def frame_for_time(seconds, fps_num, fps_den):
    """返回时间对应的帧号。"""
    raise NotImplementedError

def sync_decision(audio_time, video_time, threshold, keyframes):
    """返回 (drift, action, target)。"""
    raise NotImplementedError
