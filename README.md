## 代码功能

批量对钙成像数据降噪，降噪前建议先进行配准。降噪模块使用的是 [deepcadrt](https://github.com/cabooster/DeepCAD-RT)。
> custom_deepcad 模块 对deepcadrt的输出文件夹进行了简化

## 运行代码

运行条件：可以直接复制本文件夹到任意文件夹下，只需要电脑配有deepcadrt环境即可

运行方式
1. 在命令行中运行：
    1. 进入本文件夹，在文件夹路径输入 `cmd` 打开终端
    2. 输入 `conda activate deepcadrt`，激活 conda 环境
    3. 运动代码 `python deepcadrt_rt.py`
2. 双击 `deepcadrt_rt.sh`
3. 在pycharm/VSCode中，选择 conda 环境后，直接运行本文件

## 运行成功

弹出弹窗，选择包含tif文件的文件夹，进行降噪

## 运行结果

1. 如果选择的文件夹下，有多个子文件夹，那么会对每个子文件夹进行降噪
2. 如果选择的文件夹下，没有子文件夹，那么会对该文件夹下的所有tif文件进行降噪
3. 降噪后的文件会保存在选择的文件夹下的同级目录下，文件夹名为：选择的文件夹名_denoised




