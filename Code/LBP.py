# Divide the examined window to cells (e.g. 16x16 pixels for each cell).

# For each pixel in a cell, compare the pixel to each of its 8 neighbors 
# (on its left-top, left-middle, left-bottom, right-top, etc.). Follow the 
# pixels along a circle, i.e. clockwise or counter-clockwise.
    
# Where the center pixel's value is greater than the neighbor, write "1". 
# Otherwise, write "0". This gives an 8-digit binary number (which is usually 
# converted to decimal for convenience).

# Compute the histogram, over the cell, of the frequency of each "number" 
# occurring (i.e., each combination of which pixels are smaller and which are 
# greater than the center).
    
# Optionally normalize the histogram. Concatenate normalized histograms of all 
# cells. This gives the feature vector for the window.
