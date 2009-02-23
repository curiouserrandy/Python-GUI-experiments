#!/usr/local/bin/python

import struct
import re
import socket
import Image
import sys

class cstruct(object):
    def __init__(self, eles):
        for e in eles:
            self.__dict__[e] = None

## Debug constants
DebugPrintBytes = 7
DebugPrintProtocol = 5
DebugSaveFBUpdate = 4
DebugPrintRFBDetails = 3
DebugPrintRFBMessages = 2

# Keysym constants

class KeySyms(object):
    BackSpace = 0xFF08
    Tab = 0xFF09
    Linefeed = 0xFF0A
    Clear = 0xFF0B
    Return = 0xFF0D
    Pause = 0xFF13
    Scroll_Lock = 0xFF14
    Sys_Req = 0xFF15
    Escape = 0xFF1B
    Delete = 0xFFFF

    Home = 0xFF50
    Left = 0xFF51
    Up = 0xFF52
    Right = 0xFF53
    Down = 0xFF54
    Prior = 0xFF55
    Page_Up = 0xFF55
    Next = 0xFF56
    Page_Down = 0xFF56
    End = 0xFF57
    Begin = 0xFF58

    Select = 0xFF60
    Print = 0xFF61
    Execute = 0xFF62
    Insert = 0xFF63
    Undo = 0xFF65
    Redo = 0xFF66
    Menu = 0xFF67
    Find = 0xFF68
    Cancel = 0xFF69
    Help = 0xFF6A
    Break = 0xFF6B
    Mode_switch = 0xFF7E
    script_switch = 0xFF7E
    Num_Lock = 0xFF7F

    KP_Space = 0xFF80
    KP_Tab = 0xFF89
    KP_Enter = 0xFF8D
    KP_F1 = 0xFF91
    KP_F2 = 0xFF92
    KP_F3 = 0xFF93
    KP_F4 = 0xFF94
    KP_Home = 0xFF95
    KP_Left = 0xFF96
    KP_Up = 0xFF97
    KP_Right = 0xFF98
    KP_Down = 0xFF99
    KP_Prior = 0xFF9A
    KP_Page_Up = 0xFF9A
    KP_Next = 0xFF9B
    KP_Page_Down = 0xFF9B
    KP_End = 0xFF9C
    KP_Begin = 0xFF9D
    KP_Insert = 0xFF9E
    KP_Delete = 0xFF9F
    KP_Equal = 0xFFBD
    KP_Multiply = 0xFFAA
    KP_Add = 0xFFAB
    KP_Separator = 0xFFAC
    KP_Subtract = 0xFFAD
    KP_Decimal = 0xFFAE
    KP_Divide = 0xFFAF

    KP_0 = 0xFFB0
    KP_1 = 0xFFB1
    KP_2 = 0xFFB2
    KP_3 = 0xFFB3
    KP_4 = 0xFFB4
    KP_5 = 0xFFB5
    KP_6 = 0xFFB6
    KP_7 = 0xFFB7
    KP_8 = 0xFFB8
    KP_9 = 0xFFB9

    F1 = 0xFFBE
    F2 = 0xFFBF
    F3 = 0xFFC0
    F4 = 0xFFC1
    F5 = 0xFFC2
    F6 = 0xFFC3
    F7 = 0xFFC4
    F8 = 0xFFC5
    F9 = 0xFFC6
    F10 = 0xFFC7
    F11 = 0xFFC8
    L1 = 0xFFC8
    F12 = 0xFFC9
    L2 = 0xFFC9
    F13 = 0xFFCA
    L3 = 0xFFCA
    F14 = 0xFFCB
    L4 = 0xFFCB
    F15 = 0xFFCC
    L5 = 0xFFCC
    F16 = 0xFFCD
    L6 = 0xFFCD
    F17 = 0xFFCE
    L7 = 0xFFCE
    F18 = 0xFFCF
    L8 = 0xFFCF
    F19 = 0xFFD0
    L9 = 0xFFD0
    F20 = 0xFFD1
    L10 = 0xFFD1
    F21 = 0xFFD2
    R1 = 0xFFD2
    F22 = 0xFFD3
    R2 = 0xFFD3
    F23 = 0xFFD4
    R3 = 0xFFD4
    F24 = 0xFFD5
    R4 = 0xFFD5
    F25 = 0xFFD6
    R5 = 0xFFD6
    F26 = 0xFFD7
    R6 = 0xFFD7
    F27 = 0xFFD8
    R7 = 0xFFD8
    F28 = 0xFFD9
    R8 = 0xFFD9
    F29 = 0xFFDA
    R9 = 0xFFDA
    F30 = 0xFFDB
    R10 = 0xFFDB
    F31 = 0xFFDC
    R11 = 0xFFDC
    F32 = 0xFFDD
    R12 = 0xFFDD
    F33 = 0xFFDE
    R13 = 0xFFDE
    F34 = 0xFFDF
    R14 = 0xFFDF
    F35 = 0xFFE0
    R15 = 0xFFE0

    Shift_L = 0xFFE1
    Shift = Shift_L
    Shift_R = 0xFFE2
    Control_L = 0xFFE3
    Control = Control_L
    Control_R = 0xFFE4
    Caps_Lock = 0xFFE5
    Shift_Lock = 0xFFE6

    Meta_L = 0xFFE7
    Meta = Meta_L
    Meta_R = 0xFFE8
    Alt_L = 0xFFE9
    Alt = Alt_L
    Alt_R = 0xFFEA
    Super_L = 0xFFEB
    Super = Super_L
    Super_R = 0xFFEC
    Hyper_L = 0xFFED
    Hyper = Hyper_L
    Hyper_R = 0xFFEE
    space = 0x020
    exclam = 0x021
    quotedbl = 0x022
    numbersign = 0x023
    dollar = 0x024
    percent = 0x025
    ampersand = 0x026
    apostrophe = 0x027
    quoteright = 0x027
    parenleft = 0x028
    parenright = 0x029
    asterisk = 0x02a
    plus = 0x02b
    comma = 0x02c
    minus = 0x02d
    period = 0x02e
    slash = 0x02f
    N0 = 0x030
    N1 = 0x031
    N2 = 0x032
    N3 = 0x033
    N4 = 0x034
    N5 = 0x035
    N6 = 0x036
    N7 = 0x037
    N8 = 0x038
    N9 = 0x039
    colon = 0x03a
    semicolon = 0x03b
    less = 0x03c
    equal = 0x03d
    greater = 0x03e
    question = 0x03f
    at = 0x040
    A = 0x041
    B = 0x042
    C = 0x043
    D = 0x044
    E = 0x045
    F = 0x046
    G = 0x047
    H = 0x048
    I = 0x049
    J = 0x04a
    K = 0x04b
    L = 0x04c
    M = 0x04d
    N = 0x04e
    O = 0x04f
    P = 0x050
    Q = 0x051
    R = 0x052
    S = 0x053
    T = 0x054
    U = 0x055
    V = 0x056
    W = 0x057
    X = 0x058
    Y = 0x059
    Z = 0x05a
    bracketleft = 0x05b
    backslash = 0x05c
    bracketright = 0x05d
    asciicircum = 0x05e
    underscore = 0x05f
    grave = 0x060
    quoteleft = 0x060
    a = 0x061
    b = 0x062
    c = 0x063
    d = 0x064
    e = 0x065
    f = 0x066
    g = 0x067
    h = 0x068
    i = 0x069
    j = 0x06a
    k = 0x06b
    l = 0x06c
    m = 0x06d
    n = 0x06e
    o = 0x06f
    p = 0x070
    q = 0x071
    r = 0x072
    s = 0x073
    t = 0x074
    u = 0x075
    v = 0x076
    w = 0x077
    x = 0x078
    y = 0x079
    z = 0x07a
    braceleft = 0x07b
    bar = 0x07c
    braceright = 0x07d
    asciitilde = 0x07e


    nobreakspace = 0x0a0
    exclamdown = 0x0a1
    cent = 0x0a2
    sterling = 0x0a3
    currency = 0x0a4
    yen = 0x0a5
    brokenbar = 0x0a6
    section = 0x0a7
    diaeresis = 0x0a8
    copyright = 0x0a9
    ordfeminine = 0x0aa
    guillemotleft = 0x0ab
    notsign = 0x0ac
    hyphen = 0x0ad
    registered = 0x0ae
    macron = 0x0af
    degree = 0x0b0
    plusminus = 0x0b1
    twosuperior = 0x0b2
    threesuperior = 0x0b3
    acute = 0x0b4
    mu = 0x0b5
    paragraph = 0x0b6
    periodcentered = 0x0b7
    cedilla = 0x0b8
    onesuperior = 0x0b9
    masculine = 0x0ba
    guillemotright = 0x0bb
    onequarter = 0x0bc
    onehalf = 0x0bd
    threequarters = 0x0be
    questiondown = 0x0bf
    Agrave = 0x0c0
    Aacute = 0x0c1
    Acircumflex = 0x0c2
    Atilde = 0x0c3
    Adiaeresis = 0x0c4
    Aring = 0x0c5
    AE = 0x0c6
    Ccedilla = 0x0c7
    Egrave = 0x0c8
    Eacute = 0x0c9
    Ecircumflex = 0x0ca
    Ediaeresis = 0x0cb
    Igrave = 0x0cc
    Iacute = 0x0cd
    Icircumflex = 0x0ce
    Idiaeresis = 0x0cf
    ETH = 0x0d0
    Eth = 0x0d0
    Ntilde = 0x0d1
    Ograve = 0x0d2
    Oacute = 0x0d3
    Ocircumflex = 0x0d4
    Otilde = 0x0d5
    Odiaeresis = 0x0d6
    multiply = 0x0d7
    Ooblique = 0x0d8
    Oslash = Ooblique
    Ugrave = 0x0d9
    Uacute = 0x0da
    Ucircumflex = 0x0db
    Udiaeresis = 0x0dc
    Yacute = 0x0dd
    THORN = 0x0de
    Thorn = 0x0de
    ssharp = 0x0df
    agrave = 0x0e0
    aacute = 0x0e1
    acircumflex = 0x0e2
    atilde = 0x0e3
    adiaeresis = 0x0e4
    aring = 0x0e5
    ae = 0x0e6
    ccedilla = 0x0e7
    egrave = 0x0e8
    eacute = 0x0e9
    ecircumflex = 0x0ea
    ediaeresis = 0x0eb
    igrave = 0x0ec
    iacute = 0x0ed
    icircumflex = 0x0ee
    idiaeresis = 0x0ef
    eth = 0x0f0
    ntilde = 0x0f1
    ograve = 0x0f2
    oacute = 0x0f3
    ocircumflex = 0x0f4
    otilde = 0x0f5
    odiaeresis = 0x0f6
    division = 0x0f7
    oslash = 0x0f8
    ooblique = oslash
    ugrave = 0x0f9
    uacute = 0x0fa
    ucircumflex = 0x0fb
    udiaeresis = 0x0fc
    yacute = 0x0fd
    thorn = 0x0fe
    ydiaeresis = 0x0ff

## This is a python module implementing an RFB protocol object endpoint.

class ProtocolEndpoint(object):
    def __init__(self, host, port, debug=0):
        print self
        self.sock = socket.socket()
        addr = socket.gethostbyname(host)
        self.sock.connect((addr, port))
        self.debug = debug

    def close(self):
        self.sock.close()

    def __simpleread(self, descr):
        """Read a protocol message using the given struct template
        directly from the endpoint."""
        size = struct.calcsize(descr)
        inp = ""
        while len(inp) < size:
            br = self.sock.recv(size - len(inp))
            if self.debug >= DebugPrintBytes:
                print >> sys.stderr, "Bytes received on socket: ", [hex(ord(z)) for z in br] 
            inp += br
        return struct.unpack(descr, inp)

    def __simplewrite(self, descr, tuple):
        tmp = struct.pack(descr, *tuple)
        while len(tmp) > 0:
            bw = self.sock.send(tmp)
            if self.debug >= DebugPrintBytes:
                print >> sys.stderr, "Bytes send on socket: ", [hex(ord(z)) for z in tmp[0:bw]]
            tmp = tmp[bw:]

    ## Read/write functions.  General philosophy is that the format on the
    ## wire should be determined by the descriptor, and the format
    ## passed/returned in to the function should be determined by
    ## the function.
    def readele(self, descr):
        """DESCR describes a single argument on the protocol stream, which 
        is returned from the routine."""
        result = self.__simpleread(descr)
        assert len(result) == 1
        if self.debug >= DebugPrintProtocol:
            print >> sys.stderr, "Protocol read (%s): " % descr, result[0]
        return result[0]

    def readlist(self, descr):
        """DESCR describes a (fixed) set of arguments on the protocol stream,
        which are returned as a list."""
        result = self.__simpleread(descr)
        if self.debug >= DebugPrintProtocol:
            print >> sys.stderr, "Protocol read (%s): " % descr, result
        return result

    def readvarlist(self, descr):
        """DESCR is a two element sequence; the first element describes the
        number of elements in the list, and the second each individual element
        on the list (the endian marker from the first element is applied to the
        second.)  The return value is a list of the appropriate length.  This
        list will be either in the form (e1, e2, e3, ...) if DESCR[1] describes
        a single element or ( (a1, b1, c1), (a2, b2, c2), ...) otherwise."""
        assert len(descr) == 2 and not isinstance(descr, str)
        l = self.__simpleread(descr[0])
        assert len(l) == 1
        l = l[0]
        d2 = descr[0][0] + descr[1] * l
        result = self.__simpleread(d2)
        if len(result) != l:
            # Nest
            r2 = []
            while result:
                r2.append(result[0:l])
                result = result[l:]
        if self.debug >= DebugPrintProtocol:
            print >> sys.stderr, "Protocol read (%s,%s): " % descr, result
        return result

    def readstring(self, lengthdescr):
        """Read string from the protocol stream.
        LENGTHDESCR describes the format in which the string length
        will be read from the wire; the format of the following string
        is assumed to be <LENGTH>s."""
        l = self.__simpleread(lengthdescr)
        d2 = lengthdescr[0] + "%ds" % l
        result = self.__simpleread(d2)
        if self.debug >= DebugPrintProtocol:
            print >> sys.stderr, "Protocol string read (%s): " % lengthdescr, result
        return result

    def writeargs(self, descr, *args):
        """DESCR describes a (fixed) set of arguments on the protocol stream,
        ARGS are written to the stream using that descriptor.  The number of
        args passed must match DESCR."""
        if self.debug >= DebugPrintProtocol:
            print >> sys.stderr, "Protocol write (%s): " % descr, args
        self.__simplewrite(descr, args)

    def writevarlist(self, descr, eles):
        """DESCR is a two element sequence; the first element describes the
        number of elements in the list, and the second each individual element
        on the list (the endian marker from the first element is applied to the
        second.)  The passed list is written to the stream using that
        descriptor.  The elements of the list must match the descriptor as
        described in the documentation for readvarlist."""
        assert len(descr) == 2 and not isinstance(descr, str)
        if self.debug >= DebugPrintProtocol:
            print >> sys.stderr, "Protocol write (%s,%s): " % descr, eles
        l = len(eles)
        self.__simplewrite(descr[0], (l,))
        d2 = descr[0][0] + descr[1] * l
        if isinstance(eles[0], (tuple,list)): 
            # Flatten
            eles = reduce(lambda x,y:x+y, eles)
        self.__simplewrite(d2, eles)

    def writestring(self, lengthdescr, s):
        """Write a string to the protocol stream in a "length, string"
        format.  LENGTHDESCR describes the format for the length; the string is
        assumed to have format <LENGTH>s."""
        if self.debug >= DebugPrintProtocol:
            print >> sys.stderr, "Protocol string write (%s): " % lengthdescr, s
        l = len(s)
        self.__simplewrite(lengthdescr, (l,))
        d2 = lengthdescr[0] + "%ds" % l
        self.__simplewrite(d2, (s,))
                

##### Notes on RFBEndpoint
# Almost all helper routines are put outside of the class itself, as a way
# of keeping the namespace minimized and focussed on user tasks.              
# Protocol formats, helper routines, and helper constants defined below,
# before the actual class.            

# Protocol formats, structured by protocol interaction
# Handshake 
Version = ">12s"                # "RFB %03d.%03d".  3.3, 3.7, or 3.8
SecTypes = (">B", "B")
SecType = ">B"                  # One per NumSecTypes
				# 0: Invalid
                                # 1: None
                                # 2: VNC Authentication
FailureReason = ">L"            # For many different failures
VncAuthExchange = ">16B"
SecResult = ">L"                # 0 OK, 1 Failed
# Init
ClientInit = ">B"               # 1 shared, 0 exclusive
ServerInit1 = ">HH"             # fb-width, fb-height
PixelFormat = ">BBBBHHHBBBxxx" 	# bits-per-pixel,
				# depth, big-endian-flag
                                # true-color-flag
                                # red-max
                                # green-max
                                # blue-max
                                # red-shift
                                # green-shift
                                # blue-shift
ServerInit2 = ">L"              # Name string

######## Regular Messages, Client ######
ClientMessageType = ">B"        # 0 SetPixelFormat
				# 2 SetEncodings
                                # 3 FramebufferUpdateRequest
                                # 4 KeyEvent
                                # 5 PointerEvent
                                # 6 ClientCutText
                                # ClientMessageType is first byte of
                                # all client messges
# SetPixelFormat: ClientMessageType + "xxx" + PixelFormat
SetEncodings = (">xH", "l") # List of encodings allowed/prefered by client
				# 0: Raw, 1: CopyRect, 2: RRE, 5: Hextile
                                # 16: ZRLE, -239: Cursor Psuedo
                                # -223: DesktopSize Pseudo
FrameBufferUpdateReq = ">BHHHH" # incremental: 1/0 (true/false)
				# x, y, width, height
KeyEvent = ">BxxL"              # down-flag, keysym (usually ascii)
PointerEvent = ">BHH"           # button-mask, x, y
CutText = ">xxxL"

####### Regular Messages, Server ######
serverMessageType = ">B" 	# 0: FrameBufferUpdate, 1 SetColourMapEntries,
				# 2: Bell, 3: ServerCutText
FrameBufferHeader = ">xH"       # Number of rectangles
FrameBufferRectangleHeader = ">HHHHl" # x, y, width, height, encoding type

## Currently supporting only 0 & 1 (raw and copy rect)
## (-239 is also supported, but that just says not to send the cursor)
## Raw encoding is w X h X bytes per pixel and is done by hand
FrameBufferCopyRect = ">HH"     # src-x, src-y

SetColourMapEntries1 = ">xH"         # first color
SetColourMapEntries2 = (">H", "HHH") # number of colors, colors
Bell = ""                   # Nothing other than message type
# ServerCutText same as ClientCutText above.

# Helper routines for below class that I want easily accessible and 
# not in the exported namespace

def RFBHandshake(rfbe):
    """Do initial handshake with VNC server.  Modifies rfbe fields directly;
    should be considered a private method of RFBEndpoint."""

    #### Version handshake
    serverVersion = rfbe.readele(Version)
    # We can handle 3.3, 3.7, 3.8
    if not re.match(r"RFB [0-9]{3}\.[0-9]{3}\n", serverVersion):
        raise RFBEndpoint.BadFormat, ("Bad Version String: " + serverVersion)
    if rfbe.debug >= DebugPrintRFBDetails:
        print >> sys.stderr, "RFB version: ", serverVersion
    major = int(serverVersion[4:7])
    minor = int(serverVersion[8:11])
    if (major < 3 or (major == 3 and minor <= 8 and minor not in (3, 7, 8))):
        raise RFBEndpoint.BadVersion, ("%d.%d" % (major, minor))
    rfbe.major = 3
    rfbe.minor = min(8, minor)
    rfbe.writeargs(Version, "RFB %03d.%03d\n" % (rfbe.major, rfbe.minor))

    #### Security handlshake, conditionalized by version.
    if (rfbe.major == 3 and rfbe.minor == 3):
        # Server sends sectype, sectype specific negotiation is done
        # (None for sectype None (== 1))
        rfbe.sectype = rfbe.readele(SecType)
        if rfbe.sectype != 1:
            raise RFBEndpoint.BadSecType, ("Sectype %d chosen by server"
        				   % rfbe.sectype)
        if rfbe.debug >= DebugPrintRFBDetails:
            print >> sys.stderr, "RFB security type: ", rfbe.sectype
    elif (rfbe.major == 3 and rfbe.minor == 7):
        # Server sends sectypes, client picks one, sectype specific
        # negotiation is done (None for sectype None (== 1))
        # Server sends neogotiation ok/not ok (if sectype != None)
        secTypes = rfbe.readvarlist(SecTypes)
        if len(secTypes) == 0:
            failureReason = rfbe.readstring(FailureReason)
            raise BadSecType, ("No sectypes sent by server, reason: "
                               + failureReason)
        if 1 not in secTypes:
            raise BadSecType, ("Sectype 1 not allowed by server.  Valid sectypes: "
        		       + secTypes.repr())
        rfbe.sectype = 1
        rfbe.writeargs(SecType, rfbe.sectype)
        if rfbe.sectype != 1:
            secresult = rfbe.readele(SecResult)
            if secresult != 0:
                raise RFBEndpoint.ServerError, ("Sec Type %d not accepted by server"
            					% rfbe.sectype)
        if rfbe.debug >= DebugPrintRFBDetails:
            print >> sys.stderr, "RFB security type: ", rfbe.sectype
    elif (rfbe.major == 3 and rfbe.minor == 8):
        # Server sends sectypes, client picks one, sectype specific
        # negotiation is done (None for sectype None (== 1))
        # Server sends neogotiation ok/not ok, with following
        # reason if not ok.
        secTypes = rfbe.readvarlist(SecTypes)
        if len(secTypes) == 0:
            failureReason = rfbe.readstring(FailureReason)
            raise RFBEndpoint.BadSecType, ("No sectypes sent by server, reason: "
        				   + failureReason)
        if 1 not in secTypes:
            raise RFBEndpoint.FailedHandshake, ("Sectype 1 not allowed by server.  Valid sectypes: "
        				   + str(secTypes))
        rfbe.sectype = 1
        rfbe.writeargs(SecType, 1)
        if (rfbe.readele(SecResult)):
            raise RFBEndpoint.ServerError, rfbe.readstring(FailureReason)
        if rfbe.debug >= DebugPrintRFBDetails:
            print >> sys.stderr, "RFB security type: ", rfbe.sectype
    else:
        raise RFBEndpoint.BadVersion, ("%d.%d" % rfbe.major, rfbe.minor)
    if rfbe.debug >= DebugPrintRFBMessages:
        print >> sys.stderr, "RFB Handshake complete"

def RFBInitialize(rfbe):
    """Do client/server initialization once handshake completed.
    Modifies rfbe fields directly; should be considered a private method
    of RFBEndpoint."""
    ### Inform the server that access may be shared,
    ### read size of frame buffer, pixelformat, and frame buffer name

    rfbe.writeargs(ClientInit, 1) # Shared
    rfbe.fbsize = rfbe.readlist(ServerInit1)
    if rfbe.debug >= DebugPrintRFBDetails:
        print >> sys.stderr, "FBSize: ", rfbe.fbsize
    tmp = rfbe.readlist(PixelFormat)
    pf = cstruct(("bpp", "depth", "bigendian", "truecolorp", "rgbmax", "rgbshift"))
    (pf.bpp, pf.depth, pf.bigendian, pf.truecolorp) = tmp[0:4]
    pf.rgbmax = tmp[4:7]
    pf.rgbshift = tmp[7:10]
    if rfbe.debug >= DebugPrintRFBDetails:
        print >> sys.stderr, "PixelFormat: Bpp: %d, Depth: %d, TCP: %d, big-endian: %d, Max: (%d, %d, %d), Shift: (%d, %d, %d)" % tmp

    rfbe.fbformat = pf
    rfbe.fbname = rfbe.readstring(ServerInit2)
    if rfbe.debug >= DebugPrintRFBDetails:
        print >> sys.stderr, "RFB Name: ", rfbe.fbname
    if rfbe.debug >= DebugPrintRFBMessages:
        print >> sys.stderr, "Connection initialization done."

def RFBreadFrameBufferUpdate(rfbe):
    numrect = rfbe.readele(FrameBufferHeader)
    result = []
    for i in range(numrect):
        recheader = rfbe.readlist(FrameBufferRectangleHeader)
        if rfbe.debug >= DebugPrintRFBDetails:
            print >> sys.stderr, "Received rectangle update for rect (%d,%d)->(%d,%d), encoding %d" % recheader
        enctype = recheader[-1]
        recheader = recheader[0:4]
        assert enctype in (rfbe.FBURaw, rfbe.FBUCopyRect, rfbe.FBUPNoCursor)
        if enctype == rfbe.FBURaw:
            str = rfbe.readele(">%ds" % (recheader[2] * recheader[3] * rfbe.fbformat.bpp/8))
            args = recheader + (str,)
        elif enctype == rfbe.FBUCopyRect:
            src = rfbe.readlist(FrameBufferCopyRect)
            args = recheader + src
        elif enctype == rfbe.FBUPNoCursor:
            str = rfbe.readele(">%ds" % (recheader[2] * recheader[3] * rfbe.fbformat.bpp/8))
            str2 = rfbe.readele(">%ds" % (((recheader[2] +7)//8)*recheader[3]))
            args = recheader + (str, str2)

        if not rfbe.rcallbacks[enctype]:
            raise rfbe.NotYetImplemented, "No rectangle callback for type %d" % enctype
        for f in rfbe.rcallbacks[enctype]:
            f(*args)
    if rfbe.debug >= DebugPrintRFBMessages:
        print >> sys.stderr, "Frame buffer update received and processed."
            

def RFBreadSetColourMapEntries(rfbe):
    first = rfbe.readele(SetColourMapEntries1)
    colors = rfbe.readvarlist(SetColourMapEntries2)
    if rfbe.debug >= DebugPrintRFBMessages:
        print >> sys.stderr, "Set Colour map entries message received and parsed."
    return (first, colors)

def RFBreadBell(rfbe):
    ## No args
    if rfbe.debug >= DebugPrintRFBMessages:
        print >> sys.stderr, "Bell message received and parsed."
    return ()

def RFBreadServerCutText(rfbe):
    if rfbe.debug >= DebugPrintRFBMessages:
        print >> sys.stderr, "Server Cut Text message received and parsed."
    return rfbe.readstring(CutText)

## Server message handling
RFBMessageHandlers = ( RFBreadFrameBufferUpdate,
                       RFBreadSetColourMapEntries,
                       RFBreadBell,
                       RFBreadServerCutText)

class RFBEndpoint(ProtocolEndpoint):
    # Exceptions
    class BadFormat(Exception): pass
    class BadVersion(Exception): pass
    class FailedHandshake(Exception): pass
    class NotYetImplemented(Exception): pass
    class NoHandler(Exception): pass
    class ServerError(Exception): pass

    # Constants for server side messages
    FrameBufferUpdate = 0
    SetColourMapEntries = 1
    Bell = 2               
    ServerCutText = 3      
    
    # Constants for encoding type of frame buffer update
    FBURaw = 0                  # encres == string of length w X h x bytespp
    FBUCopyRect = 1             # encres = (src-x, src-y)
    # Others not currently supported
    FBUPNoCursor = -239         # Don't paint cursor on virtual screen.

    def __init__(self, host, vncserverinstance, debug=0):
        ProtocolEndpoint.__init__(self, host, 5900 + vncserverinstance, debug=debug)
        try:
            RFBHandshake(self)
            RFBInitialize(self)
        except:
            ProtocolEndpoint.close(self)
            raise
        self.mcallbacks = {}
        self.rcallbacks = {}
    
    ## Get data stored by initialization (and any replacements from later)
    def getFBSize(self):
        return self.fbsize

    def getPixelFormat(self):
        """Get the pixel format currently in use by the connection.
        This is a tuple in the form:
        (bits-per-pixel, depth, big-endian-p, true-color-p, rgbmax, rgbshift)
        rgb* are triples of the values of each for red, green, and blue.
        bits-per-pixel is the # of bits on the wire per pixel, depth the
        number of these bits that have useful information.
        big-endian-p describes the layout of data within that pixel value.
        If true-color-p, then rgbmax and rgbshift are valid.
        *max is the maximum value for that color within the pixel
        *shift is the amount to right shift the pixel to get that value.
        In other words Xvalue = (pixel >> Xshift) & Xmax."""
        return self.fbformat

    def getName(self):
        return rfbe.fbname

    ## Client side messages
    def setPixelFormat(self, pf):
        """Pixel format is a list:
        (bpp, depth, big-endian-p, true-color-p, rgbmax, rgbshift).
        rgb* are three tuples of the values for red, green, and blue."""
        self.writeargs(ClientMessageType, 0)
        self.writeargs("xxx")
        self.writeargs(PixelFormat, pf.bpp, pf.depth, pf.bigendian,
                       pf.truecolorp, *(pf.rgbmax + pf.rgbshift))
        self.fbformat = pf

    def setEncodings(self, *encodinglist):
        self.writeargs(ClientMessageType, 2)
        self.writevarlist(SetEncodings, encodinglist)

    def updateFrameBuffer(self, x, y, width, height, inc=True):
        "Do an incremental frame buffer update on the specified rectangle."
        self.writeargs(ClientMessageType, 3)
        self.writeargs(FrameBufferUpdateReq, 1 if inc else 0, x, y, width, height)

    def keyEvent(self, keysym, downFlag=True):
        self.writeargs(ClientMessageType, 4)
        self.writeargs(KeyEvent, 1 if downFlag else 0, keysym)

    def pointerEvent(self, x, y, buttons):
        """Buttons is a list of buttons in range(8) which are pressed for
        this event."""
        buttonmask = 0
        for i in buttons:
            assert i in range(8)
            buttonmask |= 1 << i
        self.writeargs(ClientMessageType, 5)
        self.writeargs(PointerEvent, buttonmask, x, y)

    def clientCutText(self, cuttext):
        self.writeargs(ClientMessageType, 6)
        self.writeargs(CutText, cuttext)

    ## Register callbacks for server side messages
    def registerMessageCallback(self, serverMessageType, func):
        """Register a callback to be called when a message of the specific
        type is received.  A NoHandler exception will be raised if a
        message is received for which no callback is registered.
        Multiple callbacks may be registered for each message type.
        Arguments to the callbacks:
        	* SetColourMapEntries:
                	(firstcolor, ((r1,g1,b1), (r2,g2,b2), ...))
        	* Bell: No arguments
                * ServerCutText: string containing text.
 	Callbacks for frame buffer updates may not be registered;
        those are registered on a per-encoding basis."""
        assert serverMessageType in (self.SetColourMapEntries, self.Bell, self.ServerCutText)
        self.mcallbacks.setdefault(serverMessageType, []).append(func)

    def registerRectangeCallback(self, encodingtype, func):
        """FrameBufferUpdate messages are handled specially, with
        callbacks being called on a per-rectangle basis.  Arguments to the
        callbacks:
        	* FBURaw: (x, y, w, h, data)
                  data is a string of length wXhXbpp
                * FBUCopyRect: (x, y, w, h, src-x, src-y)
                * FBUPNoCursor: (hotx, hoty, w, h, data, bitmask)
                  data is a string of length wXhXbpp
                  bitmask has h scanlines each padded to the first
                  integer >= w/8."""
        assert encodingtype in (self.FBURaw, self.FBUCopyRect, self.FBUPNoCursor)
        self.rcallbacks.setdefault(encodingtype, []).append(func)

    ## Read a server message
    def readMessage(self):
        """Read protocol message and update internal notes as appropriate,
        returning type of message read."""
        messagetype = self.readele(serverMessageType)
        assert messagetype >= 0 and messagetype < len(RFBMessageHandlers)
        internfunc = RFBMessageHandlers[messagetype]
        parsedargs = internfunc(self)
        if messagetype != self.FrameBufferUpdate: # FBU is handled from internal func
            if not self.callbacks[serverMessageType]:
                raise self.NotYetImplemented, "No handlers for message of type %d" % (serverMessageType,)
            for f in self.callbacks[messagetype]:
                f(*parsedargs)
        return messagetype

    def waitForServerMessage(self, messageType):
        m = self.readMessage()
        if self.debug >= DebugPrintRFBDetails:
            print >> sys.stderr, "Received message, type: ", m
        while m != messageType:
            if self.debug >= DebugPrintRFBDetails:
                print >> sys.stderr, "Received message, type: ", m
            m = self.readMessage()
    
class RemoteScreen:
    """Class representing a remote screen."""

    class NotYetImplemented(Exception): pass

    ### Does not inherit from RFBEndpoint as it isn't an
    ### RFBEndpoint (though closely related to it).
    def __init__(self, host, vncserverinstance = 0, debug=0):
        e = self.endpoint = RFBEndpoint(host, vncserverinstance, debug=debug)
        self.debug = debug
        self.cuttext = ""
        try:
            pf = e.getPixelFormat()
            ## Reset pf to be the PIL format "RGBX"
            pf.bpp = 32
            pf.depth = 24
            pf.truecolorp = 1
            pf.rgbmax = (255,255,255)
            pf.rgbshift = (24, 16, 8)
            e.setPixelFormat(pf)
            size = e.getFBSize()
            self.image = Image.new("RGBX", size)

            ## Not handling color map entries.
            e.registerMessageCallback(e.Bell, self.__handleBell)
            e.registerMessageCallback(e.ServerCutText, self.__handleCutText)
            e.registerRectangeCallback(e.FBURaw, self.__handleRawRect)
            e.registerRectangeCallback(e.FBUCopyRect, self.__handleCopyRect)
            e.registerRectangeCallback(e.FBUPNoCursor, self.__handlePseudoCursor)
            e.setEncodings(e.FBURaw,e.FBUCopyRect,e.FBUPNoCursor)
            e.updateFrameBuffer(0, 0, size[0], size[1], False)
            e.waitForServerMessage(e.FrameBufferUpdate)
        except:
            self.endpoint.close()
            raise

    def close(self):
        self.endpoint.close()

    ## Server callbacks
    def __handleRawRect(self, x, y, w, h, data):
        if self.debug >= DebugSaveFBUpdate:
            f = open("tmpfb.raw", "w")
            f.write(data)
            f.close()
        rimage = Image.frombuffer("RGBX", (w, h), data, "raw", "RGBX", 0, 1)
        self.image.paste(rimage, (x,y))

    def __handleCopyRect(self, x, y, w, h, srcx, srcy):
        rimage = self.image.crop((srcx, srcy, x+w, y+h))
        self.image.paste(rimage, (x, y))

    def __handlePseudoCursor(self, hotx, hoty, w, h, data, bitmask):
        self.cursorimage = Image.fromstring("RGBX", (w, h), data, "raw", "RGBX", 0, 1)
        self.cursormask = Image.fromstring("1", (w, h), bitmask, "raw", "1", (w + 7)//8, 1)

    def __handleBell(self):
        pass

    def __handleCutText(self, text):
        self.serverCutText = text

    def show(self):
        """Debugging operation; show me the image!"""
        self.image.show()

    ## Operations on remote screen
    def getSubImage(self, x, y, w, h):
        """Returns an image representing the seciton of the screen specified.
        This image should be treated as read-only; it may share storage with
        the backing store for the remote screen."""
        self.endpoint.updateFrameBuffer(x, y, w, h)
        self.endpoint.waitForServerMessage(self.endpoint.FrameBufferUpdate)
        return self.image.crop((x, y, x+w, y+h))

    def pressKey(self, keysym):
        e = self.endpoint
        e.writeargs(ClientMessageType, 4)
        e.writeargs(KeyEvent, 1, keysym)

    def releaseKey(self, keysym):
        e = self.endpoint
        e.writeargs(ClientMessageType, 4)
        e.writeargs(KeyEvent, 0, KeySyms[keysym])

    def sendKey(self, keysym, shift=False, ctrl=False, option=False, cmd=False):
        if shift: self.pressKey(self, KeySyms.Shift_L)
        if ctrl: self.pressKey(self, KeySyms.Control_L)
        if option: self.pressKey(self, KeySyms.Alt_L)
        if cmd: self.pressKey(self, KeySyms.Meta_L)
        self.pressKey(keysym)
        self.releaseKey(keysym)
        if cmd: self.releaseKey(self, KeySyms.Meta_L)
        if option: self.releaseKey(self, KeySyms.Alt_L)
        if ctrl: self.releaseKey(self, KeySyms.Control_L)
        if shift: self.releaseKey(self, KeySyms.Shift_L)

    def moveMouse(self, x, y):
        "Send a mouse movement event to x, y."
        e = self.endpoint
        e.writeargs(ClientMessageType, 5)
        e.writeargs(PointerEvent, 0, x, y)
        
    def pressMouse(self, x, y, buttons):
        """Send a mouse event.  Things like Ctrl-Mouse-1 should be sent
        via sending a ctrl press, a mouse event, and a ctrl release."""
        mask = 0
        for i in buttons:
            mask |= (1 << i)
        assert(mask <= 255)
        e = self.endpoint
        e.writeargs(ClientMessageType, 5)
        e.writeargs(PointerEvent, mask, x, y)

    def dragMouse(self, fromx, fromy, tox, toy, buttons):
        e = self.endpoint
        e.pressMouse(fromx, fromy, buttons)
        e.pressMouse(tox, toy, buttons)
        e.movemouse(tox, toy)

    def clickMouse(self, x, y, buttons):
        self.pressMouse(x, y, buttons)
        self.moveMouse(x, y)

    def getCutText(self):
        return self.cuttext

    def sendCutText(self, text):
        self.writeargs(ClientMessageType, 6)
        self.writeargs(CutText, text)
        self.cuttext = text

if __name__ == "__main__":
    test = RemoteScreen("localhost", 0, DebugPrintRFBDetails)
    test.getSubImage(250, 200, 100, 100).show()
    test.close()
    
