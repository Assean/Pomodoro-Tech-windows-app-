import customtkinter as ctk
import time
import math

# 設定外觀與顏色主題
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PomodoroApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 視窗設定
        self.title("Manus 番茄鐘")
        self.geometry("400x500")
        self.resizable(False, False)

        # 計時器參數 (單位: 秒)
        self.WORK_TIME = 25 * 60
        self.SHORT_BREAK = 5 * 60
        self.LONG_BREAK = 15 * 60
        
        self.current_time = self.WORK_TIME
        self.timer_running = False
        self.mode = "Work" # "Work", "Short Break", "Long Break"
        self.timer_id = None

        # 介面配置
        self.setup_ui()

    def setup_ui(self):
        # 標題
        self.title_label = ctk.CTkLabel(self, text="專注時間", font=("Helvetica", 24, "bold"))
        self.title_label.pack(pady=20)

        # 計時器顯示
        self.timer_label = ctk.CTkLabel(self, text="25:00", font=("Helvetica", 64, "bold"))
        self.timer_label.pack(pady=20)

        # 進度條
        self.progress_bar = ctk.CTkProgressBar(self, width=300)
        self.progress_bar.set(1.0)
        self.progress_bar.pack(pady=10)

        # 控制按鈕區域
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=20)

        self.start_button = ctk.CTkButton(self.button_frame, text="開始", command=self.toggle_timer, width=100)
        self.start_button.grid(row=0, column=0, padx=10)

        self.reset_button = ctk.CTkButton(self.button_frame, text="重設", command=self.reset_timer, width=100, fg_color="gray")
        self.reset_button.grid(row=0, column=1, padx=10)

        # 模式切換按鈕區域
        self.mode_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.mode_frame.pack(pady=10)

        self.work_btn = ctk.CTkButton(self.mode_frame, text="工作", command=lambda: self.set_mode("Work"), width=80)
        self.work_btn.grid(row=0, column=0, padx=5)

        self.short_break_btn = ctk.CTkButton(self.mode_frame, text="短休", command=lambda: self.set_mode("Short Break"), width=80)
        self.short_break_btn.grid(row=0, column=1, padx=5)

        self.long_break_btn = ctk.CTkButton(self.mode_frame, text="長休", command=lambda: self.set_mode("Long Break"), width=80)
        self.long_break_btn.grid(row=0, column=2, padx=5)

        # 狀態標籤
        self.status_label = ctk.CTkLabel(self, text="準備好開始了嗎？", font=("Helvetica", 14))
        self.status_label.pack(pady=10)

    def set_mode(self, mode):
        self.stop_timer()
        self.mode = mode
        if mode == "Work":
            self.current_time = self.WORK_TIME
            self.title_label.configure(text="專注時間", text_color="#ff7b7b")
        elif mode == "Short Break":
            self.current_time = self.SHORT_BREAK
            self.title_label.configure(text="短暫休息", text_color="#7bff7b")
        elif mode == "Long Break":
            self.current_time = self.LONG_BREAK
            self.title_label.configure(text="長效休息", text_color="#7b7bff")
        
        self.update_timer_display()
        self.progress_bar.set(1.0)
        self.status_label.configure(text=f"已切換至 {mode} 模式")

    def update_timer_display(self):
        minutes = math.floor(self.current_time / 60)
        seconds = self.current_time % 60
        self.timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")

    def toggle_timer(self):
        if not self.timer_running:
            self.start_timer()
        else:
            self.pause_timer()

    def start_timer(self):
        self.timer_running = True
        self.start_button.configure(text="暫停", fg_color="#e67e22")
        self.status_label.configure(text="計時中...")
        self.run_timer()

    def pause_timer(self):
        self.timer_running = False
        self.start_button.configure(text="開始", fg_color=["#3B8ED0", "#1f538d"])
        self.status_label.configure(text="已暫停")
        if self.timer_id:
            self.after_cancel(self.timer_id)

    def stop_timer(self):
        self.timer_running = False
        self.start_button.configure(text="開始", fg_color=["#3B8ED0", "#1f538d"])
        if self.timer_id:
            self.after_cancel(self.timer_id)

    def reset_timer(self):
        self.stop_timer()
        self.set_mode(self.mode)

    def run_timer(self):
        if self.timer_running and self.current_time > 0:
            self.current_time -= 1
            self.update_timer_display()
            
            # 更新進度條
            total = self.WORK_TIME if self.mode == "Work" else (self.SHORT_BREAK if self.mode == "Short Break" else self.LONG_BREAK)
            self.progress_bar.set(self.current_time / total)
            
            self.timer_id = self.after(1000, self.run_timer)
        elif self.current_time == 0:
            self.timer_running = False
            self.start_button.configure(text="開始")
            self.status_label.configure(text="時間到！休息一下吧！")
            # 這裡可以加入音效提醒 (如果系統支援)
            self.bell() # 系統提示音

if __name__ == "__main__":
    app = PomodoroApp()
    app.mainloop()
