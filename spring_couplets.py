import requests
import tkinter as tk
from tkinter import font, messagebox, ttk
import os
from datetime import datetime
import json
import random
import math

class APISettingsDialog:
    def __init__(self, parent, current_api_key=""):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("API设置")
        self.dialog.geometry("500x200")
        self.dialog.resizable(False, False)
        
        # 设置模态
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # 设置背景色
        self.dialog.configure(bg='#990000')
        
        # 创建内容框架
        content_frame = tk.Frame(self.dialog, bg='#990000', padx=20, pady=20)
        content_frame.pack(expand=True, fill='both')
        
        # API密钥标签和输入框
        tk.Label(
            content_frame,
            text="请输入Deepseek API密钥：",
            font=("Microsoft YaHei", 12),
            bg='#990000',
            fg='#FFD700'
        ).pack(pady=(0, 10))
        
        self.api_entry = tk.Entry(
            content_frame,
            font=("Microsoft YaHei", 12),
            width=40,
            bg='white',
            fg='black'
        )
        self.api_entry.pack(pady=(0, 20))
        self.api_entry.insert(0, current_api_key)
        
        # 按钮框架
        button_frame = tk.Frame(content_frame, bg='#990000')
        button_frame.pack(pady=(0, 10))
        
        # 保存按钮
        tk.Button(
            button_frame,
            text="保存",
            command=self.save,
            font=("Microsoft YaHei", 12),
            bg='#FFD700',
            fg='#990000',
            width=10,
            relief='raised'
        ).pack(side='left', padx=10)
        
        # 取消按钮
        tk.Button(
            button_frame,
            text="取消",
            command=self.dialog.destroy,
            font=("Microsoft YaHei", 12),
            bg='#FFD700',
            fg='#990000',
            width=10,
            relief='raised'
        ).pack(side='left', padx=10)
        
        self.result = None
        
    def save(self):
        self.result = self.api_entry.get().strip()
        self.dialog.destroy()

class RoundedFrame(tk.Canvas):
    def __init__(self, parent, bg_color, border_color, corner_radius=25, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.bg_color = bg_color
        self.border_color = border_color
        self.corner_radius = corner_radius
        
        self.bind('<Configure>', self._draw_rounded_frame)
        
    def _draw_rounded_frame(self, event=None):
        self.delete('all')
        width = self.winfo_width()
        height = self.winfo_height()
        
        # 绘制渐变背景
        gradient_steps = 50
        for i in range(gradient_steps):
            # 计算渐变色
            ratio = i / gradient_steps
            r1 = int(0x99 * (1 - ratio) + 0x80 * ratio)
            r2 = int(0x00 * (1 - ratio) + 0x00 * ratio)
            r3 = int(0x00 * (1 - ratio) + 0x00 * ratio)
            color = f'#{r1:02x}{r2:02x}{r3:02x}'
            
            # 绘制渐变矩形
            y1 = height * i / gradient_steps
            y2 = height * (i + 1) / gradient_steps
            self.create_rectangle(0, y1, width, y2, fill=color, outline=color)
        
        # 绘制细边框
        self.create_rounded_rectangle(1, 1, width-2, height-2, 
                                    self.corner_radius, 
                                    outline=self.border_color,
                                    width=1)  # 减小边框宽度
        
        # 绘制装饰性花纹
        self.draw_decorations(width, height)
    
    def draw_decorations(self, width, height):
        # 绘制四角装饰
        corner_size = 40
        margin = 10
        
        # 左上角装饰
        self.create_corner_decoration(margin, margin, corner_size, 0)
        # 右上角装饰
        self.create_corner_decoration(width-margin-corner_size, margin, corner_size, 90)
        # 左下角装饰
        self.create_corner_decoration(margin, height-margin-corner_size, corner_size, 270)
        # 右下角装饰
        self.create_corner_decoration(width-margin-corner_size, height-margin-corner_size, corner_size, 180)
    
    def create_corner_decoration(self, x, y, size, rotation):
        # 创建中国风角落装饰
        points = []
        steps = 8
        for i in range(steps):
            angle = (i * 360 / steps + rotation) * 3.14159 / 180
            r = size * (0.5 + 0.3 * (i % 2))  # 创建不规则的花形
            px = x + size/2 + r * 0.5 * math.cos(angle)
            py = y + size/2 + r * 0.5 * math.sin(angle)
            points.extend([px, py])
        
        self.create_polygon(points, fill="", outline=self.border_color, width=1, smooth=True)
        
        # 添加内部装饰
        inner_size = size * 0.6
        inner_points = []
        for i in range(steps):
            angle = (i * 360 / steps + rotation + 22.5) * 3.14159 / 180
            r = inner_size * (0.5 + 0.3 * (i % 2))
            px = x + size/2 + r * 0.5 * math.cos(angle)
            py = y + size/2 + r * 0.5 * math.sin(angle)
            inner_points.extend([px, py])
        
        self.create_polygon(inner_points, fill="", outline=self.border_color, width=1, smooth=True)

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, width=120, height=40, corner_radius=10, bg='#DAA520', fg='#990000', font=None):
        super().__init__(parent, width=width, height=height, bg=parent['bg'], highlightthickness=0)
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.bg = bg
        self.fg = fg
        self.text = text
        self.font = font
        self.command = command
        self.is_pressed = False
        
        # 绘制初始状态
        self.draw_button()
        
        # 绑定事件
        self.bind('<Button-1>', self.on_press)
        self.bind('<ButtonRelease-1>', self.on_release)
        
    def draw_button(self, scale=1.0):
        self.delete('all')
        width = int(self.width * scale)
        height = int(self.height * scale)
        x_offset = (self.width - width) // 2
        y_offset = (self.height - height) // 2
        
        # 创建圆角矩形
        self.create_rounded_rect(
            x_offset + 1,
            y_offset + 1,
            x_offset + width - 2,
            y_offset + height - 2,
            int(self.corner_radius * scale),
            fill=self.bg,
            outline=self.bg
        )
        
        # 创建文本
        if isinstance(self.font, str):
            font_family = self.font
            font_size = 12
        else:
            font_family = self.font[0] if isinstance(self.font, tuple) else self.font.actual('family')
            font_size = self.font[1] if isinstance(self.font, tuple) else self.font.actual('size')
        
        scaled_font = (font_family, int(font_size * scale))
        self.create_text(
            self.width // 2,
            self.height // 2,
            text=self.text,
            fill=self.fg,
            font=scaled_font
        )
    
    def on_press(self, event):
        if not self.is_pressed:
            self.is_pressed = True
            self.draw_button(scale=1.1)  # 放大5%
            
    def on_release(self, event):
        if self.is_pressed:
            self.is_pressed = False
            self.draw_button(scale=1.0)  # 恢复原始大小
            self.command()  # 执行命令
        
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

class CoupletDisplay:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("新春春联生成器")
        
        # 尝试加载保存的API密钥
        self.api_key = self.load_api_key()
        
        # 设置窗口大小和位置
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = 1200
        window_height = 1000
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 设置颜色
        self.bg_color = '#990000'  # 更深的红色
        self.border_color = '#DAA520'  # 使用 goldenrod 金黄色
        self.text_color = '#000000'  # 黑色
        self.explanation_color = '#CD9B1D'  # 使用稍暗的金黄色作为解释文字颜色
        self.window.configure(bg='#800000')  # 设置窗口背景为深红色
        
        # 创建圆角主容器
        self.outer_frame = RoundedFrame(
            self.window,
            bg_color=self.bg_color,
            border_color=self.border_color,
            corner_radius=35,
            highlightthickness=0,
            bd=0
        )
        self.outer_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        # 创建主框架
        main_frame = tk.Frame(self.outer_frame, bg=self.bg_color)
        main_frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
        
        # 添加水印
        watermark = tk.Label(
            main_frame,
            text="Created by @Travisma2233",
            font=("Microsoft YaHei", 10),
            bg=self.bg_color,
            fg=self.explanation_color,
            cursor="hand2"  # 鼠标悬停时显示手型
        )
        watermark.pack(side='bottom', pady=5)
        watermark.bind("<Button-1>", lambda e: self.open_github())
        
        # 创建标题
        title_frame = tk.Frame(main_frame, bg=self.bg_color)
        title_frame.pack(fill='x', pady=(10, 20))
        
        title_label = tk.Label(
            title_frame,
            text="✨ 新春春联生成器 ✨",
            font=("华文行楷", 32, "bold"),
            bg=self.bg_color,
            fg=self.border_color
        )
        title_label.pack(side='left', padx=20)
        
        # 创建设置按钮
        settings_button = RoundedButton(
            title_frame,
            text="⚙️ API设置",
            command=self.show_api_settings,
            width=120,
            height=35,
            corner_radius=17,
            bg=self.border_color,
            fg=self.bg_color,
            font=("Microsoft YaHei", 12)
        )
        settings_button.pack(side='right', padx=20)
        
        # 创建不同大小的字体
        try:
            font_names = ['华文行楷', '方正舒体', '华文楷体', 'Microsoft YaHei']
            self.font_name = next(name for name in font_names if name in font.families())
        except StopIteration:
            self.font_name = 'Microsoft YaHei'
        
        self.horizontal_font = font.Font(family=self.font_name, size=48, weight="bold")
        self.couplet_font = font.Font(family=self.font_name, size=36, weight="bold")
        # 使用楷体作为解释文字的字体
        try:
            explanation_font_name = next(name for name in ['楷体', '华文楷体', 'Microsoft YaHei'] if name in font.families())
        except StopIteration:
            explanation_font_name = 'Microsoft YaHei'
        self.explanation_font = font.Font(family=explanation_font_name, size=18)
        
        # 创建内容主框架
        content_main = tk.Frame(main_frame, bg=self.bg_color)
        content_main.pack(expand=True, fill='both')
        
        # 创建横批框架
        horizontal_frame = tk.Frame(content_main, bg=self.bg_color)
        horizontal_frame.pack(pady=(20, 40))
        
        self.horizontal_label = tk.Label(
            horizontal_frame,
            text="",
            font=self.horizontal_font,
            bg=self.bg_color,
            fg=self.text_color
        )
        self.horizontal_label.pack()
        
        # 创建对联主框架
        couplets_main_frame = tk.Frame(content_main, bg=self.bg_color)
        couplets_main_frame.pack(expand=True, fill='both', padx=20)
        
        # 左边的上联部分
        left_side = tk.Frame(couplets_main_frame, bg=self.bg_color)
        left_side.pack(side='left', expand=True)
        
        # 上联容器
        self.upper_labels = []
        self.upper_container = tk.Frame(left_side, bg=self.bg_color)
        self.upper_container.pack(pady=(0, 20))
        
        # 创建固定高度的容器来放置上联解释文字
        upper_text_container = tk.Frame(left_side, bg=self.bg_color)
        upper_text_container.pack(fill='both', expand=True)
        
        # 上联解释
        self.upper_explanation = tk.Label(
            upper_text_container,
            text="",
            font=self.explanation_font,
            bg=self.bg_color,
            fg=self.explanation_color,
            wraplength=350,  # 减小文本宽度以适应显示
            justify='left',
            anchor='nw'  # 文本左上对齐
        )
        self.upper_explanation.pack(fill='both', expand=True, padx=10)
        
        # 右边的下联部分
        right_side = tk.Frame(couplets_main_frame, bg=self.bg_color)
        right_side.pack(side='right', expand=True)
        
        # 下联容器
        self.lower_labels = []
        self.lower_container = tk.Frame(right_side, bg=self.bg_color)
        self.lower_container.pack(pady=(0, 20))
        
        # 创建固定高度的容器来放置下联解释文字
        lower_text_container = tk.Frame(right_side, bg=self.bg_color)
        lower_text_container.pack(fill='both', expand=True)
        
        # 下联解释
        self.lower_explanation = tk.Label(
            lower_text_container,
            text="",
            font=self.explanation_font,
            bg=self.bg_color,
            fg=self.explanation_color,
            wraplength=350,  # 减小文本宽度以适应显示
            justify='left',
            anchor='nw'  # 文本左上对齐
        )
        self.lower_explanation.pack(fill='both', expand=True, padx=10)
        
        # 添加生成按钮
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(side='bottom', pady=20)
        
        generate_button = RoundedButton(
            button_frame,
            text="生成新春联",
            command=self.generate_couplets,
            width=160,
            height=50,
            corner_radius=25,
            bg=self.border_color,
            fg=self.bg_color,
            font=(self.font_name, 18)
        )
        generate_button.pack()

    def display_vertical_text(self, text, container, labels_list):
        # 清除现有的标签
        for label in labels_list:
            label.destroy()
        labels_list.clear()
        
        # 为每个字创建新的标签
        for char in text:
            label = tk.Label(
                container,
                text=char,
                font=self.couplet_font,
                bg=self.bg_color,
                fg=self.text_color,
                pady=5  # 字符间距
            )
            label.pack()
            labels_list.append(label)

    def parse_couplets(self, text):
        """解析API返回的文本，提取春联内容和解释"""
        lines = text.strip().split('\n')
        upper, lower, horizontal = "", "", ""
        upper_exp, lower_exp = "", ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if '上联：' in line:
                upper = line.split('上联：')[-1].strip()
            elif '下联：' in line:
                lower = line.split('下联：')[-1].strip()
            elif '横批：' in line:
                horizontal = line.split('横批：')[-1].strip()
            elif '上联解释：' in line:
                upper_exp = line.split('上联解释：')[-1].strip()
            elif '下联解释：' in line:
                lower_exp = line.split('下联解释：')[-1].strip()
        
        return upper, lower, horizontal, upper_exp, lower_exp

    def show_api_settings(self):
        dialog = APISettingsDialog(self.window, self.api_key)
        self.window.wait_window(dialog.dialog)
        if dialog.result is not None:
            self.api_key = dialog.result
            self.save_api_key(dialog.result)

    def save_api_key(self, api_key):
        """保存API密钥到配置文件"""
        if not api_key:
            messagebox.showwarning("警告", "请输入API密钥")
            return
            
        config = {'api_key': api_key}
        try:
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f)
            messagebox.showinfo("成功", "API密钥已保存")
        except Exception as e:
            messagebox.showerror("错误", f"保存API密钥失败：{str(e)}")

    def load_api_key(self):
        """从配置文件加载API密钥"""
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('api_key', '')
        except:
            return ''

    def generate_couplets(self):
        # 获取当前输入的API密钥
        api_key = self.api_key
        if not api_key:
            messagebox.showwarning("警告", "请先输入Deepseek API密钥")
            return
            
        url = "https://api.deepseek.com/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 生成一些随机主题词，增加多样性
        themes = [
            "新春佳节，万象更新", "阖家欢乐，事业有成",
            "福禄双至，五福临门", "四季平安，万事如意",
            "春回大地，万物复苏", "喜迎新春，万事顺遂",
            "金玉满堂，家和业兴", "龙腾虎跃，吉星高照",
            "瑞雪丰年，国泰民安", "春满乾坤，福寿康宁",
            "花开富贵，岁岁平安", "风调雨顺，五谷丰登",
            "春暖花开，前程似锦", "岁月静好，幸福安康",
            "云程发轫，鸿运高照", "春华秋实，百业兴旺",
            "锦绣前程，万事亨通", "春意盎然，吉祥如意",
            "和风细雨，丰收在望", "紫气东来，万事大吉",
            "春色满园，欢乐祥和", "金玉满堂，喜气盈门",
            "春光明媚，事业腾达", "四海升平，百福骈臻",
            "春和景明，百业俱兴", "瑞气盈门，百事亨通"
        ]
        
        # 生成一些随机风格词
        styles = [
            "典雅祥和", "欢快喜庆", "大气磅礴",
            "文雅隽永", "吉祥如意", "富贵吉庆",
            "清新雅致", "庄重大方", "灵动飘逸",
            "古朴典雅", "优雅脱俗", "喜气洋洋"
        ]
        
        # 随机选择主题和风格
        selected_theme = random.choice(themes)
        selected_style = random.choice(styles)
        
        # 随机选择生成策略
        strategies = [
            f'请以"{selected_theme}"为主题，生成一副{selected_style}的春联，要求对仗工整，意境优美。',
            f'以"{selected_theme}"为背景，创作一副富有{selected_style}韵味的春联。',
            f'围绕"{selected_theme}"的意境，写一副体现{selected_style}特色的春联。',
            f'基于"{selected_theme}"的美好寓意，创作一副{selected_style}的新春对联。',
            f'以"{selected_theme}"为核心，写一副具有{selected_style}格调的春联。'
        ]
        
        prompt = random.choice(strategies)
        
        data = {
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个专门创作春联的AI助手。请生成一副传统新年春联，要求：\n1. 必须包含上联、下联和横批\n2. 对上下联分别进行简短解释\n3. 横批必须4个字\n4. 上下联字数相等且工整对仗\n5. 要求内容新颖独特，避免使用常见的春联用语\n\n请严格按照以下格式返回：\n上联：[上联内容]\n上联解释：[解释内容]\n下联：[下联内容]\n下联解释：[解释内容]\n横批：[横批内容]"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "model": "deepseek-chat",
            "temperature": 1.0,  # 增加随机性
            "top_p": 0.95,
            "presence_penalty": 0.8,
            "frequency_penalty": 0.8,
            "max_tokens": 500
        }
        
        try:
            # 显示正在生成的提示
            self.horizontal_label.config(text="⋯⋯")
            self.display_vertical_text("正在生成", self.upper_container, self.upper_labels)
            self.upper_explanation.config(text="")
            self.display_vertical_text("请稍候", self.lower_container, self.lower_labels)
            self.lower_explanation.config(text="")
            self.window.update()
            
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"使用主题：{selected_theme}")
            print(f"使用风格：{selected_style}")
            print(f"使用提示：{prompt}")
            print("API返回内容：", content)
            
            upper, lower, horizontal, upper_exp, lower_exp = self.parse_couplets(content)
            print(f"解析结果：\n横批：{horizontal}\n上联：{upper}\n下联：{lower}\n上联解释：{upper_exp}\n下联解释：{lower_exp}")
            
            if all([upper, lower, horizontal]):
                self.horizontal_label.config(text=horizontal)
                self.display_vertical_text(upper, self.upper_container, self.upper_labels)
                self.upper_explanation.config(text=upper_exp)
                self.display_vertical_text(lower, self.lower_container, self.lower_labels)
                self.lower_explanation.config(text=lower_exp)
            else:
                raise ValueError("春联格式不完整，请重试")
            
        except requests.exceptions.Timeout:
            messagebox.showerror("错误", "网络请求超时，请重试")
            self.reset_labels()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("错误", f"网络连接错误：{str(e)}")
            self.reset_labels()
        except Exception as e:
            messagebox.showerror("错误", f"生成春联时出错：{str(e)}")
            self.reset_labels()

    def reset_labels(self):
        """重置标签显示"""
        self.horizontal_label.config(text="")
        self.display_vertical_text("", self.upper_container, self.upper_labels)
        self.upper_explanation.config(text="")
        self.display_vertical_text("", self.lower_container, self.lower_labels)
        self.lower_explanation.config(text="")

    def open_github(self):
        """打开GitHub主页"""
        import webbrowser
        webbrowser.open("https://github.com/Travisma2233")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = CoupletDisplay()
    app.run() 