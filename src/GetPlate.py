from pylab import array, zeros, inv, dot, svd, shape
from Interpolation import pV

def getPlateAt(image, points, M, N):
    '''Returns an image of size MxN of the licenseplate (or any rectangular 
    object) defined by 4 corner points.'''
    # Construct the matrix M
    x1_a, y1_a = 0, 0
    x2_a, y2_a = M, 0
    x3_a, y3_a = M, N
    x4_a, y4_a = 0, N
    
    p_i = []
    
    for point in points:
        p_i.append([point.x, point.y])
    
    mat_M = array([[p_i[0][0], p_i[0][1], 1, 0,  0,  0, \
                        -x1_a * p_i[0][0], -x1_a * p_i[0][1], -x1_a], \
                   [0,  0,  0, p_i[0][0], p_i[0][1], 1, \
                        -y1_a * p_i[0][0], -y1_a * p_i[0][1], -y1_a], \
                   [p_i[1][0], p_i[1][1], 1, 0,  0,  0, \
                        -x2_a * p_i[1][0], -x2_a * p_i[1][1], -x2_a], \
                   [0,  0,  0, p_i[1][0], p_i[1][1], 1, \
                        -y2_a * p_i[1][0], -y2_a * p_i[1][1], -y2_a], \
                   [p_i[2][0], p_i[2][1], 1, 0,  0,  0, \
                        -x3_a * p_i[2][0], -x3_a * p_i[2][1], -x3_a], \
                   [0,  0,  0, p_i[2][0], p_i[2][1], 1, \
                        -y3_a * p_i[2][0], -y3_a * p_i[2][1], -y3_a], \
                   [p_i[3][0], p_i[3][1], 1, 0,  0,  0, \
                        -x4_a * p_i[3][0], -x4_a * p_i[3][1], -x4_a], \
                   [0,  0,  0, p_i[3][0], p_i[3][1], 1, \
                        -y4_a * p_i[3][0], -y4_a * p_i[3][1], -y4_a]])
    
    # Get the vector p and the values that are in there by taking the SVD. 
    # Since D is diagonal with the eigenvalues sorted from large to small on
    # the diagonal, the optimal q in min ||Dq|| is q = [[0]..[1]]. Therefore, 
    # p = Vq means p is the last column in V.
    U, D, V = svd(mat_M)
    p = V[8][:]                
    a, b, c, d, e, f, g, h, i = p[0], \
                                p[1], \
                                p[2], \
                                p[3], \
                                p[4], \
                                p[5], \
                                p[6], \
                                p[7], \
                                p[8]
    
    # P is the resulting matrix that describes the transformation
    P = array([[a, b, c], \
               [d, e, f], \
               [g, h, i]])
    
    # Create the new image
    b = array([zeros(M, float)] * N)
    for i in range(0, M):
        for j in range(0, N):
            or_coor = dot(inv(P),([[i],[j],[1]]))
            or_coor_h = or_coor[1][0] / or_coor[2][0], \
                      or_coor[0][0] / or_coor[2][0]
            b[j][i] = pV(image, or_coor_h[0], or_coor_h[1])
    
    return b
