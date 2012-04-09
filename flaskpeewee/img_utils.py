try:
    import Image
except ImportError:
    try:
        from PIL import Image
    except ImportError:
        Image = None

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


def resize(source, dest, width, height=None):
    """
    Resize an image to the given width/height, if no height is specificed it
    will be calculated.  Returns the new width and height.
    """
    # open image with PIL
    img_obj = Image.open(source)
    
    # get a file-like object for the new image and its new dimensions
    img_buffer, img_width, img_height = _resize(img_obj, width, height)
    
    # write out the new file
    fh = open(dest, 'w')
    fh.write(img_buffer.getvalue())
    fh.close()
    
    return img_buffer, img_width, img_height

def _resize(img_obj, width, height=None):
    """
    Perform calculations to resize and scale, returning a file-like object and
    the new dimensions
    """
    format = img_obj.format
    img_width, img_height = img_obj.size
    
    if img_width > width or (height is not None and height < img_height):
        wpercent = (width / float(img_width))
        if height:
            hpercent = (height / float(img_height))
        else:
            hpercent = 0
        
        if wpercent < hpercent or not height:
            hsize = int((float(img_height) * float(wpercent)))
            img_obj = img_obj.resize((width, hsize), Image.ANTIALIAS)
            img_width = width
            img_height = hsize
        else:
            wsize = int((float(img_width) * float(hpercent)))
            img_obj = img_obj.resize((wsize, height), Image.ANTIALIAS)
            img_width = wsize
            img_height = height
        
    img_buffer = StringIO()
    img_obj.MAXBLOCK = 1024 * 1024
    img_obj.save(img_buffer, format=format)
    
    return img_buffer, img_width, img_height
