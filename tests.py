import unittest
from lupa import LuaRuntime
import pyray as pr


class TestECSIntegration(unittest.TestCase):
    def setUp(self):
        # Create a Lua runtime and expose pyray as 'pr' in Lua
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        self.lua.globals().pr = pr

        # Load the ECS script
        with open("ecs.lua", "r") as f:
            self.lua.execute(f.read())

        # Load the game state script
        with open("game_state.lua", "r") as f:
            self.lua.execute(f.read())

    def test_create_entity(self):
        # Test creating a new entity with components
        self.lua.execute(
            """
            create_entity({
                Position = { x = 400, y = 400 },
                Velocity = { x = 0, y = 0 },
                Render = true,
                Color = pr.YELLOW
            })
        """
        )

        # Verify the entity was added to the entities table
        entities = self.lua.eval("entities")
        self.assertEqual(len(entities), 4)  # 3 initial entities + 1 new entity
        self.assertEqual(entities[4].Position.x, 400)
        self.assertEqual(entities[4].Position.y, 400)
        self.assertEqual(entities[4].Color, pr.YELLOW)

    def test_input_system(self):
        # Mock the keyboard input
        self.lua.execute(
            """
            pr.is_key_down = function(key)
                return key == pr.KEY_RIGHT
            end
        """
        )

        # Run the input system
        self.lua.execute("input_system()")

        # Verify the player entity's velocity was updated
        entities = self.lua.eval("entities")
        player = entities[1]
        self.assertEqual(player.Velocity.x, 2)
        self.assertEqual(player.Velocity.y, 0)

    def test_movement_system(self):
        # Set initial position and velocity for the player entity
        self.lua.execute(
            """
            entities[1].Position = { x = 100, y = 100 }
            entities[1].Velocity = { x = 2, y = 2 }
        """
        )

        # Run the movement system
        self.lua.execute("movement_system()")

        # Verify the player entity's position was updated
        entities = self.lua.eval("entities")
        player = entities[1]
        self.assertEqual(player.Position.x, 102)
        self.assertEqual(player.Position.y, 102)

    def test_draw_game(self):
        # Mock the draw functions
        draw_text_called = False
        draw_rectangle_called = False

        def mock_draw_text(text, x, y, size, color):
            nonlocal draw_text_called
            draw_text_called = True
            self.assertEqual(text, "ECS in Lua: Input & Rendering in Lua!")
            self.assertEqual(x, 10)
            self.assertEqual(y, 10)
            self.assertEqual(size, 20)
            self.assertEqual(color, pr.BLACK)

        def mock_draw_rectangle(x, y, width, height, color):
            nonlocal draw_rectangle_called
            draw_rectangle_called = True
            self.assertEqual(width, 50)
            self.assertEqual(height, 50)

        self.lua.globals().pr.draw_text = mock_draw_text
        self.lua.globals().pr.draw_rectangle = mock_draw_rectangle

        # Run the draw game function
        self.lua.execute("draw_game()")

        # Verify the draw functions were called
        self.assertTrue(draw_text_called)
        self.assertTrue(draw_rectangle_called)

    def test_edge_case_no_components(self):
        # Create an entity with no components
        self.lua.execute(
            """
            create_entity({})
        """
        )

        # Verify the entity was added but has no components
        entities = self.lua.eval("entities")
        self.assertEqual(len(entities), 4)  # 3 initial entities + 1 new entity
        self.assertEqual(len(entities[4]), 0)  # No components

    def test_edge_case_missing_velocity(self):
        # Create an entity with Position but no Velocity
        self.lua.execute(
            """
            create_entity({
                Position = { x = 500, y = 500 },
                Render = true
            })
        """
        )

        # Run the movement system
        self.lua.execute("movement_system()")

        # Verify the entity's position was not updated
        entities = self.lua.eval("entities")
        entity = entities[4]
        self.assertEqual(entity.Position.x, 500)
        self.assertEqual(entity.Position.y, 500)

    def test_edge_case_missing_render(self):
        # Create an entity with Position but no Render component
        self.lua.execute(
            """
            create_entity({
                Position = { x = 600, y = 600 }
            })
        """
        )

        # Run the draw game function
        self.lua.execute("draw_game()")

        # Verify the entity was not rendered
        entities = self.lua.eval("entities")
        entity = entities[4]
        self.assertIsNone(entity.Render)


if __name__ == "__main__":
    unittest.main()
