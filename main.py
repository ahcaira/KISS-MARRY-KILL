import os
import random
from tkinter import *

from PIL import Image, ImageTk


# 1920x1080, 1500,720
screen_width, screen_height =   1500,900  # TODO strange resolution
picture_width, picture_height = 460, 700
between_x_space = (screen_width - picture_width * 3) / 4
between_y_space = (screen_height - picture_height) / 2

# Main screen
root = Tk()
root.attributes("-fullscreen", True)
root.geometry(f'{screen_width}x{screen_height}')
root.resizable(width=False, height=False)

# Background
canvas = Canvas(root, height=screen_height, width=screen_width)
canvas.pack()
background_image = ImageTk.PhotoImage(Image.open(os.getcwd() + '/background_images/img.png')
                                      .resize((screen_width, screen_height)))
background = Label(canvas, image=background_image)
background.place(x=0, y=0)

# Photos
photo_1 = Label(canvas, cursor='fleur', background='green') # TODO collapse 3 in 1
photo_2 = Label(canvas, cursor='fleur', background='green')
photo_3 = Label(canvas, cursor='fleur', background='green')
photo_1.place(x=between_x_space, y=between_y_space)
photo_2.place(x=picture_width + between_x_space + between_x_space, y=between_y_space)
photo_3.place(x=(picture_width + between_x_space) * 2 + between_x_space, y=between_y_space)

# Useful variables
rectangle_colors = ['red', 'white', 'black']
cursors = ['fleur', 'heart', 'dotbox']
cursor_pointer = 1
number_of_pics_picked = 0
number_of_fake_photos = [0, 0, 0]  # photos for roulette
pics_picked = {'!label2': False, '!label3': False, '!label4': False}  # TODO change
image_paths = ['', '', '']
image_folders = ['', '', '']
images = ['', '', '']
roulette_images = ['' for _ in range(16)]
number_of_game = 1

cwd = os.getcwd() + '/images/'


def pickImage(which):
    # which as int is for filling roulette images, as list is for filling 3 main images
    # TODO: refactor excluding main if
    if type(which) is int:
        number_of_pics_generated = 0
        while number_of_pics_generated != which:
            randomFolder = random.choice(os.listdir(cwd))
            randomfile = random.choice(os.listdir(cwd + '/' + randomFolder))
            full_path = cwd + '/' + randomFolder + '/' + randomfile
            if full_path[-3:] == 'jpg' and randomFolder != 'removed':
                roulette_images[number_of_pics_generated] = ImageTk.PhotoImage(
                    Image.open(full_path).resize((picture_width, picture_height)))
                number_of_pics_generated += 1
    else:
        for pic_number in which:
            image_paths[pic_number] = ''
            image_folders[pic_number] = ''
            while image_paths[pic_number] == '':
                randomFolder = random.choice(os.listdir(cwd))
                if randomFolder in image_folders:
                    continue
                randomfile = random.choice(os.listdir(cwd + '/' + randomFolder))
                image_folders[pic_number] = randomFolder
                full_path = cwd + '/' + randomFolder + '/' + randomfile
                if full_path not in image_paths and full_path[-3:] == 'jpg' and randomFolder != 'removed':
                    image_paths[pic_number] = full_path
                    images[pic_number] = ImageTk.PhotoImage(Image.open(image_paths[pic_number])
                                                       .resize((picture_width, picture_height)))


def mark_chosen_pic(event):
    global rectangle_colors, number_of_pics_picked, pics_picked, cursor_pointer
    if number_of_pics_picked < 3 and not pics_picked[event.widget.winfo_name()]:
        event.widget.config(background=rectangle_colors[number_of_pics_picked])
        pics_picked[event.widget.winfo_name()] = True
        number_of_pics_picked += 1
        photo_1.config(cursor=cursors[cursor_pointer])
        photo_2.config(cursor=cursors[cursor_pointer])
        photo_3.config(cursor=cursors[cursor_pointer])
        cursor_pointer = (cursor_pointer + 1) % 3
    elif number_of_pics_picked >= 3:
        draw_new_pictures([0, 1, 2])
        pics_picked = {'!label2': False, '!label3': False, '!label4': False}
        number_of_pics_picked = 0


def draw_new_pictures(which):
    global cwd, number_of_game
    print(f'Game number №{number_of_game}')
    number_of_game += 1
    pickImage(which)
    pickImage(15)

    for i in range(3):
        number_of_fake_photos[i] = random.randint(3, 5)

    roulette_images_1 = roulette_images[0:number_of_fake_photos[0] - 1]
    roulette_images_2 = roulette_images[number_of_fake_photos[0]:number_of_fake_photos[0] + number_of_fake_photos[1] - 1]
    roulette_images_3 = roulette_images[
            number_of_fake_photos[0] + number_of_fake_photos[1]:number_of_fake_photos[0] + number_of_fake_photos[1] +
                                                                number_of_fake_photos[2] - 1]
    if 0 in which:
        move_image(photo_1, roulette_images_1, 0, images[0], number_of_fake_photos[0], 70, between_x_space)
    if 1 in which:
        move_image(photo_2, roulette_images_2, 0, images[1], number_of_fake_photos[1], 50, picture_width +
                   between_x_space + between_x_space)
    if 2 in which:
        move_image(photo_3, roulette_images_3, 0, images[2], number_of_fake_photos[2], 25,
                   (picture_width + between_x_space) * 2 + between_x_space)


def move_image(image, roulette_imgs, number_of_photo_in_roulette, actual_photo, num, speed, x):
    y = int(image.place_info()['y'])
    if y > 50 and number_of_photo_in_roulette == num - 1:
        image.place(x=x, y=between_y_space)
        image.config(background='green')
        image.config(image=actual_photo)
        image.image = actual_photo
        return 0

    if y > 800:
        image.place(x=x, y=-700)
        if number_of_photo_in_roulette == num - 2:
            image.config(image=actual_photo)
            image.image = actual_photo
            number_of_photo_in_roulette += 1
        else:
            image.config(image=roulette_imgs[number_of_photo_in_roulette])
            image.image = roulette_imgs[number_of_photo_in_roulette]
            number_of_photo_in_roulette += 1
    else:
        image.place(x=x, y=y+speed)
    image.after(20, move_image, image, roulette_imgs, number_of_photo_in_roulette, actual_photo, num, speed, x)


def delete_photo(event=None): # TODO make great again
    x, y = event.x, event.y
    which = 5
    if x < picture_width and 10 < y < 10 + picture_height:
        which = 0
    if picture_width + between_x_space < x < picture_width + between_x_space + picture_width and 10 < y < 10 + picture_height:
        which = 1
    if (picture_width + between_x_space) * 2 < x and 10 < y < 10 + picture_height:
        which = 2
    os.rename(image_paths[which], os.getcwd() + f"/inst_filtered/removed/{image_paths[which].split('/')[-1]}")
    draw_new_pictures([which])


def delete_folder(event):
    # if number_of_game == 10:
    #    shutil.rmtree('./temp_images')
    pass


def show_image(event): # TODO add statistics
    for path in image_paths:
        print(path)


if __name__ == "__main__":
    draw_new_pictures([0, 1, 2])

    photo_1.bind("<Button 1>", mark_chosen_pic)
    photo_2.bind("<Button 1>", mark_chosen_pic)
    photo_3.bind("<Button 1>", mark_chosen_pic)

    root.bind('ESC', lambda root: root.attributes("-fullscreen", False))
    # label2.bind_all("<space>", delete_photo)
    # label2.bind_all('<Button 2>', show_image)
    root.mainloop()
