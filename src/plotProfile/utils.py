
import matplotlib.colors as mpc

def desaturate(originalColor, factor):
    # Convert RGB to HLS
    import colorsys
    rgb = mpc.to_rgb(originalColor)
    hls = colorsys.rgb_to_hls(*rgb)
    hls_new = (hls[0], 1 - (0.4 * factor), 0.3 * factor)
    rgb_new = colorsys.hls_to_rgb(*hls_new)
    return rgb_new