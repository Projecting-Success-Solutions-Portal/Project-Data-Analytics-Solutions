import tkinter as tk
from tkinter import simpledialog, filedialog
from PIL import Image, ImageTk
from pdf2image import convert_from_path
import json



# input PDF file name and path
# output: template files

class DrawRectangle(tk.Tk):
    def __init__(self, image, ratio):
        tk.Tk.__init__(self)
        self.x = self.y = 0
        self.ratio = ratio
        self.image = image

        self.keywords = ""
        self.lms_id = ""
        self.name_of_proj = ""

        self.name_coordinates = []
        self.cert_name_coordinates = []
        self.period_coordinates = []
        self.issue_coordinates = []
        self.vendor_coordinates = []
        # self.orientation = orientation

        self.json_template = {}

        self.canvas = tk.Canvas(self, width=image.width, height=image.height, cursor="cross")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<Motion>", self.on_mouse_move)

        self.rect = None

        self.start_x = None
        self.start_y = None

        self._draw_image(image)

    def _draw_image(self, image):
         self.im = Image.open(image.filename)
         self.tk_im = ImageTk.PhotoImage(self.im)
         self.canvas.create_image(0,0,anchor="nw",image=self.tk_im)

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y

        # create rectangle
        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='red')

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

        self._draw_cross_hair(event)

    def on_mouse_move(self, event):
        self._draw_cross_hair(event)

    def _draw_cross_hair(self, event):
        try:
            self.canvas.delete(self.mouse_hor)
            self.canvas.delete(self.mouse_vert)
        except:
            pass

        self.start_x_cross = event.x
        self.start_y_cross = event.y
        self.mouse_vert = self.canvas.create_line(self.start_x_cross, 0, self.start_x_cross, self.image.height, fill='blue')
        self.mouse_hor = self.canvas.create_line(0, self.start_y_cross , self.image.width, self.start_y_cross, fill='blue')

    def on_button_release(self, event):

        box_input = simpledialog.askstring(title="What have you selected",
                                  prompt="Please select the number corresponding to what you have selected: \n 1: Name of Employee \n 2: Certificate Name \n 3: Training period \n 4: Issue Information \n 5: Vendor \n <empty line>: Everything Entered")

        x0 = round((self.start_x / self.ratio) / 200, 5) # 200 dpi resolution
        y0 = (self.start_y / self.ratio) / 200
        x1 = (event.x / self.ratio) / 200
        y1 = (event.y / self.ratio) / 200

        # if box_input == "1":

        if box_input == "1":
            self.name_coordinates = [x0, y0, x1, y1]
            print(f"Name of Employee is found at coordinates {self.name_coordinates}")

        if box_input == "2":
            self.cert_name_coordinates = [x0, y0, x1, y1]
            print(f"Certificate Name is found at coordinates {self.cert_name_coordinates}")

        if box_input == "3":
            self.period_coordinates = [x0, y0, x1, y1]
            print(f"Training period is found at coordinates {self.period_coordinates}")

        if box_input == "4":
            self.issue_coordinates = [x0, y0, x1, y1]
            print(f"Issue Information is found at coordinates {self.issue_coordinates}")

        if box_input == "5":
            self.vendor_coordinates = [x0, y0, x1, y1]
            print(f"Vendor is found at coordinates {self.vendor_coordinates}")


        if (box_input == "" or box_input == "10"):
            self.name_of_proj = simpledialog.askstring(title="Name of this Project",
                            prompt="Please Enter the Name of this Project")
            self.lms_id = simpledialog.askstring(title=f"Project: {self.name_of_proj}",
                            prompt="What is the LMS ID for this certificate:")
            self.keywords = simpledialog.askstring(title=f"Project: {self.name_of_proj}",
                            prompt="Please enter keywords found in the certificate:")
            self.canvas.delete(self.rect)
            # self.canvas.delete("all")

    def convert_pixel2inch(self, width, height, image):
        x_resolution = width * image.width
        y_resolution = width * image.width


def check_orientation(width, height):
    if round(height/width,1) == 1.4 or round(width/height,1) == 1.4:
        if height > width:
            return "portrait"
        elif width > height:
            print("landscape")
    else:
        print("Error: Picture is not A4")


class TemplateCreator:
    def __init__(self, pdf):
        root = tk.Tk()
        root.attributes('-fullscreen', 1) # make the root window fullscreen

        scr_width = root.winfo_screenwidth()
        scr_height = root.winfo_screenheight()
        root.destroy()

        images = convert_from_path(pdf)

        # for i, image in enumerate(images):
        # Just pick the first page
        i = 0
        image = images[0]

   # for i, image in enumerate(images):
        # Save pages as images in the pdf
        jpg_name = str(pdf) + '_page'+ str(i) +'.jpg'
        image.save(jpg_name, 'JPEG')

        im = Image.open(jpg_name)

        if im.width > scr_width or im.height > scr_height:
            # only resize image bigger than the screen
            ratio = min((scr_width-100)/im.width, (scr_height-100)/im.height)
            im = im.resize((int(im.width*ratio), int(im.height*ratio)))
            im.save(jpg_name, format='JPEG', dpi=(200,200))

        im = Image.open(jpg_name)

        app = DrawRectangle(im, ratio)
        app.mainloop()

        if app.keywords == "":
            root = tk.Tk()
            root.withdraw()
            app.name_of_proj = simpledialog.askstring(title="Name of this Project",
                            prompt="Please Enter the Name of this Project")
            app.lms_id = simpledialog.askstring(title=f"Project: {app.name_of_proj}",
                            prompt="What is the LMS ID for this certificate:")
            app.keywords = simpledialog.askstring(title=f"Project: {app.name_of_proj}",
                            prompt="Please enter keywords found in the certificate:")

        # Create dicts for JSON
        dict_template = {'keywords': app.keywords.split(','), 'LMS ID': app.lms_id}

        dict_template["fields"] = {}
        dict_template["fields"]["Name"] = app.name_coordinates
        dict_template["fields"]["Certificate type"] = app.cert_name_coordinates
        dict_template["fields"]["Training period"] = app.period_coordinates
        dict_template["fields"]["Issue info"] = app.issue_coordinates
        dict_template["fields"]["Company"] = app.vendor_coordinates

        print(dict_template)

        templatefile = "templates/" + app.name_of_proj + ".json"
        # the json file where the output must be stored
        with open(templatefile, 'w') as f:
            # outfile = open(app.name_of_proj + ".json", "w")
            json.dump(dict_template, f, indent = 4)
            print(f'Saved template successfully {templatefile}')

        self.templatefile = templatefile
        # self.templatefile = templatefile


# if __name__ == "__main__":
#     # print("asking")
#     # print("done")
#     # pdf = filedialog.askopenfilename()
#
#     root = tk.Tk()
#     root.attributes('-fullscreen', 1) # make the root window fullscreen
#     # root.config(cursor="none")  # hide the mouse cursor
#
#     # get the screen size
#     scr_width = root.winfo_screenwidth()
#     scr_height = root.winfo_screenheight()
#
#     root.destroy()
#
#     print("Preparing images ...")
#
#     # Store Pdf with convert_from_path function
#     pdf = "Certificates/1-Single/Cypress1.pdf"
#
#     images = convert_from_path(pdf)
#
#     for i, image in enumerate(images):
#         # Save pages as images in the pdf
#         jpg_name = str(pdf) + '_page'+ str(i) +'.jpg'
#         image.save(jpg_name, 'JPEG')
#
#         im = Image.open(jpg_name)
#
#         # print(im.info['dpi'])
#
#         if im.width > scr_width or im.height > scr_height:
#             # only resize image bigger than the screen
#             ratio = min((scr_width-100)/im.width, (scr_height-100)/im.height)
#             im = im.resize((int(im.width*ratio), int(im.height*ratio)))
#             im.save(jpg_name, format='JPEG')
#             orientation = check_orientation(im.width, im.height)
#
#         im = Image.open(jpg_name)
#
#         app = DrawRectangle(im, ratio, orientation)
#         app.mainloop()
#
#         if app.keywords == "":
#             root = tk.Tk()
#             root.withdraw()
#             app.name_of_proj = simpledialog.askstring(title="Name of this Project",
#                             prompt="Please Enter the Name of this Project")
#             app.lms_id = simpledialog.askstring(title=f"Project: {app.name_of_proj}",
#                             prompt="What is the LMS ID for this certificate:")
#             app.keywords = simpledialog.askstring(title=f"Project: {app.name_of_proj}",
#                             prompt="Please enter keywords found in the certificate:")
#
#         # Create dicts for JSON
#         dict_template = {'keywords': app.keywords, 'LMS ID': app.lms_id}
#
#         dict_template["fields"] = {}
#         dict_template["fields"]["Name"] = app.name_coordinates
#         dict_template["fields"]["Certificate type"] = app.cert_name_coordinates
#         dict_template["fields"]["Training period"] = app.period_coordinates
#         dict_template["fields"]["Issue info"] = app.issue_coordinates
#         dict_template["fields"]["Company"] = app.vendor_coordinates
#
#         # the json file where the output must be stored
#         out_file = open(app.name_of_proj + ".json", "w")
#         json.dump(dict_template, out_file, indent = 6)
#         out_file.close()
