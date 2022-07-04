import mss
import mss.tools

with mss.mss() as sct:
    # the screen part to capture
    monitor = {"top": 160, "left": 160, "width": 160, "height": 135}
    # grab the data
    sct_img = sct.grab(monitor)
    # save the screenshot as a PNG image
    output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)
    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    print(output)
