import tkinter as tk
from tkinter import messagebox
from PIL import Image
import mss
import pyautogui

class ScreenshotTool:
    def __init__(self, root):
        self.root = root
        self.root.title("123截屏工具")  # 修改标题
        self.root.geometry("400x200")    # 增大窗口尺寸
        self.root.resizable(False, False)

        # 创建按钮
        self.fullscreen_btn = tk.Button(root, text="全屏截屏", command=self.capture_fullscreen, width=25, height=2)
        self.fullscreen_btn.pack(pady=15)

        self.region_btn = tk.Button(root, text="区域截屏", command=self.capture_region, width=25, height=2)
        self.region_btn.pack(pady=15)

        self.quit_btn = tk.Button(root, text="退出", command=root.quit, width=25, height=2)
        self.quit_btn.pack(pady=15)

    def capture_fullscreen(self):
        try:
            with mss.mss() as sct:
                monitor = sct.monitors[1]  # 0 是所有监视器，1 是第一个监视器
                img = sct.grab(monitor)
                img_pil = Image.frombytes("RGB", img.size, img.rgb)
                save_path = "fullscreen_screenshot.png"
                img_pil.save(save_path)
                messagebox.showinfo("截屏成功", f"全屏截屏已保存为 {save_path}")
        except Exception as e:
            messagebox.showerror("错误", f"截屏失败: {e}")

    def capture_region(self):
        # 隐藏主窗口
        self.root.withdraw()
        self.overlay = tk.Toplevel()
        self.overlay.attributes("-fullscreen", True)
        self.overlay.attributes("-alpha", 0.3)
        self.overlay.configure(bg='gray')

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas = tk.Canvas(self.overlay, cursor="cross", bg="grey")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        # 记录起始点
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        # 创建一个矩形
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_move_press(self, event):
        cur_x, cur_y = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        # 更新矩形
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        # 获取终点坐标
        end_x, end_y = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        # 计算区域坐标
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)
        self.overlay.destroy()

        # 显示主窗口
        self.root.deiconify()

        # 获取屏幕分辨率
        screen_width, screen_height = pyautogui.size()

        # 确保坐标在屏幕范围内
        x1 = max(0, min(x1, screen_width))
        y1 = max(0, min(y1, screen_height))
        x2 = max(0, min(x2, screen_width))
        y2 = max(0, min(y2, screen_height))

        width = x2 - x1
        height = y2 - y1

        if width == 0 or height == 0:
            messagebox.showwarning("警告", "选择区域的大小无效！")
            return

        try:
            with mss.mss() as sct:
                monitor = {"top": int(y1), "left": int(x1), "width": int(width), "height": int(height)}
                img = sct.grab(monitor)
                img_pil = Image.frombytes("RGB", img.size, img.rgb)
                save_path = "region_screenshot.png"
                img_pil.save(save_path)
                messagebox.showinfo("截屏成功", f"区域截屏已保存为 {save_path}")
        except Exception as e:
            messagebox.showerror("错误", f"截屏失败: {e}")

def main():
    root = tk.Tk()
    app = ScreenshotTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()
