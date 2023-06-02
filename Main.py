import telebot

from reportlab.pdfgen import canvas

from io import BytesIO

# Connect to the Telegram bot

bot = telebot.TeleBot('YOUR_TELEGRAM_BOT_TOKEN')

# Directory to store downloaded images

IMAGES_DIR = 'images/'

# Create the directory if it doesn't exist

if not os.path.exists(IMAGES_DIR):

    os.makedirs(IMAGES_DIR)

# Store the messages and pictures from the group chat

messages = []

pictures = []

# Retrieve messages and pictures from the group chat

@bot.message_handler(func=lambda message: True)

def handle_messages(message):

    # Save the message

    messages.append(message.text)

    

    # Save the picture to a file

    if message.photo:

        file_id = message.photo[-1].file_id

        file_info = bot.get_file(file_id)

        downloaded_file = bot.download_file(file_info.file_path)

        picture_path = os.path.join(IMAGES_DIR, f'picture_{len(pictures)}.jpg')

        with open(picture_path, 'wb') as pic:

            pic.write(downloaded_file)

        pictures.append(picture_path)

# Handle the "/compile" command to compile messages and pictures into a PDF

@bot.message_handler(commands=['compile'])

def handle_compile(message):

    # Create a PDF document

    pdf_path = 'output.pdf'

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)

    # Add messages to the PDF document

    y = 750  # Initial y-coordinate

    for message in messages:

        pdf.drawString(50, y, message)

        y -= 20  # Decrease y-coordinate for the next message

    # Add pictures to the PDF document

    for picture_path in pictures:

        pdf.drawInlineImage(picture_path, 50, y, width=400, height=400)

        y -= 420  # Decrease y-coordinate for the next picture

    pdf.save()

    # Get the PDF content from the buffer

    buffer.seek(0)

    pdf_bytes = buffer.getvalue()

    # Send the compiled PDF back to the user who requested it

    bot.send_document(chat_id=message.chat.id, data=pdf_bytes, filename='output.pdf')

# Start the bot

bot.polling()

