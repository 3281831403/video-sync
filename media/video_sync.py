"""视频同步：时间基换算、有理帧率帧号、以音频为主时钟的漂移决策。"""

from __future__ import annotations

import math


def timeline_seconds(pts, timescale):
    """把 PTS 按 timescale 换算成秒（不硬编码毫秒）。"""
    if timescale == 0:
        raise ValueError("timescale 不能为 0")
    return pts / timescale


def frame_for_time(seconds, fps_num, fps_den):
    """按有理帧率 (fps_num/fps_den) 返回时间对应的帧号（向下取整）。"""
    if fps_den == 0:
        raise ValueError("fps_den 不能为 0")
    return math.floor(seconds * fps_num / fps_den)


def sync_decision(audio_time, video_time, threshold, keyframes):
    """以音频时钟为基准判断漂移。

    返回 (drift, action, target)：
    - drift = audio_time - video_time，正值表示视频落后；
    - |drift| < threshold 时 'hold'，达到或超过阈值才 'seek'，避免频繁追帧；
    - target 为不超过 audio_time 的最近关键帧（seek 对齐关键帧），无关键帧时为 0。
    """
    drift = audio_time - video_time
    action = 'hold' if abs(drift) < threshold else 'seek'
    target = 0
    for kf in keyframes:
        if kf <= audio_time and kf > target:
            target = kf
    return (drift, action, target)
