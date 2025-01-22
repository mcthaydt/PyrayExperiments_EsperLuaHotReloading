-- game_state.lua
game_state = {
    entities = {
        -- Player entity
        {
            Position = { x = 100, y = 100 },
            Velocity = { x = 0, y = 0 },
            Input = true,
            Render = true,
            Color = pr.RED  
        },
        -- Enemy entity 1
        {
            Position = { x = 200, y = 200 },
            Velocity = { x = 0, y = 0 },
            Render = true,
            Color = pr.BLUE  
        },
        -- Enemy entity 2
        {
            Position = { x = 300, y = 300 },
            Velocity = { x = 0, y = 0 },
            Render = true,
            Color = pr.GREEN  
        }
    }
}