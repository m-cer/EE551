from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
import psutil
import os
import time
from datetime import datetime

class system_stats:
	def __init__(self):
		net = psutil.net_io_counters()
		self.sent = net[0]
		self.recv = net[1]
		self.datetime = datetime.now()
		
	def overlay(self, frame):
		cpu = 'CPU: {} %'.format(psutil.cpu_percent())
		
		load = ''
		for each in os.getloadavg():
			if load == '':
				load = 'Load: ' + str(each)
			else:
				load = load + ', ' + str(each)
		mem = 'RAM Usage: {} %'.format(psutil.virtual_memory().percent)

		
		net = psutil.net_io_counters()
		dt = (datetime.now()-self.datetime).total_seconds()
		
		s_recv = (net[0] - self.sent)/dt
		recv, r_u = simple_bits(s_recv) 
		recv = 'Down: {:.2f} {}'.format(recv, r_u)
		
		s_sent = (net[1] - self.recv)/dt
		sent, s_u = simple_bits(s_sent) 
		sent = 'Up: {:.2f} {}'.format(sent, s_u)
		
		s_tot = s_recv+s_sent
		tot, t_u = simple_bits(s_tot)
		tot = 'Total: {:.2f} {}'.format(tot, t_u)
		
		stats = '\n'.join((cpu, load, mem, sent, recv, tot))
		
		self.sent = net[0]
		self.recv = net[1]
		self.datetime = datetime.now()
		
		font = ImageFont.truetype("FreeMono.ttf", 18)
		draw = ImageDraw.Draw(frame)
		draw.text((5,5),stats,fill="white")
		return frame

def simple_bits(bits):
	if bits/(1024**2) < 1:
		if bits/1024 < 1:
			unit = 'bps'
		else:
			bits = bits/1024
			unit = 'kibps'
	else:
		bits = bits/(1024**2)
		unit = 'Mibps'
	return (bits, unit)
			
			
			
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
		draw.polygon([(com_w/2-3,0),(com_w/2+3,0),(com_w/2, 3)],fill = 'white')
		
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
