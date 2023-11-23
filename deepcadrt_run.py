"""
## 代码功能

批量进行降噪，custom_deepcad 对deepcadrt的输出文件夹进行了简化

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




"""
from custom_deepcad.test_collection import testing_class
from custom_deepcad.movie_display import display
from custom_deepcad.utils import get_first_filename, download_demo
import tkinter as tk
import os
from tkinter import filedialog


def main():
    # GUI choose  the path of datasets
    root = tk.Tk()
    root.withdraw()
    parent_folder_path = filedialog.askdirectory()  # Ask the user to select a folder
    if not parent_folder_path:
        print("\033[91m" + "No folder selected. Program is terminated. " + "\033[0m")
        return
    print("Choose Path:", parent_folder_path)

    # Get all subfolders
    subfolders = [
        f.path
        for f in os.scandir(parent_folder_path)
        if f.is_dir() and not f.name.endswith("_denoised")
    ]
    # If no subfolders, consider the parent folder for processing
    if not subfolders:
        datasets_path = parent_folder_path
        output_dir = os.path.join(
            os.path.dirname(parent_folder_path),
            os.path.basename(parent_folder_path) + "_denoised",
        )
        os.makedirs(output_dir, exist_ok=True)

        # Reg all tif files
        run_deepcad_rt(datasets_path, output_dir)
    else:
        # How many subfolders
        print("Subfolders:", subfolders, "\n", "Number of subfolders:", len(subfolders))
        for datasets_path in subfolders:
            # Create the output folder
            output_dir = os.path.join(
                os.path.dirname(parent_folder_path),
                os.path.basename(parent_folder_path) + "_denoised",
                os.path.basename(datasets_path),
            )
            os.makedirs(output_dir, exist_ok=True)

            # Reg all tif files
            run_deepcad_rt(datasets_path, output_dir)



def run_deepcad_rt(datasets_path, output_dir):
    # set model dir
    pth_dir = r"./pth"  # './pth'
    denoise_model = "deepcad_model"  # A folder containing pth models to be tested
    # the number of frames to be tested (test all frames if the number exceeds the total number of frames in a .tif file)
    test_datasize = 100000
    # the index of GPU you will use for computation (e.g. '0', '0,1', '0,1,2')
    GPU = "0"
    patch_xy = 150  # the width and height of 3D patches
    patch_t = 150  # the time dimension of 3D patches
    # the overlap factor between two adjacent patches.
    overlap_factor = 0.60
    # Since the receptive field of 3D-Unet is ~90, seamless stitching requires an overlap (patch_xyt*overlap_factor）of at least 90 pixels.
    # if you use Windows system, set this to 0.
    num_workers = 0

    # %% Setup some parameters for result visualization during testing period (optional)
    # choose whether to display inference performance after each epoch
    visualize_images_per_epoch = False
    # choose whether to save inference image after each epoch in pth path
    save_test_images_per_epoch = True

    ## ----------------------------------------- Parameter Settings --------------------------------------------##

    test_dict = {
        # dataset dependent parameters
        "patch_x": patch_xy,
        "patch_y": patch_xy,
        "patch_t": patch_t,
        "overlap_factor": overlap_factor,
        "scale_factor": 1,  # the factor for image intensity scaling
        "test_datasize": test_datasize,
        "datasets_path": datasets_path,
        "pth_dir": pth_dir,  # pth file root path
        "denoise_model": denoise_model,
        "output_dir": output_dir,  # result file root path
        # network related parameters
        "fmap": 16,  # the number of feature maps
        "GPU": GPU,
        "num_workers": num_workers,
        "visualize_images_per_epoch": visualize_images_per_epoch,
        "save_test_images_per_epoch": save_test_images_per_epoch,
    }
    # %%% Testing preparation
    # first we create a testing class object with the specified parameters
    tc = testing_class(test_dict)
    # start the testing process
    tc.run()


if __name__ == "__main__":
    main()
