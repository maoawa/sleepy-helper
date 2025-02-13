# Sleepy Helper
**Sleepy Helper** 是 **Project Sleepy**([**maoawa/project-sleepy**](https://github.com/maoawa/project-sleepy)) 的扩展。

*****HA***** = **Home Assistant**

目前包括如下几个功能:  
1. 通过 Python 脚本定时向 Home Assistant 发送当前 macOS 或 Windows 设备上捕获焦点(前台程序)的标题。  
(见 [**前台程序报告器**](#app-reporter) 部分)
2. 通过快捷指令实现在 Apple 设备上更新网站上展示的消息，同时设置过期时间，亦可使消息立即过期。  
(见 [**快捷指令**](#shortcuts) 部分)
3. 将各种传感器和控制器通过 [**ESPHome**](https://esphome.io) 接入 Home Assistant，来控制如**隐私模式**等功能的开关。  
(见 [**ESPHome**](#esphome) 部分)

## 前台程序报告器<a id="app-reporter"></a>
macOS 版: [app-reporter/macos](./app-reporter/macos/)  
Windows 版: [app-reporter/windows](./app-reporter/windows)

当 Python 脚本运行时，将会根据同目录下的 `config.py` 中设置的时间间隔定时像 Home Assistant 发送当前捕获焦点的程序名。  
在 Home Assistant 中应有一个类型为 Text 的 Helper 来储存程序名，详见 [**HA 官方文档**](https://www.home-assistant.io/integrations/input_text/#:~:text=The%20preferred%20way%20to%20configure%20an%20input%20text,add%20button%20and%20then%20choose%20the%20Text%20option.)。以下假定这个 Helper 的实体 ID (Entity ID) 为 `input_text.my_device`

`config.py` 中需要定义以下几个变量 (`config-example.py` 中有模板):
1. `HASS_URL`: 你的 Home Assistant 的 REST API 修改状态的 URL (默认为 `<HA DOMAIN>/api/states/<TEXT HELPER>`，如 `https://your-home.example.net/api/states/input_text.my_device`)
2. `HASS_TOKEN`: 你的长期访问令牌(在控制台左下角用户面板的底部生成，详见 [**HA 官方文档**](https://developers.home-assistant.io/docs/auth_api/#long-lived-access-token))
3. `UPDATE_INTERVAL`: 向 Home Assistant 发送的时间间隔，单位为秒
4. `IGNORE_SSL_ERRORS`: 忽略 SSL 证书错误。建议仅在需要并能确保通信安全时开启(例如您的 HA 设备在内网，您希望直接通过内网向其发送数据)
5. `ATTRIBUTES`: Helper 的默认属性，格式为 JSON，以下是一个示例:
```json
ATTRIBUTES = {
    "editable": "true", // 是否可在 HA 控制台中编辑
    "min": 0, // 文本最小长度
    "max": 255, // 文本最大长度
    "pattern": "null",
    "mode": "text",
    "icon": "mdi:monitor", // Helper 的图标
    "friendly_name": "My Device", // Helper 的名称
}
```

## 快捷指令<a id="shortcuts"></a>
**Project Sleepy** 允许您在网页上显示自定义信息，并自定义它的过期时间。但在 Apple 设备上，并不能直接通过 HomeKit 来修改这个自定义信息。幸运的是，我们可以通过快捷指令来解决这个问题。  
在 Home Assistant 中应有一个类型为 Text 的 Helper 来储存自定义信息，详见 [**HA 官方文档**](https://www.home-assistant.io/integrations/input_text/#:~:text=The%20preferred%20way%20to%20configure%20an%20input%20text,add%20button%20and%20then%20choose%20the%20Text%20option.)。以下假定这个 Helper 的实体 ID (Entity ID) 为 `input_text.message`。

同时应有一个类型为 Date and/or time 的 Helper 储存信息过期时间，设置为包含日期和时间，并配置自动化使到达该时间时将自定义消息的值设置为 **`EXPIRED`**，详见 [**HA 官方文档**](https://www.home-assistant.io/integrations/input_datetime/#:~:text=The%20preferred%20way%20to%20configure%20input%20datetime,add%20button%20and%20then%20choose%20the%20Date%20and/or%20time%20option.)。以下假定这个 Helper 的实体 ID (Entity ID) 为 `input_datetime.message_timer`。

注意: 为了保证正确指向变量，请直接修改快捷指令**文本**(Text)中的数据，而不是删除后重新创建文本。

### 更新网页消息 (Update Message)
[通过 iCloud 连接获取](https://www.icloud.com/shortcuts/7a2c65bdde874b10866310b0002acd9e) 或下载 [shortcuts/update-message.shortcut](./shortcuts/update-message.shortcut) 并导入 快捷指令 APP

### 手动使网页消息过期 (Expire Message)
若想手动使网页消息过期，Home Assistant 中需要有一个类型为 Button 的 Helper，并配置自动化使按钮在触发时将自定义消息的值设置为 **`EXPIRED`**，详见 [**HA 官方文档**](https://www.home-assistant.io/integrations/input_button/#:~:text=The%20preferred%20way%20to%20configure%20button%20helpers,add%20button;%20next%20choose%20the%20Button%20option.)。以下假定这个 Helper 的实体 ID (Entity ID) 为 `input_button.message_expire`。

[通过 iCloud 连接获取](https://www.icloud.com/shortcuts/b0edf4a5e1324822add8889cfa652b30) 或下载 [shortcuts/expire-message.shortcut](./shortcuts/expire-message.shortcut) 并导入 快捷指令 APP

## ESPHome<a id="esphome"></a>
[**ESPHome**](https://esphome.io) 是一个自动化平台，允许用户使用简单的 **YAML 配置** 来定义设备功能，并将其无缝集成到 **Home Assistant**。它支持各种传感器、开关、显示屏等，并提供 无线 OTA 更新 和 本地控制，无需依赖云端。

### 屏幕与矩阵键盘实现显示数据与控制开关 ([Sleepy Helper](./esphome/sleepy-helper.yaml))
在 **Project Sleepy** 中，有**当前状态显示(醒着/睡似了/自定义...)**和一个简易的**请求量统计系统**。这些数据可以通过 **ESPHome** 显示在 ESP32 上。除此之外，还有**隐私模式等开关**，也可以通过 **ESPHome** 在 ESP32 上控制。

**模块选择**:
1. 12864 [I²C](https://zh.wikipedia.org/wiki/I²C) 接口 OLED 屏幕
2. 四位矩阵键盘 (四按钮)

**接线表**:
<table>
  <tr>
    <th>模块</th>
    <th>模块接口</th>
    <th>对应 ESP32 接口</th>
    <th>功能</th>
  </tr>
  <tr>
    <td rowspan="4">I²C 屏幕</td>
    <td>SDA</td>
    <td>GPIO21 (D21)</td>
    <td rowspan="2">传输数据</td>
  </tr>
  <tr>
    <td>SCL</td>
    <td>GPIO22 (D22)</td>
  </tr>
  <tr>
    <td>VCC</td>
    <td>VIN (5V)</td>
    <td>供电</td>
  </tr>
  <tr>
    <td>GND</td>
    <td>GND</td>
    <td>接地</td>
  </tr>
  <tr>
    <td rowspan="5">矩阵键盘</td>
    <td>按钮1</td>
    <td>GPIO16 (D16)</td>
    <td>状态开关 (假定为"input_boolean.awake")</td>
  </tr>
  <tr>
    <td>按钮2</td>
    <td>GPIO17 (D17)</td>
    <td>隐私模式开关 (假定为"input_boolean.private_mode")</td>
  </tr>
  <tr>
    <td>按钮3</td>
    <td>GPIO18 (D18)</td>
    <td>未分配</td>
  </tr>
  <tr>
    <td>按钮4</td>
    <td>GPIO19 (D19)</td>
    <td>触发手动清除消息 (假定为"input_button.message_expire")</td>
  </tr>
  <tr>
    <td>KCOM</td>
    <td>GND</td>
    <td>接地</td>
  </tr>
</table>

*提示: 矩阵键盘模块上印的引脚名不固定，但顺序应与按键实际顺序相同，只需将 **KCOM** 接入 **GND** 其余四个引脚可自由调整接线顺序。*

**注意**:
1. 切换开关和触发按钮操作需要在 Home Assistant 的 ESPHome 集成中启用 `Allow the device to make Home Assistant service calls.` 选项，授予 ESP32 控制权限。
2. 请确保 ESP32 和 Home Assistant 在一个时区。
3. 显示文字的字体只支持英文，无法显示中文。

**特性**: 如果搭配下方的 **环境光强度、温湿度和气压传感器** 一起使用，屏幕将在光敏电阻检测到环境光变暗时自动关闭，同理环境光变暗时自动亮起。也可以自行修改配置集成光敏电阻。

**成品预览(开发板)**:

![Sleepy Helper Preview](https://api.maao.cc/static/sleepy-helper/readme/sleepy-helper.jpeg)

**配置文件**: [./esphome/sleepy-helper.yaml](./esphome/sleepy-helper.yaml)

### 环境光强度、温湿度和气压传感器 ([Sleepy Helper Sensors](./esphome/sleepy-helper-sensors.yaml))
在 **Project Sleepy** 中，网页上会显示环境光强度、室内温湿度和气压数据。这是通过 **ESPHome** 读取 ESP32 上传感器模块的数据，并上传给 Home Assistant 实现的。

**模块选择**:
1. 光敏电阻
2. AMT20+BMP280 温湿度大气压传感器

*(光敏电阻可以通过调节模块上的电位器来调整判断亮或暗的阈值，但一般出厂时已经调整至合适状态，建议仅在需要时调节)*

**接线表**:
<table>
  <tr>
    <th>模块</th>
    <th>模块接口</th>
    <th>对应 ESP32 接口</th>
    <th>功能</th>
  </tr>
  <tr>
    <td rowspan="3">光敏电阻</td>
    <td>DO</td>
    <td>GPIO27 (D27)</td>
    <td>传输数据(高低电平)</td>
  </tr>
  <tr>
    <td>VCC</td>
    <td>VIN (5V)</td>
    <td>供电</td>
  </tr>
  <tr>
    <td>GND</td>
    <td>GND</td>
    <td>接地</td>
  </tr>
  <tr>
    <td rowspan="4">传感器</td>
    <td>SDA</td>
    <td>GPIO21 (D21)</td>
    <td rowspan="2">传输数据</td>
  </tr>
  <tr>
    <td>SCL</td>
    <td>GPIO22 (D22)</td>
  </tr>
  <tr>
    <td>VDD</td>
    <td>3V3</td>
    <td>供电</td>
  </tr>
  <tr>
    <td>GND</td>
    <td>GND</td>
    <td>接地</td>
  </tr>
</table>

**成品预览(开发板)**:

![Sleepy Helper Sensors Preview](https://api.maao.cc/static/sleepy-helper/readme/sleepy-helper-sensors.jpeg)

*焊工有限，轻喷*

**配置文件**: [./esphome/sleepy-helper-sensors.yaml](./esphome/sleepy-helper-sensors.yaml)

### 整合版 ([Sleepy Helper Master](./esphome/sleepy-helper-master.yaml))

对以上两个设计的整合，允许屏幕显示更多信息，更直观，优化控制逻辑防误触等。

**模块选择**:
1. 12864 [I²C](https://zh.wikipedia.org/wiki/I²C) 接口 OLED 屏幕
2. 四位矩阵键盘 (四按钮)
3. 光敏电阻
4. AMT20+BMP280 温湿度大气压传感器

<table>
  <tr>
    <th>模块</th>
    <th>模块接口</th>
    <th>对应 ESP32 接口</th>
    <th>功能</th>
  </tr>
  <tr>
    <td rowspan="4">I²C 屏幕</td>
    <td>SDA</td>
    <td>GPIO21 (D21)</td>
    <td rowspan="2">传输数据</td>
  </tr>
  <tr>
    <td>SCL</td>
    <td>GPIO22 (D22)</td>
  </tr>
  <tr>
    <td>VCC</td>
    <td>VIN (5V)</td>
    <td>供电</td>
  </tr>
  <tr>
    <td>GND</td>
    <td>GND</td>
    <td>接地</td>
  </tr>
  <tr>
    <td rowspan="5">矩阵键盘</td>
    <td>按钮1</td>
    <td>GPIO16 (D16)</td>
    <td>状态开关 (假定为"input_boolean.awake")</td>
  </tr>
  <tr>
    <td>按钮2</td>
    <td>GPIO17 (D17)</td>
    <td>隐私模式开关 (假定为"input_boolean.private_mode")</td>
  </tr>
  <tr>
    <td>按钮3</td>
    <td>GPIO18 (D18)</td>
    <td>临时点亮屏幕五秒 (适用于暗光自动熄屏后想检查状态时)</td>
  </tr>
  <tr>
    <td>按钮4</td>
    <td>GPIO19 (D19)</td>
    <td><strong>双击</strong>触发手动清除消息 (假定为"input_button.message_expire")</td>
  </tr>
  <tr>
    <td>KCOM</td>
    <td>GND</td>
    <td>接地</td>
  </tr>
  <tr>
    <td rowspan="3">光敏电阻</td>
    <td>DO</td>
    <td>GPIO27 (D27)</td>
    <td>传输数据(高低电平)</td>
  </tr>
  <tr>
    <td>VCC</td>
    <td>3V3</td>
    <td>供电</td>
  </tr>
  <tr>
    <td>GND</td>
    <td>GND</td>
    <td>接地</td>
  </tr>
  <tr>
    <td rowspan="4">温湿度大气压传感器</td>
    <td>SDA</td>
    <td>GPIO33 (D33)</td>
    <td rowspan="2">传输数据</td>
  </tr>
  <tr>
    <td>SCL</td>
    <td>GPIO32 (D32)</td>
  </tr>
  <tr>
    <td>VDD</td>
    <td>3V3</td>
    <td>供电</td>
  </tr>
  <tr>
    <td>GND</td>
    <td>GND</td>
    <td>接地</td>
  </tr>
</table>

**成品预览(开发板)**:

![Sleepy Helper Master Preview](https://api.maao.cc/static/sleepy-helper/readme/sleepy-helper-master.jpeg)

*焊工有限，轻喷*

**配置文件**: [./esphome/sleepy-helper-master.yaml](./esphome/sleepy-helper-master.yaml)
