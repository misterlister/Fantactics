from graphics import Window, Point, WINDOW_HEIGHT, WINDOW_WIDTH, BG_COL, LINE_WIDTH
from tkinter import Tk
from PIL import ImageTk, Image
from userInterface import UserInterface, SPRITE_BUFFER, do_nothing
from constants import *


class GameBoard:
    def __init__(
            self,
            window: Window,
            root: Tk,
            ui: UserInterface,
            x_start: int = DEFAULT_X_POS,
            y_start: int = DEFAULT_Y_POS,
            square_size: int = DEFAULT_SQUARE_SIZE
                 ) -> None:
        self.window = window
        self.root = root
        self.ui = ui
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_start + (BOARD_COLS * square_size) 
        self.y_end = y_start + (BOARD_ROWS * square_size)
        self.square_size = square_size
        self.__spaces = [[Space(i, j) for j in range(BOARD_COLS)] for i in range(BOARD_ROWS)]
        self.connect_spaces(self.__spaces)
        self.draw_board()
        self.window.canvas.bind('<Button-1>', self.click)
        self.window.canvas.bind('<Button-3>', self.right_click)
        self.selected_space = None
        self.selected_unit = None
        self.action_space = None
        self.__valid_moves = None
        self.__attack_spaces = None
        self.__ability_spaces = None
        self.__transparent_square = self.set_transparency()
        self.__game_state = None
    
    def draw_board(self) -> None:
        for i in range (BOARD_ROWS + 1):
            y_position = self.get_row_y(i)
            p1 = Point(self.x_start, y_position)
            p2 = Point(self.x_end, y_position)
            self.window.draw_line(p1, p2)

        for j in range (BOARD_COLS + 1):
            x_position = self.get_col_x(j)
            p1 = Point(x_position, self.y_start)
            p2 = Point(x_position, self.y_end)
            self.window.draw_line(p1, p2)

    def link_to_state(self, state):
        self.__game_state = state

    def click(self, event):
        if event.x > self.x_start and event.x < self.x_end:
            if event.y > self.y_start and event.y < self.y_end:
                row = (event.y-self.y_start) // self.square_size
                col = (event.x-self.x_start) // self.square_size
                contents = self.check_square(row, col)
                print(f"Clicked square {row},{col}. Contents: {contents}")
                new_space = self.__spaces[row][col]
                if self.selected_unit is None: # No unit is currently selected
                    if self.selected_space is not None: # If another space was already selected
                        if self.selected_space == new_space: # If a selected space is selected, deselect it
                            self.deselect_space()
                            self.clear_stats_panel()
                            return
                        self.deselect_space()
                    self.select_space(row, col)
                    self.update_stats_panel(self.selected_unit)
                    return
                else: # A unit is currently selected
                    unit = self.selected_unit
                    if unit.get_player().is_current_turn():
                        if self.__attack_spaces != None: # Attack range is active
                            if new_space in self.__attack_spaces: # A valid target is selected
                                self.update_stats_panel(new_space.get_unit()) 
                                self.move_unit(unit, self.action_space)
                                self.combat(unit, new_space.get_unit())
                                self.end_turn()
                                return
                        if self.__ability_spaces != None: # Ability range is active
                            if new_space in self.__ability_spaces: # A valid target is selected
                                self.move_unit(unit, self.action_space)
                                self.update_stats_panel(new_space.get_unit()) 
                                self.activate_ability(unit, new_space)
                                self.end_turn()
                                return
                        if self.action_space == new_space: # Movement to a new space is confirmed
                            self.move_and_wait(unit, new_space)
                            return
                        elif new_space in self.__valid_moves: # A new action space is selected
                            self.set_action_space(unit, new_space)
                            self.set_attack_spaces(unit, new_space)
                            return
                    else:
                        print("You cannot move enemy units")

                    print("Cancelled Action.")
                    self.cancel_action()

    def right_click(self, event):
        self.cancel_action()
                
    def connect_spaces(self, spaces):
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if j-1 >= 0:
                    spaces[i][j].set_left(spaces[i][j-1])
                if i-1 >= 0:
                    spaces[i][j].set_up(spaces[i-1][j])
                if j+1 < BOARD_COLS:
                    spaces[i][j].set_right(spaces[i][j+1])
                if i+1 < BOARD_ROWS:
                    spaces[i][j].set_down(spaces[i+1][j])


    # Update the stats panel items
    # Should be called on selection of a unit
    def update_stats_panel(self, unit):
        if unit is not None:
            if unit.get_player().is_current_turn():
                panel = 'friendlyUnitPanel'
            else:
                panel = 'enemyUnitPanel'
            sprite = unit.get_sprite()
            self.ui.statsPanel[panel].update_image(self.window.get_sprite(sprite))
            self.ui.statsPanel[panel].update_name(unit.get_name())
            self.ui.statsPanel[panel].update_health(unit.get_curr_hp(), unit.get_max_hp())
            self.ui.statsPanel[panel].update_damage(unit.get_damage_val())
            self.ui.statsPanel[panel].update_armour(unit.get_armour_val())
            self.ui.statsPanel[panel].update_movement(unit.get_movement())
        else:
            self.clear_stats_panel()

    def clear_stats_panel(self):
        for panel in self.ui.statsPanel:
            self.ui.statsPanel[panel].clear()

    def outline_space(self, row: int, col: int, colour: str) -> None:
        x1 = self.get_col_x(col) + LINE_WIDTH
        y1 = self.get_row_y(row) + LINE_WIDTH
        x2 = self.get_col_x(col+1) - LINE_WIDTH
        y2 = self.get_row_y(row+1) - LINE_WIDTH
        self.window.canvas.create_rectangle(x1, y1, x2, y2, width=SELECTION_BUFFER, outline=colour)

    def check_square(self, row: int, col: int):
        if row > BOARD_ROWS or col > BOARD_COLS:
            return "Outside Grid"
        else:
            unit = self.__spaces[row][col].get_unit()
            if unit is None:
                return unit
            return unit.get_name()
        
    def get_space(self, row, col):
        return self.__spaces[row][col]
        
    def place_unit(self, unit, row: int, col: int) -> bool:
        if self.__spaces[row][col].get_unit() != None:
            return False
        self.__spaces[row][col].assign_unit(unit)
        return True
    
    def draw_space(self, space) -> None:
        col = space.get_col()
        row = space.get_row()
        x = self.get_col_x(col) + SPRITE_BUFFER/2
        y = self.get_row_y(row) + SPRITE_BUFFER/2
        #terrain = self.__spaces[i][j].get_terrain()
        #terrain_sprite = terrain.get_sprite()
        #self.window.draw_sprite(x, y, terrain_sprite)

        ### TEMPORARY
        self.erase(row, col)
        ###

        unit = space.get_unit()
        if unit is not None:
            unit_sprite = unit.get_sprite()
            self.window.draw_sprite(x, y, unit_sprite)
        if space.is_selected():
            self.outline_space(row, col, 'blue')
        if space == self.action_space:
            self.outline_space(row, col, 'purple')

    def draw_sprites(self):
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                self.draw_space(self.__spaces[i][j])


###### TEMPORARY
    def erase(self, row, col):
        x1 = self.get_col_x(col)
        y1 = self.get_row_y(row)
        x2 = self.get_col_x(col+1)
        y2 = self.get_row_y(row+1)
        self.window.canvas.create_rectangle(x1, y1, x2, y2, fill=BG_COL, outline = 'black', width=2)
######

    def get_movement_spaces(self, unit, space) -> set:
        range = unit.get_movement()
        if unit.get_move_type() == MoveType.FLY:
            pass_dict = ALL_TARGETS
        else:
            pass_dict = MOVE_TARGETS
        target_dict = MOVE_TARGETS
        valid_coords = unit.find_target_spaces(space, range, target_dict, pass_dict)
        valid_spaces = self.set_spaces(valid_coords, 'green')
        return valid_spaces
    
    def get_target_spaces(self, unit, space) -> set:
        range = unit.get_ability_range()
        target_dict = unit.get_ability_targets()
        valid_coords = unit.find_target_spaces(space, range, target_dict)
        valid_spaces = self.set_spaces(valid_coords, 'yellow')
        return valid_spaces
    
    def get_attack_spaces(self, unit, space) -> set:
        range = 1
        target_dict = ENEMY_TARGETS
        valid_coords = unit.find_target_spaces(space, range, target_dict)
        valid_spaces = self.set_spaces(valid_coords, 'red')
        return valid_spaces
    
    def set_spaces(self, coords, colour):
        valid_spaces = []
        for tuple in coords:
            self.outline_space(tuple[0], tuple[1], colour)
            valid_spaces.append(self.__spaces[tuple[0]][tuple[1]])
        return valid_spaces

    def select_space(self, row: int, col: int) -> None:
        new_space = self.__spaces[row][col]
        new_space.select()
        self.selected_space = new_space
        unit = new_space.get_unit()
        self.selected_unit = unit
        self.draw_space(new_space)
        if unit is not None:
            self.__valid_moves = self.get_movement_spaces(unit, new_space)
            self.set_action_space(unit, new_space)
            self.set_attack_spaces(unit, new_space)

    def deselect_space(self) -> None:
        space = self.selected_space
        if space is not None:
            space.deselect()
            self.unset_unit_buttons()
            self.selected_space = None
            self.selected_unit = None
            self.action_space = None
            self.reset_target_spaces()
            self.draw_space(space)
            if self.__valid_moves is not None:
                for sp in self.__valid_moves:
                    self.draw_space(sp)
            self.__valid_moves = None

    def move_unit(self, unit, space):
        old_space = unit.get_location()
        try:  
            unit.move(space)
            self.deselect_space()
            self.draw_space(old_space)
            self.draw_space(space)
            if old_space != space:
                self.ui.logItems['text'].add_text(f"{unit.get_name()} -> {space.get_row()},{space.get_col()}. \n") # Send movement to combat log
        except Exception as e:
            print(e)

    def cancel_action(self):
        self.action_space = None
        self.draw_sprites()
        self.deselect_space()
        self.clear_stats_panel()


    def get_col_x(self, col):
        x = self.x_start + (col * (self.square_size))
        return x
        
    def get_row_y(self, row):
        y = self.y_start + (row * (self.square_size))
        return y
    
    def set_action_space(self, unit, space):
        if self.action_space is not None: # If a new action space is being selected, overriding another
            self.draw_space(self.selected_space)
            if self.action_space == self.selected_unit.get_location(): # If the old space was the current unit's space
                self.outline_space(self.action_space.get_row(), self.action_space.get_col(), 'blue')
            else: # Otherwise, this is another space in the current unit's range
                self.draw_space(self.action_space)
                self.outline_space(self.action_space.get_row(), self.action_space.get_col(), 'green')
        self.reset_target_spaces()
        self.set_unit_buttons(unit, space)
        self.outline_space(space.get_row(), space.get_col(), 'purple')
        self.preview_sprite(unit, space)
        self.action_space = space

    def set_attack_spaces(self, unit, space):
        self.reset_target_spaces()
        row = space.get_row()
        col = space.get_col()
        self.draw_space(space)
        self.preview_sprite(unit, space)
        try:
            self.__attack_spaces = self.get_attack_spaces(unit, space)
        except Exception as e:
            print(e)

    def set_ability_spaces(self, unit, space):
        self.reset_target_spaces()
        row = space.get_row()
        col = space.get_col()
        self.draw_space(space)
        self.preview_sprite(unit, space)
        try:
            self.__ability_spaces = self.get_target_spaces(unit, space)
        except Exception as e:
            print(e)
    
    def set_unit_buttons(self, unit, space):
        self.ui.controlBar.buttons['red'].change_unclick_func(lambda: self.set_attack_spaces(unit, space))
        self.ui.controlBar.buttons['yellow'].change_unclick_func(lambda: self.set_ability_spaces(unit, space))
        self.ui.controlBar.buttons['green'].change_unclick_func(lambda: self.move_unit(unit, space))
        self.ui.controlBar.buttons['grey'].change_unclick_func(self.cancel_action)


    def unset_unit_buttons(self):
        self.ui.controlBar.buttons['red'].change_unclick_func(do_nothing)
        self.ui.controlBar.buttons['yellow'].change_unclick_func(do_nothing)
        self.ui.controlBar.buttons['green'].change_unclick_func(do_nothing)
        self.ui.controlBar.buttons['grey'].change_unclick_func(do_nothing)

    def reset_target_spaces(self):
        if self.__ability_spaces is not None:
            for space in self.__ability_spaces:
                self.draw_space(space)
        self.__ability_spaces = None
        if self.__attack_spaces is not None:
            for space in self.__attack_spaces:
                self.draw_space(space)
        self.__attack_spaces = None


    def combat(self, unit, target):
        unit_name = unit.get_name()
        target_name = target.get_name()
        unit_loc = unit.get_location()
        target_loc = target.get_location()
        attack_log = unit.basic_attack(target)
        self.update_stats_panel(target) 
        # Send attack details to combat log
        self.ui.logItems['text'].add_text(attack_log) 
        if target.is_dead(): # If the target is dead, remove them and take their place
            self.ui.logItems['text'].add_text(f"{unit_name} has slain {target_name}!\n")
            target_loc.assign_unit(None)
            self.move_unit(unit, target_loc)
        else: # Otherwise, they will retaliate
            retaliation_log = target.retaliate(unit)
            self.update_stats_panel(unit)
            # Send retaliation details to combat log
            self.ui.logItems['text'].add_text(retaliation_log) 
            if unit.is_dead(): # If the unit died, remove them
                self.ui.logItems['text'].add_text(f"{unit_name} has been slain by {target_name}!\n")
                unit_loc.assign_unit(None)
                self.action_space = None
                self.draw_sprites()
                self.deselect_space()
        
            
    def preview_sprite(self, unit, space):
        preview = unit.get_sprite()
        x = self.get_col_x(space.get_col())
        y = self.get_row_y(space.get_row())
        sprite_x = x + SPRITE_BUFFER//2
        sprite_y = y + SPRITE_BUFFER//2
        self.window.draw_sprite(sprite_x, sprite_y, preview)
        box_x = x + LINE_WIDTH + SELECTION_BUFFER
        box_y = y + LINE_WIDTH + SELECTION_BUFFER
        self.window.canvas.create_image(box_x, box_y, image=self.__transparent_square, anchor='nw')

    def set_transparency(self):
        width = DEFAULT_SQUARE_SIZE - LINE_WIDTH - SELECTION_BUFFER*2
        height = DEFAULT_SQUARE_SIZE - LINE_WIDTH - SELECTION_BUFFER*2
        alpha = 126
        # Use the fill variable to fill the shape with transparent color
        fill_col = self.root.winfo_rgb(BG_COL) + (alpha,)
        cover = Image.new('RGBA', size=(width, height), color=fill_col)
        transparent_square = ImageTk.PhotoImage(image=cover)
        return transparent_square
    
    def activate_ability(self, unit, space):
        special_log = unit.special_ability(space.get_unit(), self.__spaces)
        for message in special_log:
            self.ui.logItems['text'].add_text(message)
        self.draw_sprites()

    def end_turn(self):
        self.__game_state.next_turn()

    def move_and_wait(self, unit, space):
        self.move_unit(unit, space)
        self.end_turn()



class Terrain:
    def __init__(self) -> None:
        pass
    

class Space:
    def __init__(
            self,
            row: int,
            col: int,
            ) -> None:
        self.__row = row
        self.__col = col
        self.__terrain = None
        self.__unit = None
        self.__selected = False
        self.__left = None
        self.__up = None
        self.__right = None
        self.__down = None

    def get_unit(self):
        return self.__unit
    
    def assign_unit(self, unit):
        self.__unit = unit

    def get_terrain(self):
        return self.__terrain
    
    def get_unit_sprite(self):
        if self.__unit == None:
            return None
        return self.__unit.get_sprite()
    
    def get_terrain_sprite(self):
        pass
    
    def get_row(self):
        return self.__row
    
    def get_col(self):
        return self.__col
    
    def select(self):
        self.__selected = True

    def deselect(self):
        self.__selected = False

    def is_selected(self):
        return self.__selected
    
    def set_left(self, space):
        self.__left = space

    def set_up(self, space):
        self.__up = space

    def set_right(self, space):
        self.__right = space

    def set_down(self, space):
        self.__down = space

    def get_left(self):
        return self.__left
    
    def get_up(self):
        return self.__up
    
    def get_right(self):
        return self.__right
    
    def get_down(self):
        return self.__down

