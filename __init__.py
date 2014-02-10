#coding: utf-8
from __future__ import unicode_literals

from os import path

from pytils.numeral import in_words

# from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.rl_config import defaultPageSize
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont

from math import sqrt

DEFAULT_WIDTH = 600
IMG_PATH = path.join(path.dirname(path.abspath(__file__)), 'png')
FONT_PATH = path.join(path.dirname(path.abspath(__file__)), 'fonts', 'DejaVuSans.ttf')

registerFont(TTFont('DejaVu', FONT_PATH))


def drawString(canvas, x, y, string):
    canvas.drawString(x, DEFAULT_WIDTH * 1.414 - y, string)


def drawNumber(canvas, x, y, number):
    y = DEFAULT_WIDTH * 1.414 - y
    if number == '0':
        canvas.line(x, y, x + 20, y)  # -
        canvas.line(x + 20, y, x + 20, y - 40)  # |
        canvas.line(x + 20, y - 40, x, y - 40)  # _
        canvas.line(x, y - 40, x, y)  # _
    elif number == '1':
        canvas.line(x, y - 20, x + 20, y)  # /
        canvas.line(x + 20, y, x + 20, y - 40)  # |
    elif number == '2':
        canvas.line(x, y, x + 20, y)
        canvas.line(x + 20, y, x + 20, y - 20)
        canvas.line(x + 20, y - 20, x, y - 40)
        canvas.line(x, y - 40, x + 20, y - 40)
    elif number == '3':
        canvas.line(x, y, x + 20, y)
        canvas.line(x + 20, y, x, y - 20)
        canvas.line(x, y - 20, x + 20, y - 20)
        canvas.line(x + 20, y - 20, x, y - 40)
    elif number == '4':
        canvas.line(x, y, x, y - 20)
        canvas.line(x, y - 20, x + 20, y - 20)
        canvas.line(x + 20, y, x + 20, y - 40)
    elif number == '5':
        canvas.line(x + 20, y, x, y)
        canvas.line(x, y, x, y - 20)
        canvas.line(x, y - 20, x + 20, y - 20)
        canvas.line(x + 20, y - 20, x + 20, y - 40)
        canvas.line(x + 20, y - 40, x, y - 40)
    elif number == '6':
        canvas.line(x + 20, y, x, y - 20)
        canvas.line(x, y - 20, x + 20, y - 20)
        canvas.line(x + 20, y - 20, x + 20, y - 40)
        canvas.line(x + 20, y - 40, x, y - 40)
        canvas.line(x, y - 40, x, y - 20)
    elif number == '7':
        canvas.line(x, y, x + 20, y)
        canvas.line(x + 20, y, x, y - 20)
        canvas.line(x, y - 20, x, y - 40)
    elif number == '8':
        canvas.line(x, y, x + 20, y)
        canvas.line(x + 20, y, x + 20, y - 40)
        canvas.line(x + 20, y - 40, x, y - 40)
        canvas.line(x, y - 40, x, y)
        canvas.line(x, y - 20, x + 20, y - 20)
    elif number == '9':
        canvas.line(x, y, x + 20, y)
        canvas.line(x + 20, y, x + 20, y - 20)
        canvas.line(x + 20, y - 20, x, y - 20)
        canvas.line(x, y - 20, x, y)
        canvas.line(x + 20, y - 20, x, y - 40)


def drawCheck(canvas, x, y):
    y = DEFAULT_WIDTH * 1.414 - y
    canvas.line(x, y, x + 5, y - 10)
    canvas.line(x + 5, y - 10, x + 10, y)


class LengthExceeded(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

    def string(self):
        return self.value


def splitToLines(string, lines_length):
    words = string.split(' ')
    line_number = 0
    outer_line_number = len(lines_length)
    lines = ['', ]

    for word in words:
        while len(lines[line_number]) + len(' ') + len(word) > lines_length[line_number]:
            # Not enough space at this line
            line_number += 1
            lines.append('')
            if line_number == outer_line_number:
                # LInes exceeded
                raise LengthExceeded(string)

        lines[line_number] += ' ' + word
    return lines


def verbose_price(price):
    if price is None or price == 0:
        return '-' * 30
    else:
        return str(price) + ' (' + in_words(price) + ') р.'


def numeric_price(price):
    if price is None or price == 0:
        return '-' * 10
    else:
        return str(price)


class RuspostBlank:
    canvas = None

    def render(self, canvas):
        pass

    def save(self, path):
        self.canvas = Canvas(path, pagesize=(defaultPageSize[0], defaultPageSize[1]))
        self.render(self.canvas)
        self.canvas.showPage()
        self.canvas.save()


class F7(RuspostBlank):
    def __init__(
        self,
        sender={
            'name': '',
            'address': '',
            'index': '',
        },
        recipient={
            'name': '',
            'address': '',
            'index': ' ' * 6,
        },
        price={
            'value': 0,
            'on_delivery': 0,
        },
        options={
            'standard': False,
            'heavy': False,
            'non_standard': False,
            'heavy_big': False,
            'usual': False,
            'valuable': False,
            'cash_on_delivery': False,
            'with_notification': False,
            'with_inventory': False,
        }
    ):
        self.sender = sender
        self.recipient = recipient
        self.price = price
        self.options = options

    def render(self, canvas):
        canvas.setFont('DejaVu', 14)

        # Set real size
        canvas.scale(1 / sqrt(2), 1 / sqrt(2))
        canvas.translate(10, 348)

        canvas.drawImage(path.join(IMG_PATH, 'F7.png'), 0, 11, width=595, height=None, preserveAspectRatio=True)

        # Sender
        sender_name_lines = splitToLines(self.sender.get('name', ''), (23, 30))
        drawString(canvas, 57, 162, sender_name_lines[0])
        if len(sender_name_lines) > 1:
            drawString(canvas, 10, 185, sender_name_lines[1])

        sender_address_lines = splitToLines(self.sender.get('address', ''), (23, 30, 18))
        drawString(canvas, 65, 212, sender_address_lines[0])
        if len(sender_address_lines) > 1:
            drawString(canvas, 10, 234, sender_address_lines[1])
        if len(sender_address_lines) > 2:
            drawString(canvas, 10, 259, sender_address_lines[2])

        for i in range(6):
            drawString(canvas, 141 + 20 * i, 254, self.sender.get('index', ' ' * 6)[i])

        # Price
        price_valuable_lines = splitToLines(verbose_price(self.price.get('value', 0)), (38, 38))
        if len(price_valuable_lines) == 1:
            drawString(canvas, 270, 179, price_valuable_lines[0])
        else:
            drawString(canvas, 270, 172, price_valuable_lines[0])
            drawString(canvas, 270, 184, price_valuable_lines[1])

        price_cash_on_delivery_lines = splitToLines(verbose_price(self.price.get('on_delivery', 0)), (38, 38))
        if len(price_cash_on_delivery_lines) == 1:
            drawString(canvas, 270, 224, price_cash_on_delivery_lines[0])
        else:
            drawString(canvas, 270, 215, price_cash_on_delivery_lines[0])
            drawString(canvas, 270, 229, price_cash_on_delivery_lines[1])

        # Recipient
        recipient_name_lines = splitToLines(self.recipient.get('name', ''), (31, 35))
        drawString(canvas, 317, 254, recipient_name_lines[0])
        if len(recipient_name_lines) > 1:
            drawString(canvas, 290, 278, recipient_name_lines[1])

        recipient_address_lines = splitToLines(self.recipient.get('address', ''), (31, 35, 21))
        drawString(canvas, 315, 303, recipient_address_lines[0])
        if len(recipient_address_lines) > 1:
            drawString(canvas, 290, 328, recipient_address_lines[1])
        if len(recipient_address_lines) > 2:
            drawString(canvas, 290, 353, recipient_address_lines[2])

        for i in range(6):
            drawString(canvas, 465 + 20 * i, 348, self.recipient.get('index', ' ' * 6)[i])

        # Index
        for i in range(6):
            drawNumber(canvas, 52 + 36 * i, 366, self.recipient.get('index', ' ' * 6)[i])

        # Options
        if self.options.get('standard', False):
            drawCheck(canvas, 232, 47)
        if self.options.get('heavy', False):
            drawCheck(canvas, 349, 47)
        if self.options.get('non_standard', False):
            drawCheck(canvas, 232, 77)
        if self.options.get('heavy_big', False):
            drawCheck(canvas, 348, 79)
        if self.options.get('usual', False):
            drawCheck(canvas, 15, 112)
        if self.options.get('valuable', False):
            drawCheck(canvas, 138, 112)
        if self.options.get('cash_on_delivery', False):
            drawCheck(canvas, 298, 112)
        if self.options.get('with_notification', False):
            drawCheck(canvas, 15, 131)
        if self.options.get('with_inventory', False):
            drawCheck(canvas, 138, 131)


class F7_1CL(RuspostBlank):
    def __init__(
        self,
        sender={
            'name': '',
            'address': '',
            'index': ' ' * 6,
        },
        recipient={
            'name': '',
            'address': '',
            'index': ' ' * 6,
        },
        price={
            'value': 0,
            'on_delivery': 0,
        },
        options={
            'letter_1_class': False,
            'parcel_1_class': False,
            'registered': False,
            'valuable': False,
            'cash_on_delivery': False,
            'with_simple_notification': False,
            'with_registered_notification': False,
            'with_inventory': False,
        }
    ):
        self.sender = sender
        self.recipient = recipient
        self.price = price
        self.options = options

    def render(self, canvas):
        canvas.setFont('DejaVu', 14)

        # Set real size
        canvas.scale(1 / sqrt(2), 1 / sqrt(2))
        canvas.translate(10, 348)

        canvas.drawImage(path.join(IMG_PATH, 'F7_1cl.png'), 0, 15, width=595, height=None, preserveAspectRatio=True)

        # Sender
        sender_name_lines = splitToLines(self.sender.get('name', ''), (23, 30))
        drawString(canvas, 55, 170, sender_name_lines[0])
        if len(sender_name_lines) > 1:
            drawString(canvas, 10, 193, sender_name_lines[1])

        sender_address_lines = splitToLines(self.sender.get('address', ''), (23, 30, 30))
        drawString(canvas, 55, 220, sender_address_lines[0])
        if len(sender_address_lines) > 1:
            drawString(canvas, 10, 241, sender_address_lines[1])
        if len(sender_address_lines) > 2:
            drawString(canvas, 10, 266, sender_address_lines[2])

        for i in range(6):
            drawString(canvas, 137 + 20 * i, 286, self.sender.get('index', ' ' * 6)[i])

        # Price
        price_valuable_lines = splitToLines(verbose_price(self.price.get('value', 0)), (38, 38))
        if len(price_valuable_lines) == 1:
            drawString(canvas, 270, 170, price_valuable_lines[0])
        else:
            drawString(canvas, 270, 165, price_valuable_lines[0])
            drawString(canvas, 270, 178, price_valuable_lines[1])

        price_cash_on_delivery_lines = splitToLines(verbose_price(self.price.get('on_delivery', 0)), (38, 38))
        if len(price_cash_on_delivery_lines) == 1:
            drawString(canvas, 270, 210, price_cash_on_delivery_lines[0])
        else:
            drawString(canvas, 270, 205, price_cash_on_delivery_lines[0])
            drawString(canvas, 270, 220, price_cash_on_delivery_lines[1])

        # Recipient
        recipient_name_lines = splitToLines(self.recipient.get('name', ''), (31, 35))
        drawString(canvas, 315, 252, recipient_name_lines[0])
        if len(recipient_name_lines) > 1:
            drawString(canvas, 283, 272, recipient_name_lines[1])

        recipient_address_lines = splitToLines(self.recipient.get('address', ''), (31, 35, 21))
        drawString(canvas, 305, 301, recipient_address_lines[0])
        if len(recipient_address_lines) > 1:
            drawString(canvas, 280, 324, recipient_address_lines[1])
        if len(recipient_address_lines) > 2:
            drawString(canvas, 280, 350, recipient_address_lines[2])

        for i in range(6):
            drawString(canvas, 460 + 20 * i, 345, self.recipient.get('index', ' ' * 6)[i])

        # Index
        for i in range(6):
            drawNumber(canvas, 52 + 36 * i, 368, self.recipient.get('index', ' ' * 6)[i])

        # Options
        if self.options.get('letter_1_class', False):
            drawCheck(canvas, 230, 22)
        if self.options.get('parcel_1_class', False):
            drawCheck(canvas, 230, 38)
        if self.options.get('registered', False):
            drawCheck(canvas, 230, 52)
        if self.options.get('valuable', False):
            drawCheck(canvas, 230, 72)
        if self.options.get('cash_on_delivery', False):
            drawCheck(canvas, 336, 22)
        if self.options.get('with_simple_notification', False):
            drawCheck(canvas, 336, 39)
        if self.options.get('with_registered_notification', False):
            drawCheck(canvas, 336, 53)
        if self.options.get('with_inventory', False):
            drawCheck(canvas, 336, 72)


class F113(RuspostBlank):
    def __init__(
        self,
        sender={
            'name': '',
            'address': '',
            'index': ' ' * 6,
        },
        recipient={
            'name': '',
            'address': '',
            'index': ' ' * 6,
            'inn': ' ' * 12,
            'ks': '' * 20,
            'bank': '',
            'rs': ' ' * 20,
            'bik': ' ' * 9,
        },
        price={
            'on_delivery': 0,
        }
    ):
        self.sender = sender
        self.recipient = recipient
        self.price = price

    def render_page(self, canvas, page):
        canvas.setFont('DejaVu', 9)

        if page == 1:
            canvas.drawImage(path.join(IMG_PATH, 'F113_1.png'), 0, 110, width=600, height=None, preserveAspectRatio=True)

            # Price
            drawString(canvas, 450, 158, numeric_price(self.price.get('on_delivery', 0)))
            drawString(canvas, 510, 158, '00')
            price_cash_on_delivery_lines = splitToLines(in_words(self.price.get('on_delivery', 0) or 0) + ' р. 00 к.', (55, 55))  # 'or 0' if main value is None
            if len(price_cash_on_delivery_lines) == 1:
                drawString(canvas, 250, 170, price_cash_on_delivery_lines[0])
            else:
                drawString(canvas, 250, 167, price_cash_on_delivery_lines[0])
                drawString(canvas, 250, 174, price_cash_on_delivery_lines[1])

            # Recipient
            recipient_name_lines = splitToLines(self.recipient.get('name', ''), (55, 65))
            drawString(canvas, 265, 188, recipient_name_lines[0])
            if len(recipient_name_lines) > 1:
                drawString(canvas, 250, 200, recipient_name_lines[1])

            recipient_address_lines = splitToLines(self.recipient.get('address', ''), (55, 65))
            drawString(canvas, 265, 213, recipient_address_lines[0])
            if len(recipient_address_lines) > 1:
                drawString(canvas, 250, 228, recipient_address_lines[1])

            for i in range(6):
                drawString(canvas, 505 + 8 * i - i / 3, 247, self.recipient.get('index', ' ' * 6)[i])

            # Bank
            for i in range(12):
                drawString(canvas, 266 + 8 * i - i / 3, 263, self.recipient.get('inn', ' ' * 12)[i])

            for i in range(20):
                drawString(canvas, 398 + 8 * i - i / 3, 263, self.recipient.get('ks', ' ' * 20)[i])

            bank_lines = splitToLines(self.recipient.get('bank', ''), (76, ))
            drawString(canvas, 320, 277, bank_lines[0])

            for i in range(20):
                drawString(canvas, 288 + 8 * i - i / 3, 289, self.recipient.get('rs', ' ' * 20)[i])

            for i in range(9):
                drawString(canvas, 482 + 8 * i - i / 3, 289, self.recipient.get('bik', ' ' * 9)[i])

            # Sender
            sender_name_lines = splitToLines(self.sender.get('name', ''), (26, 50))
            drawString(canvas, 280, 380, sender_name_lines[0])
            if len(sender_name_lines) > 1:
                drawString(canvas, 250, 392, sender_name_lines[1])

            sender_address_lines = splitToLines(self.sender.get('address', ''), (42, 55, 42))
            drawString(canvas, 325, 406, sender_address_lines[0])
            if len(sender_address_lines) > 1:
                drawString(canvas, 250, 420, sender_address_lines[1])
            if len(sender_address_lines) > 2:
                drawString(canvas, 250, 435, sender_address_lines[2])

            for i in range(6):
                drawString(canvas, 507 + 7 * i + i / 2, 434, self.sender.get('index', ' ' * 6)[i])
        elif page == 2:
            canvas.drawImage(path.join(IMG_PATH, 'F113_2.png'), 0, 110, width=600, height=None, preserveAspectRatio=True)
        else:
            raise ValueError('Unknown page: ' + str(page))

    def render(self, canvas):
        self.render_page(canvas, 1)
        canvas.showPage()
        self.render_page(canvas, 2)


class F116(RuspostBlank):
    def __init__(
        self,
        sender={
            'name': '',
            'address': '',
            'index': ' ' * 6,
            'document': 'паспорт',
            'serie': '',
            'number': '',
            'issue_day_month': '',
            'issue_year': '',
            'issuer': '',
        },
        recipient={
            'name': '',
            'address': '',
            'index': ' ' * 6,
        },
        price={
            'value': 0,
            'on_delivery': 0,
        }
    ):
        self.sender = sender
        self.recipient = recipient
        self.price = price

    def render_page(self, canvas, page):
        canvas.setFont('DejaVu', 12)

        if page == 1:
            # Set real size
            canvas.scale(1 / sqrt(2), 1 / sqrt(2))
            canvas.translate(-5, 1190)
            canvas.rotate(-90)

            canvas.drawImage(path.join(IMG_PATH, 'F116_1.png'), 0, -210, width=595, height=None, preserveAspectRatio=True)

            # Price
            price_valuable_lines = splitToLines(verbose_price(self.price.get('value', 0)), (37, 40))
            if len(price_valuable_lines) == 1:
                drawString(canvas, 90, 206, price_valuable_lines[0])
            else:
                drawString(canvas, 90, 203, price_valuable_lines[0])
                drawString(canvas, 95, 212, price_valuable_lines[1])

            price_cash_on_delivery_lines = splitToLines(verbose_price(self.price.get('on_delivery', 0)), (37, 40))
            if len(price_cash_on_delivery_lines) == 1:
                drawString(canvas, 90, 240, price_cash_on_delivery_lines[0])
            else:
                drawString(canvas, 90, 235, price_cash_on_delivery_lines[0])
                drawString(canvas, 95, 244, price_cash_on_delivery_lines[1])

            # Recipient
            recipient_name_lines = splitToLines(self.recipient.get('name', ''), (29, 29))
            if len(recipient_name_lines) == 1:
                drawString(canvas, 130, 273, recipient_name_lines[0])
            else:
                drawString(canvas, 130, 264, recipient_name_lines[0])
                drawString(canvas, 132, 273, recipient_name_lines[1])

            recipient_address_lines = splitToLines(self.recipient.get('address', ''), (29, 34, 17))
            drawString(canvas, 130, 289, recipient_address_lines[0])
            if len(recipient_address_lines) > 1:
                drawString(canvas, 95, 305, recipient_address_lines[1])
            if len(recipient_address_lines) > 2:
                drawString(canvas, 95, 322, recipient_address_lines[2])

            for i in range(6):
                drawString(canvas, 225 + 19 * i + i / 2, 320, self.recipient.get('index', ' ' * 6)[i])

            # Sender
            sender_name_lines = splitToLines(self.sender.get('name', ''), (53, ))
            drawString(canvas, 143, 342, sender_name_lines[0])

            sender_address_lines = splitToLines(self.sender.get('address', ''), (55, 50))
            drawString(canvas, 135, 361, sender_address_lines[0])
            if len(sender_address_lines) > 1:
                drawString(canvas, 95, 380, sender_address_lines[1])

            for i in range(6):
                drawString(canvas, 395 + 19 * i + i / 2, 377, self.sender.get('index', ' ' * 6)[i])

            drawString(canvas, 167, 436, self.sender.get('document', 'паспорт'))
            drawString(canvas, 260, 436, self.sender.get('serie', ''))
            drawString(canvas, 310, 436, self.sender.get('number', ''))
            drawString(canvas, 430, 436, self.sender.get('issue_day_month', ''))
            drawString(canvas, 490, 436, self.sender.get('issue_year', ''))

            sender_issuer_lines = splitToLines(self.sender.get('issuer', ''), (59, 59))
            if len(sender_issuer_lines) == 1:
                drawString(canvas, 100, 459, sender_issuer_lines[0])
            else:
                drawString(canvas, 100, 450, sender_issuer_lines[0])
                drawString(canvas, 100, 459, sender_issuer_lines[1])

            # # Price
            drawString(canvas, 180, 657, numeric_price(self.price.get('value', 0)))
            drawString(canvas, 410, 657, numeric_price(self.price.get('on_delivery', 0)))

            # Recipient
            recipient_name_lines = splitToLines(self.recipient.get('name', ''), (55, 55))
            if len(recipient_name_lines) == 1:
                drawString(canvas, 130, 683, recipient_name_lines[0])
            else:
                drawString(canvas, 130, 675, recipient_name_lines[0])
                drawString(canvas, 130, 683, recipient_name_lines[1])

            recipient_address_lines = splitToLines(self.recipient.get('address', ''), (55, 30))
            drawString(canvas, 135, 705, recipient_address_lines[0])
            if len(recipient_address_lines) > 1:
                drawString(canvas, 100, 725, recipient_address_lines[1])

            for i in range(6):
                drawString(canvas, 398 + 19 * i + i / 2, 725, self.recipient.get('index', ' ' * 6)[i])
        elif page == 2:
            # Set real size
            canvas.scale(1 / sqrt(2), 1 / sqrt(2))
            canvas.translate(850, 600)
            canvas.rotate(90)

            canvas.drawImage(path.join(IMG_PATH, 'F116_2.png'), 0, -210, width=595, height=None, preserveAspectRatio=True)
        else:
            raise ValueError('Unknown page: ' + str(page))

    def render(self, canvas):
        self.render_page(canvas, 1)
        canvas.showPage()
        self.render_page(canvas, 2)
