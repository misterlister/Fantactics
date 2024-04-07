from graphics import Window, Point
from tkinter import Tk, Label
from PIL import ImageTk, Image
from userInterface import UserInterface, do_nothing
from constants import (
    DEFAULT_X_POS,
    DEFAULT_Y_POS,
    DEFAULT_SQUARE_SIZE,
    BOARD_COLS,
    BOARD_ROWS,
    TerrainType,
    BG_COL,
    FONT,
    DEFAULT_FONT_SIZE,
    LINE_WIDTH,
    SELECTION_BUFFER,
    SPRITE_BUFFER,
    MoveType,
    ActionType,
    TargetType,
    TARGET_ALL,
    TARGET_ENEMIES,
    TARGET_MOVE
)
from units import Soldier, Unit
from space import (
    Space,
    Forest,
    Fortress,
    Plains,
    Path
    )

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
        self.__x_start = x_start
        self.__y_start = y_start
        self.x_end = x_start + (BOARD_COLS * square_size) 
        self.y_end = y_start + (BOARD_ROWS * square_size)
        self.square_size = square_size
        self.__spaces = [[Space(i, j) for j in range(BOARD_COLS)] for i in range(BOARD_ROWS)]
        self.rowLabel = []
        self.colLabel = []
        self.connect_spaces(self.__spaces)
        self.draw_board()
        self.__transparent_square = self.set_transparency()
        self.bind_buttons()
        self.__selected_space = None # Space currently selected
        self.__selected_unit = None # Unit currently selected
        self.__action_space = None # Location where selected unit will move to take an action
        self.__target_space = None # Target space where the selected unit will act on
        self.__area_of_effect_spaces = [] # Spaces within the area of effect of a targeted action
        self.__valid_moves = None # Spaces where the selected unit can move to
        self.__attack_spaces = None # Spaces the selected unit can attack from the selected action space
        self.__ability_spaces = None # Spaces the selected unit can target with their ability from the selected action space
        self.__guarded_spaces = [] # Spaces which are guarded by soldiers, and cannot be targeted with ranged abilities
        self.__action_confirmed = False # Keeps track of if the current action has been confirmed
        self.__game_state = None # Links to game state object
        
    def bind_buttons(self):
        self.window.canvas.bind('<Button-1>', self.click)
        self.window.canvas.bind('<Button-3>', self.right_click)
        self.root.bind('<z>', self.ui.controlBar.buttons['attack'].unclick)
        self.root.bind('<x>', self.ui.controlBar.buttons['ability'].unclick)
        self.root.bind('<space>', self.ui.controlBar.buttons['confirm'].unclick)
        self.root.bind('<Shift-KeyPress>', self.ui.controlBar.buttons['cancel'].unclick)
        
    def unbind_buttons(self):
        self.window.canvas.bind('<Button-1>', do_nothing)
        self.window.canvas.bind('<Button-3>', do_nothing)
        self.root.bind('<z>', do_nothing)
        self.root.bind('<x>', do_nothing)
        self.root.bind('<space>', do_nothing)
        self.root.bind('<Shift-KeyPress>', do_nothing)
        self.unset_unit_buttons()
    
    def draw_board(self) -> None:
        for i in range (BOARD_ROWS + 1):
            y_position = self.get_row_y(i)
            self.rowLabel.append(Label(self.root, text=i + 1, anchor='center', bg=BG_COL, font=(FONT, DEFAULT_FONT_SIZE)))
            self.rowLabel[i].place(x=330, y=(i * DEFAULT_SQUARE_SIZE) + 60)
            p1 = Point(self.__x_start, y_position)
            p2 = Point(self.x_end, y_position)
            self.window.draw_line(p1, p2)

        for j in range(BOARD_COLS + 1):
            x_position = self.get_col_x(j)
            self.colLabel.append(Label(self.root, text=chr(65 + j), anchor='center', bg=BG_COL, font=(FONT, DEFAULT_FONT_SIZE)))
            self.colLabel[j].place(x=(j * DEFAULT_SQUARE_SIZE) + 380, y=614)
            p1 = Point(x_position, self.__y_start)
            p2 = Point(x_position, self.y_end)
            self.window.draw_line(p1, p2)

        # Destroy excess labels, not most elegant solution but least code
        self.rowLabel[i].destroy()
        self.colLabel[j].destroy()
        
    def setup_map(self, game_map):
        map_size = BOARD_COLS * BOARD_ROWS
        if len(game_map) != map_size:
            print("Alert: Map does not match the board size. Reverting to default map.")
            game_map = [TerrainType.PLAINS * (map_size)]
        cell = 0
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                space = self.__spaces[i][j]
                if game_map[cell] == TerrainType.FOREST:
                    space.set_terrain(Forest(space))
                elif game_map[cell] == TerrainType.FORTRESS:
                    space.set_terrain(Fortress(space))
                elif game_map[cell] == TerrainType.PATH:
                    space.set_terrain(Path(space))
                else:
                    space.set_terrain(Plains(space))
                cell += 1
                        
    def link_to_state(self, state):
        self.__game_state = state

    def click(self, event):
        self.clear_info_panel()
        if event.x > self.__x_start and event.x < self.x_end:
            if event.y > self.__y_start and event.y < self.y_end:
                row = (event.y-self.__y_start) // self.square_size
                col = (event.x-self.__x_start) // self.square_size
                #contents = self.check_square(row, col)
                #print(f"Clicked square {row},{col}. Contents: {contents}")
                new_space = self.__spaces[row][col]
                if self.__selected_unit is None: # No unit is currently selected
                    self.click_no_unit_selected(new_space)
                else: # A unit is currently selected
                    self.click_unit_selected(self.__selected_unit, new_space)

    def click_no_unit_selected(self, space: Space):
        if self.__selected_space is not None: # If another space was already selected
            if self.__selected_space == space: # If a selected space is selected, deselect it
                self.deselect_space()
                self.clear_stats_panel()
                return
            self.deselect_space()
        self.select_space(space)
        self.update_stats_panel(self.__selected_unit)
        return

    def click_unit_selected(self, unit: Unit, space: Space):
        unit = self.__selected_unit
        if unit.get_player().is_current_turn():
            if self.__attack_spaces != None: # Attack range is active
                if space in self.__attack_spaces: # A valid target is selected
                    if space == self.__target_space and self.__action_confirmed:
                        ### Send self.__action_space, unit, space, attack_action to server
                        self.attack_action(unit, space)
                    else:
                        self.setup_action(self.attack_action, unit, space, "red")
                    return
            elif self.__ability_spaces != None: # Ability range is active
                if space in self.__guarded_spaces:
                    self.update_info_panel("This unit is guarded by an enemy soldier. It cannot be targeted.")
                    self.unconfirm_action()
                    return
                if space in self.__ability_spaces: # A valid target is selected
                    if space == self.__target_space and self.__action_confirmed:
                        ### Send self.__action_space, unit, space, ability_action to server
                        self.ability_action(unit, space)
                    else:
                        self.setup_action(self.ability_action, unit, space, "yellow")
                    return
            if self.__action_space == space: # Movement to a new space is confirmed
                if self.__action_confirmed:
                    ### Send self.__action_space, unit, space, move_and_wait to server
                    self.move_and_wait(unit, space)
                else:
                    self.setup_action(self.move_and_wait, unit, space, "green")
                return
            elif space in self.__valid_moves: # A new action space is selected
                self.set_action_space(unit, space)
                self.set_attack_spaces(unit, space)
                return
        else:
            if self.__game_state.game_is_over():
                self.update_info_panel("The game is over, no more actions can be taken.")
            else:
                self.update_info_panel("You cannot move enemy units")
        self.cancel_action()

    def right_click(self, event):
        self.cancel_action()

    def attack_action(self, unit: Unit, space: Space):
        self.update_stats_panel(space.get_unit()) 
        self.move_unit(unit, self.__action_space)
        self.combat(unit, space.get_unit())
        self.ui.controlBar.buttons['attack'].untoggle_keys()
        self.end_turn()
        return
    
    def ability_action(self, unit: Unit, space: Space):
        self.move_unit(unit, self.__action_space)
        self.update_stats_panel(space.get_unit()) 
        self.activate_ability(unit, space)
        self.ui.controlBar.buttons['attack'].untoggle_keys()
        self.end_turn()
        return

    def setup_action(self, action, unit: Unit, space: Space, colour):
        self.__action_confirmed = True
        if self.__target_space is not None: # If there was a selected space before, redraw all area of effect spaces
            for sp in self.__area_of_effect_spaces:
                self.draw_space(sp)
        self.__target_space = space
        self.draw_space(self.__action_space)
        self.preview_sprite(unit, self.__action_space)
        target = space.get_unit()
        self.ui.controlBar.buttons['confirm'].change_unclick_func(lambda: action(unit, space))
        if action == self.ability_action: # If this is an ability, highlight the area of effect
            self.__area_of_effect_spaces = unit.get_area_of_effect(space)
            for effect_space in self.__area_of_effect_spaces:
                self.circle_outline_space(effect_space, colour)
            self.ability_preview(unit, target)
        else: # Otherwise, highlight the target space
            self.circle_outline_space(space, colour)
            if action == self.attack_action:
                self.combat_preview(unit, target)
                
    def unconfirm_action(self):
        self.__action_confirmed = False
        if self.__target_space != None:
            self.draw_space(self.__target_space)
            self.__target_space = None
        if len(self.__area_of_effect_spaces) > 0:
            self.draw_space_list(self.__area_of_effect_spaces)
            self.__area_of_effect_spaces = []

    def combat_preview(self, unit: Unit, target: Unit):
        target_damage = unit.attack_preview(target, True)
        if target_damage < target.get_curr_hp():
            unit_damage = target.attack_preview(unit, False)
        else:
            unit_damage = 0
        self.update_stats_panel(target, target_damage)
        self.update_stats_panel(unit, unit_damage)

    def ability_preview(self, unit: Unit, target: Unit):
        damage_val = unit.get_ability_value()
        damage_type = unit.get_special_damage_type()
        if target != None:
            target_damage, unit_damage = unit.ability_preview(target)
            if target_damage != None:
                self.update_stats_panel(target, target_damage)
                self.update_stats_panel(unit, unit_damage, damage_val, damage_type) 
                return
        self.update_stats_panel(unit, 0, damage_val, damage_type)
                
    def connect_spaces(self, spaces: Space):
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
    def update_stats_panel(self, unit: Unit, damage_preview = 0, damage_val = None, damage_type = None):
        if unit is not None:
            if unit.get_player().is_current_turn():
                panel = 'friendlyUnitPanel'
            else:
                panel = 'enemyUnitPanel'
            if damage_val == None:
                damage_val = unit.get_damage_val()
            if damage_type == None:
                damage_type = unit.get_damage_type()
            sprite = unit.get_sprite()
            self.ui.statsPanel[panel].update_image(self.window.get_sprite(sprite))
            self.ui.statsPanel[panel].update_class(unit.get_unit_type())
            self.ui.statsPanel[panel].update_name(unit.get_name())
            self.ui.statsPanel[panel].update_health(unit.get_curr_hp(), unit.get_max_hp(), damage_preview)
            self.ui.statsPanel[panel].update_damage(damage_val, damage_type, unit.get_damage_mod())
            self.ui.statsPanel[panel].update_defense(unit.get_armour_type(), unit.get_defense_mod())
            self.ui.statsPanel[panel].update_movement(unit.get_movement())
            self.ui.statsPanel[panel].update_description(unit.get_ability_name(), unit.get_ability_description())
        else:
            self.clear_stats_panel()
            
    def update_info_panel(self, message):
        self.ui.info.update(message)
        
    def clear_info_panel(self):
        self.ui.info.update('')

    def clear_stats_panel(self):
        for panel in self.ui.statsPanel:
            self.ui.statsPanel[panel].clear()

    def outline_space(self, space: Space, colour: str) -> None:
        row = space.get_row()
        col = space.get_col()
        x1 = self.get_col_x(col) + (LINE_WIDTH)
        y1 = self.get_row_y(row) + (LINE_WIDTH)
        x2 = self.get_col_x(col+1) - (LINE_WIDTH + 2)
        y2 = self.get_row_y(row+1) - (LINE_WIDTH + 2)
        self.window.canvas.create_rectangle(x1, y1, x2, y2, width=SELECTION_BUFFER, outline=colour)
        self.window.canvas.create_rectangle(x1-2, y1-2, x2+2, y2+2, width=3, outline="black")

    def outline_spaces(self, spaces: list, colour: str) -> None:
        for space in spaces:
            self.outline_space(space, colour)

    def circle_outline_space(self, space: Space, colour: str) -> None:
        row = space.get_row()
        col = space.get_col()
        x1 = self.get_col_x(col) + ((LINE_WIDTH * 2)) 
        y1 = self.get_row_y(row) + ((LINE_WIDTH * 2)) 
        x2 = self.get_col_x(col+1) - (LINE_WIDTH * 2) - 2
        y2 = self.get_row_y(row+1) - (LINE_WIDTH * 2) - 2
        self.window.canvas.create_oval(x1, y1, x2, y2, width=SELECTION_BUFFER, outline=colour)

    def x_out_space(self, space: Space, colour: str) -> None:
        row = space.get_row()
        col = space.get_col()
        x1 = self.get_col_x(col) + ((LINE_WIDTH * 2) - 1) 
        y1 = self.get_row_y(row) + ((LINE_WIDTH * 2) - 1) 
        x2 = self.get_col_x(col+1) - (LINE_WIDTH * 2)
        y2 = self.get_row_y(row+1) - (LINE_WIDTH * 2)
        self.window.canvas.create_line(x1, y1, x2, y2, width=LINE_WIDTH, fill=colour)
        self.window.canvas.create_line(x2, y1, x1, y2, width=LINE_WIDTH, fill=colour)

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
    
    def draw_space(self, space: Space) -> None:
        col = space.get_col()
        row = space.get_row()
        terrain_x = self.get_col_x(col)
        terrain_y = self.get_row_y(row)
        ### TEMPORARY
        self.erase_space(row, col)
        ###
        terrain_sprite = space.get_terrain_sprite()
        
        self.window.draw_sprite(terrain_x, terrain_y, terrain_sprite)
        unit_x = terrain_x + SPRITE_BUFFER/2
        unit_y = terrain_y + SPRITE_BUFFER/2
        unit = space.get_unit()
        if unit is not None:
            unit_sprite = unit.get_sprite()
            self.window.draw_sprite(unit_x, unit_y, unit_sprite)
        if self.__valid_moves != None:
            if space in self.__valid_moves:
                self.outline_space(space, 'green')
        if space.is_selected():
            self.outline_space(space, 'blue')
        if space == self.__action_space:
            self.outline_space(space, 'purple')
        if self.__attack_spaces != None:
            if space in self.__attack_spaces:
                self.outline_space(space, 'red')
        if self.__ability_spaces != None:
            if space in self.__ability_spaces:
                self.outline_space(space, 'yellow')
        if space in self.__guarded_spaces:
            for sp in self.__guarded_spaces:
                self.x_out_space(sp, "grey")

    def draw_all_spaces(self):
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                self.draw_space(self.__spaces[i][j])

    def erase_space(self, row, col):
        x1 = self.get_col_x(col)
        y1 = self.get_row_y(row)
        x2 = self.get_col_x(col+1)
        y2 = self.get_row_y(row+1)
        self.window.canvas.create_rectangle(x1, y1, x2, y2, fill=BG_COL, outline = 'grey', width=2)

    def get_movement_spaces(self, unit: Unit, space: Space) -> set:
        range = unit.get_movement()
        if unit.get_move_type() == MoveType.FLY:
            pass_dict = TARGET_ALL
        else:
            pass_dict = TARGET_MOVE
        target_dict = TARGET_MOVE
        action = ActionType.MOVE
        valid_spaces = unit.find_target_spaces(space, range, target_dict, action, pass_dict)
        self.outline_spaces(valid_spaces, 'green')
        return valid_spaces
    
    def get_ability_spaces(self, unit, space) -> set:
        range = unit.get_ability_range()
        valid_spaces = set()
        min_range = unit.get_ability_min_range()
        target_dict = unit.get_ability_targets()
        action = ActionType.ABILITY
        valid_spaces = valid_spaces.union(unit.find_target_spaces(space, range, target_dict, action))
        if unit.get_ability_targets()[TargetType.ITSELF]:
            valid_spaces = valid_spaces.difference({unit.get_space()})
            valid_spaces = valid_spaces.union({self.__action_space})
            
        if min_range > 1:
            invalid_spaces = unit.find_target_spaces(space, min_range-1, target_dict)
            valid_spaces = valid_spaces.difference(invalid_spaces)
        if range > 1:
            self.update_guarded_spaces(valid_spaces, unit)
            valid_spaces = valid_spaces.difference(self.__guarded_spaces)
            self.draw_space_list(self.__guarded_spaces)
        self.outline_spaces(valid_spaces, 'yellow')
        return valid_spaces
    
    def get_attack_spaces(self, unit: Unit, space: Space) -> set:
        range = 1
        target_dict = TARGET_ENEMIES
        action = ActionType.ATTACK
        valid_spaces = unit.find_target_spaces(space, range, target_dict, action)
        self.outline_spaces(valid_spaces, 'red')
        return valid_spaces
    
    def update_guarded_spaces(self, valid_spaces: list, unit: Unit):
        guarded_spaces = set()
        for space in valid_spaces:
            target = space.get_unit()
            if target != None:
                if not target.is_ally(unit):
                    if not target.is_unit_type(Soldier):
                        if target.adjacent_to(Soldier, True):
                            guarded_spaces.add(space)
        self.__guarded_spaces = guarded_spaces
    
    def draw_space_list(self, spaces: list):
        for space in spaces:
            self.draw_space(space)

    def select_space(self, space) -> None:
        space.select()
        self.__selected_space = space
        unit = space.get_unit()
        self.__selected_unit = unit
        self.draw_space(space)
        if unit is not None:
            self.__valid_moves = self.get_movement_spaces(unit, space)
            self.set_action_space(unit, space)
            if self.ui.controlBar.buttons['ability'].get_toggle_status():
                self.set_ability_spaces(unit, space)
            else:
                self.set_attack_spaces(unit, space)

    def deselect_space(self) -> None:
        space = self.__selected_space
        if space is not None:
            space.deselect()
        self.unset_unit_buttons()
        self.__selected_space = None
        if self.__selected_unit != None:
            self.__selected_unit.reset_action_space()
        self.__selected_unit = None
        self.__action_space = None
        self.__target_space = None
        self.__area_of_effect_spaces = []
        self.__valid_moves = None
        self.__attack_spaces = None
        self.__ability_spaces = None
        self.__guarded_spaces = []
        self.__action_confirmed = False
        ### REMOVE COMBAT/ABILITY PREVIEW HERE
        self.draw_all_spaces()

    def move_unit(self, unit: Unit, space: Space):
        old_space = unit.get_space()
        try:  
            move_log = unit.move(space)
            self.deselect_space()
            self.draw_space(old_space)
            self.draw_space(space)
            for message in move_log:
                self.ui.logItems['text'].add_text(message) # Send movement to combat log
        except Exception as e:
            print(e)

    def cancel_action(self):
        self.__action_space = None
        self.draw_all_spaces()
        self.deselect_space()
        self.clear_stats_panel()
        self.ui.controlBar.buttons['attack'].untoggle_keys()

    def get_col_x(self, col):
        x = self.__x_start + (col * (self.square_size))
        return x
        
    def get_row_y(self, row):
        y = self.__y_start + (row * (self.square_size))
        return y
    
    def set_action_space(self, unit: Unit, space: Space):
        if self.__action_space is not None: # If a new action space is being selected, overriding another
            self.draw_space(self.__selected_space)
            if self.__action_space == self.__selected_unit.get_space(): # If the old space was the current unit's space
                self.outline_space(self.__action_space, 'blue')
            else: # Otherwise, this is another space in the current unit's range
                self.draw_space(self.__action_space)
                self.outline_space(self.__action_space, 'green')
        self.reset_target_spaces()
        unit.set_action_space(space)
        self.update_stats_panel(unit)
        self.set_unit_buttons(unit, space)
        self.outline_space(space, 'purple')
        self.preview_sprite(unit, space)
        
        self.__action_space = space

    def set_attack_spaces(self, unit: Unit, space: Space):
        self.ui.controlBar.buttons['attack'].toggle()
        self.ui.controlBar.buttons['ability'].untoggle()
        self.reset_target_spaces()
        self.draw_space(space)
        self.preview_sprite(unit, space)
        try:
            self.__attack_spaces = self.get_attack_spaces(unit, space)
        except Exception as e:
            print(e)

    def set_ability_spaces(self, unit: Unit, space: Space):
        if unit.ability_expended():
            self.update_info_panel("This unit's ability cannot be used again")
            return
        if unit.ability_disabled():
            self.update_info_panel(unit.get_disabled_message())
            return
        self.reset_target_spaces()
        self.draw_space(space)
        self.preview_sprite(unit, space)
        try:
            self.__ability_spaces = self.get_ability_spaces(unit, space)
        except Exception as e:
            print(e)
    
    def set_unit_buttons(self, unit: Unit, space: Space):
        self.ui.controlBar.buttons['attack'].change_unclick_func(lambda: self.set_attack_spaces(unit, space))
        self.ui.controlBar.buttons['ability'].change_unclick_func(lambda: self.set_ability_spaces(unit, space))
        self.ui.controlBar.buttons['confirm'].change_unclick_func(lambda: self.move_and_wait(unit, space))
        self.ui.controlBar.buttons['cancel'].change_unclick_func(self.cancel_action)

    def unset_unit_buttons(self):
        self.ui.controlBar.buttons['attack'].change_unclick_func(do_nothing)
        self.ui.controlBar.buttons['ability'].change_unclick_func(do_nothing)
        self.ui.controlBar.buttons['confirm'].change_unclick_func(do_nothing)
        self.ui.controlBar.buttons['cancel'].change_unclick_func(do_nothing)

    def reset_target_spaces(self):
        self.clear_info_panel()
        self.unconfirm_action()
        ### REMOVE COMBAT/ABILITY PREVIEW HERE
        ability_spaces_reset = self.__ability_spaces
        self.__ability_spaces = None
        if ability_spaces_reset is not None:     
            self.draw_space_list(ability_spaces_reset)
        guarded_spaces_reset = self.__guarded_spaces
        self.__guarded_spaces = []
        self.draw_space_list(guarded_spaces_reset)
        attack_spaces_reset = self.__attack_spaces
        self.__attack_spaces = None
        if attack_spaces_reset is not None:
            self.draw_space_list(attack_spaces_reset)
        area_spaces_reset = self.__area_of_effect_spaces
        self.__area_of_effect_spaces = []
        if len(area_spaces_reset) > 0:
            for sp in area_spaces_reset:
                self.draw_space(sp)

    def combat(self, unit: Unit, target: Unit):
        attack_log = unit.basic_attack(target)
        self.update_stats_panel(target) 
        self.update_stats_panel(unit)
        for message in attack_log:
            self.ui.logItems['text'].add_text(message)
        self.__action_space = None
        self.draw_all_spaces()
        self.deselect_space()
        
    def preview_sprite(self, unit: Unit, space: Space):
        preview = unit.get_sprite()
        x = self.get_col_x(space.get_col())
        y = self.get_row_y(space.get_row())
        sprite_x = x + SPRITE_BUFFER//2
        sprite_y = y + SPRITE_BUFFER//2
        self.window.draw_sprite(sprite_x, sprite_y, preview)
        box_x = x + (LINE_WIDTH - 2) + SELECTION_BUFFER
        box_y = y + (LINE_WIDTH - 2) + SELECTION_BUFFER
        self.window.canvas.create_image(box_x, box_y, image=self.__transparent_square, anchor='nw')
        self.outline_space(space, "purple")

    def set_transparency(self):
        width = DEFAULT_SQUARE_SIZE - (LINE_WIDTH) - (SELECTION_BUFFER * 2)
        height = DEFAULT_SQUARE_SIZE - (LINE_WIDTH) - (SELECTION_BUFFER * 2)
        alpha = 126
        # Use the fill variable to fill the shape with transparent color
        fill_col = self.root.winfo_rgb(BG_COL) + (alpha,)
        cover = Image.new('RGBA', size=(width, height), color=fill_col)
        transparent_square = ImageTk.PhotoImage(image=cover)
        return transparent_square
    
    def activate_ability(self, unit: Unit, space: Space):
        special_log = unit.special_ability(space.get_unit(), space)
        for message in special_log:
            self.ui.logItems['text'].add_text(message)
        self.draw_all_spaces()

    def end_turn(self):
        self.__game_state.next_turn()

    def move_and_wait(self, unit: Unit, space: Space):
        self.ui.controlBar.buttons['attack'].untoggle_keys()
        self.move_unit(unit, space)
        self.end_turn()

    
class MapLayout:
    PL = TerrainType.PLAINS
    FS = TerrainType.FOREST
    FT = TerrainType.FORTRESS
    PT = TerrainType.PATH
    Maps = {
        "Great Plains": [
            PL, PL, PL, PL, PL, PL, PL, PL,
            PL, PL, PL, PL, PL, PL, PL, PL,
            FS, PT, PT, PL, FS, PT, PL, PT,
            PL, PT, FT, FS, PL, PT, PT, PT
        ],
        "Checkered Woods": [
            PL, PL, PT, PL, PL, PL, PL, FS,
            PL, PL, PT, PL, PL, PL, FS, PL,
            PT, PT, PT, FS, PL, FS, PL, FS,
            PT, FT, FS, PL, FS, PL, FS, PL
        ],
        "Forest Ambush": [
            FS, PL, PL, PL, PL, PT, PL, PL,
            FS, PL, PL, PT, PT, PT, FS, FS,
            PL, PL, FS, PT, FS, PT, PT, FS,
            PT, FS, FS, FT, FS, FS, PT, PT
        ],
        "Centre Road": [
            PL, PL, PL, PL, PL, PT, PL, PL,
            PL, PL, FS, PT, PT, PT, PL, FS,
            FS, PL, PL, PT, FS, PL, PL, PL,
            FS, FS, PT, PT, PT, FT, PL, FS
        ],
        "Fortresses of Altria": [
            PL, PL, PT, PT, PT, PT, PT, PL,
            PL, PL, PT, PL, PL, PL, PT, PL,
            FT, PL, PT, FS, FS, PT, PT, FS,
            PT, PT, PT, FS, FS, FT, PL, FS
        ],
    }
    