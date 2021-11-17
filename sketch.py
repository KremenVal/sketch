from tkinter import filedialog as fd
from tkinter import *
import os
import cv2
import shutil
from PIL import Image, ImageTk


class Sketch:
    root = None
    width = 550
    height = 0

    def __init__(self):
        self.sp_win = Tk()
        self.sp_win.title('Sketching images by Kremen')
        self.sp_win.overrideredirect(True)
        bg = Image.open('background/bg.jpg')
        width, height = bg.size
        self.height = round(self.width * (round(height / width, 2)))

        window_width = self.sp_win.winfo_screenwidth()
        window_height = self.sp_win.winfo_screenheight()
        position_right = int(window_width / 2 - self.width / 2)
        position_down = int(window_height / 2 - self.height / 2)
        self.sp_win.geometry('{}x{}+{}+{}'.format(self.width, self.height, position_right, position_down))

        bg = ImageTk.PhotoImage(bg.resize((self.width, self.height), Image.ANTIALIAS))
        label = Label(self.sp_win, image=bg)
        label.image = bg
        label.place(x=0, y=0, relwidth=1, relheight=1)

        self.sp_label_text = Label(self.sp_win, text="I Love You, My Honey!!!", fg="red", font=('Times New Roman', 30))\
            .pack(pady=50)
        self.sp_win.after(3000, self.main_window)
        mainloop()

    def main_window(self):
        self.sp_win.destroy()

        self.root = Tk()

        self.root.title('Sketching images by Kremen')

        window_width = self.root.winfo_screenwidth()
        window_height = self.root.winfo_screenheight()
        position_right = int(window_width / 2 - self.width / 2)
        position_down = int(window_height / 2 - self.height / 2)
        self.root.geometry('{}x{}+{}+{}'.format(self.width, self.height, position_right, position_down))

        main_menu = Menu(self.root)
        file_menu = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Open ...', command=self.select_image)
        file_menu.add_command(label='Save as ...', command=self.save_image)
        self.root.config(menu=main_menu)

    def select_image(self):
        # Set file types that user can choose from folders
        file_types = [('JPG files', '*.jpg'), ('JPEG files', '*.jpeg'), ('PNG files', '*.png')]

        # Getting file from selected folder
        file = fd.askopenfile(mode='a', title='Open a file', initialdir='/', filetypes=file_types)

        if file:
            # Getting path to image
            image_path = file.name

            if not os.path.isdir('image'):
                os.mkdir('image')
                shutil.copy(file.name, 'image')

            # Creating image from numpy array
            img = Image.fromarray(self.sketching(image_path))

            # Getting new sizes for new and old image for showing in window
            new_width = self.root.winfo_width() // 2
            new_height = round(new_width * round(img.height / img.width, 2))

            # Find coordinate y for placing images on the middle of window
            y = self.root.winfo_height() / 2 - new_height / 2

            # Reformatting images that we can paste them on window
            old_img = ImageTk.PhotoImage(Image.open(image_path).resize((new_width, new_height), Image.ANTIALIAS))
            img = ImageTk.PhotoImage(img.resize((new_width, new_height), Image.ANTIALIAS))

            # Pasting images into the window
            self.paste_image(img, new_width, y)
            self.paste_image(old_img, y=y)

    def save_image(self):
        # Set file types that user can choose from folders
        file_type = [('JPG files', '*.jpg'), ('JPEG files', '*.jpeg'), ('PNG files', '*.png')]

        # Getting path with name of new image where it will be saved
        file = fd.asksaveasfile(mode='w', title='Save as ...', initialdir='/', defaultextension=".jpg",
                                filetypes=file_type)

        # Verifying that the user has applied the save and folder with his image is existing
        if file and os.path.isdir('image'):
            # Getting users image
            files = os.listdir('image')

            # Verifying that image is existing
            if len(files) > 0:
                # Generating new sketch image and save it to selected dir, then remove folder with users image
                self.sketching('./image/' + files[0], file.name)
                shutil.rmtree('image')

    def sketching(self, file_path, image_name=None):
        image = cv2.imread(file_path, 1)
        output = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        output = cv2.GaussianBlur(output, (3, 3), 0)

        output = cv2.Laplacian(output, -1, ksize=5)

        output = 255 - output

        ret, output = cv2.threshold(output, 150, 255, cv2.THRESH_BINARY)

        if image_name is not None:
            cv2.imwrite(image_name, output)

        return output

    def paste_image(self, img, x=0, y=0):
        label = Label(self.root, image=img)
        label.image = img
        label.place(x=x, y=y)


sketch = Sketch()
# import cv2


# image = cv2.imread('./test-2.jpg', 1)
# output = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
# #Apply gaussian blur
# output = cv2.GaussianBlur(output, (3, 3), 0)
#
# #detect edges in the image
# output = cv2.Laplacian(output, -1, ksize=5)
#
# #invert the binary image
# output = 255 - output
#
# #binary thresholding
# ret, output = cv2.threshold(output, 150, 255, cv2.THRESH_BINARY)
#
# #create widnows to dispplay images
# cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE)
# cv2.namedWindow("pencilsketch", cv2.WINDOW_AUTOSIZE)
#
# #display images
# cv2.imwrite('test-2-3.jpg', output)
