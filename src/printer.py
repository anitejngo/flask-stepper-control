from PIL import Image, ImageDraw, ImageFont
from brother_ql.backends.helpers import send
from brother_ql.conversion import convert
from brother_ql.raster import BrotherQLRaster


def print_label_and_description(cut, cut_description):
    cut = str(cut)
    try:
        filename = 'label.png'
        font = ImageFont.truetype('./assets/Lato-Regular.ttf', 68)
        img = Image.new('RGB', (696, 100), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        if cut_description:
            cut_description = str(cut_description)
            d.text((12, 6), cut_description + " | " + cut + 'm', font=font, fill=(0, 0, 0))
        else:
            d.text((12, 6), cut + 'cm', font=font, fill=(0, 0, 0))

        img.save('./labelPrint/' + filename)
        print("IMG sent to PRINTER")
        send_to_printer('./labelPrint/' + filename)
    except Exception as E:
        print("Failed to print")
        print(E)
        pass


def send_to_printer(image):
    im = Image.open(image)
    backend = 'pyusb'  # 'pyusb', 'linux_kernal', 'network'
    model = 'QL-700'  # your printer model.
    printer = 'usb://0x04f9:0x2042'

    qlr = BrotherQLRaster(model)
    qlr.exception_on_warning = True

    instructions = convert(
        qlr=qlr,
        images=[im],  # Takes a list of file names or PIL objects.
        label='62',
        rotate='0',  # 'Auto', '0', '90', '270'
        threshold=70.0,  # Black and white threshold in percent.
        dither=False,
        compress=False,
        red=False,  # Only True if using Red/Black 62 mm label tape.
        dpi_600=False,
        hq=True,  # False for low quality.
        cut=True
    )

    send(instructions=instructions, printer_identifier=printer, backend_identifier=backend, blocking=True)
