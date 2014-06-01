'''  *****************************************************************************
  *                                                                           *
  *                                  fpa size    roi loc   roi siz    roi     *
  * Usage: binFileRoiCmp.py fname    cols rows   row col   rows cols  exp val *
  * e.g. : binFileRoiCmp.py my.bin  (324, 256)  (100,200)  (10,  20)  0x200A  *
  *                                                                           *
  * The above example first reads the specified .bin file into a 324x256      *
  * array of shorts (16-bit entities).  Then from that array a second,        *
  * smaller, array will be extracted.  The location (upper left corner) and   *
  * size of the array to be extracted are specified on the command line.      *
  * Finally it is determined if every pixel in the second, extracted array,   *
  * has the value specified on the command line.  If all the values are       *
  * correct, 0 it returned, else 1 is returned.                               *
  *                                                                           *
  * NOTE: Expected Value must be spcified in hex and begin with '0x'.         *
  *                                                                           *
  *****************************************************************************
'''
############################################################################

def getCmdLineArgsErrMsgAndExit():
    print( )
    print( '  *****************************************************************************')
    print( '  *                                                                           *')
    print( '  * !!! ILL-FORMED COMMAND LINE !!!                                           *')
    print( '  *                                                                           *')
    print(__doc__)
    exit(1)

def getCmdLineArgs():
    if len(sys.argv) == 6:
        fn        = sys.argv[1] # file name.
        fpaTup    = sys.argv[2] # FPA Size.
        roiLocTup = sys.argv[3] # ROI Loc.
        roiSizTup = sys.argv[4] # ROI Size.
        roiStrVal = sys.argv[5] # ROI Expected Value.
    else:
        getCmdLineArgsErrMsgAndExit()

    if (fpaTup[0]    == '(' and fpaTup[-1]    == ')') and \
       (roiLocTup[0] == '(' and roiLocTup[-1] == ')') and \
       (roiSizTup[0] == '(' and roiSizTup[-1] == ')') and \
       (roiStrVal[0:2] == '0x') :
        pass
    else:
        getCmdLineArgsErrMsgAndExit()

    fname       = fn
    fpaNumCols  = int( str.split(    fpaTup[ 1:-1 ], ',' ) [0] )
    fpaNumRows  = int( str.split(    fpaTup[ 1:-1 ], ',' ) [1] )
    roiStartRow = int( str.split( roiLocTup[ 1:-1 ], ',' ) [0] )
    roiStartCol = int( str.split( roiLocTup[ 1:-1 ], ',' ) [1] )
    roiNumRows  = int( str.split( roiSizTup[ 1:-1 ], ',' ) [0] )
    roiNumCols  = int( str.split( roiSizTup[ 1:-1 ], ',' ) [1] )
    roiExpVal   = int( roiStrVal,16 ) 

    return fname,      fpaNumRows, fpaNumCols, roiStartRow, roiStartCol,\
           roiNumRows, roiNumCols, roiExpVal
############################################################################

if __name__ == '__main__':
    
    import sys

    # Code to build a little test file.
    # f=open( 'test.bin', 'wb' )
    # t ='xxxxxx0000xxxxxxxxxxxx0000xxxxxxxxxxxx0000xxxxxx0000000000000000xxxxxx0000xxxxxxxxxxxx0000xxxxxxxxxxxx0000xxxxxx'
    # f.write(bytes(t, 'UTF-8'))
    # f.close()

    # Declare some variables.
    allPix = []; idxsOfRoiPix = []; roiPix = []

    # Get the Command Line Parameters.
    fname,      fpaNumRows, fpaNumCols, roiStartRow, roiStartCol, \
    roiNumRows, roiNumCols, value = getCmdLineArgs()

    # Read the input binary file into a 1-dimensional list (array) of bytes.
    allBytes  = list(open( fname, 'rb' ).read())
    

    # Use above list to make a 1-dimensional list of pixel (2-byte) values.
    for ii in range( 0, len( allBytes ), 2 ):
        allPix.append( allBytes[ ii ] * 256 + allBytes[ ii+1 ] )
    # Use the cmd line parameters to make an 'offset-list'.
    # Offsets = indeces into allPix where roi pixs live.
    for r in range( roiStartRow, roiStartRow + roiNumRows, 1 ):
        for c in range( roiStartCol, roiStartCol + roiNumCols, 1 ):
            idxsOfRoiPix.append( r * fpaNumCols + c )

    # Use 'offset-list' to make a list of any,all,only pixs in the roi.
    for idx in idxsOfRoiPix:
        roiPix.append( allPix[ idx ] )

    # See if all pixs in roi are all equal to cmd line value.
    allSame = roiPix.count(roiPix[0]) == len( roiPix )
    allEqCmdLineVal = allSame and ( roiPix[ 0 ] == value )
    rtnVal = not allEqCmdLineVal # Return 0 if all same

    # User message.
    if allEqCmdLineVal: 
        print( 'PASS: All pixels in ROI equal specified value' )
    else:
        print( 'FAIL: All pixels in ROI do not equal specified value' )
        print('Expected : ' + str(value) + ' Received : ' + str(roiPix[0]) + '\n')

    ######### DEBUG PRINTS ##################################################
    if(0):
    
        print( '\n', allSame, ( roiPix[0] == value ), '\n' )
        for r in range( roiNumRows ):
            for c in range( roiNumCols ):
                print( ' {:7d}'.format( idxsOfRoiPix[ r * roiNumCols + c ] ), end='' )
            print()
        print()
        for r in range( roiNumRows ):
            for c in range( roiNumCols ):
                print( ' {:7x}'.format( roiPix[ r * roiNumCols + c ] ), end='' )
            print()
    ######### DEBUG PRINTS ##################################################

    # OS. message.
    exit( rtnVal )
