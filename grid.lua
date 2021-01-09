-- "Goof Troop"
local World
local room


while (true) do

    World = memory.readbyte(0xB6)
    room= memory.readbyte(0xB7)


    for i=1,16 do
        gui.drawLine(16 * i,0, 16*i,255)
        gui.drawLine(0,16 * i, 355,16 * i)
    end

    for i=1,16 do  -- Column of the left
        gui.drawText(0,  2 + 16 * i, i, 0xFF16c6de)  -- This is for the left column
    end
    for i=1,16 do
        for j=0,16 do
            gui.drawText(16 * i,1 + 16 *j, i, 0xFF000000)
        end
    end
    gui.drawBox(0,0, 32,16, 0xFFFFFFFF, 0xFFFFFFFF)
    gui.drawText(0,0,World .. "-" .. room, 0xFF9353D2, 0x00000000)

    emu.frameadvance();
end