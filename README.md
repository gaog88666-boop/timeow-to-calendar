# Timeow → macOS Calendar

[中文](#中文说明) | [English](#english)

---

## English

Automatically sync [Timeow](https://github.com/f-person/timeow-mac) active periods to your macOS Calendar. Each active session becomes a calendar event, giving you a visual record of your daily and weekly computer usage.

### What You Get

Your macOS Calendar becomes a work-time archive — each active period appears as an event, making it easy to review how many hours you spent at your computer each day or week.

### Requirements

- macOS with Python 3 (pre-installed; verify with `python3 --version`)
- [Timeow](https://github.com/f-person/timeow-mac/releases) (free, ~6MB)
- A calendar named **"Office"** in the macOS Calendar app (create one if you don't have it)

### Setup

#### 1. Install Timeow

Download the dmg from [GitHub Releases](https://github.com/f-person/timeow-mac/releases), drag it to Applications, and launch. Timeow will display your active session time in the menu bar and automatically pause when you lock the screen or close the lid.

**Use Timeow for at least one day** to accumulate some data before proceeding.

#### 2. Save the Script

Place `timeow_to_calendar.py` anywhere you like, for example:

```
~/Scripts/timeow_to_calendar.py
```

#### 3. Run

Open Terminal and run:

```bash
python3 ~/Scripts/timeow_to_calendar.py
```

The script will list all active periods from the past 7 days that haven't been imported yet, grouped by date with total duration. Type `Y` to confirm and import them to your calendar. Already-imported periods are never duplicated.

On first run, macOS may prompt you to allow Python to control Calendar — click **Allow**.

### Configuration

| Setting | Location | Default |
|---------|----------|---------|
| Calendar name | `CALENDAR_NAME` in script | `"Office"` |
| Lookback days | `LOOKBACK_DAYS` in script | `7` |

### Credits

- [Timeow](https://github.com/f-person/timeow-mac) by f-person

---

## 中文说明

将 [Timeow](https://github.com/f-person/timeow-mac) 记录的电脑活跃时间，自动导入 macOS 自带日历。每段活跃会话变成一个日历事件，方便回顾每天、每周的工作时长。

### 你会得到什么

日历中按时间段记录每天的电脑使用情况，方便回顾每天、每周的工作时间分布。

### 需要什么

- macOS（需要自带 Python 3，终端输入 `python3 --version` 确认）
- [Timeow](https://github.com/f-person/timeow-mac/releases)（免费，6MB）
- macOS 自带日历中需要有一个名为 **"Office"** 的日历（没有就新建一个）

### 安装步骤

#### 1. 安装 Timeow

从 [GitHub Releases](https://github.com/f-person/timeow-mac/releases) 下载 dmg，拖入"应用程序"文件夹，打开即可。Timeow 会在菜单栏显示当前活跃时长，合盖/锁屏自动暂停。

**先正常使用 Timeow 至少一天**，让它积累一些数据，再进行下一步。

#### 2. 保存脚本

把 `timeow_to_calendar.py` 放到你喜欢的位置，比如：

```
~/Scripts/timeow_to_calendar.py
```

#### 3. 运行

打开终端，运行：

```bash
python3 ~/Scripts/timeow_to_calendar.py
```

（路径换成你实际放置的位置）

脚本会列出过去 7 天所有未导入的活跃时间段，按日期分组显示总时长，输入 `Y` 确认后导入日历。已导入过的不会重复添加。

首次运行时 macOS 可能会弹窗，要求授权 Python 控制"日历"，点**允许**。

### 可配置项

| 设置 | 位置 | 默认值 |
|------|------|--------|
| 日历名称 | 脚本顶部 `CALENDAR_NAME` | `"Office"` |
| 回溯天数 | 脚本顶部 `LOOKBACK_DAYS` | `7` |

### 致谢

- [Timeow](https://github.com/f-person/timeow-mac) by f-person
