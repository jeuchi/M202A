import numpy as np 
import cv2 
from constants import *
import os 
from ultralytics import YOLO

def extract_results_cropped(results, image_path=None, image_num=None, save_image=False, save_cropped_image=False, show_cropped_image=False, show_image=False):
    keypoints_norm = []
    img = cv2.imread(image_path)

    car_center_norm = (0.0, 0.0)
    cropped_image = None
    cropped_image_norm = []

    for result in results:
        boxes = result.boxes 
        keypoints = result.keypoints
        numpy_boxes = boxes.numpy()
        numpy_keypoints = keypoints.numpy()
        pixels_around_box = []
        
        if len(numpy_boxes) > 0:
            for box in numpy_boxes[0]:
                xtl = int(box.xyxy[0][0])
                ytl = int(box.xyxy[0][1])
                xbr = int(box.xyxy[0][2])
                ybr = int(box.xyxy[0][3])

                #cropped_img = img[ytl-padding:ytl+padding, xtl-padding:xtl+padding]
                car_center = (int((xtl + xbr)/2), int((ytl + ybr)/2))
                keypoints_norm.append(car_center[0]/IMAGE_WIDTH)
                keypoints_norm.append(car_center[1]/IMAGE_HEIGHT)
                #keypoints_norm.append(xtl/IMAGE_WIDTH)
                #keypoints_norm.append(ytl/IMAGE_HEIGHT)
                #keypoints_norm.append(xbr/IMAGE_WIDTH)
                #keypoints_norm.append(ybr/IMAGE_HEIGHT)

                cv2.rectangle(img, (xtl, ytl), (xbr, ybr), [255,0,0], 1)
                cv2.circle(img, (car_center[0], car_center[1]), 1, [255,0,0], -1)
                
                xtl = int((xtl+xbr)/2)
                ytl = int((ytl+ybr)/2)

                #print(xtl, ytl)
                padding_width = int(PIXELS_WIDTH/2)
                padding_height = int(PIXELS_HEIGHT/2)

                cropped_image = img[ytl-padding_height:ytl+padding_height, xtl-padding_width:xtl+padding_width]

                if show_cropped_image:
                    cv2.imshow("Cropped", cropped_image)
                    if not show_image:
                        cv2.waitKey(0)

                cropped_image_norm = cropped_image.flatten()
                cropped_image_norm = cropped_image_norm.astype(np.float32) / 255.0
                #print(PIXELS_ARRAY_SIZE, len(cropped_image))

                pad_width = PIXELS_ARRAY_SIZE - len(cropped_image_norm)
                cropped_image_norm = np.pad(cropped_image_norm, (0, pad_width), mode='constant', constant_values=0)

        for keypoints in numpy_keypoints:
            for index, p in enumerate(keypoints.xy[0], start=1):
                if len(keypoints_norm) >= 34:
                    break
                x = int(p[0])
                y = int(p[1])
                keypoints_norm.append(x/IMAGE_WIDTH)
                keypoints_norm.append(y/IMAGE_HEIGHT)
                #cv2.circle(img, (x, y), 1, [255,100,255] if index == LABEL_MAPPING['front_bumper_center'] else [0,255,0], -1)
                cv2.circle(img, (x, y), 1, [0,255,0], -1)

        #pad_width = CROPPED_IMAGE_ARRAY_SIZE - len(cropped_img_norm_flattened)
        #cropped_img_norm_flattened = np.pad(cropped_img_norm_flattened, (0, pad_width), mode='constant', constant_values=0)

        if len(cropped_image_norm) == 0 or np.shape(cropped_image_norm) == ():
            cropped_image_norm = np.zeros(PIXELS_ARRAY_SIZE)
        else:
            pad_width = PIXELS_ARRAY_SIZE- len(cropped_image_norm)
            cropped_image_norm = np.pad(cropped_image_norm, (0, pad_width), mode='constant', constant_values=0)

        pad_width = 34 - len(keypoints_norm)
        keypoints_norm = np.pad(keypoints_norm, (0, pad_width), mode='constant', constant_values=0)

        if show_image:
            cv2.imshow("Keypoints", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows() 

        if image_num is not None:
            if save_image:
                cv2.imwrite('../../data/training/images/%s.png' % image_num, img)
            
            if save_cropped_image and cropped_image is not None:
                cv2.imwrite('../../data/demo/%s.png' % image_num, cropped_image)

    return cropped_image_norm, keypoints_norm

def extract_results(results, image_path=None, image_num=None, save_image=False, save_cropped_image=False, show_cropped_image=False, show_image=False):
    keypoints_norm = []
    cropped_img_norm_flattened = []
    img = cv2.imread(image_path)

    car_center_norm = (0.0, 0.0)

    for result in results:
        boxes = result.boxes 
        keypoints = result.keypoints
        numpy_boxes = boxes.numpy()
        numpy_keypoints = keypoints.numpy()
        cropped_img = None
        cropped_img_norm_flattened = []
        pixels_around_box = []

        if len(numpy_boxes) > 0:
            for box in numpy_boxes[0]:
                xtl = int(box.xyxy[0][0])
                ytl = int(box.xyxy[0][1])
                xbr = int(box.xyxy[0][2])
                ybr = int(box.xyxy[0][3])

                #cropped_img = img[ytl-padding:ytl+padding, xtl-padding:xtl+padding]
                car_center = (int((xtl + xbr)/2), int((ytl + ybr)/2))
                keypoints_norm.append(car_center[0]/IMAGE_WIDTH)
                keypoints_norm.append(car_center[1]/IMAGE_HEIGHT)
                #keypoints_norm.append(xtl/IMAGE_WIDTH)
                #keypoints_norm.append(ytl/IMAGE_HEIGHT)
                #keypoints_norm.append(xbr/IMAGE_WIDTH)
                #keypoints_norm.append(ybr/IMAGE_HEIGHT)

                cv2.rectangle(img, (xtl, ytl), (xbr, ybr), [255,0,0], 1)
                cv2.circle(img, (car_center[0], car_center[1]), 1, [255,0,0], -1)
                
                ytl_orig = ytl
                xtl_orig = xtl

                #xtl = int((xtl+xbr)/2)
                #ytl = int((ytl+ybr)/2)
                #print(ytl)

                pixels_top_left = img[ytl-PIXELS_HEIGHT+40: ytl+40,  xtl-PIXELS_WIDTH:xtl]
                pixels_bottom_left = img[ybr: ybr+PIXELS_HEIGHT, xtl-PIXELS_WIDTH:xtl]
                pixels_top_right = img[ytl-PIXELS_HEIGHT+40: ytl+40, xbr:xbr+PIXELS_WIDTH]
                pixels_bottom_right = img[ybr: ybr+PIXELS_HEIGHT, xbr:xbr+PIXELS_WIDTH]

                if show_cropped_image:
                    pixels = np.concatenate((pixels_top_left, pixels_bottom_left, pixels_top_right, pixels_bottom_right), axis=1)
                    cv2.imshow("Cropped", pixels)
                    if not show_image:
                        cv2.waitKey(0)

                pixels_top_left = pixels_top_left.flatten()
                pixels_bottom_left = pixels_bottom_left.flatten()
                pixels_top_right = pixels_top_right.flatten()
                pixels_bottom_right = pixels_bottom_right.flatten()

                pad_width = PIXELS_ARRAY_SIZE - len(pixels_top_left)
                pixels_top_left = np.pad(pixels_top_left, (0, pad_width), mode='constant', constant_values=0)
                pad_width = PIXELS_ARRAY_SIZE - len(pixels_bottom_left)
                pixels_bottom_left = np.pad(pixels_bottom_left, (0, pad_width), mode='constant', constant_values=0)
                pad_width = PIXELS_ARRAY_SIZE - len(pixels_top_right)
                pixels_top_right = np.pad(pixels_top_right, (0, pad_width), mode='constant', constant_values=0)
                pad_width = PIXELS_ARRAY_SIZE - len(pixels_bottom_right)
                pixels_bottom_right = np.pad(pixels_bottom_right, (0, pad_width), mode='constant', constant_values=0)

                pixels_around_box = np.concatenate([pixels_top_left, pixels_bottom_left, pixels_top_right, pixels_bottom_right])
                pixels_around_box = pixels_around_box.astype(np.float32) / 255.0

                #if len(cropped_img) == 0 or np.shape(cropped_img) == ():
                 #   cropped_img_norm_flattened = np.zeros(CROPPED_IMAGE_ARRAY_SIZE)
                #else:
                 #   cropped_img_norm = cropped_img.astype(np.float32) / 255.0
                 #   cropped_img_norm_flattened = cropped_img_norm.flatten()

        for keypoints in numpy_keypoints:
            for index, p in enumerate(keypoints.xy[0], start=1):
                if len(keypoints_norm) >= 34:
                    break
                x = int(p[0])
                y = int(p[1])
                keypoints_norm.append(x/IMAGE_WIDTH)
                keypoints_norm.append(y/IMAGE_HEIGHT)
                cv2.circle(img, (x, y), 1, [255,100,255] if index == LABEL_MAPPING['rear_bumper_left'] else [0,255,0], -1)
                #cv2.circle(img, (x, y), 1, [0,255,0], -1)

        #pad_width = CROPPED_IMAGE_ARRAY_SIZE - len(cropped_img_norm_flattened)
        #cropped_img_norm_flattened = np.pad(cropped_img_norm_flattened, (0, pad_width), mode='constant', constant_values=0)

        pad_width = (PIXELS_ARRAY_SIZE * 4) - len(pixels_around_box)
        pixels_around_box = np.pad(pixels_around_box, (0, pad_width), mode='constant', constant_values=0)
        #print(len(pixels_around_box))

        pad_width = 34 - len(keypoints_norm)
        keypoints_norm = np.pad(keypoints_norm, (0, pad_width), mode='constant', constant_values=0)

        if show_image:
            cv2.imshow("Keypoints", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows() 

        if show_cropped_image and cropped_img is not None:
            cv2.imshow("Cropped", cropped_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows() 

        if image_num is not None:
            if save_image:
                cv2.imwrite('../../data/training/images/%s.png' % image_num, img)
            
            if save_cropped_image and cropped_img is not None:
                cv2.imwrite('../../data/training/cropped/%s.png' % image_num, cropped_img)

    return pixels_around_box, keypoints_norm

if __name__ == "__main__":
    model = YOLO('../../data/detection_model/weights/last.pt')

    image_num = 50
    for i in range(20,25):
        print(i)
        for j in range(0, 10):
            image_path = '../../data/recordings/good/%s/videos/%s.png' % (i,j)
            #image_path = '../../data/test/images/9.png'
            results = model(image_path, verbose=False)
            cropped_img_norm, keypoints_norm = extract_results(results, image_path, image_num=0, save_image=False, save_cropped_image=False, show_cropped_image=False, show_image=True)
            #cropped_img_norm, keypoints_norm = extract_results_cropped(results, image_path, image_num=image_num, save_image=False, save_cropped_image=True, show_cropped_image=False, show_image=False)
            image_num += 1