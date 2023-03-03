from tkinter import * 
from PIL import Image, ImageTk
from functools import partial
from pathlib import Path
import tkinter.font as font
import pandas as pd
import os
import glob
import argparse

window = Tk()
window.geometry("1000x600")        # window size
col = ['Name', 'A', 'HSM', 'C', 'Cut', 'Wire', 'None', 'Path', 'Labeled']

class GUI(Frame):
    def __init__(self, args, master=None):
        super().__init__(master)
        self.pack()
        self.button_list    = []
        self.base_btn_list  = []
        self.state          = [False] * 8
        self.df             = None
        self.img_index      = 0
        self.last_idx       = 0
        self.file_name      = f"{args.data}_label.csv"

        self.GUI_font       = font.Font(family='맑은 고딕')   
        self.label          = Button(window, text='', width=5, height=3)
        self.button         = ['Previous', 'A', 'HSM', 'C', 'Cut', 'Wire', 'None', 'Next']
        self.btn_clr        = ['#4444f2', '#65eb34', '#65eb34', '#65eb34', '#f2aa44', '#f2aa44', '#f2aa44', '#4444f2']

        dir_img_list        = os.listdir(f'.\\IMAGE\\{args.data}')
        dir_img_list.sort()
        labeled_imgs        = self.create_DF(len(dir_img_list))        

        if labeled_imgs:
            for img in labeled_imgs:
                dir_img_list.remove(img)
            labeled_imgs.extend(dir_img_list)
            self.img_list = labeled_imgs
        else:
            self.img_list = dir_img_list

        self.img_list = [os.path.join(f'.\\IMAGE\\{args.data}', img) for img in self.img_list]

        self.app_base()                 # GUI 기본 Setting
        self.app_outline()              # Button Setting

    def create_DF(self, all):
        if os.path.exists(f".\\LABEL\\{self.file_name}"):
            data = pd.read_csv(f".\\LABEL\\{self.file_name}")
            last_idx   = data.iloc[-1,0] 
            labeled_images = data.iloc[:,1].to_list()
            index = last_idx + 1
            data = data.iloc[:,1:]
            if last_idx == all -1:
                index = last_idx
        else:
            data = pd.DataFrame(columns=col)
            index = 0
            labeled_images = None

        self.df = data
        self.img_index = index

        return  labeled_images

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

        fname_label = Label(window, text=f'{self.img_list[self.img_index]}'.split('\\')[-1])
        fname_label.config(font=(self.GUI_font ,13))
        fname_label.pack(side='top',anchor='ne', expand=False)
        self.base_btn_list.append(fname_label)

        count_label = Label(window, text=f'[{self.img_index+1} || {len(self.img_list)}]')
        count_label.config(font=(self.GUI_font ,13, 'bold'))
        count_label.pack(side='top',anchor='ne', expand=True)
        self.base_btn_list.append(count_label)

    def app_outline(self):
        for i in range(8):
            btn = Button(window, text=self.button[i], width=8, height=3, bg=self.btn_clr[i], font=(self.GUI_font, 12, 'bold'), fg='black', state=DISABLED)
            btn.pack(side='left', anchor='s', expand=True, fill=X)       
            btn.configure(command=partial(self.select_button, btn, i))
            self.button_list.append(btn)

    def set_btn(self, img_name):
        Img_name = img_name
        if Img_name in self.df['Name'].to_list():
            val = self.df[self.df['Name']==Img_name].values.tolist()[0]
            img_label = val[1:7]
            self.state = [False] * 8
        
            for i in range(1,7):
                if img_label[i-1] == 1:
                    self.button_list[i].config(bg="light gray")
                    self.state[i] = True
                else:
                    pass
        else:
            self.state = [False] * 8

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

    def Save_Label(self):
        if self.img_index < 0 or self.img_index >= len(self.img_list):
            return
        
        label = [int(i) for i in self.state[1:7]]

        if sum(label) == 0:
            labeled = False
        else:
            labeled = True
        
        Img_name = self.img_list[self.img_index].split('\\')[-1]
        img_path = self.img_list[self.img_index]

        data  = []
        # data.append(self.img_index)
        data.append(Img_name)  # image name
        data.extend(label)
        data.append(img_path)  # image path
        data.append(labeled)    


        if Img_name in list(self.df['Name']):
            img_idx  = self.df[self.df['Name']==Img_name].index.values[0]
            # img_data = self.df.iloc[img_idx]
            # ex_label = img_data.values.tolist()[2:8]
            ex_label = self.df.iloc[img_idx].values.tolist()[2:8]

            if ex_label != label:
                self.df.drop(img_idx, axis=0, inplace=True)
                new_row = pd.DataFrame([data], columns=col)
                self.df = pd.concat([self.df, new_row], ignore_index=True)
            else:
                self.df = self.df.sort_values('Name')
        else:
            new_row = pd.DataFrame([data], columns=col)
            self.df = pd.concat((self.df, new_row), ignore_index=True)   
        return 

    def Reset_button(self):
        for idx in range(8):
            self.button_list[idx].config(bg=self.btn_clr[idx])
            self.button_list[idx].config(text=self.button[idx])
            self.state[idx] = False
        return
    
    def select_Next(self):
        img_name = self.img_list[self.img_index].split('\\')[-1]
        self.show_image(self.img_index)
        self.set_btn(img_name)

    def select_Previous(self):
        img_name = self.img_list[self.img_index].split('\\')[-1]
        self.show_image(self.img_index)
        self.set_btn(img_name)
        return

    def initial_btn(self):
        for i in range(8):
            self.button_list[i].config(state=NORMAL)    # 공정 button 활성화
        self.base_btn_list[0].config(state=DISABLED)    # Start: 비활성화
        self.base_btn_list[1].config(state=NORMAL)      # Save: 활성화
        self.base_btn_list[2].config(state=NORMAL)      # Close: 활성화

    def select_button(self, button, idx):
        if idx == 0:
            # Previous
            self.Save_Label()
            self.img_index -= 1

            if self.img_index < 0:
                self.img_index = 0
            else:
                self.base_btn_list[-1].config(text=f'{self.img_index + 1}||{len(self.img_list)}')
                self.Reset_button()
                self.select_Previous()  # 이전 이미지 셋팅.
    
        elif idx == 7:
            # Next
            self.Save_Label()
            self.img_index += 1
            if self.img_index > len(self.img_list) - 1:
                self.img_index = len(self.img_list) - 1
            else:
                self.base_btn_list[-1].config(text=f'{self.img_index + 1}||{len(self.img_list)}')
                self.Reset_button()
                self.select_Next()
        
        elif idx == 100:
            # Start --> Labeling 시작
            self.initial_btn()
            self.show_image(self.img_index)         # create_DF 에서 설정한 self.img_index 
            img_name = self.img_list[self.img_index].split('\\')[-1]
            self.set_btn(img_name)

        elif idx == 77:
            # Save
            save_data = self.df[self.df['Labeled']==True]
            save_data.sort_values('Name')
            save_data.reset_index(drop=True)
            print(save_data)
            print()
            save_data.to_csv(path_or_buf=f"LABEL\\{self.file_name}", index=True) # df row cvs 저장
            return

        elif idx == -1:
            # close
            save_data = self.df[self.df['Labeled']==True]
            save_data = save_data.sort_values('Name')
            save_data = save_data.reset_index()
            save_data = save_data.drop(['index'], axis='columns')
            save_data.to_csv(path_or_buf=f"LABEL\\{self.file_name}", index=True) # df row cvs 저장
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
    parser.add_argument('--data', type=str, default='train1')
    args = parser.parse_args()

    if not os.path.exists('.\\LABEL'):
        os.makedirs('.\\LABEL')

    app = GUI(args)
    app.master.title("Classification Labeling")
    app.mainloop()

