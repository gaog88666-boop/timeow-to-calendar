# Timeow → macOS 日历自动同步

将 [Timeow](https://github.com/f-person/timeow-mac) 记录的电脑活跃时间，自动导入 macOS 自带日历。

## 你会得到什么

日历中按时间段记录每天的电脑使用情况，方便回顾每天、每周的工作时长。

## 需要什么

- macOS（需要自带 Python 3，终端输入 `python3 --version` 确认）
- [Timeow](https://github.com/f-person/timeow-mac/releases)（免费，6MB，安装后在菜单栏显示电脑使用时长）
- macOS 自带日历中需要有一个名为 **"Office"** 的日历（没有就新建一个）

## 安装步骤

### 1. 安装 Timeow

从 [GitHub Releases](https://github.com/f-person/timeow-mac/releases) 下载 dmg，拖入"应用程序"文件夹，打开即可。Timeow 会在菜单栏显示当前活跃时长，合盖/锁屏自动暂停。

**先正常使用 Timeow 至少一天**，让它积累一些数据，再进行下一步。

### 2. 放置脚本

把 `timeow_to_calendar.py` 放到你喜欢的位置，比如：

```
~/Scripts/timeow_to_calendar.py
```

### 3. 运行

打开终端，运行：

```bash
python3 ~/Scripts/timeow_to_calendar.py
```

（路径换成你实际放置的位置）

脚本会列出过去 7 天所有未导入的活跃时间段，按日期分组显示总时长，输入 `Y` 确认后导入日历。已导入过的不会重复添加。

首次运行时 macOS 可能会弹窗，要求授权 Python 控制"日历"，点**允许**。

## 常见问题

**Q: 想改日历名称？**

打开 `timeow_to_calendar.py`，修改顶部的 `CALENDAR_NAME = "Office"` 即可。

**Q: 想改回溯天数？**

修改顶部的 `LOOKBACK_DAYS = 7`，比如改成 `14` 就是回溯两周。

## 致谢

- [Timeow](https://github.com/f-person/timeow-mac) by f-person
