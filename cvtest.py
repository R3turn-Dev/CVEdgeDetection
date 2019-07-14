import cv2 as cv
import traceback
from os import listdir, mkdir


def main(filename, RESIZE_RATIO=.25, MODE_ALL=False, show=False, return_all=False):
    image = cv.imread(filename, cv.IMREAD_UNCHANGED)
    cols, rows, chns = image.shape

    image = cv.resize(image, dsize=(int(rows*RESIZE_RATIO), int(cols*RESIZE_RATIO)), interpolation=cv.INTER_AREA)
    h, w = image.shape[:2]

    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    blurred = cv.GaussianBlur(gray, (3, 3), 0)
    canny = cv.Canny(blurred, 100, 255)
    contours, hierarachy = cv.findContours(canny.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    if MODE_ALL:
        out = image.copy()

        for c in contours:
            cv.drawContours(out, [cv.approxPolyDP(c, 3, True)], 0, (0, 255, 0), 3, cv.LINE_AA, hierarachy, 0)

    else:
        MAX_Size = 0
        MAX = None

        for c in contours:
            area = cv.contourArea(c)
            if area > MAX_Size:
                MAX_Size = area
                MAX = c

        out = image.copy()

        cv.drawContours(out, [cv.approxPolyDP(MAX, 7.5, True)], 0, (0, 255, 0), 3, cv.LINE_AA, hierarachy, 0)

    if show:
        cv.imshow("original", image)
        cv.imshow("out", out)
        cv.waitKey(0)
        cv.destroyAllWindows()

    return (
        image, gray, blurred, canny, out
    ) if return_all else (
        canny, out
    )


if __name__ == "__main__":
    if "data-in" not in listdir("."):
        print("Please put image files in 'data-in' directory.")
        exit(-1)

    if "data-out" not in listdir("."):
        mkdir("data-out")

    msg = ["canny", "mixed"]
    for f in listdir("data-in"):
        for ratio in (.25, .5, 1):
            for all in (False, True):
                try:
                    out = 0
                    name, ext = [x[::-1] for x in f[::-1].split(".", 1)][::-1]
                    for file in main(f"data-in/{f}", RESIZE_RATIO=.25, MODE_ALL=all, show=False):
                        cv.imwrite(f"data-out/{name}-x{ratio}-AllRectangle({all})-{msg[out]}.{ext}", file)
                        out += 1
                except:
                    print("Error on", f, traceback.format_exc())
