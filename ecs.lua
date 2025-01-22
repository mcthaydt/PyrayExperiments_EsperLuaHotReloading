-- ecs.lua
-- A simple ECS in Lua with systems for Input, Movement, and Rendering.

-- Load game_state.lua
dofile("game_state.lua")

-- Use game_state.entities as the main entities table
entities = game_state.entities

-------------------------------------------------------------
-- Helper: create_entity(components_table)
-- Takes a table of components and appends it to 'entities'.
-------------------------------------------------------------
function create_entity(components)
    local new_entity = {}
    for k, v in pairs(components) do
        new_entity[k] = v
    end
    table.insert(entities, new_entity)
    return new_entity  -- Return the actual entity (a Lua table)
end

-------------------------------------------------------------
-- SYSTEM: Input
-- Reads keyboard input, updates an entity's Velocity if it
-- has an "Input" component.
-------------------------------------------------------------
function input_system()
    for _, entity in ipairs(entities) do
        -- If this entity handles input AND has Velocity, update it
        if entity.Input and entity.Velocity then
            local vx, vy = 0, 0
            if pr.is_key_down(pr.KEY_RIGHT) then
                vx = 2
            end
            if pr.is_key_down(pr.KEY_LEFT) then
                vx = -2
            end
            if pr.is_key_down(pr.KEY_UP) then
                vy = -2
            end
            if pr.is_key_down(pr.KEY_DOWN) then
                vy = 2
            end
            entity.Velocity.x = vx
            entity.Velocity.y = vy
        end
    end
end

-------------------------------------------------------------
-- SYSTEM: Movement
-- Updates Position based on Velocity if the entity has both.
-------------------------------------------------------------
function movement_system()
    for _, entity in ipairs(entities) do
        if entity.Position and entity.Velocity then
            entity.Position.x = entity.Position.x + entity.Velocity.x
            entity.Position.y = entity.Position.y + entity.Velocity.y
        end
    end
end

-------------------------------------------------------------
-- FUNCTION: update_game
-- Called every frame by Python. Runs all systems.
-------------------------------------------------------------
function update_game()
    input_system()
    movement_system()
end

-------------------------------------------------------------
-- FUNCTION: draw_game
-- Called every frame by Python after update_game.
-- Renders text & any entity with a Position + Render component.
-------------------------------------------------------------
function draw_game()
    pr.draw_text("ECS in Lua: Input & Rendering in Lua!", 10, 10, 20, pr.BLACK)
    for _, entity in ipairs(entities) do
        if entity.Position and entity.Render then
            pr.draw_rectangle(
                math.floor(entity.Position.x),
                math.floor(entity.Position.y),
                50,
                50,
                entity.Color or pr.RED  -- Use the entity's color, default to RED if not specified
            )
        end
    end
end