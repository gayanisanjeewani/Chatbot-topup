from tkinter import *
from chat_for_gui import get_response, ai_bot_name
from style import AllStyles as Gui


class ChatGUI:
    def __init__(self):
        self.window = Tk()  # top level widget
        self._setup_main_window()  # helper function

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("First Aid Guide")  # window title
        self.window.resizable(width=False, height=False)  # prevent resizing
        self.window.configure(width=520, height=640, bg=Gui.BG_COLOR)  # window attributes

        # header label
        header_label = Label(self.window, bg=Gui.BG_COLOR, fg=Gui.TEXT_COLOR, text="A.I. First AID Assistant",
                             font=Gui.FONT_BOLD, pady=10)
        header_label.place(relwidth=1)

        # tiny divider
        hr = Label(self.window, width=500, bg=Gui.BG_GRAY)
        hr.place(relwidth=1, rely=0.07, relheight=0.012)

        # text area
        self.text_area = Text(self.window, width=20, height=2, bg=Gui.TEXT_INPUT, fg=Gui.TEXT_COLOR,
                              font=Gui.FONT, padx=5, pady=5, border=0)
        self.text_area.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_area.configure(cursor="arrow", state=DISABLED)

        # text area scroll bar
        scrollbar = Scrollbar(self.text_area)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_area.yview())

        # footer label
        footer_label = Label(self.window, bg=Gui.BG_COLOR, height=80)
        footer_label.place(relwidth=1, rely=0.825)

        # message text box
        self.usr_msg = Entry(footer_label, bg=Gui.BG_COLOR, fg=Gui.TEXT_COLOR, font=Gui.FONT, border=0,
                             insertbackground="yellow")
        self.usr_msg.place(relwidth=0.98, relheight=0.042, relx=0.02)
        self.usr_msg.focus()
        self.usr_msg.bind("<Return>", self._enter_key_pressed)

        # send button
        send_btn = Button(footer_label, text="S E N D", font=Gui.FONT_SEND, width=50, height=2, bg=Gui.BG_GRAY,
                          command=lambda: self._enter_key_pressed(None))
        send_btn.place(relx=0.005, rely=0.045)

    def _enter_key_pressed(self, event):
        msg = self.usr_msg.get()
        self._insert_message(msg, "You")

    def _insert_message(self, msg, sender):
        if not msg:
            return

        self.text_area.tag_config('send_color', foreground="white")
        self.text_area.tag_config('reply_color', foreground="yellow")

        self.usr_msg.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_area.configure(state=NORMAL)
        self.text_area.insert(END, msg1, "send_color")
        self.text_area.configure(state=DISABLED)

        msg2 = f"{ai_bot_name}: {get_response(msg)}\n\n"
        self.text_area.configure(state=NORMAL)
        self.text_area.insert(END, msg2, "reply_color")
        self.text_area.configure(state=DISABLED)

        self.text_area.see(END)  # scroll to end


if __name__ == "__main__":
    app = ChatGUI()
    app.run()
