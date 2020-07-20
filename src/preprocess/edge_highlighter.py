import cv2
import os
import numpy as np

def edge_highlighter(img): 
    # this func is designed to on image of 700x700
    # the poly mask will only work for 700x700 size

    # gray-scale and canny
    img = cv2.resize(img, (700, 700),interpolation = cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.GaussianBlur(gray, (5,5),0)  
    canny_blur = cv2.Canny(gray_blur, threshold1 = 30, threshold2 = 60)

    # detect edges and highlight them with white color
    mask = np.zeros_like(canny_blur)
    triangle1 = np.array([[0,700], [700,700],[0,365]], np.int32)
    triangle2 = np.array([[700,700],[0,365],[700,365]], np.int32)
    cv2.fillPoly(mask, [triangle1,triangle2], 255)
    masked_canny = cv2.bitwise_and(canny_blur,mask)
    kernel = np.ones((3,3),np.uint8)
    masked_canny = cv2.dilate(masked_canny,kernel,iterations=1)
    masked_canny = cv2.cvtColor(masked_canny, cv2.COLOR_GRAY2RGB)
    diff_image = cv2.addWeighted(masked_canny,0.6,img,1,1)

    # cropping the image
    # diff_image = diff_image[325:700,0:700]

    #Resizing it again
    diff_image = cv2.resize(diff_image, (700, 700),interpolation = cv2.INTER_CUBIC)
    return diff_image
	
if __name__ == '__main__':
	path = 'D:/Yogendra D/Self_driving_Car_for_GTA-San-Andreas/src/tf_dataset/forward_left/'
	files = os.listdir(path)
	img = cv2.imread(os.path.join(path,files[2]))
	ans_img = edge_highlighter(img)
	cv2.imshow('Edge Highlighted Image',ans_img)
	if cv2.waitKey(0) & 0xFF == ord("q"):
		cv2.destroyAllWindows()