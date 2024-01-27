
import pygame_menu
from pygame_menu import themes
import pygame


pygame.init()
surface = pygame.display.set_mode((1280, 640), pygame.RESIZABLE)
pygame.display.set_caption("MAIN MENU")

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.otf", size)
def set_difficulty(value, difficulty):
    print(value)
    print(difficulty)
def recognition():
    from image_process import get_output_image
    pygame.display.set_caption("DIGIT RECOGNIZER")
    # pre defined colors, pen radius and font color
    black = [0, 0, 0]
    white = [255, 255, 255]
    draw_on = False
    last_pos = (0, 0)
    color = (255, 128, 0)
    radius = 5


    # image size
    width = 640
    height = 640

    # initializing screen
    # screen = pygame.display.set_mode((width * 2, height))
    surface.fill(white)
    pygame.font.init()



    def show_output_image(img):
        surf = pygame.pixelcopy.make_surface(img)
        surf = pygame.transform.rotate(surf, -270)
        surf = pygame.transform.flip(surf, 0, 1)
        surface.blit(surf, (width + 2, 0))

    def crope(orginal):
        cropped = pygame.Surface((width - 5, height - 5))
        cropped.blit(orginal, (0, 0), (0, 0, width - 5, height - 5))
        return cropped

    def roundline(srf, color, start, end, radius=1):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        distance = max(abs(dx), abs(dy))
        for i in range(distance):
            x = int(start[0] + float(i) / distance * dx)
            y = int(start[1] + float(i) / distance * dy)
            pygame.draw.circle(srf, color, (x, y), radius)

    def draw_partition_line():
        # middle line
        pygame.draw.line(surface, black, [width, 0], [width, height], 2)
        pygame.draw.line(surface, (139,125,107), [width+2, 0], [width+2, height], 3)


    try:
        while True:

            # get all events
            e = pygame.event.wait()
            draw_partition_line()

            # clear screen after right click
            if (e.type == pygame.MOUSEBUTTONDOWN and e.button == 3):
                surface.fill(white)


            # quit
            if e.type == pygame.QUIT:
                raise StopIteration

            # start drawing after left click
            if (e.type == pygame.MOUSEBUTTONDOWN and e.button != 3):
                color = black
                pygame.draw.circle(surface, color, e.pos, radius)
                draw_on = True

            # stop drawing after releasing left click
            if e.type == pygame.MOUSEBUTTONUP and e.button != 3:
                draw_on = False
                fname = "out.png"

                img = crope(surface)
                pygame.image.save(img, fname)

                output_img = get_output_image(fname)
                show_output_image(output_img)

            # start drawing line on screen if draw is true
            if e.type == pygame.MOUSEMOTION:
                if draw_on:
                    pygame.draw.circle(surface, color, e.pos, radius)
                    roundline(surface, color, e.pos, last_pos, radius)
                last_pos = e.pos

            pygame.display.flip()

    except StopIteration:
        pass
    menu_bar()
    # pygame.quit()
def menu_bar():

    def open_the_app():
        mainmenu._open(loading)
        pygame.time.set_timer(update_loading, 10)


    # menu//////////////
    mainmenu = pygame_menu.Menu('Welcome', 1280, 640, theme=themes.THEME_SOLARIZED)
    mainmenu.add.button('Open', open_the_app)
    mainmenu.add.button('Quit', pygame_menu.events.EXIT)



    loading = pygame_menu.Menu('Loading...', 1280, 640, theme=themes.THEME_DARK)
    loading.add.progress_bar("Progress", progressbar_id="1", default=0, width=200, )

    arrow = pygame_menu.widgets.RightArrowSelection(arrow_size=(10, 15))

    update_loading = pygame.USEREVENT + 0

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == update_loading:
                progress = loading.get_widget("1")
                progress.set_value(progress.get_value() + 1)
                if progress.get_value() == 100:
                    pygame.time.set_timer(update_loading, 0)
                    mainmenu.disable()
                    recognition()


            if event.type == pygame.QUIT:
                exit()

        if mainmenu.is_enabled():
            mainmenu.update(events)
            mainmenu.draw(surface)
            if (mainmenu.get_current().get_selected_widget()):
                arrow.draw(surface, mainmenu.get_current().get_selected_widget())

        pygame.display.update()
menu_bar()