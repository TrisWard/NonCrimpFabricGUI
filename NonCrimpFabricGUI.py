# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 21:34:06 2025

@author: Tristen Ward
"""
from TexGen.Core import *
import wx
import math

def ModelScriptTricot(l, w, s, h, domain, d, o):

        layers = l
        angle_GUI = o
        radius = d/2             
        Textile = CTextile()
        Yarns = [CYarn()]
                
        Yarns[0].AddNode(CNode(XYZ(0, 0, 0)))
        Yarns[0].AddNode(CNode(XYZ(0, s, 0)))
              
        
        # Loop over all the yarns in the list
        for Yarn in Yarns:
         	# Assign a power ellipse to the inlay yarns
         	InlaySection = CSectionPowerEllipse(w, h, 0.5)
         	Yarn.AssignSection(CYarnSectionConstant(InlaySection))
         	#Add repeats
         	Yarn.AddRepeat(XYZ(s, 0, 0))
         	Yarn.AddRepeat(XYZ(0, s, 0))
         	# Set the interpolation function
         	Yarn.AssignInterpolation(CInterpolationCubic())
         	# set the resolution of the surface mesh created
         	Yarn.SetResolution(40)
         	# Add the yarn to our textile
         	Textile.AddYarn(Yarn)
        	
        # Define constants for the stitching
        adjustment = 0.05 #Height adjustment
        upper = 0.5*h+radius
        lower = -0.5*h-radius
        domain_height_adjust = (h*layers)-0.5*h + 2*radius
        # Create a stitch yarn 
        StitchYarn = CYarn()

        
        # Create stitch yarn path. This path is quite complex and has been 
        # created with a fair amount of tweaking. Note that the tangents
        # at the nodes have been specified for further control on the path.
        StitchYarn.AddNode(CNode(XYZ(2*adjustment, adjustment, upper), XYZ(1, 1, 0)))
        StitchYarn.AddNode(CNode(XYZ(s+adjustment, s-adjustment, upper), XYZ(1, 1, 0)))
        
        StitchYarn.AddNode(CNode(XYZ(s+adjustment, s, lower), XYZ(0, 1, 0))) 
        StitchYarn.AddNode(CNode(XYZ(s+2*adjustment, 2*s-adjustment, lower+adjustment), XYZ(0, 1, 0)))
        
        StitchYarn.AddNode(CNode(XYZ(s+adjustment, 2*s, lower+adjustment), XYZ(-1, 0, 0))) 
        StitchYarn.AddNode(CNode(XYZ(s-adjustment, 2*s, lower+adjustment), XYZ(-1, 0, 0)))
        
        StitchYarn.AddNode(CNode(XYZ(s+adjustment, 2*s, lower+adjustment), XYZ(0, -1, 0)))
        StitchYarn.AddNode(CNode(XYZ(s-adjustment, s, lower), XYZ(0, -1, 0)))
        
        StitchYarn.AddNode(CNode(XYZ(s-2*adjustment, s+adjustment, upper), XYZ(-1, 1, 0)))
        StitchYarn.AddNode(CNode(XYZ(-adjustment, 2*s-adjustment, upper), XYZ(-1, 1, 0)))
        	
        StitchYarn.AddNode(CNode(XYZ(-adjustment, 2*s, lower), XYZ(0, 1, 0)))
        StitchYarn.AddNode(CNode(XYZ(-2*adjustment, 3*s-adjustment, lower), XYZ(0, 1, 0)))
        
        StitchYarn.AddNode(CNode(XYZ(-adjustment, 3*s, lower+adjustment), XYZ(1, 0, 0)))
        StitchYarn.AddNode(CNode(XYZ(adjustment, 3*s, lower+adjustment), XYZ(1, 0, 0)))
        
        StitchYarn.AddNode(CNode(XYZ(2*adjustment, 3*s-adjustment, lower), XYZ(0, -1, 0)))
        StitchYarn.AddNode(CNode(XYZ(adjustment, 2*s, lower), XYZ(0, -1, 0)))
        
        StitchYarn.AddNode(CNode(XYZ(2*adjustment, 2*s+adjustment, upper), XYZ(1, 1, 0)))
        
        # Add the repeat vectors for the stitching
        StitchYarn.AddRepeat(XYZ(s, 0, 0))
        StitchYarn.AddRepeat(XYZ(0, 2*s, 0))
        
        # Assign a circular section to the stitch yarns
        StitchSection = CSectionEllipse(2*radius, 2*radius)
        StitchYarn.AssignSection(CYarnSectionConstant(StitchSection))
        # Set the interpolation functin to Bezier so that 
        # the yarn tangents specified above are respected
        StitchYarn.AssignInterpolation(CInterpolationBezier())
        # Set a lower surface mesh resolution than for the inlays.
        # The stitching is so thin that a high resolution is not needed
        StitchYarn.SetResolution(8)
        # Translate the stitch yarn so that it falls between the inlay yarns
        StitchYarn.Translate(XYZ(0.5*s, 0.5*s+radius, 0))
        # Add the yarn to the textile
        Textile.AddYarn(StitchYarn)
        # # Create a domain and assign it to the textile
        Textile.AssignDomain(CDomainPlanes(XYZ(0, 0, lower-radius), XYZ(domain, domain, upper+radius)))
       
        # Creating plies for value in parameter layers
        if layers == 1:
            Textile.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[0]))), XYZ(0,0,0))
            
            AddTextile("NonCrimpComposite",Textile)
    
        if layers == 2:
            Textile.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[0]))), XYZ(0,0,0))
            Textile2 = CTextile(Textile)     
            
            LayeredTextile = CTextileLayered()
            LayeredTextile.AddLayer( Textile, XYZ(0, 0, 0) )            
            Textile2.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[1])-int(angle_GUI[0]))), XYZ(0,0,0))            
            LayeredTextile.AddLayer( Textile2, XYZ(0, 0, h) )                            
            Domain = CDomainPlanes( XYZ(0, 0, lower-radius), XYZ(domain, domain, domain_height_adjust) )           
            LayeredTextile.AssignDomain( Domain )
            
            AddTextile("NonCrimpComposite: 2 Layers",LayeredTextile)
    
        if layers == 3:
            
            Textile.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[0]))), XYZ(0,0,0))
            Textile2 = CTextile(Textile)
            Textile3 = CTextile(Textile)
           
            LayeredTextile = CTextileLayered()
            LayeredTextile.AddLayer( Textile, XYZ(0, 0, 0) )           
            Textile2.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[1])-int(angle_GUI[0]))), XYZ(0,0,0))           
            LayeredTextile.AddLayer( Textile2, XYZ(0, 0, h) )           
            Textile3.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[2])-int(angle_GUI[0]))), XYZ(0,0,0))
            LayeredTextile.AddLayer( Textile3, XYZ(0,0,h*2) )
            Domain = CDomainPlanes( XYZ(0, 0, lower-radius), XYZ(domain, domain, domain_height_adjust) )
            LayeredTextile.AssignDomain( Domain )
    
            AddTextile("NonCrimpComposite: 3 Layers",LayeredTextile)
    
        if layers == 4:
        
            Textile.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[0]))), XYZ(0,0,0))
            Textile2 = CTextile(Textile)
            Textile3 = CTextile(Textile)
            Textile4 = CTextile(Textile)
            
            LayeredTextile = CTextileLayered()
            LayeredTextile.AddLayer( Textile, XYZ(0, 0, 0) )           
            Textile2.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[1])-int(angle_GUI[0]))), XYZ(0,0,0))
            LayeredTextile.AddLayer( Textile2, XYZ(0, 0, h) )
            Textile3.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[2])-int(angle_GUI[0]))), XYZ(0,0,0))
            LayeredTextile.AddLayer( Textile3, XYZ(0,0,h*2) )
            Textile4.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[3])-int(angle_GUI[0]))), XYZ(0,0,0))
            LayeredTextile.AddLayer( Textile4, XYZ(0,0,h*3) )
            Domain = CDomainPlanes( XYZ(0, 0, lower-radius), XYZ(domain, domain, domain_height_adjust) )
            LayeredTextile.AssignDomain( Domain )
          
            AddTextile("NonCrimpComposite: 4 Layers",LayeredTextile)
        
        if layers == 5:
            
            Textile.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[0]))), XYZ(0,0,0))
            Textile2 = CTextile(Textile)
            Textile3 = CTextile(Textile)
            Textile4 = CTextile(Textile)
            Textile5 = CTextile(Textile)
           
            LayeredTextile = CTextileLayered()
            LayeredTextile.AddLayer( Textile, XYZ(0, 0, 0) )
            Textile2.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[1])-int(angle_GUI[0]))), XYZ(0,0,0))
            LayeredTextile.AddLayer( Textile2, XYZ(0, 0, h) )
            Textile3.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[2])-int(angle_GUI[0]))), XYZ(0,0,0))
            LayeredTextile.AddLayer( Textile3, XYZ(0,0,h*2) )
            Textile4.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[3])-int(angle_GUI[0]))), XYZ(0,0,0))
            LayeredTextile.AddLayer( Textile4, XYZ(0,0,h*3) )
            Textile5.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[4])-int(angle_GUI[0]))), XYZ(0,0,0))
            LayeredTextile.AddLayer( Textile5, XYZ(0,0,h*4) )
            Domain = CDomainPlanes( XYZ(0, 0, lower-radius), XYZ(domain, domain, domain_height_adjust) )
            LayeredTextile.AssignDomain( Domain )
             
            AddTextile("NonCrimpComposite: 5 Layers",LayeredTextile)
            
        if layers == 6:
            
            Textile.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[0]))), XYZ(0,0,0))
            Textile2 = CTextile(Textile)
            Textile3 = CTextile(Textile)
            Textile4 = CTextile(Textile)
            Textile5 = CTextile(Textile)
            Textile6 = CTextile(Textile)
           
            LayeredTextile = CTextileLayered()
            LayeredTextile.AddLayer( Textile, XYZ(0, 0, 0) )
            Textile2.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[1])-int(angle_GUI[0]))), XYZ(0,0,0))
            LayeredTextile.AddLayer( Textile2, XYZ(0, 0, h) )
            Textile3.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[2])-int(angle_GUI[0]))), XYZ(0,0,0))
            LayeredTextile.AddLayer( Textile3, XYZ(0,0,h*2) )
            Textile4.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[3])-int(angle_GUI[0]))), XYZ(0,0,0))
            LayeredTextile.AddLayer( Textile4, XYZ(0,0,h*3) )
            Textile5.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[4])-int(angle_GUI[0]))), XYZ(0,0,0))
            LayeredTextile.AddLayer( Textile5, XYZ(0,0,h*4) )
            Textile6.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[5])-int(angle_GUI[0]))), XYZ(0,0,0))  
            LayeredTextile.AddLayer( Textile6, XYZ(0,0,h*5) )
            Domain = CDomainPlanes( XYZ(0, 0, lower-radius), XYZ(domain, domain, domain_height_adjust) )
            LayeredTextile.AssignDomain( Domain )
              
            AddTextile("NonCrimpComposite: 6 Layers",LayeredTextile)
            
        if layers == 7:
            
            Textile.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[0]))), XYZ(0,0,0))
            Textile2 = CTextile(Textile)
            Textile3 = CTextile(Textile)
            Textile4 = CTextile(Textile)
            Textile5 = CTextile(Textile)
            Textile6 = CTextile(Textile)
            Textile7 = CTextile(Textile)
           
            LayeredTextile = CTextileLayered()
            LayeredTextile.AddLayer( Textile, XYZ(0, 0, 0) )
            Textile2.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[1])-int(angle_GUI[0]))), XYZ(0,0,0))
            LayeredTextile.AddLayer( Textile2, XYZ(0, 0, h) )
            Textile3.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[2])-int(angle_GUI[0]))), XYZ(0,0,0))
            LayeredTextile.AddLayer( Textile3, XYZ(0,0,h*2) )
            Textile4.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[3])-int(angle_GUI[0]))), XYZ(0,0,0))
            LayeredTextile.AddLayer( Textile4, XYZ(0,0,h*3) )
            Textile5.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[4])-int(angle_GUI[0]))), XYZ(0,0,0))
            LayeredTextile.AddLayer( Textile5, XYZ(0,0,h*4) )
            Textile6.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[5])-int(angle_GUI[0]))), XYZ(0,0,0))  
            LayeredTextile.AddLayer( Textile6, XYZ(0,0,h*5) )
            Textile7.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[6])-int(angle_GUI[0]))), XYZ(0,0,0))  
            LayeredTextile.AddLayer( Textile7, XYZ(0,0,h*6) )
            Domain = CDomainPlanes( XYZ(0, 0, lower-radius), XYZ(domain, domain, domain_height_adjust) )
            LayeredTextile.AssignDomain( Domain )
          
            AddTextile("NonCrimpComposite: 7 Layers",LayeredTextile)
            
        if layers == 8:
            
            Textile.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[0]))), XYZ(0,0,0))
            Textile2 = CTextile(Textile)
            Textile3 = CTextile(Textile)
            Textile4 = CTextile(Textile)
            Textile5 = CTextile(Textile)
            Textile6 = CTextile(Textile)
            Textile7 = CTextile(Textile)
            Textile8 = CTextile(Textile)
           
            LayeredTextile = CTextileLayered()
            LayeredTextile.AddLayer( Textile, XYZ(0, 0, 0) )
            Textile2.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[1])-int(angle_GUI[0]))), XYZ(0,0,0))
            LayeredTextile.AddLayer( Textile2, XYZ(0, 0, h) )
            Textile3.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[2])-int(angle_GUI[0]))), XYZ(0,0,0))
            LayeredTextile.AddLayer( Textile3, XYZ(0,0,h*2) )
            Textile4.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[3])-int(angle_GUI[0]))), XYZ(0,0,0))
            LayeredTextile.AddLayer( Textile4, XYZ(0,0,h*3) )
            Textile5.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[4])-int(angle_GUI[0]))), XYZ(0,0,0))
            LayeredTextile.AddLayer( Textile5, XYZ(0,0,h*4) )
            Textile6.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[5])-int(angle_GUI[0]))), XYZ(0,0,0))  
            LayeredTextile.AddLayer( Textile6, XYZ(0,0,h*5) )
            Textile7.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[6])-int(angle_GUI[0]))), XYZ(0,0,0))  
            LayeredTextile.AddLayer( Textile7, XYZ(0,0,h*6) )
            Textile8.Rotate(WXYZ(XYZ(0,0,1),math.radians(int(angle_GUI[7])-int(angle_GUI[0]))), XYZ(0,0,0))  
            LayeredTextile.AddLayer( Textile8, XYZ(0,0,h*7) )
            Domain = CDomainPlanes( XYZ(0, 0, lower-radius), XYZ(domain, domain, domain_height_adjust) )
            LayeredTextile.AssignDomain( Domain )
                     
            AddTextile("NonCrimpComposite: 8 Layers",LayeredTextile)
        
class PageOne(wx.Panel):
    def __init__(self,parent,switch_callback):
        super().__init__(parent)
        self.switch_callback = switch_callback
        
        self.parent=parent
        main_layout = wx.BoxSizer(wx.HORIZONTAL)
        
        # Adding image
        image_path = r"C:\Users\trist\Documents\ProjectScripts\TexGen.PNG" 
        image_size = (200,200)
        image = wx.Image(image_path, wx.BITMAP_TYPE_PNG)
        image = image.Scale(*image_size, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.Bitmap(image)
        image_widget = wx.StaticBitmap(self, bitmap=bitmap)

        main_layout.Add(image_widget, flag=wx.ALIGN_TOP, border=10)
        right_layout = wx.BoxSizer(wx.VERTICAL)

        # Top text
        Text = wx.StaticText(self, label="This wizard will create a Non-Crimp Unidirectional model for you.") 
        right_layout.Add(Text, flag=wx.ALL, border=10)

        # Grid layout for inputs
        grid_layout = wx.FlexGridSizer(7, 2, 10, 10)

        # Labels and Inputs
        labels = ["Number of Layers:","Yarn Spacing:", "Yarn Width:", "Fabric Thickness:","Domain Size:", "Stitch Thickness:", "Type of Stitch:"]
        self.inputs = {}
        values = "1 1.5 1.45 0.4 6 0.05 Tricot"
        float_values = [(k) for k in values.split()]
        i = 0
        for label in labels:
            grid_layout.Add(wx.StaticText(self, label=label), flag=wx.ALIGN_CENTER_VERTICAL)
            
            if label == "Type of Stitch:":
                stitch_types = ["Tricot", "Chain","Tricot-Chain"]
                input_field = wx.Choice(self,choices=stitch_types)
                input_field.SetSelection(0)
                
            elif label == "Number of Layers:":
                single_values = str(float_values[i])
                input_field = wx.TextCtrl(self, value=single_values)
                input_field.Bind(wx.EVT_TEXT, self.on_number_of_layers_change)
                input_field.Bind(wx.EVT_CHAR, self.on_number_only)
                input_field.Bind(wx.EVT_KILL_FOCUS, self.validate_numeric_input)
                i += 1
            
            else:
                single_values = str(float_values[i])
                input_field = wx.TextCtrl(self, value=single_values)
                input_field.Bind(wx.EVT_CHAR, self.on_number_only)
                input_field.Bind(wx.EVT_KILL_FOCUS, self.validate_numeric_input)
                i += 1

            self.inputs[label] = input_field
            grid_layout.Add(input_field, flag=wx.EXPAND)
            

        right_layout.Add(grid_layout, flag=wx.ALL | wx.EXPAND, border=10)

        separator = wx.StaticLine(self, size=(-1, 2))  
        right_layout.Add(separator, flag=wx.EXPAND | wx.ALL, border=10)

        # Buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        back_btn = wx.Button(self, label="Back")
        next_btn = wx.Button(self, label="Next")
        cancel_btn = wx.Button(self, label="Cancel")
        
        # Events to Buttons
        next_btn.Bind(wx.EVT_BUTTON,self.on_next)
        cancel_btn.Bind(wx.EVT_BUTTON,self.on_cancel)
        back_btn.Enable(False)

        button_sizer.Add(back_btn, flag=wx.RIGHT, border=5)
        button_sizer.Add(next_btn, flag=wx.RIGHT, border=5)
        button_sizer.Add(cancel_btn)

        right_layout.Add(button_sizer, flag=wx.ALL | wx.ALIGN_RIGHT, border=10)
        main_layout.Add(right_layout, flag=wx.ALL | wx.EXPAND, border=10)

        # Set sizer and show GUI
        self.SetSizer(main_layout)
        
        
    def on_next(self,event):
        input_data = {
            label: (field.GetStringSelection() if isinstance(field, wx.Choice) else field.GetValue().strip())
            for label, field in self.inputs.items()
        }
    
        # Storing data
        input_data = {label: (field.GetStringSelection() if isinstance(field, wx.Choice) else field.GetValue()) for label, field in self.inputs.items()}
        layer_input = int(float(input_data.pop("Number of Layers:")))
        yarn_spacing_input = (float(input_data.pop("Yarn Spacing:")))  # Extract yarn spacing count
        yarn_width_input = (float(input_data.pop("Yarn Width:")))  # Extract yarn width count
        fabric_thickness_input = (float(input_data.pop("Fabric Thickness:"))) # Extract fabric thickness count
        domain_size_input = (float(input_data.pop("Domain Size:")))
        stitch_thickness_input = (float(input_data.pop("Stitch Thickness:")))
        stitch_type = (str(input_data.pop("Type of Stitch:")))
      
        expected_diff = stitch_thickness_input
        actual_diff = yarn_spacing_input - yarn_width_input
    
        # Calculation check
        if abs(actual_diff - expected_diff) > 1e-6:
            msg = (
                f"The difference between Yarn Spacing and Yarn Width is recommended to be equal to the Stitch Thickness.\n\n"
                f"Yarn Spacing - Yarn Width = {actual_diff:.4f}\n"
                f"Stitch Thickness = {expected_diff:.4f}\n\n"
                f"Do you want to proceed anyway?"
            )
            dlg = wx.MessageDialog(self, msg, "Confirm Input", wx.YES_NO | wx.ICON_WARNING)
            if dlg.ShowModal() != wx.ID_YES:
                dlg.Destroy()
                return
            dlg.Destroy()
        
        self.switch_callback(layer_input, yarn_spacing_input, yarn_width_input, fabric_thickness_input, domain_size_input, stitch_thickness_input, stitch_type)
            

    def on_cancel(self,event):

        main_frame = wx.GetTopLevelParent(self)  
        main_frame.Destroy()
     
        
    def on_number_of_layers_change(self, event):
        ctrl = event.GetEventObject()
        value = ctrl.GetValue()
    
        if value.isdigit():
            number = int(value)
            if number > 8:
                wx.Bell()  # sound feedback
                ctrl.SetValue("8")
                ctrl.SetInsertionPointEnd()
        elif value:  # contains something but not digits
            wx.Bell()
            ctrl.SetValue("")
        

    def on_number_only(self, event):
        key_code = event.GetKeyCode()
        if key_code in (wx.WXK_BACK, wx.WXK_DELETE):  # Allow backspace, delete
            event.Skip()
            return
    
        char = chr(key_code)
#        ctrl = event.GetEventObject()
    
        if char.isdigit() or char == ".":
            event.Skip()
        else:
            wx.Bell()
    
 
    def validate_numeric_input(self, event):
        ctrl = event.GetEventObject()
        value = ctrl.GetValue().strip()
    
        if value == "":
            wx.Bell()
            wx.MessageBox("Please enter a numeric value.",
                          "Missing Input", wx.ICON_WARNING)
            ctrl.SetFocus()
            return
    
        try:
            float(value)  # Valid number
        except ValueError:
            wx.Bell()
            wx.MessageBox("Only numeric input is allowed.", 
                          "Invalid Input", wx.ICON_WARNING)
            ctrl.SetValue("")
            ctrl.SetFocus()
    
        event.Skip()


         
class PageTwo(wx.Panel):
    def __init__(self, parent, main_frame, layer_input):
        super().__init__(parent)
        self.main_frame = main_frame

        main_layout = wx.BoxSizer(wx.VERTICAL)

        text = wx.StaticText(self, label="Layer Wizard - Please enter 0, 90, +45 or -45.")
        main_layout.Add(text, flag=wx.ALL, border=10)

        self.Inputs = []
        layer_orientation_dropdown = ["0", "90", "+45", "-45"]

        # Determine number of columns and rows
        columns = (layer_input + 3) // 4  # ceiling division to wrap every 4
        rows = min(4, layer_input)

        grid_sizer = wx.FlexGridSizer(rows=rows, cols=columns, hgap=20, vgap=10)

        for i in range(layer_input):  # Generate input fields
            label = wx.StaticText(self, label=f"Layer {i + 1}:")
            choice_ctrl = wx.Choice(self, choices=layer_orientation_dropdown)
            choice_ctrl.SetSelection(0)

            self.Inputs.append(choice_ctrl)

            sub_sizer = wx.BoxSizer(wx.VERTICAL)
            sub_sizer.Add(label, flag=wx.BOTTOM, border=2)
            sub_sizer.Add(choice_ctrl, flag=wx.BOTTOM, border=5)

            grid_sizer.Add(sub_sizer, flag=wx.ALL, border=5)

        main_layout.Add(grid_sizer, flag=wx.ALL, border=10)

        # Back and OK buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        back_btn = wx.Button(self, label="Back")
        ok_btn = wx.Button(self, label="Ok")

        back_btn.Bind(wx.EVT_BUTTON, lambda event: main_frame.show_page_one())
        ok_btn.Bind(wx.EVT_BUTTON, self.on_ok)

        button_sizer.Add(back_btn, flag=wx.RIGHT, border=5)
        button_sizer.Add(ok_btn, flag=wx.RIGHT, border=5)

        main_layout.Add(button_sizer, flag=wx.ALIGN_RIGHT | wx.ALL, border=10)

        self.SetSizer(main_layout)
        
    def on_ok(self, event):
        
        selected_values = [choice.GetStringSelection() for choice in self.Inputs]

        
        self.main_frame.store_layer_values(selected_values)

class NCUDC(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Non-Crimp Unidirectional Model Wizard", size=(650, 500))

        self.panel = wx.Panel(self)
        self.main_layout = wx.BoxSizer(wx.VERTICAL)
        
        self.layer_input = None
        self.yarn_spacing_input = None
        self.yarn_width_input = None
        self.fabric_thickness_input = None
        self.domain_size_input = None
        self.selected_orientations = None  # For PageTwo
        self.stitch_type_input = None
        self.stitch_thickness_input = None

        self.page_one = PageOne(self.panel, self.show_page_two)
        self.page_two = None


        self.main_layout.Add(self.page_one, 1, wx.EXPAND)
        self.panel.SetSizer(self.main_layout)
        
        
        self.Centre()
        self.Show()
        
        
    def show_page_two(self, layer_input, yarn_spacing, yarn_width, fabric_thickness, domain_size, stitch_thickness, stitch_type):
        
        # Store PageOne values
        self.layer_input = layer_input
        self.yarn_spacing_input = yarn_spacing
        self.yarn_width_input = yarn_width
        self.fabric_thickness_input = fabric_thickness
        self.domain_size_input = domain_size
        self.stitch_type_input = stitch_type
        self.stitch_thickness_input = stitch_thickness

        self.main_layout.Hide(self.page_one)  # Hide PageOne

        if self.page_two:
            if self.page_two.GetContainingSizer():
                self.page_two.GetContainingSizer().Detach(self.page_two)  # Detach safely
            self.page_two.Destroy()

        # Pass stored values to PageTwo
        self.page_two = PageTwo(self.panel, self, layer_input)
        self.main_layout.Add(self.page_two, 1, wx.EXPAND)
        self.main_layout.Layout()
        

    def show_page_one(self):
        
        self.main_layout.Hide(self.page_two)  # Hide PageTwo

        if self.page_two:
            self.page_two.Destroy()  # Deleting PageTwo when pressing back button

        self.page_one.Show()
        self.main_layout.Layout()
        
    def store_layer_values(self, orientations):
        """ Store PageTwo values and print final selections. """
        self.selected_orientations = orientations

        # Print all collected values
        print("Final Input Values:")
        print(f"Number of Layers: {self.layer_input}")
        print(f"Yarn Spacing: {self.yarn_spacing_input}")
        print(f"Yarn Width: {self.yarn_width_input}")
        print(f"Fabric Thickness: {self.fabric_thickness_input}")
        print(f"Domain Size: {self.domain_size_input}")
        print(f"Layer Orientations: {self.selected_orientations}")
        print(f"Stitch Type: {self.stitch_type_input}")
        print(f"Stitch Thickness: {self.stitch_thickness_input}")

        # Close the wizard after storing data
        self.Destroy()
        
        if self.stitch_type_input == "Tricot":
            ModelScriptTricot(self.layer_input, self.yarn_width_input, self.yarn_spacing_input, 
                        self.fabric_thickness_input, self.domain_size_input,
                        self.stitch_thickness_input, self.selected_orientations)
 

app = wx.App(False)
frame = NCUDC()
app.MainLoop()
    

    