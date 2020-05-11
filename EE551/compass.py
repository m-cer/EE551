from PIL import Image, ImageDraw, \
    ImageFilter, ImageFont, ImageChops

class compass():
    def __init__(self, width = 360, height = 20):
        self.width = width
        self.height = height
    def overlay(self, frame, theta):
        #width is 2 pixels/degree
        dx = 2*theta

        com_w = self.width
        com_h = self.height

        font = ImageFont.truetype("FreeMono.ttf", 18)
        text = {com_w/2-4*90-dx+theta%5:'S',
                com_w/2-2*90-dx+theta%5:'W',
                com_w/2-dx+theta%5:'N',
                com_w/2+2*90-dx+theta%5:'E',
                com_w/2+4*90-dx+theta%5:'S',
                com_w/2+6*90-dx+theta%5:'W',
                com_w/2+8*90-dx+theta%5:'N',}

        #create base compass image
        img = Image.new('RGBA', (com_w, com_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        for x in range(0,com_w):
            if x in text.keys():
                w, h = draw.textsize(text[x])
                draw.text((x-w/2,(com_h-h)/2),text[x],fill="white")
            elif (x+theta%5)%10==0:
                draw.line([(x,0),(x,com_h)], fill=(255,255,255,255))

        #get alpha of img
        alpha = img.split()[-1]
        alpha = alpha.convert('L')

        #create gradient mask
        mask = Image.new('L', (com_w, com_h), 0)
        draw_m = ImageDraw.Draw(mask)
        draw_m.rectangle([(70,0),(com_w-70,com_h)],fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(50))

        #alpha from img needs to override alpha from mask
        comp = ImageChops.darker(alpha,mask)

        img.putalpha(comp)
        fr_w, fr_h = frame.size
        frame.paste(img, (int(fr_w/2-com_w/2), int(fr_h-com_h)), img)
        return frame

def test():
    com = compass()
    frame = Image.open('test.jpeg')
    frame.convert('RGBA')
    return com.overlay(frame, 45)
