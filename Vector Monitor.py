from PIL import ImageGrab
from PIL import Image
from PIL import ImageDraw
import anki_vector
import time
import win32gui


args = anki_vector.util.parse_command_args()
with anki_vector.Robot(args.serial) as robot:
  while True:
    image = ImageGrab.grab()
    screenwidth = image.size[0]
    screenheight = image.size[1]
    smaller_image = image.resize((184, 96), Image.ADAPTIVE)
    #smaller_image = Image.new("RGB", (184,96), (0,0,0))
    cursor_pos = win32gui.GetCursorPos()
    try:
      robot_cursor_pos =(int(cursor_pos[0] / (screenwidth /184)), int(cursor_pos[1] / (screenheight / 96)))
      

      #get pixel average
      pixel = smaller_image.getpixel(robot_cursor_pos)

      avg = pixel[0] + pixel[1] + pixel[2]
      avg = avg / 3

      if avg < 127.5:
        ImageDraw.Draw(smaller_image).rectangle((robot_cursor_pos, (robot_cursor_pos[0] + 2, robot_cursor_pos[1] + 2)),fill=(255,255,255))
        
      else:
        ImageDraw.Draw(smaller_image).rectangle((robot_cursor_pos, (robot_cursor_pos[0] + 2, robot_cursor_pos[1] + 2)),fill=(0,0,0))
    except:
      pass
    
    fps = 1/30
    roboImage = anki_vector.screen.convert_image_to_screen_data(smaller_image)
    robot.screen.set_screen_with_image_data(roboImage, fps)
    time.sleep(fps)