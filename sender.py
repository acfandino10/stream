import cv2
import socket
import math
import struct
import sys

NUM_ARCHIVO = sys.argv[1]
class FrameSegment(object):
  MAX_DGRAM = 2**16
  MAX_IMAGE_DGRAM = MAX_DGRAM - 64 # minus 64 bytes in case UDP frame overflown
  def __init__(self, sock, port, addr='127.0.0.1'):
    self.s = sock
    self.port = port
    self.addr = addr
  def udp_frame(self, img):
    MAX_DGRAM = 2**16
    MAX_IMAGE_DGRAM = MAX_DGRAM - 64
    compress_img = cv2.imencode('.jpg', img)[1]
    dat = compress_img.tobytes()
    size = len(dat)
    num_of_segments = math.ceil(size/(MAX_IMAGE_DGRAM))
    array_pos_start = 0
    
    while num_of_segments:
      array_pos_end = min(size, array_pos_start + MAX_IMAGE_DGRAM)
      self.s.sendto(
                   struct.pack('B', num_of_segments) +
                   dat[array_pos_start:array_pos_end], 
                   (self.addr, self.port)
                   )
      array_pos_start = array_pos_end
      num_of_segments -= 1

def main():
  # Set UDP socket
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  port = 12345
  fs = FrameSegment(s, port)
  
  if NUM_ARCHIVO == '1':
    print('entra')
    cap = cv2.VideoCapture('./video.mp4')
  elif NUM_ARCHIVO == '2':
    print('entra2')
    cap = cv2.VideoCapture('./woman.mp4')
  elif NUM_ARCHIVO == '3':
    print('entra2')
    cap = cv2.VideoCapture('./pexels.mp4')
  elif NUM_ARCHIVO == '0':
    print('entra2')
    cap = cv2.VideoCapture(0)

  while (cap.isOpened()):
    _,frame = cap.read()
    fs.udp_frame(frame)
  cap.release()
  cv2.destroyAllWindows()
  s.close()

main()