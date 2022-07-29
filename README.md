[GitHub](https://github.com/shigebeyond/AppiumBoot) | [Gitee](https://gitee.com/shigebeyond/AppiumBoot)

# AppiumBoot - yaml驱动Appium测试

## 概述
Appium是移动端的自动化测试工具，但是要写python代码；

考虑到部分测试伙伴python能力不足，因此扩展Appium，支持通过yaml配置测试步骤;

框架通过编写简单的yaml, 就可以执行一系列复杂的浏览器操作步骤, 如点击/输入/拖拽/上下滑/左右滑/放大缩小/提取变量/打印变量等，极大的简化了伙伴编写自动化测试脚本的工作量与工作难度，大幅提高人效；

框架通过提供类似python`for`/`if`/`break`语义的步骤动作，赋予伙伴极大的开发能力与灵活性，能适用于广泛的测试场景。

框架提供`include`机制，用来加载并执行其他的步骤yaml，一方面是功能解耦，方便分工，一方面是功能复用，提高效率与质量，从而推进测试整体的工程化。

## 特性
1. 基于 Appium 的webdriver
2. 支持通过yaml来配置执行的步骤，简化了自动化测试开发:
每个步骤可以有多个动作，但单个步骤中动作名不能相同（yaml语法要求）;
动作代表webdriver上的一种操作，如tap/swipe/scoll等等;
3. 支持复杂的手势: 拖拽/上下滑/左右滑/放大缩小/多个点组成的移动轨迹等;
4. 支持提取器
5. 支持校验器
6. 支持识别验证码(使用有道ocr)
7. 支持类似python`for`/`if`/`break`语义的步骤动作，灵活适应各种场景
8. 支持`include`引用其他的yaml配置文件，以便解耦与复用

## todo
1. 支持更多的动作

## 安装
```
pip3 install AppiumBoot
```

安装后会生成命令`AppiumBoot`;

注： 对于深度deepin-linux系统，生成的命令放在目录`~/.local/bin`，建议将该目录添加到环境变量`PATH`中，如
```
export PATH="$PATH:/home/shi/.local/bin"
```

## 使用
```
# 1 执行单个文件
AppiumBoot 步骤配置文件.yml

# 2 执行多个文件
AppiumBoot 步骤配置文件1.yml 步骤配置文件2.yml ...

# 3 执行单个目录, 即执行该目录下所有的yml文件
AppiumBoot 步骤配置目录

# 4 执行单个目录下的指定模式的文件
AppiumBoot 步骤配置目录/step-*.yml
```

- 如执行 `AppiumBoot example/step-material.yml`:
你需要先安装[android material组件demo app](https://gitee.com/lizhenghaodamowang/material-components-android);
输出如下:
```
加载并执行步骤文件: /ohome/shi/code/python/AppiumBoot/example/step-material.yml
处理动作: init_driver={'executor': 'http://localhost:4723/wd/hub', 'desired_caps': {'platformName': 'Android', 'platformVersion': '9', 'deviceName': 'f978cc97', 'appPackage': 'io.material.catalog', 'appActy': 'io.material.catalog.main.MainActivity', 'automationName': 'UiAutomator2', 'noReset': True}}
处理动作: include=material/comp1.yml
加载并执行步骤文件: /ohome/shi/code/python/AppiumBoot/example/material/comp1.yml
处理动作: click_by={'xpath': '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/aid.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout'}
处理动作: sleep=1
处理动作: click_by={'id': 'io.material.catalog:id/cat_demo_landing_row_root'}
处理动作: swipe_up=None
处理动作: sleep=1
处理动作: swipe_down=None
处理动作: sleep=1
处理动作: click_by={'id': 'io.material.catalog:id/end'}
处理动作: sleep=2
处理动作: click_by={'id': 'io.material.catalog:id/center'}
处理动作: sleep=2
处理动作: click_by={'id': 'io.material.catalog:id/attach_toggle'}
处理动作: sleep=2
处理动作: click_by={'id': 'io.material.catalog:id/center'}
处理动作: include=material/back.yml
加载并执行步骤文件: /ohome/shi/code/python/AppiumBoot/example/material/back.yml
处理动作: sleep=1
处理动作: back=None
处理动作: sleep=1
处理动作: back=None
处理动作: include=material/comp2.yml
加载并执行步骤文件: /ohome/shi/code/python/AppiumBoot/example/material/comp2.yml
处理动作: click_by={'xpath': '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/aid.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[2]/android.widget.LinearLayout'}
处理动作: sleep=1
处理动作: click_by={'xpath': '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/aid.view.ViewGroup/android.widget.ScrollView/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout'}
处理动作: click_by={'aid': 'Page 2'}
处理动作: click_by={'aid': 'Theme Switcher'}
处理动作: sleep=1
处理动作: click_by={'xpath': '(//android.widget.RadioButton[@content-desc="Green"])[1]'}
处理动作: sleep=1
处理动作: click_by={'id': 'io.material.catalog:id/apply_button'}
处理动作: sleep=1
处理动作: click_by={'id': 'io.material.catalog:id/add_button'}
处理动作: sleep=1
处理动作: click_by={'id': 'io.material.catalog:id/remove_button'}
处理动作: sleep=2
处理动作: back=None
处理动作: sleep=1
处理动作: click_by={'xpath': '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/aid.view.ViewGroup/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.RelativeLayout[3]'}
处理动作: sleep=1
处理动作: click_by={'aid': 'Alarm'}
处理动作: sleep=1
处理动作: click_by={'aid': 'Clock'}
处理动作: sleep=1
处理动作: click_by={'aid': 'Timer'}
处理动作: sleep=1
处理动作: click_by={'aid': 'Stopwatch'}
处理动作: include=material/back.yml
加载并执行步骤文件: /ohome/shi/code/python/AppiumBoot/example/material/back.yml
处理动作: sleep=1
处理动作: back=None
处理动作: sleep=1
处理动作: back=None
处理动作: include=material/comp3.yml
加载并执行步骤文件: /ohome/shi/code/python/AppiumBoot/example/material/comp3.yml
处理动作: click_by={'xpath': '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/aid.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[3]/android.widget.LinearLayout'}
处理动作: sleep=1
处理动作: click_by={'id': 'io.material.catalog:id/cat_demo_landing_row_root'}
处理动作: print=非全屏的上拉
非全屏的上拉
处理动作: sleep=1
处理动作: swipe_up=None
处理动作: sleep=1
处理动作: swipe_vertical=0.55,0.8
处理动作: sleep=1
处理动作: click_by={'id': 'io.material.catalog:id/cat_fullscreen_switch'}
处理动作: sleep=1
处理动作: print=全屏的上拉
全屏的上拉
处理动作: swipe_up=None
处理动作: sleep=1
处理动作: swipe_down=None
处理动作: include=material/back.yml
加载并执行步骤文件: /ohome/shi/code/python/AppiumBoot/example/material/back.yml
处理动作: sleep=1
处理动作: back=None
处理动作: sleep=1
处理动作: back=None
处理动作: include=material/comp4.yml
加载并执行步骤文件: /ohome/shi/code/python/AppiumBoot/example/material/comp4.yml
处理动作: click_by={'xpath': '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/aid.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[4]/android.widget.LinearLayout'}
处理动作: sleep=1
处理动作: click_by={'xpath': '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/aid.view.ViewGroup/android.widget.ScrollView/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout'}
处理动作: click_by={'aid': 'Theme Switcher'}
处理动作: sleep=1
处理动作: click_by={'xpath': '(//android.widget.RadioButton[@content-desc="Yellow"])[1]'}
处理动作: sleep=1
处理动作: click_by={'id': 'io.material.catalog:id/apply_button'}
处理动作: click_by={'id': 'io.material.catalog:id/material_button'}
处理动作: sleep=1
处理动作: back=None
......
```
命令会自动打开[android material组件demo app](https://gitee.com/lizhenghaodamowang/material-components-android)，并按照步骤配置文件的描述来执行动作，如下拉、上拉、左滑、点击按钮等，一个个组件页面去操作

- 如执行 `AppiumBoot example/step-zhs.yml`:
你要先安装众划算app;
输出如下:
```
加载并执行步骤文件: /ohome/shi/code/python/AppiumBoot/example/step-zhs.yml
处理动作: init_driver={'executor': 'http://localhost:4723/wd/hub', 'desired_caps': {'platformName': 'Android', 'platformVersion': '9', 'deviceName': 'f978cc97', 'appPackage': 'com.zhs.zhonghuasuanapp', 'apivity': 'com.zhs.activity.StartActivity', 'automationName': 'UiAutomator2', 'noReset': True}}
处理动作: sleep=7
处理动作: click_by_if_exist={'id': 'com.zhs.zhonghuasuanapp:id/img_start'}
处理动作: start_recording_screen=None
处理动作: swipe_up=None
处理动作: include=zhs/login.yml
加载并执行步骤文件: /ohome/shi/code/python/AppiumBoot/example/zhs/login.yml
处理动作: click_by={'id': 'com.zhs.zhonghuasuanapp:id/tab_my_image'}
处理动作: sleep=2
处理动作: once=[{'moveon_if': "boot.exist_by('id', 'com.zhs.zhonghuasuanapp:id/tv_account_login')", 'click_by': {'id': 'com.zhs.zhonghuasuanapp:id/tv_account_login'}, 'sleep': 2}, {'input_by_id': {'com.zhsnghuasuanapp:id/edit_login_username': 'shigebeyond', 'com.zhs.zhonghuasuanapp:id/edit_login_password': 'shige123'}}, {'click_by': {'id': 'com.zhs.zhonghuasuanapp:id/box_user_agreement'}}, {'click_by': {'id': 'com.zhs.zhonghuasuanapp:id/login_submit'}, 'sleep': 4}, {'click_by_if_exist': {'id': 'com.zhs.zhonghuasuanapp:id/btn_i_know'}}, {'click_by_if_exist': {'id': 'com.zhs.zhonghuasuanapp:id/tv_hid_guid'}}]
-- 开始循环: for(1) -- 
第1次迭代
处理动作: moveon_if=boot.exist_by('id', 'com.zhs.zhonghuasuanapp:id/tv_account_login')
-- 跳出循环: for(1), 跳出条件: not (boot.exist_by('id', 'com.zhs.zhonghuasuanapp:id/tv_account_login')) -- 
处理动作: sleep=2
处理动作: include=zhs/apply.yml
加载并执行步骤文件: /ohome/shi/code/python/AppiumBoot/example/zhs/apply.yml
处理动作: click_by={'id': 'com.zhs.zhonghuasuanapp:id/tab_new_image'}
处理动作: sleep=4
处理动作: swipe_up=None
处理动作: sleep=2
处理动作: swipe_down=None
......
```
命令会自动打开众划算app，并按照步骤配置文件的描述来执行动作，如下拉、上拉、左滑、点击按钮等

## 步骤配置文件及demo
用于指定多个步骤, 示例见源码 [example](https://github.com/shigebeyond/AppiumBoot/tree/main/example) 目录下的文件;

顶级的元素是步骤;

每个步骤里有多个动作(如sleep)，如果动作有重名，就另外新开一个步骤写动作，这是由yaml语法限制导致的，但不影响步骤执行。

[demo](https://github.com/shigebeyond/AppiumBoot/blob/main/example/)

## 查找元素的方法
1. id:
2. sid: accessibility_id
3. class: 
4. xpath:

## 配置详解
支持通过yaml来配置执行的步骤;

每个步骤可以有多个动作，但单个步骤中动作名不能相同（yaml语法要求）;

动作代表webdriver上的一种操作，如tap/swipe/scoll等等;

下面详细介绍每个动作:

1. init_driver: 初始化driver
```yaml
init_driver:
    executor: http://localhost:4723/wd/hub
    desired_caps:
      platformName: Android
      platformVersion: '9'
      deviceName: f978cc97
      appPackage: io.material.catalog
      appActivity: io.material.catalog.main.MainActivity
      automationName: UiAutomator2
      noReset: true
```

2. close_driver: 关闭driver
```yaml
close_driver:
```

3. sleep: 线程睡眠; 
```yaml
sleep: 2 # 线程睡眠2秒
```

4. print: 打印, 支持输出变量/函数; 
```yaml
# 调试打印
print: "总申请数=${dyn_data.total_apply}, 剩余份数=${dyn_data.quantity_remain}"
```

变量格式:
```
$msg 一级变量, 以$为前缀
${data.msg} 多级变量, 用 ${ 与 } 包含
```

函数格式:
```
${random_str(6)} 支持调用函数，目前仅支持3个函数: random_str/random_int/incr
```

函数罗列:
```
random_str(n): 随机字符串，参数n是字符个数
random_int(n): 随机数字，参数n是数字个数
incr(key): 自增值，从1开始，参数key表示不同的自增值，不同key会独立自增
```

5. input_by_id: 填充 id 指定的输入框; 
```yaml
input_by_id:
  # 输入框id: 填充的值(支持写变量)
  'io.material.catalog:id/cat_demo_input': '18877310999'
```

6. input_by_aid: 填充 accessibility_id 指定的输入框; 
```yaml
input_by_aid:
  # 输入框accessibility_id: 填充的值(支持写变量)
  'Input name': '18877310999'
```

7. input_by_class: 填充 指定类名的输入框; 
```yaml
input_by_class:
  # 输入框类名: 填充的值(支持写变量)
  'android.widget.EditText': '18877310999'
```

8. input_by_xpath: 填充 xpath 指定的输入框; 
```yaml
input_by_xpath:
  # 输入框xpath路径: 填充的值(支持写变量)
  '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.FrameLayout/android.widget.EditText': aaa
```

9. hide_keyboard: 隐藏键盘
```yaml
hide_keyboard:
```

10. swipe: 屏幕横扫(传坐标)
```yaml
swipe: 
    from: 100,100 # 起点坐标
    to: 200,200 # 终点坐标
    duration: 2 # 耗时秒数, 可省
```

11. swipe_up: 上滑(传比例)
```yaml
swipe_up: 0.55 # 移动幅度比例(占屏幕高度的比例)
swipe_up: # 默认移动幅度比例为0.5
```

12. swipe_down: 下滑(传y坐标)
```yaml
swipe_down: 100 # y坐标
swipe_down: # 默认y坐标为中间
```

13. swipe_left: 左滑(传y坐标)
```yaml
swipe_left: 100 # y坐标
swipe_left: # 默认y坐标为中间
```

14. swipe_right: 右滑(传比例)
```yaml
swipe_right: 0.55 # 移动幅度比例(占屏幕宽度的比例)
swipe_right: # 默认移动幅度比例为0.5
```

15. swipe_vertical: 垂直方向(上下)滑动(传比例)
```yaml
swipe_vertical: 0.2,0.7 # y轴起点/终点位置在屏幕的比例，如 0.2,0.7，即y轴上从屏幕0.2比例处滑到0.7比例处
```

16. swipe_horizontal: 水平方向(左右)滑动(传比例)
```yaml
swipe_horizontal: 0.2,0.7 # x轴起点/终点位置在屏幕的比例，如 0.2,0.7，即x轴上从屏幕0.2比例处滑到0.7比例处
```

17. move_track: 移动轨迹(传坐标序列)
```yaml
move_track: '800,1600;100,1600;100,600;800,600;360,600;360,1100' # 坐标序列，坐标之间使用;分割，如x1,y1;x2,y2
```

18. drag_and_drop_by: 拖拽(传元素): 从一个元素滑动到另一个元素，第二个元素替代第一个元素原本屏幕上的位置
```yaml
drag_and_drop_by: 
    by: xpath # 元素查找方式: id/sid/class/xpath    
    from: /hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[4]/android.widget.LinearLayout
    to: /hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[2]/android.widget.LinearLayout
```

19. scroll_by: 滚动(传元素): 从一个元素滚动到另一元素，直到页面自动停止(有惯性)
```yaml
scroll_by: 
    by: xpath # 元素查找方式: id/sid/class/xpath    
    from: /hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[4]/android.widget.LinearLayout
    to: /hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[2]/android.widget.LinearLayout
```

20. move_by: 移动(传元素): 从一个元素移动到另一元素，无惯性
```yaml
move_by: 
    by: xpath # 元素查找方式: id/sid/class/xpath    
    from: /hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[4]/android.widget.LinearLayout
    to: /hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[2]/android.widget.LinearLayout
```

21. zoom_in: 放大
```yaml
zoom_in: 
```

22. zoom_out: 缩小
```yaml
zoom_out: 
```

23. tap: 敲击屏幕(传坐标)
```yaml
tap: 200,200
```

24. tap_by: 敲击元素
```yaml
tap_by:
    # 元素查找方式(id/sid/class/xpath) : 查找的值
    #id: io.material.catalog:id/cat_demo_landing_row_root
    xpath: /hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout # 按钮的xpath路径
    # 耗时秒数, 可省, 可用于模拟长按
    duration: 10
```

25. click_by/click_by_if_exist: 点击元素; 
```yaml
click_by:
  # 元素查找方式(id/sid/class/xpath) : 查找的值
  #id: io.material.catalog:id/cat_demo_landing_row_root
  xpath: /hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout # 按钮的xpath路径
```

如果点击之前要先判断元素是否存在，则换用 click_by_if_exist

26. shake: 摇一摇
```yaml
shake:
```

27. set_orientation: 设置屏幕方向
```yaml
set_orientation: true # 是否竖屏, 否则横屏
```

28. set_location: 设置地理位置
```yaml
set_location: 49,123 # 纬度,经度
set_location: 49,123,10 # 纬度,经度,海拔高度
```

29. screenshot: 整个窗口截图存为png; 
```yaml
screenshot:
    save_dir: downloads # 保存的目录，默认为 downloads
    save_file: test.png # 保存的文件名，默认为:时间戳.png
```

30. screenshot_element_by: 对某个标签截图存为png; 
```yaml
screenshot_element_by
    # 元素查找方式(id/sid/class/xpath) : 查找的值
    #id: io.material.catalog:id/cat_demo_landing_row_root
    xpath: /hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout

    save_dir: downloads # 保存的目录，默认为 downloads
    save_file: test.png # 保存的文件名，默认为:时间戳.png
```

31. execute_js: 执行js; 
```yaml
execute_js: alert('hello world')
```

32. back: 返回键; 
```yaml
back: 
```

33. keyevent: 模拟系统键; 
```yaml
keyevent: '4'
```

34. open_notifications: 打开手机的通知栏; 
```yaml
open_notifications: 
```

35. get_clipboard: 读剪切板内容; 
```yaml
get_clipboard: name # 参数为记录剪切板内容的变量名
```

36. set_clipboard: 写剪切板内容; 
```yaml
set_clipboard: hello world $name # 参数是写入内容，可带参数
```

37. push_file:推文件到手机上, 即写手机上文件; 
```yaml
push_file:
    to: /storage/emulated/0/documents/test/a.txt # 写入的手机上的文件
    content: helloworld # 写入的内容, content与to只能二选一
    #from: a.txt # 写入内容的本地来源文件, content与to只能二选一
```

38. pull_file:从手机中拉文件, 即读手机上的文件; 
```yaml
pull_file:
    from: /storage/emulated/0/documents/test/a.txt # 读取的手机上的文件
    to: a.txt # 写入的本地文件, 可省
    var: content # 记录文件内容的变量, 可省
print: $content
```

39. send_sms:发送短信; 
```yaml
send_sms:
    phone: 13475556022
    content: hello $name
```

40. print_performance:打印性能信息; 
```yaml
print_performance:
```

41. start_recording_screen:开始录屏; 
start_recording_screen 与 stop_recording_screen 配合使用(start在前,stop在后)
```yaml
start_recording_screen:
```

42. stop_recording_screen:结束录屏,并存为视频文件;
start_recording_screen 与 stop_recording_screen 配合使用(start在前,stop在后), 如果两者中间的发生异常, 则系统会主动调用后续第一个stop_recording_screen动作, 以便记录好异常的全过程
```yaml
stop_recording_screen: # 默认视频文件路径为 `record-时间.mp4`
stop_recording_screen: a.mp4 # 视频文件路径
```

43. for: 循环; 
for动作下包含一系列子步骤，表示循环执行这系列子步骤；变量`for_i`记录是第几次迭代（从1开始）
```yaml
# 循环3次
for(3) :
  # 每次迭代要执行的子步骤
  - swipe_down:
    sleep: 2

# 无限循环，直到遇到跳出动作
# 有变量for_i记录是第几次迭代（从1开始）
for:
  # 每次迭代要执行的子步骤
  - break_if: for_i>2 # 满足条件则跳出循环
    swipe_down:
    sleep: 2
```

44. once: 只执行一次，等价于 `for(1)`; 
once 结合 moveon_if，可以模拟 python 的 `if` 语法效果
```yaml
once:
  # 每次迭代要执行的子步骤
  - moveon_if: for_i<=2 # 满足条件则往下走，否则跳出循环
    swipe_down:
    sleep: 2
```

45. break_if: 满足条件则跳出循环; 
只能定义在for循环的子步骤中
```yaml
break_if: for_i>2 # 条件表达式，python语法
```

46. moveon_if: 满足条件则往下走，否则跳出循环; 
只能定义在for循环的子步骤中
```yaml
moveon_if: for_i<=2 # 条件表达式，python语法
```

47. moveon_if_exist_by: 如果检查元素存在 则往下走，否则跳出循环; 
只能定义在for循环的子步骤中
```yaml
moveon_if_exist_by:
    id: com.shikee.shikeeapp:id/button1
```

48. include: 包含其他步骤文件，如记录公共的步骤，或记录配置数据(如用户名密码); 
```yaml
include: part-common.yml
```

49. set_vars: 设置变量; 
```yaml
set_vars:
  name: shi
  password: 123456
  birthday: 5-27
```

50. print_vars: 打印所有变量; 
```yaml
print_vars:
```

51. base_url: 设置基础url
```yaml
base_url: https://www.taobao.com/
```

52. get: 发get请求, 但无跳转; 
```yaml
get:
    url: $dyn_data_url # url,支持写变量
    extract_by_eval:
      dyn_data: "json.loads(response.text[16:-1])" # 变量response是响应对象
```

53. post: 发post请求, 但无跳转; 
```yaml
post:
    url: http://admin.jym1.com/store/add_store # url,支持写变量
    is_ajax: true
    data: # post的参数
      # 参数名:参数值
      store_name: teststore-${random_str(6)}
      store_logo_url: '$img'
```

54. upload: 上传文件; 
```yaml
upload: # 上传文件/图片
    url: http://admin.jym1.com/upload/common_upload_img/store_img
    files: # 上传的多个文件
      # 参数名:文件本地路径
      file: /home/shi/fruit.jpeg
    extract_by_jsonpath:
      img: $.data.url
```

55. download: 下载文件; 
变量`download_file`记录最新下载的单个文件
```yaml
download:
    url: https://img.alicdn.com/tfscom/TB1t84NPuL2gK0jSZPhXXahvXXa.jpg_q90.jpg
    save_dir: downloads # 保存的目录，默认为 downloads
    save_file: test.jpg # 保存的文件名，默认为url中最后一级的文件名
```

56. recognize_captcha: 识别验证码; 
参数同 `download` 动作， 因为内部就是调用 `download`;
而变量`captcha`记录识别出来的验证码
```
recognize_captcha:
    url: http://admin.jym1.com/login/verify_image
    # save_dir: downloads # 保存的目录，默认为 downloads
    # save_file: test.jpg # 保存的文件名，默认为url中最后一级的文件名
```

57. recognize_captcha_element: 识别验证码标签中的验证码; 
参数同 `screenshot_element_by` 动作， 因为内部就是调用 `screenshot_element_by`;
而变量`captcha`记录识别出来的验证码
```
recognize_captcha_element:
    # 元素查找方式(id/sid/class/xpath) : 查找的值
    #id: io.material.catalog:id/cat_demo_landing_row_root
    xpath: /hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout

    #save_dir: downloads # 保存的目录，默认为 downloads
    #save_file: test.jpg # 保存的文件名，默认为url中最后一级的文件名
```

## 校验器
主要是为了校验页面或响应的内容, 根据不同场景有2种写法
```
1. 针对当前页面, 那么校验器作为普通动作来写
2. 针对 get/post/upload 有发送http请求的动作, 那么校验器在动作内作为普通属性来写
```

不同校验器适用于不同场景
| 校验器 | 当前页面场景 | http请求场景 |
| ------------ | ------------ | ------------ |
| validate_by_id | Y | N |
| validate_by_aid | Y | N |
| validate_by_class | Y | N |
| validate_by_xpath | Y | Y |
| validate_by_css | N | Y |
| validate_by_jsonpath | N | Y |

1. validate_by_id:
从当前页面中校验 id 对应的元素的值
```yaml
validate_by_id:
  "io.material.catalog:id/cat_demo_text": # 元素的id
    '=': 'Hello world' # 校验符号或函数: 校验的值
```

2. validate_by_aid:
从当前页面中校验 accessibility_id 对应的元素的值
```yaml
validate_by_aid:
  "Timer": # 元素的accessibility_id
    '>': '2022-07-06 12:00:00' # 校验符号或函数: 校验的值
```

3. validate_by_class:
从当前页面中校验类名对应的元素的值
```yaml
validate_by_class:
  "android.widget.TextView": # 元素的类名
    '=': 'Hello world' # 校验符号或函数: 校验的值
```

4. validate_by_xpath: 
从当前页面或html响应中校验 xpath 路径对应的元素的值
```yaml
validate_by_xpath:
  "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout": # 元素的xpath路径
    '>': 0 # 校验符号或函数: 校验的值, 即 id 元素的值>0
  "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[2]/android.widget.LinearLayout":
    contains: 衬衫 # 即 title 元素的值包含'衬衫'
```

5. validate_by_css: 
从html响应中校验类名对应的元素的值
```yaml
validate_by_css:
  '#id': # 元素的css selector 模式
    '>': 0 # 校验符号或函数: 校验的值, 即 id 元素的值>0
  '#goods_title':
    contains: 衬衫 # 即 title 元素的值包含'衬衫'
```

6. validate_by_jsonpath: 
从json响应中校验 多层属性 的值
```yaml
validate_by_jsonpath:
  '$.data.goods_id':
     '>': 0 # 校验符号或函数: 校验的值, 即 id 元素的值>0
  '$.data.goods_title':
    contains: 衬衫 # 即 title 元素的值包含'衬衫'
```

#### 校验符号或函数
1. `=`: 相同
2. `>`: 大于
3. `<`: 小于
4. `>=`: 大于等于
5. `<=`: 小于等于
6. `contains`: 包含子串
7. `startswith`: 以子串开头
8. `endswith`: 以子串结尾
9. `regex_match`: 正则匹配

## 提取器
主要是为了从页面或响应中提取变量, 根据不同场景有2种写法
```
1. 针对当前页面, 那么提取器作为普通动作来写
2. 针对 get/post/upload 有发送http请求的动作, 那么提取器在动作内作为普通属性来写
```

不同校验器适用于不同场景
| 校验器 | 页面场景 | http请求场景 |
| ------------ | ------------ | ------------ |
| extract_by_id | Y | N |
| extract_by_aid | Y | N |
| extract_by_class | Y | N |
| extract_by_xpath | Y | Y |
| extract_by_jsonpath | N | Y |
| extract_by_css | N | Y |
| extract_by_eval | Y | Y |

1. extract_by_id:
从当前页面中解析 id 对应的元素的值
```yaml
extract_by_id:
  # 变量名: 元素id
  goods_id: "io.material.catalog:id/cat_demo_text"
```

2. extract_by_aid:
从当前页面中解析 accessibility_id 对应的元素的值
```yaml
extract_by_aid:
  # 变量名: 元素的accessibility_id
  update_time: "Timer"
```

3. extract_by_class:
从当前页面中解析类名对应的元素的值
```yaml
extract_by_class:
  # 变量名: 元素的accessibility_id
  name: "android.widget.TextView"
```

4. extract_by_xpath:
从当前页面或html响应中解析 xpath 路径指定的元素的值
```yaml
extract_by_xpath:
  # 变量名: xpath路径
  goods_id: /hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout
```

5. extract_by_css:
从html响应中解析 css selector 模式指定的元素的值
```yaml
extract_by_css:
  # 变量名: css selector 模式
  goods_id: table>tbody>tr:nth-child(1)>td:nth-child(1) # 第一行第一列
```

6. extract_by_jsonpath:
从json响应中解析 多层属性 的值
```yaml
extract_by_jsonpath:
  # 变量名: json响应的多层属性
  img: $.data.url
```

7. extract_by_eval:
使用 `eval(表达式)` 执行表达式, 并将执行结果记录到变量中
```yaml
extract_by_eval:
    # 变量名: 表达式（python语法）
    dyn_data: "json.loads(response.text[16:-1])" # 变量response是响应对象
```