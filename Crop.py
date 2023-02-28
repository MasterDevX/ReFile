import cv2
import numpy as np
from system import util

def init():
	input_dir = './In-Crop/'
	output_dir = './Out-Crop/'
	util.print_header()
	input_file_name = util.get_input_file(input_dir)
	img = util.load_image(input_dir + input_file_name, False)
	warped = transform_perspective(img, select_points(img))
	util.export_image(output_dir + input_file_name, warped, False)
	util.full_exit(0)

def select_points(img):
	print('[INFO] Selecting points...')
	img_copy = img.copy()
	params = [[img, img_copy], [(-1, -1) for i in range(4)]]
	cv2.namedWindow('Image', cv2.WINDOW_GUI_NORMAL)
	cv2.imshow('Image', img_copy)
	cv2.setMouseCallback('Image', mouse_coords, params)
	while True:
		if cv2.waitKey(0) == 13:
			cv2.destroyAllWindows()
			if (-1, -1) not in params[1]:
				break
			else:
				print('[INFO] Aborted by user!')
				util.full_exit(1)
	points = np.array(params[1], dtype='float32')
	print('[INFO] Points selected!')
	return points

def order_points(points):
	print('[INFO] Ordering points...')
	rectangle = np.zeros((4, 2), dtype='float32')
	xy_sum = points.sum(axis=1)
	rectangle[0] = points[np.argmin(xy_sum)]
	rectangle[2] = points[np.argmax(xy_sum)]
	xy_diff = np.diff(points, axis=1)
	rectangle[1] = points[np.argmin(xy_diff)]
	rectangle[3] = points[np.argmax(xy_diff)]
	print('[INFO] Points ordered!')
	return rectangle

def transform_perspective(img, points):
	print('[INFO] Transforming perspective...')
	rectangle = order_points(points)
	tl, tr, br, bl = rectangle
	width_A = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	width_B = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	max_width = max(int(width_A), int(width_B))
	height_A = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	height_B = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	max_height = max(int(height_A), int(height_B))
	destination = np.array([
		[0, 0],
		[max_width - 1, 0],
		[max_width - 1, max_height - 1],
		[0, max_height - 1]
	], dtype='float32')
	matrix = cv2.getPerspectiveTransform(rectangle, destination)
	warped = cv2.warpPerspective(img, matrix, (max_width, max_height))
	print('[INFO] Perspective transformed!')
	return warped

def mouse_coords(event, x, y, flags, params):
	if event == cv2.EVENT_LBUTTONDBLCLK:
		for i in range(4):
			if params[1][i] == (-1, -1):
				params[1][i] = (x, y)
				x1y1 = (x - 5, y - 5)
				x2y2 = (x + 5, y + 5)
				cv2.rectangle(params[0][1], x1y1, x2y2, (90, 255, 55), 3)
				break
		cv2.imshow('Image', params[0][1])
	if event == cv2.EVENT_RBUTTONUP:
		params[0][1] = params[0][0].copy()
		params[1] = [(-1, -1) for i in range(4)]
		cv2.imshow('Image', params[0][1])

if __name__ == '__main__':
	init()
