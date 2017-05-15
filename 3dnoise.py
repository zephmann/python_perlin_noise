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
        tStr += "%3d " % item
        if count % width == 0:
            print tStr
            tStr = ""
	if count % (width * height) == 0:
	    print "----------------"
        count += 1

randint = random.randint

smin = 0                  # minimum value
smax = 255                # maximum value
hval = 0.25               # h value used to define how smooth the pattern will be
ran = (smax - smin)/2     # initial random value, added to 
width = 1025              # width in pixels of the cube
height = 1025             # height in pixels of the cube
depth = 1025              # depth in pixels of the cube
slize = width * height     # number of pixels in each 2D slice
size = width * height * depth    # number of pixels in the cube

step = width-1            # number of pixels between the corners of each square
ran = (smax - smin)       # range of random values

# initialize the array to -1 for storage
data = [-1 for i in range(size)]

# initialize eight corners values
data[0] = randint(smin, smax)
data[width-1] = randint(smin, smax)
data[(height-1) * width] = randint(smin, smax)
data[slize-1] = randint(smin, smax)
data[slize * (depth-1)] = randint(smin, smax)
data[slize * (depth-1) + (width-1)] = randint(smin, smax)
data[(slize * (depth-1)) + (width*(height-1))] = randint(smin, smax)
data[size-1] = randint(smin, smax)

# When the step size becomes 1, all of the values
# have been calculated.  Each iteration, the size
# between the cubes is halved.
while step > 1:
    # max and min values for random integer generation
    # halfstep used to find the corners of the diamond.
    halfstep = step/2
    ranmax = int(ran/2)
    ranmin = -1 * ranmax

    # square step
    # calculates value for center of cube
    z = 0
    while z < (depth-1):
   	y = 0
        while y < (height-1):
	    x = 0
            while x < (width-1):
                a = x + (y*width) + (z*width*height)
	        b = a + step
        	c = a + (step*width)
                d = a + (step*width) + step
		e = a + (step*slize) 
		f = b + (step*slize)
		g = c + (step*slize)
		h = d + (step*slize)

	        mid = (a + b + c + d + e + f + g + h) / 8
        	nval = (data[a] + data[b] + data[c] + data[d] + data[e] + data[f] + data[g] + data[h]) / 8
                if ranmax > 0:
	            nval += randint(ranmin, ranmax)
        	if nval < smin:
                    nval = smin
	        if nval > smax:
        	    nval = smax

                data[mid] = nval

        	x += step
	    y += step
	z += step

    # the next three blocks calculate the values of the centers of the faces
    # mid step z
    y = 0
    while y < height-step:
    	x = 0
	while x < width-step:
    	    z = 0
            while z < depth:
		a = z*slize + y*width + x
		b = a + step
		c = a + step*width
		d = c + step
		mid = (a + b + c + d) / 4
		e = mid - (slize*halfstep)
		f = mid + (slize*halfstep)

		nval = data[a] + data[b] + data[c] + data[d]
		count = 4
		if e >= 0:
		    nval += data[e]
		    count += 1
		if f < size:
		    nval += data[f]
		    count += 1

		nval = nval / count
		if ranmax > 0:
	            nval += randint(ranmin, ranmax)
        	if nval < smin:
	            nval = smin
        	if nval > smax:
	            nval = smax
	    
		data[mid] = nval
	
		z += step
	    x += step
	y += step

    # mid step y
    z = 0
    while z < depth-step:
	x = 0
	while x < width-step:
	    y = 0
	    while y < height:
		a = x + y*width + z*slize
		b = a + step
		c = a + step*slize
		d = c + step
		mid = (a + b + c + d) / 4
		e = mid + (width*halfstep)
		f = mid - (width*halfstep)

		nval = data[a] + data[b] + data[c] + data[d]
		count = 4
		if e/slize == mid/slize:
		    nval += data[e]
		    count += 1
		if f/slize == mid/slize:
		    nval += data[f]
		    count += 1

		nval = nval / count
		if ranmax > 0:
	            nval += randint(ranmin, ranmax)
        	if nval < smin:
	            nval = smin
        	if nval > smax:
	            nval = smax
	    
		data[mid] = nval

		y += step
	    x += step
	z += step

    # mid step x
    z = 0
    while z < depth-step:
	y = 0
	while y < height-step:
	    x = 0
  	    while x < width:
	    	a = x + y*width + z*slize
	    	b = a + step*width
		c = a + step*slize
	    	d = c + step*width
	    	mid = (a + b + c + d) / 4
	    	e = mid + halfstep
	    	f = mid - halfstep

		nval = data[a] + data[b] + data[c] + data[d]
		count = 4
		if e/width == mid/width:
		    nval += data[e]
		    count += 1
		if f/width == mid/width:
		    nval += data[f]
		    count += 1

		nval = nval / count
		if ranmax > 0:
	            nval += randint(ranmin, ranmax)
        	if nval < smin:
	            nval = smin
        	if nval > smax:
	            nval = smax
	    
		data[mid] = nval

	    	x += step
	    y += step
	z += step

    # diamond step
    # the next two steps calculates the values of the middle of each
    # pair of corners
    z = 0
    zBool = True
    while z < depth:
    	yBool = True
        y = 0
        while y < height:
            x = 0
            while (x + (yBool*halfstep)) < width:
		mid = (z*slize) + (y*width) + (yBool*halfstep) + x

                a = mid-(halfstep*width)
                b = mid-halfstep
                c = mid+halfstep
                d = mid+(halfstep*width)
		e = mid-(halfstep*slize)
		f = mid+(halfstep*slize)

		nval = 0
                count = 0
                if a/slize == mid/slize:
                    nval += data[a]
                    count += 1
		if b/width == mid/width:
                    nval += data[b]
                    count += 1
                if c/width == mid/width:
                    nval += data[c]
                    count += 1
                if d/slize == mid/slize:
                    nval += data[d]
                    count += 1
		if e >= 0:
		    nval += data[e]
		    count += 1
		if f < size:
		    nval += data[f]
		    count += 1

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
	z+=step


    #diamond mid step
    z = halfstep
    while z < depth:
	y = 0
	while y < height:
	    x = 0
	    while x < width:
		mid = (z*slize) + (y*width) + x

		a = mid-(halfstep*width)
                b = mid-halfstep
                c = mid+halfstep
                d = mid+(halfstep*width)
		e = mid-(halfstep*slize)
		f = mid+(halfstep*slize)

		nval = 0
                count = 0
                if a/slize == mid/slize:
                    nval += data[a]
                    count += 1
		if b/width == mid/width:
                    nval += data[b]
                    count += 1
                if c/width == mid/width:
                    nval += data[c]
                    count += 1
                if d/slize == mid/slize:
                    nval += data[d]
                    count += 1
		if e >= 0:
		    nval += data[e]
		    count += 1
		if f < size:
		    nval += data[f]
		    count += 1

		nval = nval / count
                if ranmax > 0:
                    nval += randint(ranmin, ranmax)
                if nval < smin:
                    nval = smin
                if nval > smax:
                    nval = smax

		data[mid] = nval

		x += step
	    y += step
	z += step

    # update step and reduce range
    step = step/2
    ran = ran / (1 + hval)

# write out the cloud as a series of 2D images
z = 0
while z < depth:
    pixels = [data[i] for i in range(z*slize, ((z+1)*slize))]

    outfile = os.getcwd() + "/output/output.%03d.jpg" % z
    im = Image.new("L", (width, height))
    im.putdata(pixels)
    im.save(outfile)
    print z
    z += 1
