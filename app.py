from flask import Flask, send_file, render_template, request
import qrcode, io, time
from PIL import Image
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import VerticalGradiantColorMask


app = Flask(__name__)


@app.route("/")
def home():
  
  return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
  text = (request.form.get("text") or "QRCode Generator - SunPodder")
  fill_color = (request.form.get("fill") or (0, 0, 0))
  back_color = (request.form.get("bg") or (255, 255, 255))
  
  # image to use in the center of the QR Code (Optional)
  uploaded_img = request.files["img"]
  
  
  #convert to Tuple
  if type(back_color) == type("str"):
    back_color = tuple(map(int, back_color.split(",")))
  
  if type(fill_color) == type("str"):
    fill_color = tuple(map(int, fill_color.split(",")))
  
  
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
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    
  elif (uploaded_img and (fill_color != (0, 0, 0))):
    #only use color mask with image 
    #if color is specified by the user
    #has performance issue
    img = qr.make_image(
            color_mask=VerticalGradiantColorMask(
              back_color=back_color,
              top_color=fill_color,
              bottom_color=fill_color
            ),
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
            )
          )
  
  buf = io.BytesIO()
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


app.run(host="0.0.0.0", port=3000, debug=True)