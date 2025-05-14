from tkinter import *
from chat_for_gui import get_response, ai_bot_name
from style import AllStyles as Gui  # Make sure this includes the updated styles I gave you earlier


class ChatGUI:
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        self.window.iconbitmap("static/images/windows-bot-icon.ico")

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("TechTara.")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=520, height=640, bg=Gui.BG_COLOR)

        # Header label
        header_label = Label(
            self.window,
            bg=Gui.BG_COLOR,
            fg=Gui.TEXT_COLOR,
            text="🤖 TechTara | IT Academic Assistant",
            font=Gui.FONT_BOLD,
            pady=15
        )
        header_label.place(relwidth=1)

        # Divider line
        hr = Label(self.window, bg=Gui.BG_GRAY)
        hr.place(relwidth=1, rely=0.07, relheight=0.012)

        # Chat text area
        self.text_area = Text(
            self.window,
            bg=Gui.TEXT_INPUT,
            fg=Gui.TEXT_COLOR,
            font=Gui.FONT,
            padx=10,
            pady=10,
            wrap=WORD,
            border=0
        )
        self.text_area.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_area.configure(cursor="arrow", state=DISABLED)

        # Scrollbar
        scrollbar = Scrollbar(self.text_area)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_area.yview)

        # Footer frame
        footer = Frame(self.window, bg=Gui.BG_COLOR, height=60)
        footer.place(relwidth=1, rely=0.825, relheight=0.175)

        # Message input field
        self.usr_msg = Entry(
            master=footer,
            bg=Gui.TEXT_INPUT,
            fg=Gui.TEXT_COLOR,  # Should be black
            font=Gui.FONT,
            bd=0,
            insertbackground="black",  # Changed from yellow to black
            relief="flat"
        )
        self.usr_msg.place(
            relx=0.02,
            rely=0.1,
            relwidth=0.74,
            relheight=0.4
        )
        self.usr_msg.focus()
        self.usr_msg.bind("<Return>", self._enter_key_pressed)

        send_btn = Button(
            master=footer,
            text="Send",
            font=Gui.FONT_SEND,
            bg=Gui.BG_GRAY,
            fg=Gui.TEXT_COLOR,
            activebackground="#3E4A5A",
            activeforeground="white",
            command=lambda: self._enter_key_pressed(None),
            padx=12,
            pady=6,
            bd=0,
            relief="flat",
            cursor="hand2"
        )

        send_btn.place(relx=0.78, rely=0.09, relwidth=0.2, relheight=0.42)

    def _enter_key_pressed(self, event):
        msg = self.usr_msg.get()
        self._insert_message(msg, "You")

    def _insert_message(self, msg, sender):
        if not msg:
            return

        self.text_area.tag_config('send_color', foreground="#04168c")
        self.text_area.tag_config('reply_color', foreground="#0a0000")  # golden yellow

        self.usr_msg.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_area.configure(state=NORMAL)
        self.text_area.insert(END, msg1, "send_color")
        self.text_area.configure(state=DISABLED)

        msg2 = f"{ai_bot_name}: {get_response(msg)}\n\n"
        self.text_area.configure(state=NORMAL)
        self.text_area.insert(END, msg2, "reply_color")
        self.text_area.configure(state=DISABLED)

        self.text_area.see(END)


if __name__ == "__main__":
    app = ChatGUI()
    app.run()
