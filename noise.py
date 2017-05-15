import random
import Image
import os
import math

# Prints out array myList and returns to new line
# after each row.
def printArray (myList):
    count = 1
    tStr = ""
    for item in myList:
        tStr += str(item) + " "
        if count % width == 0:
            print tStr
            tStr = ""
        count += 1

randint = random.randint

smin = 0                  # minimum value
smax = 255                # maximum value
hval = 0.25               # h value used to define how smooth the pattern will be
ran = (smax - smin)/2     # initial random value, added to 
width = 1025              # width in pixels of the image
height = 1025             # height in pixels of the image
size = width * height     # number of pixels in the image

step = width-1            # number of pixels between the corners of each square
ran = (smax - smin)       # range of random values

# initialize the array to -1 for storage
data = [-1 for i in range(size)]

# initialize four corners values
data[0] = randint(smin, smax)
data[width-1] = randint(smin, smax)
data[(height-1) * width] = randint(smin, smax)
data[size-1] = randint(smin, smax)

# When the step size becomes 1, all of the values
# have been calculated.  Each iteration, the size
# between the squares is halved.
while step > 1:
    # max and min values for random integer generation
    ranmax = int(ran * 0.5)
    ranmin = -1 * ranmax

    # square step
    y = 0
    while y < (height-1):
        x = 0
        while x < (width-1):
	    # figure out the indexes for the corners of the square
            a = x + (y*width)
            b = a + step
            c = a + (step*width)
            d = a + (step*width) + step
            
	    # figure out the index of the center of the square
            mid = (a + b + c + d) / 4

	    # We know that the four corners are all legal because
	    # each iteration x and y are incremented by the step size,
	    # so we can just average the four corner values.
            nval = (data[a] + data[b] + data[c] + data[d]) / 4

	    # If the random min and max have become zero, then don't add the offset.
            if ranmax > 0:
                nval += randint(ranmin, ranmax)

	    # Clamp the new value to the max and min values.
            if nval < smin:
                nval = smin
            if nval > smax:
                nval = smax

	    # Store the new value in the array.
            data[mid] = nval

	    # Increment x and y.
            x += step
        y += step

    #diamond step
    yBool = True       # used to offset the index value for every other step.
    halfstep = step/2  # used to find the corners of the diamond.
    
    y = 0
    while y < height:
        x = 0
        while (x + (yBool*halfstep)) < width:
	    # figure out the index of the center of the diamond
            mid = (y*width) + (yBool*halfstep) + x

	    # figure out the index of the corners using the middle
            a = mid-(halfstep*width)
            b = mid-halfstep
            c = mid+halfstep
            d = mid+(halfstep*width)

	    # Because we are figuring out the corners from the middle
	    # we need to check to make sure that they are valid.  When
	    # we determine that they are valid, their values are added to
	    # the variable nval and count is incremented, these will then
	    # be used to find the average by dividing nval by count.
            nval = 0
            count = 0

	    # if the top corner is greater than zero
            if a >= 0:
                nval += data[a]
                count += 1

	    # Since we are using a 1D array, we can
	    # tell if the left and right corners are valid
	    # by testing to see if they are in the same
	    # row as the middle.
            if b/width == mid/width:
                nval += data[b]
                count += 1
            if c/width == mid/width:
                nval += data[c]
                count += 1

	    # if the bottom corner is less than size
            if d < size:
                nval += data[d]
                count += 1

	    # From here on out, it is the same as the square step.
            nval = nval / count
            if ranmax > 0:
                nval += randint(ranmin, ranmax)
            if nval < smin:
                nval = smin
            if nval > smax:
                nval = smax
            
            data[mid] = nval
            x += step
        y += halfstep
        yBool = not yBool

    # Reduce the step and ran variables
    step = step/2
    ran = ran / (1 + hval)

# Create and write out an image of the data.
outfile = os.getcwd() + "/output.jpg"
im = Image.new("L", (width, height))
im.putdata(data)
