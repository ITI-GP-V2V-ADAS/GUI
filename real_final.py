import tkinter as tk

import serial

import time

import threading



ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, parity=serial.PARITY_NONE,

                    stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS,

                    timeout=1.0)



class Toplevel1:

    def __init__(self, top=None):

        self.top = top

        top.geometry('944x631')  # Adjust the window size as needed

        top.title("New Toplevel")



        self.bg_image = tk.PhotoImage(file="/home/mohamed/Desktop/organized/final_6/1225.png")

        self.canvas = tk.Canvas(top, width=self.bg_image.width(), height=self.bg_image.height())

        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_image(0, 0, image=self.bg_image, anchor='nw')



        self.canvas.create_text(525, 215, fill="#42f5d7", text="AZZA AUTOMOTIVE", font=("Arial", 9))

        self.canvas.create_text(530, 335, fill="#42f5d7", text="GEAR", font=("Arial", 9))

        self.mph_text = self.canvas.create_text(290, 320, fill="#42f5d7", text="MPH: 0", font=("Arial", 12))

        self.gear_text = self.canvas.create_text(530, 350, fill="#42f5d7", text="Gear: 0", font=("Arial", 12))

        self.zozza_speed_text = self.canvas.create_text(97, 557, fill="#42f5d7", text="MPH: 0", font=("Arial", 12))

        self.zozza_direction_text = self.canvas.create_text(410, 557, fill="#42f5d7", text="direction: ", font=("Arial", 12))



        self.blindspot_image = None

        self.right_image = None

        self.left_image = None

        self.emergency_image = None

        self.black_rectangle = None



        # Start a separate thread to update values from UART

        uart_thread = threading.Thread(target=self.update_values_from_uart)

        uart_thread.daemon = True  # Set as daemon thread to terminate with main thread

        uart_thread.start()



    def update_values_from_uart(self):

        while True:

            try:

                data = ser.readline().decode('utf-8').strip()

                print("Received data:", data)



                other_speed_data, other_direction_data, my_speed_data, my_direction_data, blindspot_data, front_data, back_data = data.split(',')  # Split data



                other_speed_data = ''.join(filter(str.isdigit, other_speed_data))

                other_direction_data = ''.join(filter(str.isdigit, other_direction_data))

                my_speed_data = ''.join(filter(str.isdigit, my_speed_data))

                my_direction_data = ''.join(filter(str.isdigit, my_direction_data))

                blindspot_data = ''.join(filter(str.isdigit, blindspot_data))

                front_data = ''.join(filter(str.isdigit, front_data))

                back_data = ''.join(filter(str.isdigit, back_data))

                

                

                other_speed = int(other_speed_data)

                other_direction = int(other_direction_data)

                my_speed = int(my_speed_data)

                my_direction = int(my_direction_data)

                blindspot = int(blindspot_data)

                front = int(front_data)

                back = int(back_data)

                



                self.canvas.itemconfig(self.mph_text, text=f"MPH: {my_speed}")

                self.canvas.itemconfig(self.zozza_speed_text, text=f"other_speed: {other_speed}")

                if other_direction == 1:

                    self.canvas.itemconfig(self.zozza_direction_text, text=f"zozza direction: left")

                elif other_direction == 2:

                    self.canvas.itemconfig(self.zozza_direction_text, text=f"zozza direction: right")

                

                # Calculate gear based on MPH (uncomment if needed)

                if my_speed < 5:

                    gear = 1

                elif 5 <= my_speed < 10:

                    gear = 1

                elif 10 <= my_speed < 20:

                    gear = 2

                elif 20 <= my_speed < 30:

                    gear = 3

                elif 30 <= my_speed < 40:

                    gear = 4

                else:

                    gear = 5

                self.canvas.itemconfig(self.gear_text, text=f"Gear: {gear}")



                if blindspot == 2 and not self.blindspot_image:

                    self.blindspot_image = tk.PhotoImage(file="/home/mohamed/Desktop/organized/final_6/blindspot.png")

                    self.canvas.create_image(243, 223, image=self.blindspot_image, anchor='nw')

                elif blindspot == 0 and self.blindspot_image:

                    self.canvas.delete(self.blindspot_image)

                    self.blindspot_image = None



                if my_direction == 2 and not self.right_image:

                    self.right_image = tk.PhotoImage(file="/home/mohamed/Desktop/organized/final_5/right.png")

                    self.canvas.create_image(578, 142, image=self.right_image, anchor='nw')

                elif my_direction == 1 and not self.left_image:

                    self.left_image = tk.PhotoImage(file="/home/mohamed/Desktop/organized/final_6/left.png")

                    self.canvas.create_image(449, 144, image=self.left_image, anchor='nw')

                elif my_direction == 0 and self.right_image  and self.left_image:

                    self.canvas.delete(self.right_image)

                    self.right_image = None

                    self.canvas.delete(self.left_image)

                    self.left_image = None







                if front == 1:

                    if not self.emergency_image:

                        self.emergency_image = tk.PhotoImage(file="/home/mohamed/Desktop/organized/final_6/warning.png")

                        self.canvas.create_image(760, 282, image=self.emergency_image, anchor='nw')

                    elif self.emergency_image:

                        self.canvas.delete(self.emergency_image)

                        self.emergency_image = None

                elif front == 2:

                    if not self.emergency_image:

                        self.emergency_image = tk.PhotoImage(file="/home/mohamed/Desktop/organized/final_6/stop.png")

                        self.canvas.create_image(760, 282, image=self.emergency_image, anchor='nw')

                    elif self.emergency_image:

                        self.canvas.delete(self.emergency_image)

                        self.emergency_image = None

                elif front == 0 and self.emergency_image:

                    self.canvas.delete(self.emergency_image)

                    self.emergency_image = None



#





                if back == 1:

                    if not self.emergency_image:

                        self.emergency_image = tk.PhotoImage(file="/home/mohamed/Desktop/organized/final_6/back_warning.png")

                        self.canvas.create_image(735, 535, image=self.emergency_image, anchor='nw')

                    elif self.emergency_image:

                        self.canvas.delete(self.emergency_image)

                        self.emergency_image = None

                elif back == 2:

                    if not self.emergency_image:

                        self.emergency_image = tk.PhotoImage(file="/home/mohamed/Desktop/organized/final_6/back_stop.png")

                        self.canvas.create_image(735, 535, image=self.emergency_image, anchor='nw')

                    elif self.emergency_image:

                        self.canvas.delete(self.emergency_image)

                        self.emergency_image = None

                elif back == 0 and self.emergency_image:

                    self.canvas.delete(self.emergency_image)

                    self.emergency_image = None











                if my_speed > 0 and not self.black_rectangle:

                    self.black_rectangle = self.canvas.create_rectangle(511, 407, 551, 434, fill="black")

                elif my_speed <= 0 and self.black_rectangle:

                    self.canvas.delete(self.black_rectangle)

                    self.black_rectangle = None



                time.sleep(0.5)

            except ValueError as e:

                print("ValueError:", e)

                print("Invalid input. Please ensure the data format is correct.")



def vp_start_gui():

    global root

    root = tk.Tk()

    top = Toplevel1(root)

    root.mainloop()



if __name__ == '__main__':

    vp_start_gui()



