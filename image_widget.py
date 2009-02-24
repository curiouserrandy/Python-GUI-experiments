#!/usr/bin/python

import traceback
from Tkinter import *
from PIL import Image
import ImageTk

debug = 0

## Naming conventions for this file:
##	"dbg_" prefix: Debugigng function
##	Simple noun: Mathematical function converting inputs to that noun
##	"ev_<event>" prefix: Event handler for the named event
##	"evv_<name>": Variable used by event handlers only (no higher level)
##	"_action" suffix: Handle implementing the response to a user's
##			  action (which needs to be interpretted from the
##			  events; e.g. it's not a drag unless the mouse moves
##			  at least 5 pixels)

class NotYetImplemented(Exception): pass

## Stored integer intervals (eg. xint) here are always [inclusive, exclusive)
## Mapnum intervals are not, because we're often mapping to 0,1 in float;
## they are (inclusive, inclusive).

## Debugging functions
def dbg_display_args(*args):
    print "Args: ", args

def dbg_display_event(event):
    print event.__dict__

def dbg_display_tag_and_size(tag, event):
    print tag, ": ", event.width, event.height, event.serial, repr(event.widget)

def dbg_print_coords(x, y):
    print "Coords: ", x, y

## Transformation functions

def distance_squared(c1, c2):
    "Return the square of the distance between two sets of coords."
    (dx,dy) = (c1[0] - c2[0], c1[1] - c2[1])
    return dx*dx + dy*dy

def mapped_number(x, fromrange, torange):
    assert fromrange[0] <= x <= fromrange[1], (fromrange[0], x, fromrange[1])
    assert torange[0] <= torange[1], (torange[0], torange[1])
    ## Need to force floating point
    x *= 1.0
    return (x - fromrange[0]) / (fromrange[1] - fromrange[0]) * (torange[1] - torange[0]) + torange[0]

def difference(coord_a, coord_b):
    return (coord_b[0] - coord_a[0], coord_b[1] - coord_a[1])

class ImageWidget(Frame):
    def __init__(self, parent, gfunc, image_size, **kwargs):
        """Create an Image Widget which will display an image based on the
        function passed.  That function will be called with the arguments
        (zoom_factor, (xstart, xend), (ystart, yend)) and must return a
        TkInter PhotoImage object of size (xend-xstart, yend-ystart).
        IMAGE_SIZE describes the "base size" of the image being backed by
        gfunc.
        starting_* describes the starting window on the image."""

        ## Init parent
        Frame.__init__(self, parent)

        ## Set variables from kwargs, defaulting appropriately
        starting_zoom = kwargs.get("starting_zoom", 1.0)
        starting_size = kwargs.get("starting_size", image_size)
        starting_ul = kwargs.get("starting_ul", (0,0))
        ## Called when the mouse moves (without button down) in the image
        ## args are (x,y) and are in the unzoomed coordinate system
        self.track_func = kwargs.get("mouse_tracking_function", None)
        ## Called when the user clicks the mouse in the image
        ## (button press followed by button release without dragging)
        ## args are (x,y) and are in the unzoomed coordinate system
        self.click_func = kwargs.get("mouse_click_function", None)

        ## XXX: See if there's anything you don't know about and if so throw an
        ## error

        ## Base image parameters
        self.generator_func = gfunc
        self.isize = image_size
        self.canvas_image_id = None

        ## Modifier of base image size for coords currently working in
        self.zoom = starting_zoom

        ## Interval of augmented (zoomed) image currently shown
        ## Note that these must be integers; these map directly to pixels
        self.xint = [starting_ul[0], starting_ul[0] + starting_size[0]]
        self.yint = [starting_ul[1], starting_ul[1] + starting_size[1]]

        ## Event control
        self.evv_buttonDown = False
        self.evv_dragging = False
        self.evv_dragStart = None
        self.evv_lastActiveMouse = None

        ## Widgets
        self.canvas = Canvas(self)
        self.hscroll = Scrollbar(self, orient = HORIZONTAL,
                                 command = self.xview_action)
        self.vscroll = Scrollbar(self, orient = VERTICAL,
                                 command = self.yview_action)
        
        (self.canvas["width"], self.canvas["height"]) = starting_size

        # "scrollregion" set in refresh method.
        self.canvas.bind("<Configure>", self.ev_Configure)
        self.canvas.bind("<Button-1>", self.ev_Button_1)
        self.canvas.bind("<Motion>", self.ev_Motion)
        self.canvas.bind("<ButtonRelease-1>", self.ev_ButtonRelease_1)
        self.canvas.bind("<Leave>", self.ev_Leave)
        self.canvas.bind("<MouseWheel>", self.ev_MouseWheel)

        self.canvas_origin_offset = (int(self.canvas["borderwidth"])
                                     + int(self.canvas["highlightthickness"]))

        ## Configure widgets
        self.canvas.grid(row = 0, column = 0, sticky=N+S+E+W)
        self.hscroll.grid(row = 1, column = 0, sticky=E+W)
        self.vscroll.grid(row = 0, column = 1, sticky=N+S)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        ## And display
        self.refresh()

    ## XXX: Need to figure out and specify what coordinates arguments to the
    ## action functions should be in.
    ## Currently, canvas coords
    def move_action(self, diff):
        "Respond as appropriate to the user moving the mouse DIFF pixels (not dragging)."
        if self.track_func:
            self.track_func(int(diff[0] / self.zoom), int(diff[1] / self.zoom))

    def click_action(self, coord):
        "Respond as appropriate to the user clicking the mouse button in coord x,y."
        if self.click_func:
            self.click_func(int(coord[0] / self.zoom), int(coord[1] / self.zoom))

    def scrollWheel_action(self, count):
        "Respond as appropriate to the scroll wheel being clicked count times."
        ## Turn into hardcoded constant
        zoomFactor = pow(1.20, count)
        self.zoom = zoomFactor
        self.refresh()

    def resize_action(self, newsize):
        "Respond as appropriate to a resize event."
        orig = (self.xint[1], self.yint[1])
        self.xint[1] = min(self.xint[0]+newsize[0],
                           int(self.isize[0]*self.zoom))
        self.yint[1] = min(self.yint[0]+newsize[1],
                           int(self.isize[1]*self.zoom))
        if (self.xint[1], self.yint[1]) != orig:
            self.refresh()

    def drag_action(self, diff):
        "Respond as appropriate to the user dragging the mouse DIFF pixels (x,y)."
        origx = [i for i in self.xint]
        origy = [i for i in self.yint]
        self.general_scroll_action(self.xint, self.isize[0], diff[0])
        self.general_scroll_action(self.yint, self.isize[1], diff[1])
        if origx != self.xint or origy != self.yint: self.refresh()

    ## These next two are somewhere between event handlers and actions;
    ## they're being put in the action class since they seem closer to a
    ## user intent than a mouse click.  But I wouldn't have chosen
    ## this interface.
    def xview_action(self, subaction, *args):
        "Handle an xscroll request from a scrollbar."
        orig = [i for i in self.xint]
        self.starview_action(self.xint, self.isize[0], subaction, *args)
        if orig != self.xint: self.refresh()

    def yview_action(self, subaction, *args):
        "Handle an yscroll request from a scrollbar."
        orig = [i for i in self.yint]
        self.starview_action(self.yint, self.isize[1], subaction, *args)
        if orig != self.yint: self.refresh()

    # Helper methods for {drag,xview,yview}_action
    @staticmethod
    def general_scroll_action(axis_int, axis_size, scroll_amount):
        (s, l) = (axis_int[0], axis_int[1] - axis_int[0])
        s += scroll_amount
        s = max(0, min(axis_size - l, s))
        axis_int[0] = s
        axis_int[1] = s + l

    @staticmethod
    def starview_action(axis_int, axis_size, subaction, *args):
        "Handle a scroll request from a scrollbar."
        scrollnum = 0
        if subaction == "scroll":
            (scrollnum, scrolltype) = args
            if scrolltype == "pages":
                scrollnum *= (axis_int[1] - axis_int[0])
            else:
                assert scrolltype == "units"
        elif subaction == "moveto":
            frac = float(args[0])
            scrollnum = int(axis_size * frac) - axis_int[0]
        else:
            assert False, ("general_scroll_action: Unknown subaction ", subaction)
        ImageWidget.general_scroll_action(axis_int, axis_size, scrollnum)

    def ev_Button_1(self, event):
        self.evv_buttonDown = True
        self.evv_dragging = False
        self.evv_dragStart = (event.x, event.y)
        self.evv_lastActiveMouse = self.evv_dragStart

    def ev_Motion(self, event):
        if not self.evv_buttonDown:
            ## Notify handler of new location
            if self.track_func:
                self.track_func(int(self.canvas.canvasx(event.x) / self.zoom),
                                int(self.canvas.canvasy(event.y) / self.zoom))
        else:
            if self.evv_dragging:
                ## Already detected a drag; move since last ev_Motion event
                self.drag_action(difference((event.x,event.y),
                                            self.evv_lastActiveMouse))
            else:
                ## Need to confirm we've been pulled enough to start dragging;
                ## we might just be in the middle of a sloppy click
                if distance_squared(self.evv_dragStart, (event.x,event.y)) > 25:
                    # XXX: Make 25 defined constant
                    self.drag_action(difference((event.x,event.y),
                                                self.evv_dragStart))
                    self.evv_dragging = True
                else:
                    ## Assuing we're in the middle of a sloppy click
                    pass
        self.evv_lastActiveMouse = (event.x, event.y)

    def ev_ButtonRelease_1(self, event):
        if self.evv_lastActiveMouse != (event.x, event.y):
            # Ignoring this case for now; it's rare, and I don't think will
            # cause any surprising behavior to the user (i.e. it wouldn't
            # only be relevant if they're doing something funky, and wouldn't
            # change the final position by much then.)
            # print "Movement between ev_Motion and ButtonRelease: ", self.lastActiveMouse, " -> ", (event.x, event.y)
            pass
        if not self.evv_dragging:
            ## This was a click
            self.click_action((int(self.canvas.canvasx(event.x)),
                              int(self.canvas.canvasy(event.y))))
        self.evv_dragging = False
        self.evv_buttonDown = False
        self.evv_dragStart = None
        # Only need to do anything real here if I'm doing click or rectangle
        # outline or there's mousemovement between ev_Motion and ev_ButtonRelease_1. 

    def ev_Leave(self, event):
        if self.evv_buttonDown:
            self.evv_dragging = False
            self.evv_buttonDown = False
            self.evv_dragStart = None

    def ev_MouseWheel(self, event):
        self.scrollWheel_action(event.delta)

    def ev_Configure(self, event):
        self.resize_action((event.width, event.height))

    def refresh(self):
        """Bring the image in the frame and the scroll bars in line with the
        current values.  Note that this is not done for scrolling; that's
        taken care of directly by the scrollbar/canvas interactions.
        xint & yint are updated automatically for scrolling."""

        # Delete old image (if needed) and create new one
        if self.canvas_image_id:
            self.canvas.delete(self.canvas_image_id)
        if debug > 5:
            print "refresh: New image (x", self.zoom, ") ", self.xint, self.yint
        self.image = self.generator_func(self.zoom, self.xint, self.yint)

        self.canvas_image_id = self.canvas.create_image(0, 0, anchor=N+W,
                                                        image=self.image)

        # Figure out where scroll bars should be and put them there.
        scroll_settings = (
            (mapped_number(self.xint[0],
                    (0, self.isize[0] * self.zoom -1),
                    (0, 1)),
             mapped_number(self.xint[1] -1,
                    (0, self.isize[0] * self.zoom -1),
                    (0, 1))),
            (mapped_number(self.yint[0],
                    (0, self.isize[1] * self.zoom -1),
                    (0, 1)),
             mapped_number(self.yint[1] -1,
                    (0, self.isize[1] * self.zoom -1),
                    (0, 1))))
        if debug > 5:
            print scroll_settings
        self.hscroll.set(*scroll_settings[0])
        self.vscroll.set(*scroll_settings[1])




## Room for optimization here; don't need to resize the whole image
def gfunc_for_image(image, zoom, xint, yint):
    bbox = image.getbbox()
    isize = (bbox[2] - bbox[0], bbox[3] - bbox[1])
    ssize = (int(isize[0] * zoom), int(isize[1] * zoom))

    if debug > 5:
        print zoom, xint, yint, isize, ssize
    ri = image.resize(ssize, Image.BILINEAR)
    ci = ri.crop((xint[0],yint[0],xint[1],yint[1]))
    ki = ImageTk.PhotoImage(ci)
    return ki

def IWFromFile(parent, file, **kwargs):
    "Return an ImageWidget object based on an image on a file."
    baseimage = Image.open(file)
    (ulx, uly, lrx, lry) = baseimage.getbbox()
    return ImageWidget(parent,
                       lambda z,xint,yint,i=baseimage: gfunc_for_image(i, z, xint, yint),
                       (lrx - ulx, lry - uly),
                       **kwargs)

def IWFromImage(parent, img, **kwargs):
    "Return an imageWidget object based on a PIL image passed in."
    (ulx, uly, lrx, lry) = img.getbbox()
    return ImageWidget(parent,
                       lambda z,xint,yint,i=img: gfunc_for_image(i, z, xint, yint),
                       (lrx - ulx, lry - uly),
                       **kwargs)


if __name__ == "__main__":
    root = Tk()
    root.resizable(True, True)

    # root.bind("<Configure>", lambda e, t="root": dbg_display_tag_and_size(t, e))
    iw = IWFromFile(root, "iw_test.tiff", starting_ul = (100,100),
                    starting_size = (200, 200), starting_zoom = 1.0,
                    mouse_click_function = dbg_print_coords)
    iw.grid(row=0,column=0,sticky=N+S+E+W)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    iw.mainloop()


