import cv2
import numpy as np
from matplotlib import pyplot as plt



# img2 = cv2.resize(img2, (800, 800))
# img1 = cv2.resize(img1, (800, 800))

def mask_process(img1, measure):
    img2 = img1.copy()
    # I want to put logo on top-left corner, So I create a ROI
    # 首先获取原始图像roi
    rows, cols, channels = img2.shape
    roi = img1[0:rows, 0:cols]

    # 原始图像转化为灰度值
    # Now create a mask of logo and create its inverse mask also
    img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # cv2.imshow('img2gray', img2gray)
    # cv2.waitKey(0)
    '''
    将一个灰色的图片，变成要么是白色要么就是黑色。（大于规定thresh值就是设置的最大值（常为255，也就是白色））
    '''
    # 将灰度值二值化，得到ROI区域掩模
    # ret, mask = cv2.threshold(img2gray, 200, 255, cv2.THRESH_BINARY)
    ret, mask = cv2.threshold(img2gray, 128, 255, cv2.THRESH_BINARY + measure)
    # cv2.imshow('mask', mask)
    # cv2.waitKey(0)

    # ROI掩模区域反向掩模
    mask_inv = cv2.bitwise_not(mask)

    # cv2.imshow('mask_inv', mask_inv)
    # cv2.waitKey(0)

    # 掩模显示背景
    # Now black-out the area of logo in ROI
    img1_bg = cv2.bitwise_and(roi, roi, mask=mask)

    # cv2.imshow('img1_bg', img1_bg)
    # cv2.waitKey(0)

    # 掩模显示前景
    # Take only region of logo from logo image.
    img2_fg = cv2.bitwise_and(img2, img2, mask=mask_inv)

    # cv2.imshow('img2_fg', img2_fg)
    # cv2.waitKey(0)

    # 前背景图像叠加
    # Put logo in ROI and modify the main image

    mask2 = np.zeros_like(img1)
    w = mask.shape[0]
    h = mask.shape[1]
    for i in range(w):
        for j in range(h):
            if mask[i, j] == 255:
                mask[i, j] = 128
    mask2[:, :, 0] = mask
    mask2[:, :, 1] = mask
    mask2[:, :, 2] = mask

    dst = cv2.add(mask2, img2_fg)
    img1[0:rows, 0:cols] = dst
    # img1 = cv2.fastNlMeansDenoisingColored(img1, None, 3, 3, 7, 21)

    plt.subplot(2,2,1)
    plt.imshow(mask)

    plt.subplot(2,2,2)
    plt.imshow(img1_bg)
    # plt.show()
    plt.subplot(2,2,3)
    plt.imshow(img2_fg)
    # plt.show()
    plt.subplot(2,2,4)
    plt.imshow(img1)
    plt.show()
    return img1


def log(c, img):
    output_img = c * np.log(1.0 + img)
    output_img = np.uint8(output_img + 0.5)
    return output_img


img_name = "12.jpg"
img = cv2.imread(f"../lab_test/{img_name}")
blur = cv2.GaussianBlur(img, (5, 5), 0)
# from img_matting import get_hist
# get_hist(blur)
# w = blur.shape[0]
# h = blur.shape[1]
# for i in range(w):
#     for j in range(h):
#         if (int(blur[i, j, 0]) + int(blur[i, j, 1]) + int(blur[i, j, 2])) // 3 >= 225:
#             blur[i, j, :] = 225

# kernel = np.array([[0, -1, 0],
#                    [-1, 5, -1],
#                    [0, -1, 0]])

# dst = cv2.filter2D(img, -1, kernel)

from lab import shadow_remove
# blur = shadow_remove(blur)
# blur = cv2.GaussianBlur(img, (3, 3), 0)
# blur = cv2.blur(img,(2,2))
# b,g,r = cv2.split(blur)
# clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(4, 4))
# b = clahe.apply(b)
# g = clahe.apply(g)
# r = clahe.apply(r)
# blur = cv2.merge([b,g,r])
# b,g,r = cv2.split(img)

# b = cv2.equalizeHist(b)
# g = cv2.equalizeHist(g)
# r = cv2.equalizeHist(r)
# blur = cv2.merge([b,g,r])

plt.figure(figsize=(12, 8))
plt.subplot(1, 2, 1)
plt.imshow(img)
plt.subplot(1, 2, 2)
plt.imshow(blur)
plt.show()
# final = mask_process(blur, cv2.THRESH_TRIANGLE)
final = mask_process(blur, cv2.THRESH_TRIANGLE)
# final = mask_process(final, cv2.THRESH_TRIANGLE)
cv2.imwrite(f"../lab_mask/{img_name}", final)