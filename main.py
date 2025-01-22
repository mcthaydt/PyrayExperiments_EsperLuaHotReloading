from lupa import LuaRuntime
import pyray as pr

def load_script(lua, script_path):
    with open(script_path, "r") as f:
        code = f.read()
    lua.execute(code)

def main():
    pr.init_window(800, 600, "All-ECS-in-Lua Example")
    pr.set_target_fps(60)

    # 1) Create a Lua runtime; expose pyray as 'pr' in Lua
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.globals().pr = pr

    # 2) Load the ECS script (everything is in Lua)
    load_script(lua, "ecs.lua")

    # 3) Main loop: just call the Lua update_game() and draw_game()
    while not pr.window_should_close():
        # Run Lua's update
        lua.execute("update_game()")

        # Draw
        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        lua.execute("draw_game()")
        pr.end_drawing()

    pr.close_window()

if __name__ == "__main__":
    main()
