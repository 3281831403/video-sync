# 视频同步：时间基、帧号、漂移与关键帧跳转

播放器在 PTS 时间基、29.97 帧号、音画漂移和关键帧跳转上出错，导致追帧、重复帧和卡顿。本仓库固定时间链路。

- 领域：游戏、图形与多媒体
- 子方向：音视频处理
- 语言/框架：Python 3, pytest
- 初始状态：15 个参数化用例全部失败

## 目录结构

```
README.md
conftest.py
.gitignore
media/__init__.py
media/video_sync.py
tests/test_video_sync.py
```

## 需要修复的 10 个问题

1. PTS 按 timescale 转秒，不按毫秒硬编码
2. 帧号按有理帧率计算，29.97 不漂移
3. 音画漂移以音频时钟为基准
4. 超过阈值才跳帧，避免频繁追帧
5. 跳转目标选择不超过目标时间的关键帧
6. 丢帧时保持时间线连续
7. 可变帧率下按实际 PTS 而非帧号
8. 多轨道各自维护时间基
9. seek 后清空旧帧队列
10. 播放速率变化时同步更新漂移阈值

## 15 条验收契约

    01. pts seconds — `timeline_seconds`
    02. pts half — `timeline_seconds`
    03. pts ntsc — `timeline_seconds`
    04. pts zero — `timeline_seconds`
    05. pts large — `timeline_seconds`
    06. frame zero — `frame_for_time`
    07. frame one — `frame_for_time`
    08. frame ntsc — `frame_for_time`
    09. frame 2398 — `frame_for_time`
    10. frame partial — `frame_for_time`
    11. sync hold — `sync_decision`
    12. sync seek — `sync_decision`
    13. sync negative — `sync_decision`
    14. sync no key — `sync_decision`
    15. sync exact — `sync_decision`

## 当前状态

`media/video_sync.py` 只保留函数签名与文档字符串，所有函数体统一
`raise NotImplementedError`。`tests/test_video_sync.py` 使用一个
`@pytest.mark.parametrize` 装载 15 条契约，初始全部失败且没有 collection error。

```bash
python -m pytest -q
```

预期输出包含 `15 failed`。实现 `media/video_sync.py` 后，15 条契约应全部通过。
