import os
from PIL import Image, ImageDraw, ImageFont

list_of_names = []

def delete_old_data():
    for i in os.listdir("generated-certificates/"):
        os.remove("generated-certificates/{}".format(i))

def cleanup_data():
    with open('name-data.txt') as f:
        for line in f:
            list_of_names.append(line.strip())

def generate_certificates():
    custom_font = "CinzelDecorative-Bold.ttf"  # Path to your custom font file
    font_size = 80
    font_color = (71, 71, 71)

    for index, name in enumerate(list_of_names):
        certificate_template = Image.open("certificate-template.jpg")
        draw = ImageDraw.Draw(certificate_template)

        # Load the custom font and use it
        font = ImageFont.truetype(custom_font, font_size)
        
        # Specify the position and color
        position = (715, 618)
        draw.text(position, name.strip(), font=font, fill=font_color)

        certificate_template.save("generated-certificates/{}.jpg".format(name.strip()))
        print("Processing {} / {}".format(index + 1, len(list_of_names)))

def main():
    delete_old_data()
    cleanup_data()
    generate_certificates()

if __name__ == '__main__':
    main()
