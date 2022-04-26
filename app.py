from flask import Flask, send_file, render_template, request
import qrcode, io, time, json, base64
from PIL import Image
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.moduledrawers import *
from os import environ


app = Flask(__name__)


def makeQrCode(text, fill_color, back_color, style, uploaded_img=None):
  #basic configuration
  #see QRCode Docs
  #I don't know which does what
  qr = qrcode.QRCode(
    version=3, # try adjusting this if you don't like the image
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=20,
    border=4
  )
  
  #adds main data
  qr.add_data(text)
  qr.make(fit=True)
  
  if not uploaded_img:
    #simple QR Code
    #supports color mask without any issue
    img = qr.make_image(
      fill_color=fill_color,
      back_color=back_color,
      image_factory=StyledPilImage,
      module_drawer=eval(f"{style}Drawer()")
    )
    
  elif (uploaded_img and ((fill_color != (0, 0, 0)) or (back_color != (255, 255, 255)))):
    #only use color mask with image 
    #if color a is specified by the user
    #has performance issue
    img = qr.make_image(
            color_mask=SolidFillColorMask(
              back_color=back_color,
              front_color=fill_color,
            ),
            module_drawer=eval(f"{style}Drawer()"),
            image_factory=StyledPilImage,
            embeded_image=Image.open(
              io.BytesIO(uploaded_img.read())
            )
          )
  else:
    #skip color mask
    img = qr.make_image(
            image_factory=StyledPilImage,
            embeded_image=Image.open(
              io.BytesIO(uploaded_img.read())
            ),
            module_drawer=eval(f"{style}Drawer()")
          )
          
  return img



@app.route("/")
def home():
  
  return render_template("index.html")
  
@app.route("/api", methods=["POST"])
def api():
  text = (request.form.get("text") or "QRCode Generator - SunPodder")
  fill_color = (request.form.get("fill") or (0, 0, 0))
  back_color = (request.form.get("bg") or (255, 255, 255))
  
  style = request.form.get("style")
  
  # image to use in the center of the QR Code (Optional)
  uploaded_img = request.files["img"]
  
  
  #convert to Tuple
  if type(back_color) == type("str"):
    back_color = tuple(map(int, back_color.split(",")))
  
  if type(fill_color) == type("str"):
    fill_color = tuple(map(int, fill_color.split(",")))
  
  img = makeQrCode(text, fill_color, back_color, style, uploaded_img)
  
  buf = io.BytesIO()
  #save image in ByteStream instead of file
  img.save(buf, format="PNG")
  buf.seek(0)
  
  img_str = "data:image/png;base64," + str(base64.b64encode(buf.getvalue()).decode("utf-8"))
  
  response = {
    "code": 200,
    "image": img_str,
    "name": f"Sun_QRCode_Generator_{str(time.time()).split('.')[0]}.png"
  }
  return (json.dumps(response))


@app.route("/download", methods=["POST"])
def download():
  text = (request.form.get("text") or "QRCode Generator - SunPodder")
  fill_color = (request.form.get("fill") or (0, 0, 0))
  back_color = (request.form.get("bg") or (255, 255, 255))
  
  style = request.form.get("style")
  
  # image to use in the center of the QR Code (Optional)
  uploaded_img = request.files["img"]
  
  
  #convert to Tuple
  if type(back_color) == type("str"):
    back_color = tuple(map(int, back_color.split(",")))
  
  if type(fill_color) == type("str"):
    fill_color = tuple(map(int, fill_color.split(",")))
  
  img = makeQrCode(text, fill_color, back_color, style, uploaded_img)

  
  buf = io.BytesIO()
  #save image in ByteStream instead of file
  img.save(buf, format="PNG")
  buf.seek(0)
  
  return send_file(
    buf,
    download_name=(
      f"Sun_QRCode_Generator_{str(time.time()).split('.')[0]}.png"
    ),
    as_attachment=True,
    mimetype="image/png"
  )


app.run(host="0.0.0.0", port=(int(environ.get("PORT", 3000))), debug=True)