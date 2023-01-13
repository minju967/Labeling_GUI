from tkinter import * 
from PIL import Image, ImageTk
from functools import partial
import tkinter.font as font
import pandas as pd
import os
import glob
import argparse

window = Tk()
window.geometry("1000x600")        # window size
col = ['Idx', 'Name', 'A', 'HSM', 'C', 'Cut', 'Wire', 'None', 'Path', 'Labeled']
 
class GUI(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.button_list    = []
        self.base_btn_list  = []
        self.state          = [False] * 8
        self.df             = None
        self.img_index      = 0
        self.last_idx       = 0
        self.img_list       = self.call_img_list()
        self.GUI_font       = font.Font(family='맑은 고딕')   
        self.label          = Button(window, text='', width=5, height=3)
        self.button         = ['Preview', 'A', 'HSM', 'C', 'Cut', 'Wire', 'None', 'Next']
        self.btn_clr        = ['#4444f2', '#65eb34', '#65eb34', '#65eb34', '#f2aa44', '#f2aa44', '#f2aa44', '#4444f2']
        
        self.create_DF()
        self.app_base()
        self.app_outline()

    def call_img_list(self):
        all_images = []

        train_images = glob.glob('D:\\IMAGE\\Python_IMAGE_DEPTH_COLOR\\Train'+'\\'+'*.png')
        test_images = glob.glob('D:\\IMAGE\\Python_IMAGE_DEPTH_COLOR\\Test'+'\\'+'*.png')
        
        for img in train_images:
            if '_005.png' in img or '_009.png' in img:
                pass
            else:
                all_images.append(img)

        for img in test_images:
            if '_005.png' in img or '_009.png' in img:
                pass
            else:
                all_images.append(img)
        
        print('='*30)
        print(f'\nThe Number of total image data: {len(all_images)}\n')        
        print('='*30)

        return all_images

    def create_DF(self):
        if os.path.exists(".\\labeled_data.csv"):
            data = pd.read_csv(".\\labeled_data.csv")
            self.last_idx   = data.iloc[-1,0]
            self.img_index  = data.iloc[-1,0]
        else:
            data = pd.DataFrame(columns=col)
            self.img_index = 0
            self.last_idx  = 0

        self.df = data
        return

    def app_base(self):
        start_btn = Button(window, text='Start', width=5, height=3, bg='yellow', font=(self.GUI_font, 12, 'bold'), fg='black', state='normal')
        start_btn.pack(side='left', anchor='s',  expand=False)       
        start_btn.configure(command=partial(self.select_button, start_btn, 100))
        self.base_btn_list.append(start_btn)

        save_btn = Button(window, text='Save', width=5, height=3, bg='light green', font=(self.GUI_font, 12, 'bold'), fg='black', state=DISABLED)
        save_btn.pack(side='left', anchor='s', expand=False)       
        save_btn.configure(command=partial(self.select_button, save_btn, 77))
        self.base_btn_list.append(save_btn)
        
        close_btn = Button(window, text='Close', width=5, height=3, bg='#eb3d34', font=(self.GUI_font, 12, 'bold'), fg='black', state=DISABLED)
        close_btn.pack(side='left', anchor='s', expand=False)       
        close_btn.configure(command=partial(self.select_button, close_btn, -1))
        self.base_btn_list.append(close_btn)

        btn4 = Label(window, width=1, height=5)
        btn4.pack(side='left', anchor='s', expand=False)

        count_label = Label(window, text=f'[{self.img_index} || {len(self.img_list)}]')
        count_label.config(font=(self.GUI_font ,13, 'bold'))
        count_label.pack(side='top',anchor='ne', expand=True)
        self.base_btn_list.append(count_label)

    def app_outline(self):
        for i in range(8):
            btn = Button(window, text=self.button[i], width=8, height=3, bg=self.btn_clr[i], font=(self.GUI_font, 12, 'bold'), fg='black', state=DISABLED)
            btn.pack(side='left', anchor='s', expand=True, fill=X)       
            btn.configure(command=partial(self.select_button, btn, i))
            self.button_list.append(btn)

    def set_btn(self):
        row_data = self.df.iloc[self.img_index,2:8]
        img_label = list(row_data)
        
        self.state = [False] * 8
        
        for i in range(1,7):
            if img_label[i-1] == 1:
                self.button_list[i].config(bg="light gray")
                self.state[i] = True
            else:
                pass

    def Save_Label(self):
        label = [int(i) for i in self.state[1:7]]

        if sum(label) == 0:
            labeled = False
        else:
            labeled = True
            
        data  = []
        data.append(self.img_index)
        data.append(self.img_list[self.img_index].split('\\')[-1])
        data.extend(label)
        data.append(self.img_list[self.img_index])
        data.append(labeled)

        if self.img_index in list(self.df['Idx']):
            ex_label = list(self.df.loc[self.img_index])

            if ex_label == label:
                pass
            else:
                self.df.loc[self.img_index] = data
        else:
            self.df = self.df.append(pd.DataFrame([data], columns=col), ignore_index=True)            
        return 

    def Reset_button(self):
        for idx in range(8):
            self.button_list[idx].config(bg=self.btn_clr[idx])
            self.button_list[idx].config(text=self.button[idx])
            self.state[idx] = False
        return
    
    def call_image(self, idx):
        image = Image.open(self.img_list[idx])
        image = image.resize((500,500))
        return image
    
    def show_image(self, idx):
        image = self.call_image(idx)
        img = ImageTk.PhotoImage(image)

        label1 = Label(image=img)
        label1.image = img

        label1.place(relx=0.25, rely=0.02)

    def select_Next(self):
        if self.img_index <= self.last_idx:
            self.show_image(self.img_index)
            self.set_btn()

        else:
            self.show_image(self.img_index)
            self.last_idx = self.img_index

    def select_Previous(self):
        self.show_image(self.img_index)
        self.set_btn()
        return

    def initial_btn(self):
        for i in range(8):
            self.button_list[i].config(state=NORMAL)
        self.base_btn_list[0].config(state=DISABLED)
        self.base_btn_list[1].config(state=NORMAL)
        self.base_btn_list[2].config(state=NORMAL)

    def select_button(self, button, idx):
        if idx == 0:
            # Preview
            self.Save_Label()
            self.img_index -= 1
            if self.img_index >= 0:
                self.base_btn_list[-1].config(text=f'{self.img_index}||{len(self.img_list)}')
                self.Reset_button()
                self.select_Previous()  # 이전 이미지 셋팅.
        
        elif idx == 7:
            # Next
            self.Save_Label()
            self.Reset_button()
            self.img_index += 1
            if self.img_index < len(self.img_list):
                self.base_btn_list[-1].config(text=f'{self.img_index}||{len(self.img_list)}')
                self.select_Next()
            
        elif idx == 100:
            # Start
            self.initial_btn()
            self.show_image(self.img_index)

        elif idx == 77:
            # Save
            self.df.to_csv(path_or_buf=".\\labeled_data.csv", index=False) # df row cvs 저장
            return

        elif idx == -1:
            # close
            self.df.to_csv(path_or_buf=".\\labeled_data.csv", index=False) # df row cvs 저장
            window.destroy()

        else:
            if button["text"] == self.button[idx] or button["text"] == f'Select_{self.button[idx]}':
                if self.state[idx] == False:    
                    #  공정 선택
                    self.button_list[idx].config(bg="light gray")
                    self.button_list[idx].config(text=f"Select_{self.button[idx]}")
                    self.state[idx] = True
                else:
                    # 공정 선택 해제
                    self.button_list[idx].config(bg=self.btn_clr[idx])
                    self.button_list[idx].config(text=self.button[idx])
                    self.state[idx] = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='.\\')
    app = GUI()
    app.master.title("Classification Labeling")
    app.mainloop()

