"""Creates a 4x4 grid of test features which can directly be used to control the robot

This module creates a 4x4 grid using tk which provides an easy user interface for robot
testing. The interface button activates different functions which complete different
robot tasks.
"""

# Import tk
import tkinter as tk

import robotMovement as rm
import robotLocalization as rl
import armMovement as am

class confApp(tk.Tk):   # Class for app which configures the main program before starting
    def __init__(self): # Main body for layout, buttons and text
        super().__init__()

        self.geometry('800x750')
        self.title('Function Test Panel v0.1')

        # Title bar
        self.top_bg = tk.Frame(self, width = 800, height = 60, bg='#001240', highlightthickness=0)
        self.top_bg.pack(side = tk.TOP, fill=tk.X)
        tk.Label(self.top_bg, text='4 x 4 Robot Tester', font='Montserrat 25', bg ='#001240', fg='white').pack(side = tk.LEFT)

        # Bottom bar
        self.bot_bg = tk.Canvas(self, width = 800, height = 60, bg='#001240', highlightthickness=0).pack(side = tk.BOTTOM)

        # Arm and data bar (l5)
        self.dataBar = tk.Frame(self, width = 800)
        self.dataBar.pack(side = tk.BOTTOM)

        # Buttons bar (l4)
        self.buttonBar4 = tk.Frame(self, width = 800)
        self.buttonBar4.pack(side = tk.BOTTOM)

        # Buttons bar (l3)
        self.buttonBar3 = tk.Frame(self, width = 800)
        self.buttonBar3.pack(side = tk.BOTTOM)

        # Buttons bar (l2)
        self.buttonBar2 = tk.Frame(self, width = 800)
        self.buttonBar2.pack(side = tk.BOTTOM)

        # Buttons bar (l1)
        self.buttonBar1 = tk.Frame(self, width = 800)
        self.buttonBar1.pack(side = tk.BOTTOM)

        # Standard Button Formats
        button_width = 14
        button_height = 4
        button_font = 'Helvetica 14 bold'
        button_padx = 5
        button_pady = 5
        button_text = [
            'Rotate Left',
            'Forward',
            'Rotate Right',
            'Stop',
            'Left',
            'Back',
            'Right',
            'Get Position\nto CLI',
            'Button 8',
            'Button 9',
            'Button 10',
            'Button 11',
            'Button 12',
            'Button 13',
            'Button 14',
            'Exit',
            'Submit Target'
        ]

        # Set Variables
        self.default_settings = {
            'x_target': 1.00,
            'y_target': 1.00,
            'arm_target': 10,
        }
        self.target_x = tk.DoubleVar(self)
        self.target_y = tk.DoubleVar(self)
        self.target_arm = tk.DoubleVar(self)
        self.target_x.set(self.default_settings['x_target'])
        self.target_y.set(self.default_settings['y_target'])
        self.target_arm.set(self.default_settings['arm_target'])

        # Defining Buttons

        # First Bar
        self.b0 = tk.Button(self.buttonBar1, width=button_width, height=button_height, text = button_text[0], font=button_font)
        self.b0.pack(side=tk.LEFT, padx=button_padx, pady=button_pady)  
        self.b0['command'] = self.button_0
        self.b1 = tk.Button(self.buttonBar1, width=button_width, height=button_height, text = button_text[1], font=button_font)
        self.b1.pack(side=tk.LEFT, padx=button_padx, pady=button_pady)  
        self.b1['command'] = self.button_1
        self.b2 = tk.Button(self.buttonBar1, width=button_width, height=button_height, text = button_text[2], font=button_font)
        self.b2.pack(side=tk.LEFT, padx=button_padx, pady=button_pady)  
        self.b2['command'] = self.button_2
        self.b3 = tk.Button(self.buttonBar1, width=button_width, height=button_height, text = button_text[3], font=button_font)
        self.b3.pack(side=tk.LEFT, padx=button_padx, pady=button_pady)  
        self.b3['command'] = self.button_3

        # Second Bar
        self.b4 = tk.Button(self.buttonBar2, width=button_width, height=button_height, text = button_text[4], font=button_font)
        self.b4.pack(side=tk.LEFT, padx=button_padx, pady=button_pady)  
        self.b4['command'] = self.button_4
        self.b5 = tk.Button(self.buttonBar2, width=button_width, height=button_height, text = button_text[5], font=button_font)
        self.b5.pack(side=tk.LEFT, padx=button_padx, pady=button_pady)  
        self.b5['command'] = self.button_5
        self.b6 = tk.Button(self.buttonBar2, width=button_width, height=button_height, text = button_text[6], font=button_font)
        self.b6.pack(side=tk.LEFT, padx=button_padx, pady=button_pady)  
        self.b6['command'] = self.button_6
        self.b7 = tk.Button(self.buttonBar2, width=button_width, height=button_height, text = button_text[7], font=button_font)
        self.b7.pack(side=tk.LEFT, padx=button_padx, pady=button_pady)  
        self.b7['command'] = self.button_7

        # Third Bar
        self.b8 = tk.Button(self.buttonBar3, width=button_width, height=button_height, text = button_text[8], font=button_font)
        self.b8.pack(side=tk.LEFT, padx=button_padx, pady=button_pady)  
        self.b8['command'] = self.button_8
        self.b9 = tk.Button(self.buttonBar3, width=button_width, height=button_height, text = button_text[9], font=button_font)
        self.b9.pack(side=tk.LEFT, padx=button_padx, pady=button_pady)  
        self.b9['command'] = self.button_9
        self.b10 = tk.Button(self.buttonBar3, width=button_width, height=button_height, text = button_text[10], font=button_font)
        self.b10.pack(side=tk.LEFT, padx=button_padx, pady=button_pady)  
        self.b10['command'] = self.button_10
        self.b11 = tk.Button(self.buttonBar3, width=button_width, height=button_height, text = button_text[11], font=button_font)
        self.b11.pack(side=tk.LEFT, padx=button_padx, pady=button_pady)  
        self.b11['command'] = self.button_11

        # Fourth Bar
        self.b12 = tk.Button(self.buttonBar4, width=button_width, height=button_height, text = button_text[12], font=button_font)
        self.b12.pack(side=tk.LEFT, padx=button_padx, pady=button_pady)  
        self.b12['command'] = self.button_12
        self.b13 = tk.Button(self.buttonBar4, width=button_width, height=button_height, text = button_text[13], font=button_font)
        self.b13.pack(side=tk.LEFT, padx=button_padx, pady=button_pady)  
        self.b13['command'] = self.button_13
        self.b14 = tk.Button(self.buttonBar4, width=button_width, height=button_height, text = button_text[14], font=button_font)
        self.b14.pack(side=tk.LEFT, padx=button_padx, pady=button_pady)  
        self.b14['command'] = self.button_14
        self.b15 = tk.Button(self.buttonBar4, width=button_width, height=button_height, text = button_text[15], font=button_font, fg='red', command = lambda:self.destroy()).pack(side=tk.LEFT, padx=button_padx, pady=button_pady)  
    
        # Data Bar
        self.b16 = tk.Button(self.dataBar, width=button_width, height=button_height, text = button_text[16], font=button_font)
        self.b16.pack(side=tk.RIGHT, padx=button_padx, pady=button_pady)
        self.b16['command'] = self.button_16
        self.pos_label = tk.Label(self.dataBar, text = 'Target (X,Y) Pos.', font=button_font)
        self.arm_label = tk.Label(self.dataBar, text = 'Target Arm Pos.', font=button_font)
        self.target_x_box = tk.Entry(self.dataBar, textvariable = self.target_x, width=10)
        self.target_y_box = tk.Entry(self.dataBar, textvariable = self.target_y, width=10)
        self.target_arm_box = tk.Entry(self.dataBar, textvariable = self.target_arm, width=10)
        self.target_arm_box.pack(side=tk.RIGHT, padx=button_padx, pady=button_pady)
        self.arm_label.pack(side=tk.RIGHT, padx=button_padx, pady=button_pady)
        self.target_x_box.pack(side=tk.RIGHT, padx=button_padx, pady=button_pady)
        self.target_y_box.pack(side=tk.RIGHT, padx=button_padx, pady=button_pady)
        self.pos_label.pack(side=tk.RIGHT, padx=button_padx, pady=button_pady)

        # Button Functions
    def button_0(self):
        rm.anticlockwise()
        
    def button_1(self):
        rm.forward()
        
    def button_2(self):
        rm.clockwise()
        
    def button_3(self):
        rm.stop()
        
    def button_4(self):
        rm.left()
        
    def button_5(self):
        rm.backward()
        
    def button_6(self):
        rm.right()
        
    def button_7(self):
        print(rl.get_position())
        
    def button_8(self):
        pass
    def button_9(self):
        pass
    def button_10(self):
        pass
    def button_11(self):
        pass
    def button_12(self):
        pass
    def button_13(self):
        pass
    def button_14(self):
        pass

    # Run function that calls modules to execute based on submitted data
    def button_16(self):
        # Get targets
        targets = {
            'x': self.target_x.get(),
            'y': self.target_y.get(),
            'arm': self.target_arm.get(),
        }
        print(targets)
        am.move_arm(targets['arm'])
        rm.move_to_target(targets)


if __name__ == '__main__':
    ConfApp = confApp()             # Create configuration app class
    ConfApp.mainloop()                  # Run configuration app
