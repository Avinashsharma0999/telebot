import os  
import tkinter as tk  
from tkinter import messagebox, scrolledtext  
from telethon.sync import TelegramClient  
from telethon.tl.functions.channels import InviteToChannelRequest  
import asyncio  
import random  
import threading  

class TelegramMemberAdder:  
    def __init__(self, root):  
        self.root = root  
        self.root.title("Telegram Member Adder - Hacking UI")  
        self.root.configure(bg='black')  
        
        # Create a main frame  
        self.main_frame = tk.Frame(root, bg='black')  
        self.main_frame.pack(padx=10, pady=10)  

        self.init_ui()  

        self.loop = asyncio.new_event_loop()  
        self.loop_thread = threading.Thread(target=self.run_loop, daemon=True)  
        self.loop_thread.start()  

        self.stop_flag = False  # Flag to stop the process  

        # Ensure cleanup when the window is closed  
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  

    def init_ui(self):  
        label_style = {'bg': 'black', 'fg': 'green', 'font': ('Courier New', 12)}  
        entry_style = {'bg': 'black', 'fg': 'green', 'insertbackground': 'green', 'font': ('Courier New', 12)}  

        # API Credentials  
        tk.Label(self.main_frame, text="API ID:", **label_style).grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)  
        self.api_id_entry = tk.Entry(self.main_frame, **entry_style)  
        self.api_id_entry.grid(row=0, column=1, padx=10, pady=5)  
        self.api_id_entry.insert(0, "24803360")  

        tk.Label(self.main_frame, text="API Hash:", **label_style).grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)  
        self.api_hash_entry = tk.Entry(self.main_frame, **entry_style)  
        self.api_hash_entry.grid(row=1, column=1, padx=10, pady=5)  
        self.api_hash_entry.insert(0, "9f59779edaa8d813c57e36d24be29779")  

        # Source and Target Groups  
        tk.Label(self.main_frame, text="Source Group:", **label_style).grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)  
        self.source_group_entry = tk.Entry(self.main_frame, **entry_style)  
        self.source_group_entry.grid(row=2, column=1, padx=10, pady=5)  

        tk.Label(self.main_frame, text="Target Group:", **label_style).grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)  
        self.target_group_entry = tk.Entry(self.main_frame, **entry_style)  
        self.target_group_entry.grid(row=3, column=1, padx=10, pady=5)  

        # Delay Options  
        tk.Label(self.main_frame, text="Min Delay (sec):", **label_style).grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)  
        self.min_delay_entry = tk.Entry(self.main_frame, **entry_style)  
        self.min_delay_entry.grid(row=4, column=1, padx=10, pady=5)  

        tk.Label(self.main_frame, text="Max Delay (sec):", **label_style).grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)  
        self.max_delay_entry = tk.Entry(self.main_frame, **entry_style)  
        self.max_delay_entry.grid(row=5, column=1, padx=10, pady=5)  

        # Member Selection Options  
        self.random_order_var = tk.BooleanVar()  
        self.random_order_checkbox = tk.Checkbutton(self.main_frame, text="Random Order", variable=self.random_order_var,  
                                                     bg='black', fg='green', font=('Courier New', 12), selectcolor='black')  
        self.random_order_checkbox.grid(row=6, column=0, columnspan=2, pady=5, sticky=tk.W)  

        tk.Label(self.main_frame, text="Member Range (e.g. 10-50):", **label_style).grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)  
        self.range_entry = tk.Entry(self.main_frame, **entry_style)  
        self.range_entry.grid(row=7, column=1, padx=10, pady=5)  

        # Status Display  
        tk.Label(self.main_frame, text="Log:", **label_style).grid(row=8, column=0, padx=10, pady=10, sticky=tk.W)  
        self.status_text = scrolledtext.ScrolledText(self.main_frame, height=10, width=50, bg='black', fg='green', font=('Courier New', 12), state='normal')  
        self.status_text.grid(row=9, column=0, columnspan=2, padx=10, pady=5)  

        # Buttons  
        self.start_button = tk.Button(self.main_frame, text="Start Adding", command=self.confirm_start,  
                                       bg='green', fg='black', font=('Courier New', 12))  
        self.start_button.grid(row=10, column=0, padx=10, pady=10)  

        self.stop_button = tk.Button(self.main_frame, text="Stop Adding", command=self.confirm_stop,  
                                      bg='red', fg='white', font=('Courier New', 12))  
        self.stop_button.grid(row=10, column=1, padx=10, pady=10)  

    def run_loop(self):  
        asyncio.set_event_loop(self.loop)  
        self.loop.run_forever()  

    def validate_inputs(self):  
        try:  
            int(self.api_id_entry.get())  
            assert len(self.api_hash_entry.get()) > 0  
            assert len(self.source_group_entry.get()) > 0  
            assert len(self.target_group_entry.get()) > 0  
            int(self.min_delay_entry.get())  
            int(self.max_delay_entry.get())  
            return True  
        except:  
            return False  

    def confirm_start(self):  
        if messagebox.askyesno("Confirm Start", "Do you want to start adding members?"):  
            self.start_adding()  

    def confirm_stop(self):  
        if messagebox.askyesno("Confirm Stop", "Do you want to stop adding members?"):  
            self.stop_adding()  

    def start_adding(self):  
        if not self.validate_inputs():  
            messagebox.showerror("Error", "Invalid inputs. Please check your values!")  
            return  

        self.stop_flag = False  # Reset stop flag  

        # Get user inputs  
        api_id = int(self.api_id_entry.get())  
        api_hash = self.api_hash_entry.get()  
        source_group = self.source_group_entry.get()  
        target_group = self.target_group_entry.get()  
        min_delay = int(self.min_delay_entry.get())  
        max_delay = int(self.max_delay_entry.get())  
        random_order = self.random_order_var.get()  
        member_range = self.range_entry.get()  

        # Parse member range  
        range_start, range_end = None, None  
        if "-" in member_range:  
            parts = member_range.split("-")  
            range_start, range_end = int(parts[0]), int(parts[1])  

        # Schedule the async task on the running event loop  
        asyncio.run_coroutine_threadsafe(  
            self.copy_members(api_id, api_hash, source_group, target_group, min_delay, max_delay, random_order, range_start, range_end),  
            self.loop  
        )  

    async def copy_members(self, api_id, api_hash, source_group, target_group, min_delay, max_delay, random_order, range_start, range_end):  
        try:  
            async with TelegramClient('session_name', api_id, api_hash) as client:  
                await client.start()  
                members = await client.get_participants(source_group)  

                self.update_status(f'Starting to fetch members from {source_group}. Found {len(members)} members.')  
                print(f'Starting to fetch members from {source_group}. Found {len(members)} members.')  

                if random_order:  
                    random.shuffle(members)  

                if range_start is not None and range_end is not None:  
                    members = members[range_start:range_end]  

                added_count = 0  # Counter for added members  

                for user in members:  
                    if self.stop_flag:  
                        self.update_status("Stopping process...")  
                        print("Stopping process...")  
                        break  

                    try:  
                        if not user.bot:  
                            await client(InviteToChannelRequest(target_group, [user.id]))  
                            added_count += 1  
                            self.update_status(f'Added member number {added_count}')  
                        else:  
                            self.update_status(f'Skipping bot: {user.username or user.id}')  
                    except Exception as e:  
                        print(f'Error adding {user.username or user.id}: {str(e)}')  

                    # Delay occurs regardless of whether a member was added or skipped  
                    delay = random.randint(min_delay, max_delay)  
                    self.update_status(f'Waiting {delay} seconds before next attempt...')  
                    print(f'Waiting {delay} seconds before next attempt...')  
                    await asyncio.sleep(delay)  

        except Exception as e:  
            print(f"An error occurred: {str(e)}")  

    def stop_adding(self):  
        self.stop_flag = True  

    def on_close(self):  
        self.stop_flag = True  
        self.loop.call_soon_threadsafe(self.loop.stop)  
        self.loop_thread.join(timeout=1)  
        self.root.destroy()  

    def update_status(self, message):  
        """Update the status text area with a new message."""  
        self.status_text.configure(state='normal')  # Allow editing  
        self.status_text.insert(tk.END, message + "\n")  
        self.status_text.see(tk.END)  # Scroll to the bottom  
        self.status_text.configure(state='disabled')  # Prevent editing  

if __name__ == "__main__":  
    root = tk.Tk()  
    app = TelegramMemberAdder(root)  
    root.mainloop()